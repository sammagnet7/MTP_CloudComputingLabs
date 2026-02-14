#!/usr/bin/env python3
"""
Autograder for Activity 1: Core Docker Operations

- Uses the SAME output file and schema as Activity 0:
    -> Writes results to ../evaluate.json
    -> Each result item has: testid, status, score, maximum marks, message

- Reads:
    - /home/labDirectory/data.json   (expects key: "public-ip"; optional "username")
    - /home/labDirectory/secret-key.pem
    - /home/labDirectory/ans.json    (student-provided answers for Task 2 & 3)

Tests covered:
  Task 1
    - lab1-hello: exists, exited 0, logs contain hello text, label lab=act1
    - lab1-nginx: running, port 8080 mapped to container 80, HTTP reachable, label lab=act1
    - lab1-ubuntu: running, /lab1.txt == "ok", label lab=act1
  Task 2
    - ans.json keys exist and exact values match host:
        lab1-nginx-CreatedAt, lab1-nginx-size, lab1-ubuntu-sha256, lab1-ubuntu-path
  Task 3
    - ans.json: ubuntu-default-user, lab1-nonroot-user, lab1-nonroot-uid
    - lab1-nonroot-int runs as non-root and cannot write /root
  Task 4
    - No dangling (<none>) images remain

Output:
  ../evaluate.json with results.
"""

import json
import os
import socket
import traceback
import paramiko
from typing import Optional, List, Dict, Tuple

# ---------- Constants (kept consistent with Activity 0) ----------
LAB_DIRECTORY_PATH = "/home/labDirectory/"
EVALUATE_JSON_OUT = "../evaluate.json"

# Container & label constants
C_HELLO = "lab1-hello"
C_NGINX = "lab1-nginx"
C_UBUNTU = "lab1-ubuntu"
C_NONROOT_INT = "lab1-nonroot-int"

LAB_LABEL_KEY = "lab"
LAB_LABEL_VAL = "act1"

# ans.json expected keys (Task 2 & 3)
ANS_KEYS = [
    "lab1-nginx-CreatedAt",
    "lab1-nginx-size",
    "lab1-ubuntu-sha256",
    "lab1-ubuntu-path",
    "ubuntu-default-user",
    "lab1-nonroot-user",
    "lab1-nonroot-uid",
]


