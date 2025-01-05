import signal
import sys
import platform
import subprocess
import threading
from colorama import Fore, init
import time
import os

# Initialize colorama
init(autoreset=True)

# Global flag for exit condition
exit_program = False
scanning_in_progress = False

# Function to handle Ctrl+C gracefully
def signal_handler(sig, frame):
    global exit_program, scanning_in_progress
    if scanning_in_progress:
        print("\nScan aborted. Returning to the main menu...")
        exit_program = True
    else:
        print("\nScan is not in progress.")

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Function to clear the screen (teleportation effect)
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# ASCII loading screen with faster effect and blue/white color scheme
def fast_loading_screen():
    clear_screen()
    loading_text = '''
                                _                
   ______________ _____  ____  (_)___  ____ _    
  / ___/ ___/ __ `/ __ \/ __ \/ / __ \/ __ `/    
 (__  ) /__/ /_/ / / / / / / / / / / / /_/ / _ _ 
/____/\___/\__,_/_/ /_/_/ /_/_/_/ /_/\__, (_|_|_)
                                    /____/               
'''
    # Fast printing of each line with a very short delay and alternating colors
    for i, line in enumerate(loading_text.splitlines()):
        if i % 2 == 0:
            print(Fore.BLUE + line)  # Blue for even lines
        else:
            print(Fore.WHITE + line)  # White for odd lines
        time.sleep(0.1)  # Short delay (0.1 seconds per line)
    print(Fore.BLUE + """Running Scan...
                        Connection Completed Waiting For Results...
          """)

# Function to show the main menu logo with blue and white mix
def show_main_menu_logo():
    logo_text = r'''
    __         __  __                                 
   / /_  ___  / /_/ /____  _________ ___  ____ _____ 
  / __ \/ _ \/ __/ __/ _ \/ ___/ __ `__ \/ __ `/ __ \
 / /_/ /  __/ /_/ /_/  __/ /  / / / / / / /_/ / /_/ /
/_.___/\___/\__/\__/\___/_/  /_/ /_/ /_/\__,_/ .___/ 
                                            /_/     '''
    clear_screen()
    for i, line in enumerate(logo_text.splitlines()):
        if i % 2 == 0:
            print(Fore.BLUE + line)  # Blue for even lines
        else:
            print(Fore.WHITE + line)  # White for odd lines
        time.sleep(0.1)  # Medium delay (0.3 seconds per line)

# Function to run a scan with a given command
def run_scan(command, ip=None):
    global exit_program, scanning_in_progress
    scanning_in_progress = True
    try:
        # Display the fast loading screen
        fast_loading_screen()
        
        # Run the scan in a subprocess
        process = subprocess.Popen(command, shell=True)
        
        while process.poll() is None:
            time.sleep(0.1)  # Check every 100ms
        
        print("\nScan completed.")
        
        # Ask if the user wants to save the IPs to a file
        save_ips = input("Do you want to save the scanned IP addresses to a text file? (yes/no): ").strip().lower()
        if save_ips == "yes":
            with open("scanned_ips.txt", "a") as file:
                file.write(f"{ip}\n")
            print(f"IP addresses saved to 'scanned_ips.txt'.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running Nmap scan: {e}")
    finally:
        scanning_in_progress = False
        # Clear the screen after the scan
        clear_screen()

# Function to handle IP address input with exit option
def get_ip_address():
    ip = ""
    while True:
        ip = input("\nEnter IP address to scan (or press 'q' to cancel): ").strip()
        if ip.lower() == 'q':
            print("\nExiting IP input...")
            break
        if ip:
            return ip

# Function for automatic scan with default command
def automatic_scan():
    ip = get_ip_address()
    if ip:
        full_command = f"nmap -sV -vv -A -T4 -n {ip}"
        run_scan(full_command, ip)

# Function for automatic scan with DNS resolution disabled
def automatic_scan_no_dns():
    ip = get_ip_address()
    if ip:
        full_command = f"nmap -n -T4 {ip}"
        run_scan(full_command, ip)

# Function for automatic stealth scan
def automatic_stealth_scan():
    ip = get_ip_address()
    if ip:
        full_command = f"nmap -sS -D RND:10 -T4 {ip}"
        run_scan(full_command, ip)

# Function to scan multiple IP addresses (up to 240) with options for automatic or manual scan
def scan_multiple_ips():
    clear_screen()
    print("\nSelect an option:")
    print("1. Automatic Scan (-T4 -sS -sU --script vuln)")
    print("2. Manual Scan (Enter any Nmap scan command)")

    choice = input("\nEnter your choice: ").strip()

    if choice == '1':
        ips = input("\nEnter up to 240 IP addresses separated by space: ").split()
        if len(ips) > 240:
            print("You can only scan up to 240 IP addresses at once.")
            return
        
        full_command = f"nmap -T4 -sS -sU --script vuln {' '.join(ips)}"
        for ip in ips:
            run_scan(full_command, ip)
    
    elif choice == '2':
        ips = input("\nEnter up to 240 IP addresses separated by space: ").split()
        if len(ips) > 240:
            print("You can only scan up to 240 IP addresses at once.")
            return
        
        print("\nEnter any Nmap command for the scan:")
        command = input("Enter Nmap command (e.g., -sS, -sT, etc.): ").strip()
        for ip in ips:
            full_command = f"nmap {command} {ip}"
            run_scan(full_command, ip)

