import requests
import ssl
import socket
import time
import re
from urllib.parse import urlparse


ssl._create_default_https_context = ssl._create_unverified_context

def get_website_region(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        if response.ok:
            data = response.json()
            return data.get("regionName")
        else:
            print(f"❌ Could not retrieve region for IP address {ip_address}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to GeoIP API: {e}")

def check_website_security(url):
    
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

   
    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"\n🔍 IP address of {hostname}: {ip_address}")
    except socket.gaierror as e:
        print(f"❌ Could not resolve hostname {hostname}: {e}")

 
    region = get_website_region(ip_address)
    if region:
        print(f"🌎 {hostname} is hosted in {region}.")
    else:
        print(f"❌ Could not retrieve region for IP address {ip_address}.")

    try:
        print("\nLoading...")
        time.sleep(2) 
        response = requests.get(url)
        if response.ok:
            connection = response.raw._connection
            if connection and connection.sock:
                cert = connection.sock.getpeercert()
                if not cert:
                    print(f"\n❌ {hostname} does not have a valid SSL/TLS certificate.")
                else:
                    print(f"\n✅ {hostname} has a valid SSL/TLS certificate.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to {hostname}: {e}")

    try:
        response = requests.get(url)
        if response.ok:
            content_type = response.headers.get("Content-Type")
            server = response.headers.get("Server")
            print(f"\n🌐 {hostname} is running {server} and serving content of type {content_type}.")

          
            if "text/html" in content_type:
                text = response.text.lower()
                if "Login" in text or "Signin" in text or "log in" in text or "sign in" in text:
                    if "password" in text or "email" in text or "username" in text:
                        print(f"\n⚠️  {hostname} might be a phishing website.")
                    else:
                        print(f"\n✅ {hostname} is probably not a phishing website.")
                else:
                    print(f"\n✅ {hostname} is probably not a phishing website.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to {hostname}: {e}")


    print(f"\n🔎 Subdomains of {hostname}:")
    subdomains = find_subdomains(hostname)
    for subdomain in subdomains:
        subdomain_url = f"https://{subdomain}.{hostname}"
        try:
            response = requests.get(subdomain_url)
            if response.ok:
                print(f"✅ {subdomain_url} is active.")
            else:
                print(f"❌ {subdomain_url} is inactive.")
        except requests.exceptions.RequestException:
            print(f"❌ {subdomain_url} is inactive.")

 
    print(f"\n📧 Email addresses and usernames mentioned on {hostname}:")
    response = requests.get(url)
    if response.ok:
        emails_users = find_emails_usernames(response.text)
        if not emails_users[0] and not emails_users[1]:
            print("No email addresses or usernames found.")
        else:
            if emails_users[0]:
                print(f"📬 Email addresses: {emails_users[0]}")
            if emails_users[1]:
                print(f"🧑 Usernames: {emails_users[1]}")
    else:
        print("Could not retrieve website content.")



def check_phishing(url):
    try:
        red_flags = []
     
        print(f"\n⛳ Red flags: ")

       
        response = requests.get(url, allow_redirects=False)
        if response.status_code >= 300 and response.status_code < 400:
            red_flags.append(f"{url} (redirect detected)")

       
        if re.search(r"window.location\s*=", response.text):
            red_flags.append(f"{url} (JavaScript redirect detected)")

     
        if re.search(r"(paypal.com|paypal\.com|paypal-com\.com|paypal-login\.com)", url, re.IGNORECASE):
            red_flags.append(f"{url} (suspicious URL)")

        if "text/html" in response.headers.get("Content-Type"):
            text = response.text.lower()

         
            if re.search(r"login|signin|log in|sign in", text) and (re.search(r"password", text) or re.search(r"email|username", text)):
                red_flags.append(f"{url} (fake login form detected)")

           
            if re.search(r"paypa1|paypai|paypall|paypal1\n", text):
                red_flags.append(f"{url} (misspelled URL detected)")

        if red_flags:
            print("\033[91m" + "\n".join(red_flags) + "\033[0m") 
        else:
            print("✅ No red flags detected\n")

    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to {url}")


def find_subdomains(domain_name):
    """
    Finds all subdomains of a given domain name.
    """
    subdomains = set()
    for i in range(1, 10): 
        subdomain = f"{'.'.join(domain_name.split('.')[:-i])}"
        if subdomain != domain_name:
            subdomains.add(subdomain)
        else:
            break
    return subdomains

def find_emails_usernames(text):
    """
    Finds all email addresses and usernames in a given text.
    """
    import re

 
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    username_regex = r'\B@\w+(?!\.)'

    emails = re.findall(email_regex, text)
    usernames = re.findall(username_regex, text)

   
    return list(set(emails)), list(set(usernames))

def check_sql_injection(url):
    try:
        print("\n\033[30m                   Deeper Information                       \033[0m")
        print("\033[30m+--------------------------------------------------------+\033[0m\n")
        print(f"\n💉 Vulnerable to SQL injection: ")
        response = requests.get(url + "'")
        if response.status_code == 500:
            print(f"❌ {url} is vulnerable to SQL injection.")
        else:
            print(f"✅ {url} is not vulnerable to SQL injection.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to {url}")


def check_website_info(url):
    try:
        response = requests.get(url)
        if response.ok:
            print(f"\n🏹 Information gathering: ")

          
            cookies = response.cookies
            cookies_text = f"🍪 Cookies: {cookies}"
            if re.search(r"\b(admin|password|secret)\b", cookies_text, re.IGNORECASE):
                cookies_text = cookies_text.replace(
                    re.search(r"\b(admin|password|secret)\b", cookies_text, re.IGNORECASE).group(0),
                    "\033[91m" + re.search(r"\b(admin|password|secret)\b", cookies_text, re.IGNORECASE).group(0) + "\033[0m"
                ) 
            print(cookies_text)

           
            headers = response.headers
            headers_text = f"\n🧭 Headers: {headers}"
            if re.search(r"\b(X-|Access-Control-Allow-Origin|Server)\b", headers_text, re.IGNORECASE):
                headers_text = headers_text.replace(
                    re.search(r"\b(X-|Access-Control-Allow-Origin|Server)\b", headers_text, re.IGNORECASE).group(0),
                    "\033[91m" + re.search(r"\b(X-|Access-Control-Allow-Origin|Server)\b", headers_text, re.IGNORECASE).group(0) + "\033[0m"
                ) 
            print(headers_text)
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to {url}")


def check_xss(url):
    try:
        response = requests.get(url)
        if response.ok:
            print("\n✖️  Vulnerable to XSS attacks: ")
            if "<script>alert(" in response.text:
                print(f"❌ {url} is vulnerable to XSS attacks.")
            else:
                print(f"✅ {url} is not vulnerable to XSS attacks.")
        else:
            print(f"❌ Could not connect to {url}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to {url}")



def check_ddos_protection(url):
    cdn_providers = ["Cloudflare", "Akamai", "Fastly", "AWS CloudFront"]
    try:
        response = requests.get(url)
        if response.ok:
            print(f"\n📜 Protected against DDoS attacks:")
            headers = response.headers
            for header in headers:
                header_value = headers[header]
                if any(provider in header_value for provider in cdn_providers):
                    print(f"✅ {url} is using a CDN known for its DDoS protection.")
                    return True
            print(f"❌ {url} is not using a CDN known for its DDoS protection.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to {url}")
        return False



url = input("👉 Enter a website URL: ")


check_website_security(url)
check_phishing(url)
check_sql_injection(url)
check_xss(url)
check_ddos_protection(url)
check_website_info(url)
