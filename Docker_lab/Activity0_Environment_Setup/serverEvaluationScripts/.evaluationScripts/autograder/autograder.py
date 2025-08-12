import json
import os
import paramiko
import socket
import traceback

def check_ssh_connectivity(public_ip, key_path, data):
    """
    Attempt to SSH into the host using paramiko and report detailed failure reasons.
    On success, returns a connected paramiko.SSHClient instance; otherwise returns None.
    """
    result = {
        "testid": "SSH Connectivity",
        "status": "failure",
        "score": 0,
        "maximum marks": 1,
        "message": ""
    }

    # Basic pre-checks
    if not public_ip:
        result['message'] = "public-ip missing or empty in data.json."
        data.append(result)
        return None

    if not os.path.exists(key_path):
        result['message'] = f"SSH key not found at path: {key_path}"
        data.append(result)
        return None

    # Ensure key permissions are strict
    try:
        os.chmod(key_path, 0o400)
    except PermissionError as e:
        result['message'] = f"Failed to change permissions on SSH key: {e}"
        data.append(result)
        return None
    except Exception as e:
        result['message'] = f"Unexpected error while setting key permissions: {e}"
        data.append(result)
        return None

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Attempt to connect (username is 'ubuntu' for Ubuntu AMIs)
        ssh.connect(public_ip, username='ubuntu', key_filename=key_path, timeout=15)
    except FileNotFoundError:
        result['message'] = f"SSH key file missing: {key_path}"
        data.append(result)
        return None
    except paramiko.ssh_exception.AuthenticationException as e:
        # Bad key / wrong username
        result['message'] = f"Authentication failed: invalid SSH key or username. ({e})"
        data.append(result)
        return None
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        # Connection refused / unreachable
        result['message'] = f"Unable to connect to {public_ip}:22 — network unreachable or connection refused. ({e})"
        data.append(result)
        return None
    except socket.gaierror as e:
        result['message'] = f"Invalid public IP or DNS resolution failed for '{public_ip}': {e}"
        data.append(result)
        return None
    except TimeoutError:
        result['message'] = f"Connection to {public_ip} timed out."
        data.append(result)
        return None
    except paramiko.ssh_exception.SSHException as e:
        result['message'] = f"SSH negotiation failed — possible invalid key format or incompatible SSH settings. ({e})"
        data.append(result)
        return None
    except Exception as e:
        result['message'] = f"Unexpected error during SSH connection: {e}"
        data.append(result)
        return None
    else:
        result['status'] = "success"
        result['score'] = 1
        result['message'] = f"SSH connectivity successful to {public_ip} using provided key."
        data.append(result)
        return ssh


def check_docker_daemon(ssh, data):
    """
    Using an active SSH connection, verify Docker CLI presence and daemon active/running state.
    """
    result = {
        "testid": "Docker Daemon Check",
        "status": "failure",
        "score": 0,
        "maximum marks": 1,
        "message": ""
    }

    try:
        # 1) Check docker binary presence and version
        stdin, stdout, stderr = ssh.exec_command("docker --version")
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()

        if out and ("Docker version" in out or "docker version" in out.lower()):
            # proceed to check daemon active state
            # First try systemctl (typical for Ubuntu)
            stdin2, stdout2, stderr2 = ssh.exec_command("systemctl is-active docker || systemctl is-active docker.service || true")
            status = stdout2.read().decode().strip()
            # normalize status
            status_lower = status.lower() if status else ""

            if status_lower == "active":
                result['status'] = "success"
                result['score'] = 1
                result['message'] = "Docker CLI present and Docker daemon is active (systemctl reports 'active')."
                data.append(result)
                return
            else:
                # If systemctl does not report active, check whether dockerd process exists
                stdin3, stdout3, stderr3 = ssh.exec_command("pgrep -a dockerd || ps -ef | grep dockerd | grep -v grep || true")
                proc_out = stdout3.read().decode().strip()
                if proc_out:
                    # dockerd process exists but systemd unit not 'active' (possible if started manually)
                    result['status'] = "success"
                    result['score'] = 1
                    result['message'] = ("Docker CLI present and dockerd process is running, "
                                         f"but systemctl reported: '{status or 'unknown'}'.")
                    data.append(result)
                    return
                else:
                    # No dockerd found
                    result['message'] = ("Docker CLI is present but Docker daemon is not running. "
                                         f"systemctl output: '{status}'.")
                    data.append(result)
                    return
        else:
            # docker CLI missing or produced error
            combined = out + ("\n" + err if err else "")
            if "command not found" in combined.lower() or "docker: command not found" in combined.lower():
                result['message'] = "Docker CLI not found on PATH. Please install Docker on the instance."
                data.append(result)
                return
            else:
                result['message'] = f"Unexpected output from 'docker --version': {combined}"
                data.append(result)
                return

    except Exception as e:
        tb = traceback.format_exc()
        result['message'] = f"An error occurred while checking Docker daemon: {e}\n{tb}"
        data.append(result)
        return


def main():
    labDirectoryPath = "/home/labDirectory/"
    overall = {"data": []}
    data = []

    # 1) Load data.json and get public-ip
    try:
        with open(os.path.join(labDirectoryPath, 'data.json'), 'r') as f:
            json_data = json.load(f)
            public_ip = json_data.get('public-ip')
    except FileNotFoundError:
        data.append({
            "testid": "SSH Connectivity",
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": "data.json not found in labDirectory; cannot obtain public-ip."
        })
        data.append({
            "testid": "Docker Daemon Check",
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": "Skipped Docker checks because data.json is missing (no public-ip)."
        })
        overall['data'] = data
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        return
    except json.JSONDecodeError:
        data.append({
            "testid": "SSH Connectivity",
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": "data.json is not valid JSON."
        })
        data.append({
            "testid": "Docker Daemon Check",
            "status": "failure",
            "score": 0,
            "maximum marks": 1,
            "message": "Skipped Docker checks because data.json is invalid."
        })
        overall['data'] = data
        with open('../evaluate.json', 'w') as f:
            json.dump(overall, f, indent=4)
        return

    key_path = os.path.join(labDirectoryPath, 'secret-key.pem')

    # 2) Attempt SSH connectivity and produce a detailed result
    ssh_client = check_ssh_connectivity(public_ip, key_path, data)

    # 3) If SSH successful, perform Docker daemon check
    if ssh_client:
        check_docker_daemon(ssh_client, data)
        try:
            ssh_client.close()
        except Exception:
            pass
    else:
        # If SSH failed, ensure Docker test is present (already appended in connectivity failure handler),
        # but if not, add a clear skipped message for Docker test.
        docker_present = any(entry.get('testid') == 'Docker Daemon Check' for entry in data)
        if not docker_present:
            data.append({
                "testid": "Docker Daemon Check",
                "status": "failure",
                "score": 0,
                "maximum marks": 1,
                "message": "Skipped Docker checks due to SSH connectivity failure."
            })

    overall['data'] = data
    with open('../evaluate.json', 'w') as f:
        json.dump(overall, f, indent=4)


if __name__ == "__main__":
    main()