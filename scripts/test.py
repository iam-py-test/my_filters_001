import dns, dns.resolver
import os, sys, json, datetime, socket, random, publicsuffixlist, ssl, requests, time

dead_domains = []
print("GETTING PSL")
p = publicsuffixlist.PublicSuffixList(only_icann=True)
print("GOT PSL, SETTING UP resolver")
resolver = dns.resolver.Resolver()
print("CREATED resolver")
resolver.nameservers = ["https://unfiltered.adguard-dns.com/dns-query","94.140.14.140", "8.8.8.8","1.1.1.1"]
print("SETUP resolver")
already_resolved = {}
known_whois = {}

verbosity = 4

def get_whois_data_raw(domain, server):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, 43))
    all_data = b""
    s.send("{domain}\r\n".replace("{domain}", domain).encode())
    while True:
        try:
            newdata = s.recv(100)
            if len(newdata) == 0:
                break
            all_data += newdata
        except Exception:
            break
    s.close()
    return all_data.decode()

get_whois = None
def get_whois(domain, server = None, done_whois_servers = [], recurse=False, sub=False):
    global known_whois
    print(f"Getting WHOIS record for {domain} using {server or 'no server specified'}, recurse is {recurse}")
    if server != None:
        done_whois_servers.append(server)
    if domain in known_whois and sub == False:
        return known_whois[domain]
    if server == None:
        tld = p.publicsuffix(domain).upper()
        if tld in TLD_WHOIS_OVERRIDE:
            server = TLD_WHOIS_OVERRIDE[tld]
        else:
            server = f"{tld}.whois-servers.net"
    try:
        whois_data = get_whois_data_raw(domain, server)
    except Exception as err:
        print(f"{server} failed to get WHOIS for {domain} due to {err} ({sub} - {recurse} - {','.join(done_whois_servers)})")
        if sub == False and f"whois.nic.{tld}" not in done_whois_servers:
            print(f"Trying whois.nic.{tld}")
            done_whois_servers.append(f"whois.nic.{tld}")
            return get_whois(domain, server=f"whois.nic.{tld}", done_whois_servers=done_whois_servers, recurse=recurse, sub=sub)
        return ""
    if recurse == True:
        try:
            for line in whois_data.replace("\r", "").split("\n"):
                if line.replace(" ", "").replace("\t", "").startswith("RegistrarWHOISServer:"):
                    newserver = line.replace(" ", "").replace("\t", "").replace("RegistrarWHOISServer:", "").replace("http://", "").replace("https://", "").split("/")[0]
                    if newserver not in done_whois_servers:
                        whois_data += f"\n\nFetching more WHOIS data from {newserver}...\n\n" + get_whois(domain, server=newserver, recurse=True, sub=True, done_whois_servers=done_whois_servers)
                    done_whois_servers.append(newserver)
        except Exception as err:
            print(f"Recurse for {domain} ({server}) failed due to {err}")
                    
    if sub == False:
        known_whois[domain] = whois_data
    return whois_data


def is_alive(domain, in_list=True):
    global dead_domains
    global already_resolved
    if domain in already_resolved:
        return True
    if domain in dead_domains:
        return False
    if domain.endswith(".onion"): # can't test onions yet
        return True
    try:
        res_ips = list(resolver.resolve(domain))
        found_ips = []
        for ip in res_ips:
            found_ips.append(ip.address)
        already_resolved[domain] = found_ips
        return True
    except:
        if domain not in dead_domains and in_list:
            dead_domains.append(domain)
        return False


