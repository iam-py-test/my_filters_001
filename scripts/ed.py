print(f"{__file__} STARTED")
print("IMPORTING dns.resolver")
dnsresolver = __import__('dns.resolver')
print(dnsresolver)
print("IMPORTING NORMAL LIBS")
import os, sys, json, datetime, socket, random, publicsuffixlist, ssl, requests, time, hashlib, random
from tranco import Tranco
print("IMPORTS DONE")

TLD_WHOIS_OVERRIDE = {
    "panasonic": "whois.nic.gmo",
}

dead_domains = []
print("GETTING PSL")
p = publicsuffixlist.PublicSuffixList(only_icann=True)
print("GOT PSL, SETTING UP resolver")
dresolver = dnsresolver.resolver.Resolver()
print("CREATED dresolver")
#dresolver.nameservers = ["https://unfiltered.adguard-dns.com/dns-query","94.140.14.140", "8.8.8.8","1.1.1.1"]
print("SETUP resolver")
try:
    trancoobject = Tranco(cache=False)
    tranco_list = trancoobject.list()
    print("LOADED tranco")
except Exception as err:
    print("Failed to load tranco",err)
    try:
        yesterday_dateobj = datetime.datetime.now().replace(day=datetime.datetime.now().day-1)
        trancoobject = Tranco(cache=False,date=f"{yesterday_dateobj.year}-{yesterday_dateobj.month}-{yesterday_dateobj.day}")
        tranco_list = trancoobject.list()
        print("LOADED tranco from yesterday!")
    except Exception as err:
        print("Failed to load tranco with yesterday's date",err,datetime.datetime.now().day)
already_resolved = {}
known_whois = {}
parked_domains = []

nrd_list = []
try:
    nrd_file = requests.get("https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/domains/nrd7.txt")
    nrd_list = nrd_file.text.split("\n")
except:
    pass

try:
    parked_ips = open("parking.ips").read().split('\n')
except:
    parked_ips = []

try:
    reddomains = open("reddomains.txt").read().split('\n')
except:
    reddomains = []

verbosity = 4

def get_whois_data_raw(domain: str, server: str) -> str:
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
def get_whois(domain: str, server = None, done_whois_servers_arg = [], recurse=False, sub=False) -> str:
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

def is_alive(domain: str, in_list=True) -> bool:
    global dead_domains
    global already_resolved
    global parked_domains
    if domain in already_resolved:
        return True
    if domain.endswith(".onion"): # can't test onions yet
        return True
    try:
        if tranco_list.rank(domain) != -1:
            return True
    except:
        pass
    try:
        res_ips = list(dresolver.resolve(domain))
        found_ips = []
        for ip in res_ips:
            found_ips.append(ip.address)
            if ip.address in parked_ips:
                print(f"{domain} is parked!", len(parked_domains))
                parked_domains.append(domain)
                #return False
        already_resolved[domain] = found_ips
    except Exception:
        try:
            dresolver.resolve("www." + domain)
            return True
        except Exception:
            return False
    
    if domain.endswith(".github.io"):
        try:
            username = domain.replace(".github.io", "")
            userreq = requests.get(f"https://api.github.com/users/{username}")
            if userreq.status_code == 404:
                return False
        except:
            pass
    try:
        plain_http_req = requests.get(f"http://{domain}")
    except:
        plain_http_req = None
    if domain.endswith(".itch.io") or domain.endswith(".appspot.com") or domain.endswith(".squarespace.com") or domain.endswith(".web.app") or domain.endswith(".weeblysite.com") or domain.endswith(".square.site") or domain.endswith(".webflow.io") or domain.endswith(".firebaseio.com") or domain.endswith(".vercel.app") or domain.endswith(".studio.site"):
        try:
            if plain_http_req.status_code == 404:
                return False
        except:
            pass
    if domain.endswith(".page.link"):
        try:
            if plain_http_req.status_code == 400:
                return False
        except:
            pass
    if domain.endswith(".azurefd.net"):
        try:
            if plain_http_req.status_code == 404 and "azurefrontdoorpages.azureedge.net/pages/PageNotFound_files/favicon.ico" in plain_http_req.text:
                return False
        except:
            pass
    if domain.endswith(".glitch.me"):
        try:
            if (plain_http_req.status_code == 403 and "<title>Oops! This project isn't running.</title>" in plain_http_req.text) or plain_http_req.status_code == 401:
                return False
        except:
            pass
    if domain.endswith(".builderall.net"):
        try:
            if plain_http_req.text == f"Website not found {domain}":
                return False
        except:
            pass
    try:
        if plain_http_req.url.endswith("/cgi-sys/suspendedpage.cgi") or plain_http_req.url.startswith('http://suspended-website.com/') or plain_http_req.url.startswith('https://suspended-website.com/'):
            print('suspended:',plain_http_req.url,domain)
            return False
    except:
        pass
    try:
        pagereq = requests.get(f"https://{domain}")
        if pagereq.url.endswith("/cgi-sys/suspendedpage.cgi"):
            print(pagereq.url)
            return False
    except:
        pass
    try:
        pagereq = requests.get(f"http://{domain}:8080")
        if pagereq.url.endswith("/cgi-sys/suspendedpage.cgi"):
            print(pagereq.url)
            return False
    except:
        pass
    try:
        pagereq = requests.get(f"http://{domain}/lander")
        if "https://www.godaddy.com/forsale/" in pagereq.text or pagereq.url.startswith("https://www.godaddy.com/forsale/"):
            parked_domains.append(domain)
            print('parked url redirect detected', pagereq.url)
            return False
    except:
        pass
    try:
        pagereq = requests.get(f"https://{domain}/lander")
        if "https://www.godaddy.com/forsale/" in pagereq.text or pagereq.url.startswith("https://www.godaddy.com/forsale/"):
            parked_domains.append(domain)
            print('parked url redirect detected', pagereq.url)
            return False
    except:
        pass
    
    return True


