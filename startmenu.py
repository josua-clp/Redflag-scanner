from termcolor import colored



def display_menu():
    heading = colored(" ______     ______     _____     ______   __         ______     ______    \n/\  == \   /\  ___\   /\  __-.  /\  ___\ /\ \       /\  __ \   /\  ___\   \n\ \  __<   \ \  __\   \ \ \/\ \ \ \  __\ \ \ \____  \ \  __ \  \ \ \\__ \  \n \ \_\ \_\  \ \_____\  \ \____-  \ \_\    \ \_____\  \ \_\ \_\  \ \_____\ \n  \/_/ /_/   \/_____/   \/____/   \/_/     \/_____/   \/_/\/_/   \/_____/ \n", "red")
    print(heading)
    
    print(colored("{:^69}".format("Think twice!\n"), "red"))

    

    print("1. Start website scanner")
    print("2. Info")
    print("3. Exit")

    print(colored("{:^69}".format("Github: https://github.com/josua-clp/Redflag-scanner\n"), "red"))

def get_user_choice():
    choice = input("Enter your choice (1-3): ")
    while choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Please enter a number between 1 and 3.")
        choice = input("Enter your choice (1-3): \n")
    return int(choice)

def display_info():
    info = "This is a Python script that performs a series of checks on a website to determine its security status. The script uses the requests library to send HTTP requests and retrieve website content. The ssl, socket, time, and re libraries are also used.\n\nThe script performs the following checks:\n\n- Retrieves the IP address of the website and its region using the GeoIP API.\n- Makes a GET request to the website and checks if its SSL/TLS certificate is valid.\n- Retrieves some details about the website, such as the content type and server.\n- Checks if the website is a phishing website by looking for certain keywords in its content.\n- Finds all subdomains of the website and checks if they are active.\n- Finds all email addresses and usernames mentioned on the website.\n\nThe get_website_region function takes an IP address as input and retrieves the region name using the GeoIP API. The check_website_security function takes a website URL as input and performs all the checks described above.\n\nThe find_subdomains function takes a domain name as input and returns a set of all its subdomains. The find_emails_usernames function takes a string of text as input and returns two lists: one containing all email addresses mentioned in the text and one containing all usernames mentioned in the text."
    print(info)

if __name__ == "__main__":
    display_menu()
    choice = get_user_choice()

    if choice == 1:
        import scanner
    
    elif choice == 2:
        display_info()


    elif choice == 4:
        print("Exiting program...")



