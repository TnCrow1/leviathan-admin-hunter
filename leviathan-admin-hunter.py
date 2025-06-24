from concurrent.futures import ThreadPoolExecutor
import requests, os, sys, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style, init

init(autoreset=True)

if os.path.basename(sys.argv[0]) != "leviathan-admin-hunter.py":
    sys.exit()

header = f"""
{Fore.GREEN}+-------------------------------------------------------------+
|               LEVIATHAN ADMIN PANEL HUNTER v2              |
+-------------------------------------------------------------+
| Author   : Tn Crow                                          |
| TikTok   : @the.crow137                                     |
| Version  : v2.0 (Multi-threaded, Deep Scan, Stealth Protect)|
| Status   : © 2025 Tn Crow - All Rights Reserved             |
+-------------------------------------------------------------+{Style.RESET_ALL}
"""

full_payloads = [
    "admin", "login", "admin/login", "administrator", "user/login", "adminarea",
    "admin_panel", "cpanel", "dashboard", "masuk", "panel", "auth", "wp-admin",
    "wp-login", "admin1", "admin2", "admin123", "admin_login", "admincp",
    "systemadmin", "admincontrol", "admin_area", "useradmin", "adminsite",
    "adminConsole", "admins", "adminpanel", "admin_signin", "adminsignin",
    "login_admin", "adminSignIn", "root", "superuser", "secure", "secureadmin",
    "access", "manage", "management", "backend", "backend/login", "administrator/login",
    "adminlogin", "controlpanel", "adminconsole", "adminpage", "admin_loginpanel",
    "admininterface", "adminauth", "member/login", "staff/login", "adminsecure",
    "adminaccess", "admin_portal", "adminzone", "siteadmin", "portaladmin",
    "users/admin", "adminsection", "adm", "adminarea/login", "dashboard/login",
    "system", "login-panel", "loginarea", "paneladmin", "admin_home",
    "webadmin", "admin_homepage", "account/admin", "accounts/login", "adminview",
    "adminbackend", "adminuser", "adminusers", "adminsettings", "admin-config",
    "admin-dashboard", "adminportal", "login_adminpanel", "admininterface/login",
    "adminweb", "admin/index", "admin.php", "admin.html", "administrator/index",
    "login.php", "admin.asp", "admin.aspx", "admin.do", "admin.jsp",
    "admin.cgi", "adm/login", "useradmin/login", "root/login", "dashboardadmin",
    "adminzone/login", "panelsecure", "adminka", "beheer", "moderator", "admin.php/login"
]

def scan_path(base_url, path, results):
    url = urljoin(base_url, path)
    try:
        res = requests.get(url, timeout=5)
        status = res.status_code
        if status == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            form_found = soup.find_all("form")
            input_found = soup.find_all("input", {"type": "password"})
            if form_found and input_found:
                print(f"{Fore.YELLOW}[*] Scanning /{path:<20} --> [{status}] ✔️ (Login form terdeteksi)")
                results.append(("✔️", status, "/" + path, url))
            else:
                print(f"{Fore.YELLOW}[*] Scanning /{path:<20} --> [{status}] ❌")
                results.append(("❌", status, "/" + path, url))
        else:
            print(f"{Fore.YELLOW}[*] Scanning /{path:<20} --> [{status}] ❌")
            results.append(("❌", status, "/" + path, url))
    except:
        print(f"{Fore.YELLOW}[*] Scanning /{path:<20} --> [ERR] ❌")
        results.append(("❌", "ERR", "/" + path, url))
    time.sleep(0.3)

def run_scan():
    print(header)
    target = input(f"{Fore.GREEN}Masukkan URL target (cth: https://example.com): {Style.RESET_ALL}").strip()
    if not target.startswith("http"):
        target = "http://" + target
    return target

def get_level():
    try:
        level = int(input(f"{Fore.GREEN}Pilih Level Scan (1-10) [default: 10]: {Style.RESET_ALL}") or 10)
        if level < 1 or level > 10:
            raise ValueError
    except:
        level = 10
    return level

def scan_process(target, level):
    results = []
    paths = full_payloads[:level * 10]
    print(f"{Fore.GREEN}\n[!] Memulai scanning pada target: {target}")
    print(f"[*] Threads: 10 | Mode: Deep Scan | Level: {level} ({len(paths)} Payload)\n")

    with ThreadPoolExecutor(max_workers=10) as executor:
        for path in paths:
            executor.submit(scan_path, target, path, results)

    time.sleep(1)
    print(f"\n{Fore.GREEN}[✓] Scanning selesai. Menampilkan hasil...\n")
    print(f"{Fore.GREEN}+--------+------+----------------------+--------------------------------------------+")
    print(f"| Status | Code |        Path          | URL                                        |")
    print(f"+--------+------+----------------------+--------------------------------------------+")
    for status, code, path, url in results:
        print(f"|  {status:<5} | {code:<4} | {path:<20} | {url:<42} |")
    print(f"+--------+------+----------------------+--------------------------------------------+{Style.RESET_ALL}")

    return target

while True:
    current_target = run_scan()
    current_level = get_level()
    scan_process(current_target, current_level)

    print(f"\n{Fore.GREEN}Apa yang ingin kamu lakukan selanjutnya?")
    print("[1] Scan target lain")
    print("[2] Ulangi scan pada target ini")
    print("[3] Keluar")
    choice = input(">> ").strip()

    if choice == "1":
        continue
    elif choice == "2":
        current_level = get_level()
        scan_process(current_target, current_level)
    else:
        print(f"{Fore.GREEN}\nTerima kasih telah menggunakan Leviathan Admin Panel Hunter!")
        break
