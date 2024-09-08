print(f"{__file__} STARTED")
import dns, dns.resolver
print("IMPORTING NORMAL LIBS")
import os, sys, json, datetime, socket, random, publicsuffixlist, ssl, requests, time
print("IMPORTS DONE")

TLD_WHOIS_OVERRIDE = {
    "panasonic": "whois.nic.gmo",
}

dead_domains = []
print("GETTING PSL")
p = publicsuffixlist.PublicSuffixList(only_icann=True)
print("GOT PSL, SETTING UP resolver")
dresolver = dns.resolver.Resolver()
print("CREATED dresolver")
dresolver.nameservers = ["https://unfiltered.adguard-dns.com/dns-query","94.140.14.140", "8.8.8.8","1.1.1.1"]
print("SETUP resolver")
already_resolved = {}
known_whois = {}

try:
    parked_ips = open("parking.ips").read().split('\n')
except:
    parked_ips = []

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
def get_whois(domain, server = None, done_whois_servers_arg = [], recurse=False, sub=False):
    global known_whois
    done_whois_servers = list(done_whois_servers_arg)
    print(f"Getting WHOIS record for {domain} using {server or 'no server specified'}, recurse is {recurse}")
    if server != None:
        done_whois_servers.append(server.lower())
    if domain in known_whois and sub == False:
        return known_whois[domain]
    tld = p.publicsuffix(domain).lower()
    if server == None:
        if tld in TLD_WHOIS_OVERRIDE:
            server = TLD_WHOIS_OVERRIDE[tld]
        else:
            server = f"{tld}.whois-servers.net"
    try:
        whois_data = get_whois_data_raw(domain, server)
    except Exception as err:
        print(f"{server} failed to get WHOIS for {domain} due to {err} ({sub} - {recurse} - {','.join(done_whois_servers)})")
        if sub == False and f"whois.nic.{tld}".lower() not in done_whois_servers:
            print(f"Trying whois.nic.{tld}")
            done_whois_servers.append(f"whois.nic.{tld}".lower())
            return get_whois(domain, server=f"whois.nic.{tld}".lower(), done_whois_servers_arg=done_whois_servers, recurse=recurse, sub=sub)
        return ""
    if recurse == True:
        try:
            for line in whois_data.replace("\r", "").split("\n"):
                if line.replace(" ", "").replace("\t", "").startswith("RegistrarWHOISServer:"):
                    newserver = line.replace(" ", "").replace("\t", "").replace("RegistrarWHOISServer:", "").replace("http://", "").replace("https://", "").split("/")[0]
                    if newserver.lower() not in done_whois_servers:
                        whois_data += f"\n\nFetching more WHOIS data from {newserver}...\n\n" + get_whois(domain, server=newserver.lower(), recurse=True, sub=True, done_whois_servers_arg=done_whois_servers)
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
    if domain.endswith(".onion"): # can't test onions yet
        return True
    if domain.endswith(".github.io"):
        try:
            username = domain.replace(".github.io", "")
            userreq = requests.get(f"https://api.github.com/users/{username}")
            if userreq.status_code == 404:
                return False
        except:
            pass
    if domain.endswith(".itch.io") or domain.endswith(".appspot.com") or domain.endswith(".squarespace.com") or domain.endswith(".web.app"):
        try:
            userreq = requests.get(f"http://{domain}")
            if userreq.status_code == 404:
                return False
        except:
            pass
    if domain.endswith(".page.link"):
        try:
            userreq = requests.get(f"http://{domain}")
            if userreq.status_code == 400:
                return False
        except:
            pass
    if domain.endswith(".azurefd.net"):
        try:
            userreq = requests.get(f"http://{domain}")
            if userreq.status_code == 404 and "azurefrontdoorpages.azureedge.net/pages/PageNotFound_files/favicon.ico" in userreq.text:
                return False
        except:
            pass
    if domain.endswith(".glitch.me"):
        try:
            userreq = requests.get(f"http://{domain}")
            if (userreq.status_code == 403 and "<title>Oops! This project isn't running.</title>" in userreq.text) or userreq.status_code == 401:
                return False
        except:
            pass
    try:
        res_ips = list(dresolver.resolve(domain))
        found_ips = []
        for ip in res_ips:
            found_ips.append(ip.address)
            if ip.address in parked_ips:
                return False
        already_resolved[domain] = found_ips
        return True
    except Exception:
        return False

