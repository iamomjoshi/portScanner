import socket
import sys
import ipaddress
import time
import threading
import random
import os
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

# Clear the terminal screen for a clean interface
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ANSI color codes for vibrant terminal output
class Colors:
    BLACK = '\033[30m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    ENDC = '\033[0m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

def animate_text(text, color=Colors.WHITE, delay=0.01):
    """Animate text by printing one character at a time"""
    for char in text:
        sys.stdout.write(f"{color}{char}{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_fancy_banner():
    """Display an attractive animated banner for the port scanner."""
    clear_screen()
    
    # ASCII art for the banner
    banner_art = f"""
{Colors.CYAN}{Colors.BOLD}
 ██████╗  ██████╗ ██████╗ ████████╗    ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ 
 ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗
 ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝
 ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗
 ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║
 ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
{Colors.ENDC}"""
    
    print(banner_art)
    
    # Animated tagline
    animate_text(f"{Colors.YELLOW}{Colors.BOLD}⚡ ADVANCED NETWORK RECONNAISSANCE TOOL ⚡{Colors.ENDC}", Colors.YELLOW, 0.01)
    print()
    
    # Feature list with animation
    features = [
        f"{Colors.GREEN}✓ {Colors.BLUE}Multi-threaded scanning for lightning-fast results",
        f"{Colors.GREEN}✓ {Colors.BLUE}Service detection for open ports",
        f"{Colors.GREEN}✓ {Colors.BLUE}Interactive interface with real-time progress",
        f"{Colors.GREEN}✓ {Colors.BLUE}Comprehensive port analysis"
    ]
    
    for feature in features:
        animate_text(feature, delay=0.005)
        time.sleep(0.1)
    
    # Creator credit with special styling
    print()
    creator_text = f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}  Created by Om Joshi  {Colors.ENDC}"
    print(f"{' ' * ((80 - len('Created by Om Joshi') - 4) // 2)}{creator_text}")
    print("\n" + "=" * 80 + "\n")

def animated_loading(duration=3):
    """Display an animated loading sequence."""
    chars = "⣾⣽⣻⢿⡿⣟⣯⣷"
    start_time = time.time()
    i = 0
    
    print(f"{Colors.CYAN}Initializing scanner", end="")
    
    while time.time() - start_time < duration:
        sys.stdout.write(f"{Colors.CYAN}{Colors.BOLD} {chars[i % len(chars)]}{Colors.ENDC}")
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b\b")
        i += 1
    
    print(f"{Colors.GREEN}{Colors.BOLD} [READY]{Colors.ENDC}")

def fancy_input(prompt, color=Colors.CYAN):
    """Display a fancy prompt for user input."""
    print(f"{color}{Colors.BOLD}{prompt}{Colors.ENDC}")
    print(f"{Colors.BRIGHT_BLACK}▶ {Colors.ENDC}", end="")
    return input()

def validate_ip(ip):
    """Validate if the provided string is a valid IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def validate_port_range(start, end):
    """Validate if the port range is valid."""
    if not (1 <= start <= 65535) or not (1 <= end <= 65535):
        return False
    if start > end:
        return False
    return True

def get_service_name(port):
    """Get the service name for a given port number."""
    common_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        115: "SFTP",
        135: "RPC",
        139: "NetBIOS",
        143: "IMAP",
        194: "IRC",
        443: "HTTPS",
        445: "SMB",
        1433: "MSSQL",
        1521: "Oracle",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP-Proxy",
        8443: "HTTPS-Alt"
    }
    
    if port in common_ports:
        return common_ports[port]
    
    try:
        service = socket.getservbyport(port)
        return service
    except:
        return "unknown"

def scan_port(ip, port, timeout=1):
    """Scan a single port on the specified IP address."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    sock.close()
    return port, result == 0

def display_fancy_progress(current, total, width=50):
    """Display an attractive progress bar for the scanning process."""
    progress = current / total
    completed = int(width * progress)
    remaining = width - completed
    
    # Create a gradient effect in the progress bar
    bar = ""
    for i in range(completed):
        if i < width * 0.33:
            bar += f"{Colors.GREEN}█"
        elif i < width * 0.66:
            bar += f"{Colors.YELLOW}█"
        else:
            bar += f"{Colors.RED}█"
    
    percent = round(progress * 100, 1)
    
    # Add a pulsing effect to the remaining part
    pulse_char = "▒" if (current % 2) == 0 else "░"
    
    sys.stdout.write(f"\r{Colors.BOLD}Progress: [{bar}{Colors.BRIGHT_BLACK}{pulse_char * remaining}{Colors.ENDC}{Colors.BOLD}] {percent}% ({current}/{total} ports){Colors.ENDC}")
    sys.stdout.flush()

def display_scan_results(open_ports, ip):
    """Display scan results in an attractive table."""
    if not open_ports:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[!] No open ports found in the specified range.{Colors.ENDC}")
        return
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}[+] Scan completed! Found {len(open_ports)} open ports on {ip}:{Colors.ENDC}\n")
    
    # Table header with background color
    print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD} {'PORT':<8} {'STATE':<8} {'SERVICE':<15} {Colors.ENDC}")
    
    # Table rows with alternating colors
    for i, port in enumerate(sorted(open_ports)):
        service = get_service_name(port)
        bg_color = Colors.BG_BLACK if i % 2 == 0 else ""
        
        # Color-code services based on potential security implications
        service_color = Colors.GREEN
        if service in ["SSH", "SFTP", "HTTPS"]:
            service_color = Colors.GREEN  # Secure services
        elif service in ["HTTP", "FTP", "Telnet", "SMB"]:
            service_color = Colors.YELLOW  # Potentially insecure
        elif service in ["RDP", "MySQL", "MSSQL", "Oracle"]:
            service_color = Colors.RED  # Often targeted services
        
        print(f"{bg_color}{Colors.BOLD} {Colors.CYAN}{port:<8}{Colors.GREEN} {'OPEN':<8}{service_color} {service:<15} {Colors.ENDC}")
    
    print("\n" + "=" * 80)

