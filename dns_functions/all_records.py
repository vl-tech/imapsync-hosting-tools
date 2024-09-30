import os


def get_ip(domain):
    ip = os.popen(f'dig +short {domain}').read()
    
    return f"Domain IP is - {ip}"

def get_ns(domain):
    ns = os.popen(f'dig +short NS {domain}').read()
    
    return f"NameServers are:\n{ns}"

def get_mx(domain):
    mx = os.popen(f'dig +short MX {domain}').read()
    
    return f"Domain MX Record is - {mx}"

def get_txt(domain):
    txt = os.popen(f'dig +short TXT {domain}').read()
  
    return f"Domain TXT records\n{txt}\n"

def  ptr_lookup(domain):
    ptr = os.popen(f'host {domain}').read()
    
    return f"Domain PTR is\n{ptr}"

def whois_info(domain):
    whois = os.popen(f'whois {domain} | grep DNSSEC ').read()
    
    return f"DNSSEC Status - {whois}"
