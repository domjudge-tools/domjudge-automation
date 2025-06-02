import ipaddress
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import paramiko
from tqdm import tqdm

USERNAME = "user"
PASSWORD = "password"
PORT = 22
TIMEOUT = 3
MAX_WORKERS = 30
SUCCESS_FILE = "ssh_success.txt"

# The remote command to run after successful login
REMOTE_COMMAND = '''loginctl unlock-session $(loginctl list-sessions | grep rayan | awk '{print $1}') && loginctl activate $(loginctl list-sessions | grep rayan | awk '{print $1}')'''
# REMOTE_COMMAND = '''echo 'password' | sudo -S passwd 123'''
# REMOTE_COMMAND = '''echo 1'''

# Generate IP list from CIDR, excluding .1
LOAD_FROM_FILE = False
if LOAD_FROM_FILE:
    with open(SUCCESS_FILE) as f:
        ip_list = [l.strip() for l in f.readlines()]
else:
    ip_range = ipaddress.IPv4Network("172.100.191.0/24")
    ip_list = [str(ip) for ip in ip_range.hosts() if str(ip) != "172.100.191.1"]
# ip_list = ["172.100.191.3"]
total_ips = len(ip_list)

def check_and_run_ssh(ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=ip, port=PORT, username=USERNAME, password=PASSWORD, timeout=TIMEOUT)
        stdin, stdout, stderr = client.exec_command(REMOTE_COMMAND)
        stdout.channel.recv_exit_status()  # Wait for command to finish
        return (ip, True)
    except Exception:
        return (ip, False)
    finally:
        client.close()

def main():
    print(f"Starting SSH health check and command run on {total_ips} hosts...\n")
    success_count = 0
    failure_count = 0
    checked = 0
    start_time = time.time()
    successful_hosts = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_and_run_ssh, ip): ip for ip in ip_list}

        with tqdm(total=total_ips, desc="Checking", unit="host") as pbar:
            for future in as_completed(futures):
                ip, success = future.result()
                checked += 1
                if success:
                    success_count += 1
                    successful_hosts.append(ip)
                else:
                    if LOAD_FROM_FILE:
                        print(ip)
                    failure_count += 1

                elapsed = time.time() - start_time
                avg_time = elapsed / checked
                remaining = total_ips - checked
                eta = avg_time * remaining

                pbar.set_postfix({
                    "Success": success_count,
                    "Failed": failure_count,
                    "ETA": f"{int(eta)}s"
                })
                pbar.update(1)

    with open(SUCCESS_FILE, "w") as f:
        for ip in successful_hosts:
            f.write(ip + "\n")

    print("\n=== Summary ===")
    print(f"Total Checked: {checked}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Successful IPs saved to {SUCCESS_FILE}")

if __name__ == "__main__":
    main()