def show_scan_summary(start_time, end_time, scanned_ports, open_ports, ip):
    """Show a summary of the scan with timing information."""
    duration = end_time - start_time
    ports_per_second = scanned_ports / duration if duration > 0 else 0
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}📊 SCAN SUMMARY{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 40}{Colors.ENDC}")
    print(f"{Colors.YELLOW}🎯 Target:{Colors.ENDC} {Colors.WHITE}{ip}{Colors.ENDC}")
    print(f"{Colors.YELLOW}⏱️ Duration:{Colors.ENDC} {Colors.WHITE}{duration:.2f} seconds{Colors.ENDC}")
    print(f"{Colors.YELLOW}🔍 Ports Scanned:{Colors.ENDC} {Colors.WHITE}{scanned_ports}{Colors.ENDC}")
    print(f"{Colors.YELLOW}🚪 Open Ports:{Colors.ENDC} {Colors.WHITE}{len(open_ports)}{Colors.ENDC}")
    print(f"{Colors.YELLOW}⚡ Scan Rate:{Colors.ENDC} {Colors.WHITE}{ports_per_second:.2f} ports/second{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 40}{Colors.ENDC}")

def show_menu():
    """Display the main menu with options."""
    print(f"\n{Colors.CYAN}{Colors.BOLD}📋 MAIN MENU{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 40}{Colors.ENDC}")
    print(f"{Colors.YELLOW}1.{Colors.ENDC} {Colors.WHITE}Start New Scan{Colors.ENDC}")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} {Colors.WHITE}About{Colors.ENDC}")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} {Colors.WHITE}Exit{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 40}{Colors.ENDC}")
    
    choice = fancy_input("Select an option (1-3):")
    return choice