def get_ips(domain):
    global already_resolved
    if domain in already_resolved:
        return already_resolved[domain]
    try:
        res_ips = list(dresolver.resolve(domain))
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
    """
    causes the program to hang for some reason
    """
    return False # prevent use
    try:
        s = socket.socket()
        return s.connect_ex((host, port)) == 0
    except:
        return False

def get_tls_info(hostname):
    # https://stackoverflow.com/questions/41620369/how-to-get-ssl-certificate-details-using-python
    context = ssl.create_default_context()
    context.check_hostname = False
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 5 second timeout
    conn.settimeout(5.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    return ssl_info

def get_last_commit():
    try:
        return requests.get("https://api.github.com/repos/iam-py-test/my_filters_001/commits").json()[0]['html_url']
    except Exception as err:
        print(err)
        return None

def get_dns_record(domain, record):
    try:
        records = []
        resolved_records = dresolver.resolve(domain, record)
        for returned_record in resolved_records:
            records.append(returned_record.to_text())
    except:
        pass
    return records

print("LOADING DATA")
try:
    entry_data = json.loads(open("entry_data.json", encoding="UTF-8").read())
except:
    print("FAILED TO LOAD DATA")
    entry_data = {}
print("LOADED DATA")

print("LOADING DOMAINS")
domain_list = open("Alternative list formats/antimalware_domains.txt", encoding="UTF-8").read().replace("\r\n","\n").split("\n")
print("LOADED DOMAINS")
current_date = datetime.datetime.now().isoformat()
entry_data["last_updated"] = current_date

print("DOING RANDOM RECHECK")
# recheck a random entry regardless of it's status
random_recheck = None
try:
    random_recheck = random.choice(domain_list)
    print('random recheck',entry_data[random_recheck]['check_counter'], entry_data[random_recheck]['first_seen'] , random_recheck)
    if random_recheck in entry_data:
        entry_data[random_recheck]['check_counter'] = 55
except Exception as err:
    print('random recheck failed', err)
print("RANDOM RECHECK DONE")

root_domains = {}
for e in domain_list:
    try:
        rootdomain = p.privatesuffix(e)
        if rootdomain != e and rootdomain in domain_list:
            if rootdomain not in root_domains:
                root_domains[rootdomain] = []
            if e not in root_domains[rootdomain]:
                root_domains[rootdomain].append(e)
    except Exception as err:
        print(e, err)

print("GETTING COMMIT")
last_commit = get_last_commit()
print("GOT COMMIT, STARTING")
for e in domain_list:
    #print(e, e in entry_data)
    if (e not in entry_data or type(entry_data[e]) == str) and e != "last_updated":
        entry_is_alive = is_alive(e, True)
        entry_has_http_80 = False
        dead_since = ""
        if entry_is_alive != True:
            dead_since = current_date
        else:
            try:
                requests.head(f"http://{e}")
                entry_has_http_80 = True
            except:
                pass
        tls_info = {}
        try:
            tls_info = get_tls_info(e)
        except:
            pass
        entry_ips = get_ips(e)
        ip_whois_data = {}
        try:
            for ip in entry_ips:
                try:
                    ip_whois_data[ip] = get_whois_data_raw(ip, "whois.arin.net")
                except:
                    pass
        except:
            pass
        entry_data[e] = {
            "first_seen": current_date,
            "last_seen": current_date,
            "removed": False,
            "removed_date": "",
            "last_checked": current_date,
            "check_counter": 30,
            "check_status": entry_is_alive,
            "alive_on_creation": entry_is_alive,
            "times_checked": 1,
            "ever_rechecked": False,
            "readded": False,
            "alive_on_removal": None,
            "origin_add": "",
            "readd": "",
            "is_valid": is_valid(e),
            "ips": entry_ips,
            "dead_since": dead_since,
            "whois": get_whois(e, recurse=True),
            "had_www_on_creation": is_alive(f"www.{e}", False),
            "had_www_on_check": None,
            "tls_info": tls_info,
            "last_commit": last_commit,
            "ip_whois": ip_whois_data,
            "has_http_80": entry_has_http_80,
            "times_died": 0,
            "check_history": {
                current_date: entry_is_alive
            },
            "MX": get_dns_record(e, 'MX'),
            "TXT": get_dns_record(e, "TXT"),
            "CNAME": get_dns_record(e, "CNAME"),
            "CAA": get_dns_record(e, "CAA"),
            "SOA": get_dns_record(e, "SOA"),
            "NS": get_dns_record(e, "NS"),
            "LOC": get_dns_record(e, "LOC"), # unlikely
        }
        entry_data[e]['subdomain_status'] = {}
        if e in root_domains:
            for subdomain in root_domains[e]:
                try:
                    entry_data[e]['subdomain_status'][subdomain] = entry_data[subdomain]['check_status']
                except:
                    pass
    else:
        if "tls_info" in entry_data[e] and len(entry_data[e]["tls_info"]) == 0:
            try:
                entry_data[e]['tls_info'] = get_tls_info(e)
            except:
                del entry_data[e]["tls_info"]
        if "times_checked" not in entry_data[e]:
            entry_data[e]["times_checked"] = 0
        if "check_status" not in entry_data[e]:
            entry_data[e]['check_counter'] = 40
        elif "ips" not in entry_data[e]:
            entry_data[e]["ips"] = get_ips(e)
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
            entry_data[e]["check_counter"] = 0
        if "last_checked" not in entry_data[e]:
            entry_data[e]["last_checked"] = "Unknown"
        if "had_www_on_check" not in entry_data[e]:
            print(f"{e} doesn't have had_www_on_check")
            entry_data[e]["check_counter"] = 40 # force recheck
        if "times_died" not in entry_data[e]:
            entry_data[e]['times_died'] = 0
        entry_data[e]["check_counter"] += 1
        if e.endswith(".squarespace.com") or e.endswith(".itch.io") or e.endswith(".azurefd.net") or e.endswith(".appspot.com"): # temp measure to force recheck of these domains now that death detection has been added
            entry_data[e]["check_counter"] += 10
        last_check_status = entry_data[e]["check_status"]
        entry_data[e]['subdomain_status'] = {}
        if e in root_domains:
            for subdomain in root_domains[e]:
                try:
                    entry_data[e]['subdomain_status'][subdomain] = entry_data[subdomain]['check_status']
                except:
                    pass

        if entry_data[e]["check_counter"] > 35:
            print(f"Checking {e}...", "previous status", entry_data[e]["check_status"], "last check", entry_data[e]["last_checked"])
            domain_is_alive = is_alive(e, True)
            if "check_history" not in entry_data[e]:
                entry_data[e]['check_history'] = {}
            entry_data[e]['check_history'][current_date] = entry_data[e]["check_status"]
            entry_data[e]["check_status"] = domain_is_alive
            entry_data[e]["last_checked"] = current_date
            entry_data[e]["check_counter"] = 0
            entry_data[e]["ever_rechecked"] = True
            entry_data[e]["times_checked"] += 1
            entry_data[e]['had_www_on_check'] = is_alive(f"www.{e}", False)
            if domain_is_alive != True and last_check_status:
                entry_data[e]["dead_since"] = current_date
                entry_data[e]['times_died'] += 1
            if "MX" not in entry_data[e]:
                entry_data[e]['MX'] = get_dns_record(e, 'MX')
            if "CNAME" not in entry_data[e]:
                entry_data[e]['CNAME'] = get_dns_record(e, 'CNAME')
            if "TXT" not in entry_data[e]:
                entry_data[e]['TXT'] = get_dns_record(e, 'TXT')
            if "NS" not in entry_data[e]:
                entry_data[e]['NS'] = get_dns_record(e, 'NS')
        if entry_data[e]["check_status"] == False and last_check_status == False:
            dead_domains.append(e)
print("Done with part 1")
for e in entry_data:
    if e not in domain_list and e != "last_updated" and e != "":
        try:
            if "dead_on_removal" in entry_data[e]:
                entry_data[e]['alive_on_removal'] = entry_data[e]["dead_on_removal"]
            if entry_data[e]["removed"] == False:
                entry_data[e]["removed"] = True
                entry_data[e]["removed_date"] = current_date
                entry_data[e]["alive_on_removal"] = is_alive(e, False)
        except Exception as err:
            print(err, e, entry_data[e])
print("Done with part 2")
entry_data_file = open("entry_data.json", 'w', encoding="UTF-8")
entry_data_file.write(json.dumps(entry_data))
entry_data_file.close()

dead_stuff = open("dead.mwbcheck.txt", 'w', encoding='UTF-8')
dead_stuff.write("\n".join(dead_domains))
dead_stuff.close()