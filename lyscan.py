import dns.resolver
import argparse
import asyncio
import os
import sys
from colorama import init, Fore
import pyfiglet  # Import the pyfiglet library

# Initialize colorama
init(autoreset=True)

# List to store found subdomains
found_subdomains = []

# Function to resolve a subdomain and print the result with color immediately
async def resolve_subdomain(subdomain, domain):
    global found_subdomains
    resolver = dns.resolver.Resolver()
    # Use Google's public DNS for reliable resolution
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    
    try:
        # Attempt to resolve the subdomain
        result = resolver.resolve(f"{subdomain}.{domain}", "A")
        if result:
            found_subdomains.append(f"{subdomain}.{domain}")
            print(f"{Fore.GREEN}[+] Found: {subdomain}.{domain}")
        else:
            print(f"{Fore.RED}[-] No result for: {subdomain}.{domain}")
        sys.stdout.flush()  # Ensure that the output is immediately flushed
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        # Subdomain does not exist, this is normal
        print(f"{Fore.RED}[-] No result for: {subdomain}.{domain}")
        sys.stdout.flush()  # Ensure output is flushed immediately
    except Exception as e:
        print(f"{Fore.YELLOW}Error resolving {subdomain}.{domain}: {e}")
        sys.stdout.flush()  # Flush the output even if there is an error

# Function to scan subdomains based on a wordlist
async def scan_subdomains(domain, wordlist_path):
    if not os.path.exists(wordlist_path):
        print(f"{Fore.RED}[-] Wordlist not found at: {wordlist_path}")
        sys.stdout.flush()
        return

    # Open and read the wordlist
    with open(wordlist_path, 'r') as f:
        wordlist = f.read().splitlines()

    print(f"{Fore.CYAN}Starting scan for {len(wordlist)} subdomains...")
    sys.stdout.flush()  # Flush after initial message

    # Create and run asynchronous tasks for each subdomain in the wordlist
    tasks = []
    for word in wordlist:
        tasks.append(resolve_subdomain(word, domain))

    # Wait for all tasks to finish
    await asyncio.gather(*tasks)

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Lyscan - DNS Subdomain Enumerator")
    parser.add_argument("domain", help="The domain to scan for subdomains.")
    parser.add_argument("--wordlist", default="wordlist.txt", help="Path to wordlist for subdomain enumeration.")
    parser.add_argument("--threads", type=int, default=10, help="Number of concurrent threads.")
    return parser.parse_args()

# Function to display found subdomains after the scan
def display_found_subdomains():
    if found_subdomains:
        print(f"\n{Fore.CYAN}Found subdomains:")
        for subdomain in found_subdomains:
            print(f"{Fore.GREEN}{subdomain}")
    else:
        print(f"{Fore.RED}No subdomains were found.")

# Function to print the banner
def print_banner():
    banner = pyfiglet.figlet_format("Midnight - Ops")
    print(Fore.CYAN + banner)
    print(Fore.GREEN + "DNS Subdomain Enumeration Tool + Directory Scanner")
    print(Fore.YELLOW + "by 1yc4n0rn0t - \n")

# ASCII art underneath the banner
    ascii_art = '''
      .---.
      |---|
      |---|
      |---|
  .---^ - ^---.
  :___________:
     |  |//|
     |  |//|
     |  |//|
     |  |//|
     |  |//|
     |  |//|
     |  |.-|
     |.-'**|
      \***/
       \*/
        V

       '
        ^'
       (_)
    '''
    print(Fore.YELLOW + ascii_art)


# Main function to run the tool
def main():
    print_banner()  # Print the banner at the start
    args = parse_arguments()
    print(f"{Fore.CYAN}Starting Lyscan on {args.domain} using wordlist {args.wordlist}...")
    sys.stdout.flush()  # Flush after initial start message
    asyncio.run(scan_subdomains(args.domain, args.wordlist))
    print(f"{Fore.GREEN}Scan complete!")

    # Display found subdomains after the scan completes
    display_found_subdomains()
    sys.stdout.flush()  # Final flush after scan is done

if __name__ == "__main__":
    main()