def show_about():
    """Display information about the port scanner."""
    clear_screen()
    print(f"\n{Colors.CYAN}{Colors.BOLD}ℹ️ ABOUT THIS TOOL{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.ENDC}")
    
    about_text = [
        f"{Colors.WHITE}The Advanced Port Scanner is a powerful network reconnaissance tool",
        f"designed to identify open ports and services on target systems.",
        f"",
        f"This tool uses multi-threading to perform rapid port scanning while",
        f"providing a user-friendly interface with real-time progress updates.",
        f"",
        f"Use this tool responsibly and only on systems you have permission to scan.{Colors.ENDC}"
    ]
    
    for line in about_text:
        animate_text(line, delay=0.005)
    
    print(f"\n{Colors.YELLOW}{Colors.BOLD}Created by Om Joshi{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.ENDC}")
    
    input(f"\n{Colors.GREEN}Press Enter to return to the main menu...{Colors.ENDC}")

def perform_scan():
    """Perform the port scanning operation."""
    clear_screen()
    print(f"\n{Colors.CYAN}{Colors.BOLD}🔍 NEW SCAN{Colors.ENDC}")
    print(f"{Colors.BLUE}{'=' * 40}{Colors.ENDC}")
    
    # Get IP address with validation
    while True:
        ip = fancy_input("Enter the target IP address:")
        if validate_ip(ip):
            break
        print(f"{Colors.RED}{Colors.BOLD}[!] Invalid IP address. Please try again.{Colors.ENDC}")
    
    # Get port range with validation
    while True:
        try:
            start_port = int(fancy_input("Enter the starting port (1-65535):"))
            end_port = int(fancy_input("Enter the ending port (1-65535):"))
            
            if validate_port_range(start_port, end_port):
                break
            print(f"{Colors.RED}{Colors.BOLD}[!] Invalid port range. Ports must be between 1-65535 and start port must be less than or equal to end port.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}{Colors.BOLD}[!] Please enter valid numbers for ports.{Colors.ENDC}")
    
    # Get scan speed/threads with validation
    while True:
        try:
            threads = int(fancy_input("Enter number of threads (1-100, higher = faster):"))
            if 1 <= threads <= 100:
                break
            print(f"{Colors.RED}{Colors.BOLD}[!] Please enter a number between 1 and 100.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}{Colors.BOLD}[!] Please enter a valid number.{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}{Colors.BOLD}[*] Preparing to scan {ip} from port {start_port} to {end_port} with {threads} threads...{Colors.ENDC}")
    
    # Show animated loading
    animated_loading(2)
    
    # Prepare for scanning
    ports_to_scan = list(range(start_port, end_port + 1))
    total_ports = len(ports_to_scan)
    open_ports = []
    scanned_count = 0
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Scanning in progress...{Colors.ENDC}")
    
    # Start timing
    start_time = time.time()
    
    # Start scanning with fancy progress updates
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_port = {executor.submit(scan_port, ip, port): port for port in ports_to_scan}
        
        for future in future_to_port:
            port, is_open = future.result()
            scanned_count += 1
            
            if is_open:
                open_ports.append(port)
            
            display_fancy_progress(scanned_count, total_ports)
    
    # End timing
    end_time = time.time()
    
    # Display results
    print("\n")
    display_scan_results(open_ports, ip)
    show_scan_summary(start_time, end_time, total_ports, open_ports, ip)
    
    input(f"\n{Colors.GREEN}Press Enter to return to the main menu...{Colors.ENDC}")

def main():
    """Main function to run the port scanner."""
    try:
        while True:
            print_fancy_banner()
            choice = show_menu()
            
            if choice == "1":
                perform_scan()
            elif choice == "2":
                show_about()
            elif choice == "3":
                print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using the Advanced Port Scanner by Om Joshi!{Colors.ENDC}")
                break
            else:
                print(f"{Colors.RED}{Colors.BOLD}[!] Invalid choice. Please select a valid option.{Colors.ENDC}")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}{Colors.BOLD}[!] Scan interrupted by user.{Colors.ENDC}")
        print(f"\n{Colors.GREEN}{Colors.BOLD}Thank you for using the Advanced Port Scanner by Om Joshi!{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}{Colors.BOLD}[!] An error occurred: {str(e)}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()
