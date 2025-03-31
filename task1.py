import subprocess
import re
import requests

def get_trace_ips(host):
    result = subprocess.run(["tracert", host], capture_output=True, text=True, timeout=30)
    output = result.stdout
    ip_pattern = r"\d+\.\d+\.\d+\.\d+"
    ips = re.findall(ip_pattern, output)
    return list(dict.fromkeys(ips))

def is_public_ip(ip):
    private_blocks = [
        ("10.",),
        ("192.168.",),
        ("172.", lambda x: 16 <= int(x.split(".")[1]) <= 31),
        ("127.",),
        ("0.",)
    ]
    for block in private_blocks:
        prefix = block[0]
        if ip.startswith(prefix):
            if len(block) == 1 or block[1](ip):
                return False
    return True

def get_as_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = response.json()
        org = data.get("org", "")
        if "AS" in org:
            return org.split()[0]
        else:
            return "-"
    except Exception:
        return "-"

if __name__ == "__main__":
    host = input()
    ips = get_trace_ips(host)
    print("№ IP AS")
    for i, ip in enumerate(ips, 1):
        if is_public_ip(ip):
            as_number = get_as_info(ip)
            print(f"{i} {ip} {as_number}")
        else:
            print(f"{i} {ip} (локальный)")