class DockerLabAutograder:
    def __init__(self, public_ip: str, key_path: str, username: str = "ubuntu"):
        self.public_ip = public_ip
        self.key_path = key_path
        self.username = username or "ubuntu"
        self.results: List[Dict] = []
        self.ssh_client: Optional[paramiko.SSHClient] = None

    # ----- Common helpers (same schema as Activity 0) -----
    def append_result(self, testid: str, status: str, score: int, max_score: int, message: str):
        self.results.append({
            "testid": testid,
            "status": status,
            "score": score,
            "maximum marks": max_score,
            "message": message
        })

    def run_remote_cmd(self, command: str, timeout: int = 40) -> Tuple[int, str, str]:
        """Run a command over SSH and return (exit_code, stdout, stderr)."""
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=timeout)
            exit_status = stdout.channel.recv_exit_status()
            return exit_status, stdout.read().decode().strip(), stderr.read().decode().strip()
        except Exception as e:
            return 1, "", str(e)

    # ----- SSH & Docker sanity (mirrors Activity 0 style) -----
    def check_ssh_connectivity(self) -> bool:
        testid = "SSH Connectivity"
        if not self.public_ip:
            self.append_result(testid, "failed", 0, 1, "public-ip missing in data.json.")
            return False

        if not os.path.exists(self.key_path):
            self.append_result(testid, "failed", 0, 1, f"SSH key not found at {self.key_path}")
            return False

        try:
            os.chmod(self.key_path, 0o400)
        except Exception:
            pass

        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(self.public_ip, username=self.username, key_filename=self.key_path, timeout=20)
            self.append_result(testid, "success", 1, 1, f"SSH connectivity successful to {self.public_ip}.")
            return True
        except FileNotFoundError:
            msg = "SSH key file not found."
        except paramiko.ssh_exception.AuthenticationException:
            msg = "Authentication failed: invalid key or username."
        except paramiko.ssh_exception.NoValidConnectionsError:
            msg = "Connection refused or unreachable."
        except paramiko.ssh_exception.SSHException as e:
            msg = f"SSHException: invalid or empty key file. Details: {e}"
        except socket.gaierror:
            msg = "Invalid IP or DNS resolution failed."
        except TimeoutError:
            msg = "SSH connection timed out."
        except Exception as e:
            msg = f"Unexpected SSH error: {e}\n{traceback.format_exc()}"

        self.append_result(testid, "failed", 0, 1, msg)
        return False

    def check_docker_daemon(self) -> bool:
        testid = "Docker Daemon Check"
        code, out, err = self.run_remote_cmd("docker --version")
        if code != 0 or "Docker version" not in out:
            self.append_result(testid, "failed", 0, 1, f"Docker not found or misconfigured. {err or out}")
            return False

        code, status, _ = self.run_remote_cmd("systemctl is-active docker || true")
        if status.strip().lower() == "active":
            self.append_result(testid, "success", 1, 1, "Docker daemon is active.")
            return True
        else:
            self.append_result(testid, "failed", 0, 1, "Docker CLI present but daemon not running.")
            return False

    # ----- Task 1: Basic Containers -----
    def t1_check_hello(self):
        testid = "Task1: lab1-hello"
        msgs = []

        code, out, err = self.run_remote_cmd(f"docker inspect -f '{{{{.State.Status}}}}|{{{{.State.ExitCode}}}}' {C_HELLO}")
        if code != 0 or not out:
            self.append_result(testid, "failed", 0, 1, "Container 'lab1-hello' not found.")
            return

        parts = out.split("|")
        status = parts[0] if len(parts) > 0 else ""
        exit_code = parts[1] if len(parts) > 1 else ""
        if status != "exited" or exit_code != "0":
            msgs.append(f"Expected exited/0; got status={status}, exit={exit_code}.")

        # Hello message in logs
        code, logs, _ = self.run_remote_cmd(f"docker logs {C_HELLO} | head -n 50")
        if code != 0 or "Hello from Docker!" not in logs:
            msgs.append("Logs do not contain 'Hello from Docker!'.")

        # Label
        code, label, _ = self.run_remote_cmd(
            f"docker inspect -f '{{{{ index .Config.Labels \"{LAB_LABEL_KEY}\" }}}}' {C_HELLO} 2>/dev/null || true"
        )
        if label.strip() != LAB_LABEL_VAL:
            msgs.append("Missing or incorrect label lab=act1 on lab1-hello.")

        if msgs:
            self.append_result(testid, "failed", 0, 1, "\n".join(msgs))
        else:
            self.append_result(testid, "success", 1, 1, "lab1-hello OK.")

    def t1_check_nginx(self):
        testid = "Task1: lab1-nginx"
        msgs = []

        # Running
        code, state, _ = self.run_remote_cmd(f"docker inspect -f '{{{{.State.Status}}}}' {C_NGINX}")
        if code != 0 or state.strip() != "running":
            self.append_result(testid, "failed", 0, 1, "lab1-nginx is not running.")
            return

        # Port mapping includes host 8080 -> container 80
        code, ports, _ = self.run_remote_cmd(f"docker port {C_NGINX} 80 || true")
        if ":8080" not in (ports or ""):
            msgs.append("Expected host port 8080 mapped to container port 80.")

        # HTTP check (curl then wget fallback)
        code, http_code, _ = self.run_remote_cmd("(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 || echo '000')")
        try:
            http = int(http_code.strip() or "0")
        except Exception:
            http = 0
        if http < 200 or http >= 400:
            code, hdr, _ = self.run_remote_cmd("wget -qS --spider http://localhost:8080 2>&1 | head -n1 || true")
            if "HTTP/" not in (hdr or ""):
                msgs.append("HTTP check failed on http://localhost:8080.")

        # Label
        code, label, _ = self.run_remote_cmd(
            f"docker inspect -f '{{{{ index .Config.Labels \"{LAB_LABEL_KEY}\" }}}}' {C_NGINX} 2>/dev/null || true"
        )
        if label.strip() != LAB_LABEL_VAL:
            msgs.append("Missing or incorrect label lab=act1 on lab1-nginx.")

        if msgs:
            self.append_result(testid, "failed", 0, 1, "\n".join(msgs))
        else:
            self.append_result(testid, "success", 1, 1, "lab1-nginx OK.")

    def t1_check_ubuntu(self):
        testid = "Task1: lab1-ubuntu"
        msgs = []

        # Running
        code, state, _ = self.run_remote_cmd(f"docker inspect -f '{{{{.State.Status}}}}' {C_UBUNTU}")
        if code != 0 or state.strip() != "running":
            self.append_result(testid, "failed", 0, 1, "lab1-ubuntu is not running.")
            return

        # Label
        code, label, _ = self.run_remote_cmd(
            f"docker inspect -f '{{{{ index .Config.Labels \"{LAB_LABEL_KEY}\" }}}}' {C_UBUNTU} 2>/dev/null || true"
        )
        if label.strip() != LAB_LABEL_VAL:
            msgs.append("Missing or incorrect label lab=act1 on lab1-ubuntu.")

        # /lab1.txt contains ok
        code, txt, _ = self.run_remote_cmd(f"docker exec {C_UBUNTU} bash -lc 'cat /lab1.txt 2>/dev/null' || true")
        if not txt:
            msgs.append("/lab1.txt not found inside lab1-ubuntu.")
        elif txt.strip() != "ok":
            msgs.append("/lab1.txt does not contain 'ok'.")

        if msgs:
            self.append_result(testid, "failed", 0, 1, "\n".join(msgs))
        else:
            self.append_result(testid, "success", 1, 1, "lab1-ubuntu OK.")

    # ----- Task 2: ans.json checks -----
    def read_ans(self) -> Tuple[Optional[dict], Optional[str]]:
        path = os.path.join(LAB_DIRECTORY_PATH, "ans.json")
        try:
            with open(path, "r") as f:
                data = json.load(f)
        except Exception as e:
            return None, f"Failed to read ans.json: {e}"

        missing = [k for k in ANS_KEYS if k not in data]
        if missing:
            return None, f"ans.json missing keys: {', '.join(missing)}"
        return data, None

    def t2_check_ans(self, ans: dict):
        testid = "Task2: ans.json values"
        msgs = []

        # CreatedAt of lab1-nginx
        code, created_at, _ = self.run_remote_cmd(
            f"docker ps -a --filter name=^{C_NGINX}$ --format '{{{{.CreatedAt}}}}'"
        )
        if code != 0 or not created_at:
            msgs.append("Could not fetch lab1-nginx CreatedAt from host.")
        elif ans.get("lab1-nginx-CreatedAt", "").strip() != created_at.strip():
            msgs.append("Mismatch: lab1-nginx-CreatedAt.")

        # Size of nginx image
        code, size, _ = self.run_remote_cmd("docker images nginx:latest --format '{{.Size}}' || docker images nginx --format '{{.Size}}' | head -n1")
        if code != 0 or not size:
            msgs.append("Could not fetch nginx image size from host.")
        elif ans.get("lab1-nginx-size", "").strip() != size.strip():
            msgs.append("Mismatch: lab1-nginx-size.")

        # Image sha256 of lab1-ubuntu
        code, sha, _ = self.run_remote_cmd(f"docker inspect -f '{{{{.Image}}}}' {C_UBUNTU}")
        if code != 0 or not sha:
            msgs.append("Could not fetch lab1-ubuntu image sha256 from host.")
        elif ans.get("lab1-ubuntu-sha256", "").strip() != sha.strip():
            msgs.append("Mismatch: lab1-ubuntu-sha256.")

        # PATH from inside lab1-ubuntu
        code, path_val, _ = self.run_remote_cmd(f"docker exec {C_UBUNTU} bash -lc 'printenv PATH' || true")
        if code != 0 or not path_val:
            msgs.append("Could not fetch PATH from lab1-ubuntu.")
        elif ans.get("lab1-ubuntu-path", "").strip() != path_val.strip():
            msgs.append("Mismatch: lab1-ubuntu-path.")

        if msgs:
            self.append_result(testid, "failed", 0, 1, "\n".join(msgs))
        else:
            self.append_result(testid, "success", 1, 1, "ans.json values match.")

    # ----- Task 3: Non-root containers -----
    def t3_check_nonroot(self, ans: dict):
        testid = "Task3: non-root containers"
        msgs = []

        # Default user of ubuntu:latest
        code, whoami_def, _ = self.run_remote_cmd("docker run --rm ubuntu:latest sh -lc 'whoami || id -un'")
        if code != 0 or not whoami_def:
            msgs.append("Failed to determine default user for ubuntu:latest.")
        else:
            if ans.get("ubuntu-default-user", "").strip() != whoami_def.strip():
                msgs.append("Mismatch: ubuntu-default-user.")

        # Run as UID 1000
        code, whoami_nr, _ = self.run_remote_cmd(
            "docker run --rm --user 1000:1000 ubuntu:latest sh -lc 'whoami 2>&1 || id -u'"
        )
        if code != 0 or not whoami_nr:
            msgs.append("Failed to run ubuntu:latest as UID 1000.")
        else:
            expected = ans.get("lab1-nonroot-user", "").strip()
            # Accept either a username or uid '1000' depending on image content
            if expected not in [whoami_nr.strip(), "1000"]:
                msgs.append("Mismatch: lab1-nonroot-user.")

        # Interactive non-root container checks
        code, state, _ = self.run_remote_cmd(f"docker inspect -f '{{{{.State.Status}}}}' {C_NONROOT_INT}")
        if code != 0 or state.strip() != "running":
            msgs.append("lab1-nonroot-int is not running.")
        else:
            # UID inside should not be 0
            code, uid, _ = self.run_remote_cmd(f"docker exec {C_NONROOT_INT} id -u || true")
            if not uid:
                msgs.append("Unable to read UID inside lab1-nonroot-int.")
            else:
                if uid.strip() == "0":
                    msgs.append("lab1-nonroot-int is running as root; expected non-root.")
                if ans.get("lab1-nonroot-uid", "").strip() != uid.strip():
                    msgs.append("Mismatch: lab1-nonroot-uid.")

            # Permission check: should not be able to write to /root
            code, _, _ = self.run_remote_cmd(f"docker exec {C_NONROOT_INT} bash -lc 'touch /root/testfile'")
            if code == 0:
                msgs.append("Non-root permission check failed: was able to write to /root.")

            # Label (recommended)
            code, label, _ = self.run_remote_cmd(
                f"docker inspect -f '{{{{ index .Config.Labels \"{LAB_LABEL_KEY}\" }}}}' {C_NONROOT_INT} 2>/dev/null || true"
            )
            if label.strip() != LAB_LABEL_VAL:
                msgs.append("Missing or incorrect label lab=act1 on lab1-nonroot-int.")

        if msgs:
            self.append_result(testid, "failed", 0, 1, "\n".join(msgs))
        else:
            self.append_result(testid, "success", 1, 1, "Non-root checks passed.")

    # ----- Task 4: Housekeeping -----
    def t4_check_housekeeping(self):
        testid = "Task4: housekeeping"
        code, dangling_count, _ = self.run_remote_cmd("docker image ls -f dangling=true -q | wc -l || true")
        try:
            n = int((dangling_count or "0").strip())
        except Exception:
            n = 1  # treat as failure if parse error
        if n == 0:
            self.append_result(testid, "success", 1, 1, "No dangling images found.")
        else:
            self.append_result(testid, "failed", 0, 1, f"Found {n} dangling (<none>) images. Please prune.")

    # ----- Orchestration -----
    def run_all_tests(self):
        # SSH first
        if not self.check_ssh_connectivity():
            for t in [
                "Docker Daemon Check",
                "Task1: lab1-hello",
                "Task1: lab1-nginx",
                "Task1: lab1-ubuntu",
                "Task2: ans.json values",
                "Task3: non-root containers",
                "Task4: housekeeping",
            ]:
                self.append_result(t, "failed", 0, 1, "Skipped due to SSH failure.")
            return

        docker_ok = self.check_docker_daemon()
        if not docker_ok:
            for t in ["Task1: lab1-hello", "Task1: lab1-nginx", "Task1: lab1-ubuntu", "Task2: ans.json values", "Task3: non-root containers", "Task4: housekeeping"]:
                self.append_result(t, "failed", 0, 1, "Skipped: Docker daemon not running.")
            return

        # Task 1
        self.t1_check_hello()
        self.t1_check_nginx()
        self.t1_check_ubuntu()

        # Task 2 & 3 need ans.json
        ans, err = self.read_ans()
        if err:
            self.append_result("Task2: ans.json values", "failed", 0, 1, err)
            self.append_result("Task3: non-root containers", "failed", 0, 1, "Skipped: ans.json missing/invalid.")
        else:
            self.t2_check_ans(ans)
            self.t3_check_nonroot(ans)

        # Task 4
        self.t4_check_housekeeping()

    def save_results(self):
        with open(EVALUATE_JSON_OUT, 'w') as f:
            json.dump({"data": self.results}, f, indent=4)


def main():
    # Read data.json
    try:
        with open(os.path.join(LAB_DIRECTORY_PATH, "data.json"), 'r') as f:
            data = json.load(f)
            public_ip = data.get("public-ip") or data.get("public_ip")
            username = data.get("username") or "ubuntu"
    except Exception as e:
        public_ip = None
        username = "ubuntu"

    key_path = os.path.join(LAB_DIRECTORY_PATH, "secret-key.pem")

    grader = DockerLabAutograder(public_ip, key_path, username=username)
    grader.run_all_tests()
    grader.save_results()


if __name__ == "__main__":
    main()
