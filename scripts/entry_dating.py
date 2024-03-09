import os, sys, json, datetime, socket, random, publicsuffixlist
import dns.resolver

dead_domains = []
p = publicsuffixlist.PublicSuffixList(only_icann=True)
resolver = dns.resolver.Resolver()
resolver.nameservers = ["https://unfiltered.adguard-dns.com/dns-query","94.140.14.140", "8.8.8.8","1.1.1.1"]
already_resolved = {}
known_whois = {}

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

def get_whois(domain):
    global known_whois
    if domain in known_whois:
        return known_whois[domain]
    tld = p.publicsuffix(domain).upper()
    server = f"{tld}.whois-servers.net"
    try:
        whois_data = get_whois_data_raw(domain, server)
    except:
        return ""
    known_whois[domain] = whois_data
    return whois_data

def whois_exists(domain):
    global dead_domains
    if domain.endswith(".onion"): # can't test onions yet
        return True
    try:
        whois_data = get_whois(domain)
        if "No match for" in whois_data or "No Data Found" in whois_data or "No whois information found" in whois_data:
            return False
        return whois_data != ""
    except:
        return False

def is_alive(domain):
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
        if domain not in dead_domains and whois_exists(domain) == False:
            dead_domains.append(domain)
        return False

def get_ips(domain):
    global already_resolved
    if domain in already_resolved:
        return already_resolved[domain]
    if domain in dead_domains:
        return []
    try:
        res_ips = list(resolver.resolve(domain))
        found_ips = []
        for ip in res_ips:
            found_ips.append(ip.address)
        already_resolved[domain] = found_ips
        return found_ips
    except:
        return []

def is_valid(domain):
    try:
        return p.publicsuffix(domain, accept_unknown=False) != None
    except:
        return False

def port_open(host, port):
    try:
        s = socket.socket()
        return s.connect_ex((host, port)) == 0
    except:
        return False

try:
    entry_data = json.loads(open("entry_data.json", encoding="UTF-8").read())
except:
    entry_data = {}

domain_list = open("Alternative list formats/antimalware_domains.txt", encoding="UTF-8").read().replace("\r\n","\n").split("\n")
current_date = datetime.datetime.now().isoformat()
entry_data["last_updated"] = current_date


for e in domain_list:
    #print(e, e in entry_data)
    if (e not in entry_data or type(entry_data[e]) == str) and e != "last_updated":
        entry_is_alive = is_alive(e)
        dead_since = ""
        if entry_is_alive != True:
            dead_since = current_date
        entry_data[e] = {
            "first_seen": current_date,
            "last_seen": current_date,
            "removed": False,
            "removed_date": "",
            "last_checked": current_date,
            "check_counter": random.randint(35, 49),
            "check_status": entry_is_alive,
            "alive_on_creation": entry_is_alive,
            "times_checked": 1,
            "ever_rechecked": False,
            "readded": False,
            "alive_on_removal": None,
            "origin_add": "",
            "readd": "",
            "is_valid": is_valid(e),
            "ips": get_ips(e),
            "dead_since": dead_since,
            "whois": get_whois(e),
            "ports_open": {
                80: port_open(e, 80),
                443: port_open(e, 443),
                8000: port_open(e, 8000),
                8080: port_open(e, 8080),
                9090: port_open(e, 9090)
            }
        }
    else:
        if "times_checked" not in entry_data[e]:
            entry_data[e]["times_checked"] = 0
        if "check_status" not in entry_data[e]:
            domain_is_alive = is_alive(e)
            entry_data[e]["check_status"] = domain_is_alive
            entry_data[e]["last_checked"] = current_date
            if domain_is_alive != True:
                entry_data[e]["dead_since"] = current_date
            entry_data[e]["check_counter"] = 0
            entry_data[e]["ever_rechecked"] = True
            entry_data[e]["times_checked"] = 0
            if "ips" not in entry_data[e]:
                entry_data[e]["ips"] = get_ips(e)
        elif "ips" not in entry_data[e]:
            entry_data[e]["ips"] = get_ips(e)
        if entry_data[e]["check_status"] == False:
            dead_domains.append(e)
        if "removed" in entry_data[e]:
            if entry_data[e]["removed"] == True:
                entry_data[e]["readded"] = True
                entry_data[e]["readd"] = current_date
                entry_data[e]["origin_add"] = entry_data[e]["first_seen"]
                entry_data[e]["origin_removed_date"] = entry_data[e]["last_seen"]
        entry_data[e]["last_seen"] = current_date
        entry_data[e]["removed"] = False
        entry_data[e]["removed_date"] = ""
        entry_data[e]["is_valid"] = is_valid(e)
        if "check_counter" not in entry_data[e]:
            entry_data[e]["check_counter"] = random.randint(5, 40)
        if "last_checked" not in entry_data[e]:
            entry_data[e]["last_checked"] = "Unknown"
        entry_data[e]["check_counter"] += 1
        if entry_data[e]["check_counter"] > 45:
            print(f"Checking {e}...")
            domain_is_alive = is_alive(e)
            entry_data[e]["check_status"] = domain_is_alive
            entry_data[e]["last_checked"] = current_date
            entry_data[e]["check_counter"] = 0
            entry_data[e]["ever_rechecked"] = True
            entry_data[e]["times_checked"] += 1
            if "whois" not in entry_data[e]:
                entry_data[e]['whois'] = get_whois(e)
            if "ips" not in entry_data[e]:
                entry_data[e]["ips"] = get_ips(e)
            if domain_is_alive != True:
                entry_data[e]["dead_since"] = current_date
print("Done with part 1")
for e in entry_data:
    if e not in domain_list and e != "last_updated":
        try:
            if "dead_on_removal" in entry_data[e]:
                entry_data[e]['alive_on_removal'] = entry_data[e]["dead_on_removal"]
            if entry_data[e]["removed"] == False:
                entry_data[e]["removed"] = True
                entry_data[e]["removed_date"] = current_date
                entry_data[e]["alive_on_removal"] = is_alive(e)
        except Exception as err:
            print(err, e, entry_data[e])
print("Done with part 2")
entry_data_file = open("entry_data.json", 'w', encoding="UTF-8")
entry_data_file.write(json.dumps(entry_data))
entry_data_file.close()

dead_stuff = open("dead.mwbcheck.txt", 'w', encoding='UTF-8')
dead_stuff.write("\n".join(dead_domains))
dead_stuff.close()