# Function to show all Nmap commands
def show_all_nmap_commands():
    clear_screen()
    commands = [
        "All Nmap Commands:",
        "nmap 192.168.1.1              Scan a single IP",
        "nmap 192.168.1.1-254          Scan a range",
        "nmap -iL targets.txt          Scan targets from a file",
        "nmap -sS 192.168.1.1          TCP SYN scan",
        "nmap -sT 192.168.1.1          TCP Connect scan",
        "nmap -O 192.168.1.1           OS detection",
        "nmap -sU 192.168.1.1          UDP scan",
        "nmap -p 80 192.168.1.1        Scan port 80",
        "nmap -p 1-1000 192.168.1.1    Scan ports 1-1000",
        "nmap -sV 192.168.1.1          Version detection",
        "nmap -A 192.168.1.1           OS detection, version detection, script scanning, traceroute",
        "nmap -Pn 192.168.1.1          Disable ping scan"
    ]
    show_submenu(commands)

# Function to show OS scan commands
def show_os_scan_commands():
    clear_screen()
    commands = [
        "OS Scan Commands:",
        "nmap -O 192.168.1.1           Enable OS detection",
        "nmap -A 192.168.1.1           Aggressive scan with OS detection",
        "nmap --osscan-guess           Guess the OS if exact match is not found"
    ]
    show_submenu(commands)

# Function to show NSE script commands
def show_nse_script_commands():
    clear_screen()
    commands = [
        "NSE Script Commands:",
        "nmap --script=vuln 192.168.1.1  Run vulnerability scripts",
        "nmap --script=http-enum 192.168.1.1  Enumerate web services",
        "nmap --script=default 192.168.1.1  Run default scripts"
    ]
    show_submenu(commands)

# Function to show firewall scan commands
def show_firewall_scan_commands():
    clear_screen()
    commands = [
        "Firewall Scan Commands:",
        "nmap -Pn 192.168.1.1           Scan without ping",
        "nmap -f 192.168.1.1            Fragment packets",
        "nmap --mtu 24 192.168.1.1      Specify custom MTU"
    ]
    show_submenu(commands)

# Function to show the submenu with command options
def show_submenu(commands):
    print("\n".join(commands))
    input("\nPress Enter to return to the main menu...")

# Function to handle manual Nmap scan (option 22)
def normal_nmap_scan():
    ip = get_ip_address()
    if ip:
        command = input("Enter your Nmap command: ").strip()
        full_command = f"nmap {command} {ip}"
        run_scan(full_command, ip)

# Exiting loading screen with blue and white color scheme
def exiting_loading_screen():
    clear_screen()
    exiting_text = '''
    ______     _ __  _                ____                                      
   / ____/  __(_) /_(_)___  ____ _   / __ \_________  ____ __________ _____ ___ 
  / __/ | |/_/ / __/ / __ \/ __ `/  / /_/ / ___/ __ \/ __ `/ ___/ __ `/ __ `__ /
 / /____>  </ / /_/ / / / / /_/ /  / ____/ /  / /_/ / /_/ / /  / /_/ / / / / / /
/_____/_/|_/_/\__/_/_/ /_/\__, /  /_/   /_/   \____/\__, /_/   \__,_/_/ /_/ /_/ 
                         /____/                    /____/                                           
'''
    # Fast printing of each line with a very short delay and alternating colors
    for i, line in enumerate(exiting_text.splitlines()):
        if i % 2 == 0:
            print(Fore.BLUE + line)  # Blue for even lines
        else:
            print(Fore.WHITE + line)  # White for odd lines
        time.sleep(0.2)  # Short delay (0.1 seconds per line)
    print(Fore.BLUE + """ByeBye""")
    sys.exit(0)  # Exit the program

# Main function to handle the menu and user choices
def main():
    global exit_program  # Make sure we track the exit condition

    while True:  # Continue until exit_program is set to True
        clear_screen()  # Clear screen each time we return to the main menu
        show_main_menu_logo()  # Display the logo

        print(Fore.LIGHTWHITE_EX+'''                                          
    Main Menu  biskit@   V 0.1
    1. Automatic Scan Super Fast Scan (-sV -vv -A -T4 -n)
    2. Show All Nmap Commands
    3. Show OS Scan Commands
    4. Show NSE Script Commands
    5. Show Firewall Scan Commands
    6. Scan Multiple IP Addresses (Up to 240 IPs)
    11. Script Vulnerability Scan (-sV -D --script vuln -T4)
    22. Normal Nmap Scan (Manual Commands)
    88. Automatic Stealth Scan (-sS -D -T4)
    00. Automatic Scan with DNS Resolution Disabled (-n -T4)
    44. Exit the program
    Press Ctrl+C to exit all scans.''')
        print("\nEnter 44 to exit the program at any time.")
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            automatic_scan()
        elif choice == '2':
            show_all_nmap_commands()
        elif choice == '3':
            show_os_scan_commands()
        elif choice == '4':
            show_nse_script_commands()
        elif choice == '5':
            show_firewall_scan_commands()
        elif choice == '6':
            scan_multiple_ips()
        elif choice == '11':
            print("Script Vulnerability Scan selected")
            ip = get_ip_address()
            if ip:
                full_command = f"nmap -sV -D --script=vuln -T4 {ip}"
                run_scan(full_command, ip)
        elif choice == '22':
            normal_nmap_scan()
        elif choice == '88':
            automatic_stealth_scan()  # Updated 88 option with -sS -D -T4
        elif choice == '00':
            print("Automatic Scan with DNS Resolution Disabled selected")
            automatic_scan_no_dns()
        elif choice == '44' or exit_program:  # Exit if "44" is typed
            # Exiting loading screen with blue and white color scheme
            exiting_loading_screen()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