def get_ips(domain: str) -> list:
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

def is_valid(domain: str) -> bool:
    try:
        return p.publicsuffix(domain, accept_unknown=False) != None
    except:
        return False

def get_tls_info(hostname: str):
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

def get_last_commit() -> str:
    try:
        return requests.get("https://api.github.com/repos/iam-py-test/my_filters_001/commits").json()[0]['html_url']
    except Exception as err:
        print(err)
        return None

def get_dns_record(domain: str, record: str) -> list:
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
        entry_data[random_recheck]['check_counter'] = 99
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
            "parked": e in parked_domains,
            "red_on_add": e in reddomains,
            "is_nrd": e in nrd_list
        }
        try:
            tranco_rank = tranco_list.rank(e)
            entry_data[e]['tranco_rank'] = tranco_rank
        except:
            pass
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
        if "tranco_rank" in entry_data[e] and entry_data[e]['tranco_rank'] == None:
            try:
                print(f"{e} failed to get a tranco rank when added. Adding rank...")
                entry_data[e]["check_counter"] += 1
                tranco_rank = tranco_list.rank(e)
                entry_data[e]['tranco_rank'] = tranco_rank
            except:
                print("Failed")
                entry_data[e]["check_counter"] += 5
        for ip in entry_data[e]["ips"]:
            if ip in parked_ips:
                print(f"{e} is - and has always been - parked. Forcing recheck")
                entry_data[e]['parked'] = True
        entry_data[e]["last_seen"] = current_date
        entry_data[e]["removed"] = False
        entry_data[e]["removed_date"] = ""
        entry_data[e]["is_valid"] = is_valid(e)
        if "check_counter" not in entry_data[e]:
            entry_data[e]["check_counter"] = 40
        if "last_checked" not in entry_data[e]:
            entry_data[e]["last_checked"] = "Unknown"
        if "had_www_on_check" not in entry_data[e]:
            print(f"{e} doesn't have had_www_on_check")
            entry_data[e]["check_counter"] = 40 # force recheck
        if "times_died" not in entry_data[e]:
            entry_data[e]['times_died'] = 0
        #entry_data[e]["check_counter"] += 1
        last_check_status = entry_data[e]["check_status"]
        entry_data[e]['subdomain_status'] = {}
        if e in root_domains:
            for subdomain in root_domains[e]:
                try:
                    entry_data[e]['subdomain_status'][subdomain] = entry_data[subdomain]['check_status']
                except:
                    pass
        if "had_www_on_check" in entry_data[e] and entry_data[e]["had_www_on_check"] == True and entry_data[e]["check_status"] == False:
            print(e, entry_data[e]["check_counter"], entry_data[e]["had_www_on_check"])
        if entry_data[e]["check_counter"] > 80 and random.choice([True,False,False,False]) == True: # will revert back to 50 soon
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
            entry_data[e]["check_ips"] = get_ips(e)
            entry_data[e]['had_www_on_check'] = is_alive(f"www.{e}", False)
            if entry_data[e]['had_www_on_check'] == None:
                print(entry_data[e]['had_www_on_check'], e)
            entry_data[e]['parked'] = e in parked_domains
            if domain_is_alive != True and last_check_status:
                entry_data[e]["dead_since"] = current_date
                entry_data[e]['times_died'] += 1
                try:
                    for sub in entry_data[e]["subdomain_status"]:
                        entry_data[sub]['check_counter'] += 2
                        print(f"Increased check count on {sub} as root domain {e} is dead")
                except Exception as err:
                    print(e, err, "subdomain_status" in entry_data[e])
            if "MX" not in entry_data[e]:
                entry_data[e]['MX'] = get_dns_record(e, 'MX')
            if "CNAME" not in entry_data[e]:
                entry_data[e]['CNAME'] = get_dns_record(e, 'CNAME')
            if "TXT" not in entry_data[e]:
                entry_data[e]['TXT'] = get_dns_record(e, 'TXT')
            if "NS" not in entry_data[e]:
                entry_data[e]['NS'] = get_dns_record(e, 'NS')
            if "tranco_rank" not in entry_data[e]:
                try:
                    tranco_rank = tranco_list.rank(e)
                    entry_data[e]['tranco_rank'] = tranco_rank
                    entry_data[e]['tranco_rank_added_on'] = current_date
                except:
                    pass
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
                entry_data[e]['removed_commit'] = last_commit
                entry_data[e]['red_on_remove'] = e in reddomains
                entry_data[e]['removed_ips'] = get_ips(e)
                if "tranco_rank" not in entry_data[e]:
                    try:
                        tranco_rank = tranco_list.rank(e)
                        entry_data[e]['tranco_rank'] = tranco_rank
                        entry_data[e]['tranco_rank_added_on'] = current_date
                    except:
                        pass
        except Exception as err:
            print(err, e, entry_data[e])
print("Done with part 2")
entry_data_file = open("entry_data.json", 'w', encoding="UTF-8")
entry_data_file.write(json.dumps(entry_data))
entry_data_file.close()

dead_stuff = open("dead.mwbcheck.txt", 'w', encoding='UTF-8')
dead_stuff.write("\n".join(dead_domains))
dead_stuff.close()