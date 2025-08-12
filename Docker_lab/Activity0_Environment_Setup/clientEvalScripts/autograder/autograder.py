#!/usr/bin/env python3
"""
Autograder for Activity 0: Environment Setup

Performs:
  - SSH connectivity test
  - Docker daemon check
  - Required base packages check
  - Docker group membership check
  - CPU, Memory, Disk requirements
  - Container networking test

Output:
  ../evaluate.json with results.
"""

import json
import os
import socket
import traceback
import paramiko
from typing import Optional, List, Dict

# Constants
LAB_DIRECTORY_PATH = "/home/labDirectory/"
EVALUATE_JSON_OUT = "../evaluate.json"
REQUIRED_CPUS = 2
REQUIRED_RAM_GIB = 2
REQUIRED_DISK_GIB = 15
REQUIRED_PACKAGES = ["apt-transport-https", "curl", "conntrack"]

class DockerLabAutograder:
    def __init__(self, public_ip: str, key_path: str):
        self.public_ip = public_ip
        self.key_path = key_path
        self.results: List[Dict] = []
        self.ssh_client: Optional[paramiko.SSHClient] = None

    def append_result(self, testid, status, score, max_score, message):
        """Store test result in a consistent format."""
        self.results.append({
            "testid": testid,
            "status": status,
            "score": score,
            "maximum marks": max_score,
            "message": message
        })

    def run_remote_cmd(self, command: str, timeout: int = 30):
        """Run a command over SSH and return (exit_code, stdout, stderr)."""
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)
            exit_status = stdout.channel.recv_exit_status()
            return exit_status, stdout.read().decode().strip(), stderr.read().decode().strip()
        except Exception as e:
            return 1, "", str(e)

    def check_ssh_connectivity(self):
        """Verify SSH connection to the instance."""
        testid = "SSH Connectivity"
        if not self.public_ip:
            self.append_result(testid, "failure", 0, 1, "public-ip missing in data.json.")
            return False

        if not os.path.exists(self.key_path):
            self.append_result(testid, "failure", 0, 1, f"SSH key not found at {self.key_path}")
            return False

        try:
            os.chmod(self.key_path, 0o400)
        except Exception:
            pass  # Not fatal, paramiko can still try

        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.public_ip, username="ubuntu", key_filename=self.key_path, timeout=15)
            self.append_result(testid, "success", 1, 1, f"SSH connectivity successful to {self.public_ip}.")
            return True
        except FileNotFoundError:
            msg = "SSH key file not found."
        except paramiko.ssh_exception.AuthenticationException:
            msg = "Authentication failed: invalid key or username."
        except paramiko.ssh_exception.NoValidConnectionsError:
            msg = "Connection refused or unreachable."
        except socket.gaierror:
            msg = "Invalid IP or DNS resolution failed."
        except TimeoutError:
            msg = "SSH connection timed out."
        except Exception as e:
            msg = f"Unexpected SSH error: {e}\n{traceback.format_exc()}"

        self.append_result(testid, "failure", 0, 1, msg)
        return False

    def check_docker_daemon(self):
        """Verify Docker CLI exists and daemon is running."""
        testid = "Docker Daemon Check"
        code, out, err = self.run_remote_cmd("docker --version")
        if code != 0 or "Docker version" not in out:
            self.append_result(testid, "failure", 0, 1, f"Docker not found or misconfigured. {err or out}")
            return False

        code, status, _ = self.run_remote_cmd("systemctl is-active docker || true")
        if status.strip().lower() == "active":
            self.append_result(testid, "success", 1, 1, "Docker daemon is active.")
            return True
        else:
            self.append_result(testid, "failure", 0, 1, "Docker CLI present but daemon not running.")
            return False

    def check_base_packages(self):
        """Ensure required base packages are installed."""
        testid = "Base Packages Check"
        missing = []
        for pkg in REQUIRED_PACKAGES:
            code, out, _ = self.run_remote_cmd(f"dpkg -s {pkg} >/dev/null 2>&1 && echo OK || echo MISSING")
            if "MISSING" in out:
                missing.append(pkg)

        if not missing:
            self.append_result(testid, "success", 1, 1, "All required packages installed.")
        else:
            self.append_result(testid, "failure", 0, 1, f"Missing packages: {', '.join(missing)}")

    def check_docker_group(self):
        """Check user is in docker group."""
        testid = "Docker Group Membership"
        _, out, _ = self.run_remote_cmd("id -nG ubuntu | grep -qw docker && echo YES || echo NO")
        if "YES" in out:
            self.append_result(testid, "success", 1, 1, "'ubuntu' user in docker group.")
        else:
            self.append_result(testid, "failure", 0, 1, "'ubuntu' not in docker group. Add with 'usermod -aG docker ubuntu'.")

    def check_cpu(self):
        """Check CPU count."""
        testid = "CPU Count Check"
        _, out, _ = self.run_remote_cmd("nproc --all")
        try:
            cpus = int(out.strip())
        except:
            cpus = 0

        if cpus >= REQUIRED_CPUS:
            self.append_result(testid, "success", 1, 1, f"{cpus} vCPUs detected.")
        else:
            self.append_result(testid, "failure", 0, 1, f"Only {cpus} vCPUs; require at least {REQUIRED_CPUS}.")

    def check_memory(self):
        """Check configured/allocated memory for the VM."""
        testid = "Memory Check"
        # Use total installed memory, not currently available
        _, out, _ = self.run_remote_cmd("free --giga | awk '/Mem:/ {print $2}'")
        try:
            mem_gib = int(out.strip())
        except:
            mem_gib = 0

        if mem_gib >= REQUIRED_RAM_GIB:
            self.append_result(testid, "success", 1, 1, f"{mem_gib} GiB RAM configured for the VM.")
        else:
            self.append_result(testid, "failure", 0, 1, f"{mem_gib} GiB RAM configured; require at least {REQUIRED_RAM_GIB} GiB.")


    def check_disk(self):
        """Check configured/allocated root disk size for the VM."""
        testid = "Disk Size Check"
        # Use total size of the root volume, not available free space
        _, out, _ = self.run_remote_cmd("lsblk -b -o NAME,SIZE,MOUNTPOINT | awk '$3==\"/\" {print $2}'")
        try:
            size_gib = int(out.strip()) // (1024**3)
        except:
            size_gib = 0

        if size_gib >= REQUIRED_DISK_GIB:
            self.append_result(testid, "success", 1, 1, f"{size_gib} GiB root disk configured for the VM.")
        else:
            self.append_result(testid, "failure", 0, 1, f"{size_gib} GiB root disk configured; require at least {REQUIRED_DISK_GIB} GiB.")


    def check_container_network(self):
        """Test container can access external network."""
        testid = "Container Networking Check"
        cmd = "docker run --rm busybox ping -c 2 -W 2 8.8.8.8"
        code, out, err = self.run_remote_cmd(cmd, timeout=60)

        if code == 0 and "0% packet loss" in out:
            self.append_result(testid, "success", 1, 1, "Container network OK.")
        else:
            self.append_result(testid, "failure", 0, 1, f"Container ping failed. {err or out}")

    def run_all_tests(self):
        """Execute all tests in sequence."""
        if not self.check_ssh_connectivity():
            # If SSH fails, mark rest as skipped
            skipped_tests = [
                "Docker Daemon Check", "Base Packages Check", "Docker Group Membership",
                "CPU Count Check", "Memory Check", "Disk Size Check", "Container Networking Check"
            ]
            for t in skipped_tests:
                self.append_result(t, "failure", 0, 1, "Skipped due to SSH failure.")
            return

        docker_ok = self.check_docker_daemon()
        self.check_base_packages()
        self.check_docker_group()
        self.check_cpu()
        self.check_memory()
        self.check_disk()

        if docker_ok:
            self.check_container_network()
        else:
            self.append_result("Container Networking Check", "failure", 0, 1, "Skipped due to Docker not running.")

    def save_results(self):
        """Write results to evaluate.json."""
        with open(EVALUATE_JSON_OUT, 'w') as f:
            json.dump({"data": self.results}, f, indent=4)


def main():
    # Read data.json
    try:
        with open(os.path.join(LAB_DIRECTORY_PATH, "data.json"), 'r') as f:
            data = json.load(f)
            public_ip = data.get("public-ip")
    except Exception as e:
        public_ip = None

    key_path = os.path.join(LAB_DIRECTORY_PATH, "secret-key.pem")

    grader = DockerLabAutograder(public_ip, key_path)
    grader.run_all_tests()
    grader.save_results()


if __name__ == "__main__":
    main()
