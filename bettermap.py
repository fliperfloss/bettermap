import signal
import sys
import platform
import msvcrt
import subprocess
import threading
from colorama import Fore
import time

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

# Function to display the main menu
def main_menu():
    print(Fore.LIGHTWHITE_EX + ''' 
                                              
    __         __  __                                 
   / /_  ___  / /_/ /____  _________ ___  ____  _____ 
  / __ \/ _ \/ __/ __/ _ \/ ___/ __ __ \/ __ / __ //
 / /_/ /  __/ /_/ /_/  __/ /  / / / / / / /_/ / /_/ /
/_.___/\___/\__/\__/\___/_/  /_/ /_/ /_/\__,_/ .___/ 
                                            /_/  
    Main Menu  biskit@   V 0.1
    1. Automatic Scan (-sV -sI -p 20,21,22,23,25,53,69,139,445,1433,1434 -A -T4)
    2. Show All Nmap Commands
    3. Show OS Scan Commands
    4. Show NSE Script Commands
    5. Show Firewall Scan Commands
    6. Scan Multiple IP Addresses (Up to 240 IPs)
    11. Script Vulnerability Scan (-sV -sI --script=vuln -T4)
    22. Normal Nmap Scan (Manual Commands)
    88. Automatic Stealth Scan (-sS -sI RND:10 -T4)
    00. Automatic Scan with DNS Resolution Disabled (-n -T4)
    44. Exit the program''')

# Function to run a scan with a given command
def run_scan(command, ip=None):
    global exit_program, scanning_in_progress
    scanning_in_progress = True
    try:
        print(f"\nRunning: {command}")
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

# Function for automatic scan with default command
def automatic_scan():
    ip = input("\nEnter IP address to scan: ")
    full_command = f"nmap -sV -sI -p 20,21,22,23,25,53,69,139,445,1433,1434 -A -T4 {ip}"
    run_scan(full_command, ip)

# Function for automatic scan with DNS resolution disabled
def automatic_scan_no_dns():
    ip = input("\nEnter IP address to scan: ")
    full_command = f"nmap -n -T4 {ip}"
    run_scan(full_command, ip)

# Function to scan multiple IP addresses (up to 240) with options for automatic or manual scan
def scan_multiple_ips():
    print("\nSelect an option:")
    print("1. Automatic Scan (-sI -T4 -sS -sU --script=vuln)")
    print("2. Manual Scan (Enter any Nmap scan command)")
    
    choice = input("\nEnter your choice: ").strip()

    if choice == '1':
        ips = input("\nEnter up to 240 IP addresses separated by space: ").split()
        if len(ips) > 240:
            print("You can only scan up to 240 IP addresses at once.")
            return
        
        full_command = f"nmap -sI -T4 -sS -sU --script=vuln {' '.join(ips)}"
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

# Function to run a normal manual Nmap scan
def normal_nmap_scan():
    print("\nNormal Nmap Scan - Type your custom Nmap command:")
    while True:
        print("\n1. Scan a single IP")
        print("2. Scan a single IP with custom Nmap commands")
        print("44. Return to main menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            ip = input("\nEnter IP address to scan: ")
            full_command = f"nmap {ip}"
            run_scan(full_command, ip)
        
        elif choice == '2':
            ip = input("\nEnter IP address to scan: ")
            command = input("Enter custom Nmap command: ").strip()
            full_command = f"nmap {command} {ip}"
            run_scan(full_command, ip)
        
        elif choice == '44':
            print("Returning to the main menu...")
            return  # Return to the main menu if '44' is pressed
        
        else:
            print("Invalid choice. Please try again.")

# Function to show all Nmap commands
def show_all_nmap_commands():
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
    commands = [
        "OS Scan Commands:",
        "nmap -O 192.168.1.1           Enable OS detection",
        "nmap -A 192.168.1.1           Aggressive scan with OS detection",
        "nmap --osscan-guess           Guess the OS if exact match is not found"
    ]
    show_submenu(commands)

# Function to show NSE script commands
def show_nse_script_commands():
    commands = [
        "NSE Script Commands:",
        "nmap --script=vuln 192.168.1.1  Run vulnerability scripts",
        "nmap --script=http-enum 192.168.1.1  Enumerate web services",
        "nmap --script=default 192.168.1.1  Run default scripts"
    ]
    show_submenu(commands)

# Function to show firewall scan commands
def show_firewall_scan_commands():
    commands = [
        "Firewall Scan Commands:",
        "nmap -Pn 192.168.1.1           Scan without ping",
        "nmap -f 192.168.1.1            Fragment packets",
        "nmap --mtu 24 192.168.1.1      Specify custom MTU"
    ]
    show_submenu(commands)

# Function to display commands submenu
def show_submenu(commands):
    for command in commands:
        print(command)
    input("\nPress Enter to return to the main menu.")

# Main function to handle the menu and user choices
def main():
    while True:
        main_menu()
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
        elif choice == '22':
            normal_nmap_scan()
        elif choice == '00':
            print("Automatic Scan with DNS Resolution Disabled selected")
            print("1. Automatic Scan")
            print("2. Manual Scan")
            scan_choice = input("Enter your choice: ").strip()
            if scan_choice == '1':
                automatic_scan_no_dns()
            elif scan_choice == '2':
                normal_nmap_scan()
            else:
                print("Invalid choice. Returning to main menu.")
        elif choice == '44' or exit_program:  # Exit if "44" is typed
            print("Exiting program.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
