import dns, dns.resolver
import os, sys, json, datetime, socket, random, publicsuffixlist, ssl, requests, time

TLD_WHOIS_OVERRIDE = {
    "PANASONIC": "whois.nic.gmo",
}

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

def get_ips(domain):
    global already_resolved
    if domain in already_resolved:
        return already_resolved[domain]
    if domain in dead_domains:
        return []
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

print("GETTING COMMIT")
last_commit = get_last_commit()

print("GOT COMMIT, STARTING")
for e in domain_list:
    #print(e, e in entry_data)
    if (e not in entry_data or type(entry_data[e]) == str) and e != "last_updated":
        entry_is_alive = is_alive(e, True)
        dead_since = ""
        if entry_is_alive != True:
            dead_since = current_date
        tls_info = {}
        if port_open(e, 443):
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
            "check_counter": random.randint(0, 10),
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
            "whois": get_whois(e, recurse=False),
            "ports_open": {
                23: port_open(e, 23), # https://threatfox.abuse.ch/ioc/1252534/
                80: port_open(e, 80),
                81: port_open(e, 81), # https://threatfox.abuse.ch/ioc/1252558/
                100: port_open(e, 100), # https://threatfox.abuse.ch/ioc/1252471/
                443: port_open(e, 443),
                666: port_open(e, 666), # has been used (https://www.grc.com/port_666.htm, https://www.aircrack-ng.org/doku.php?id=airserv-ng)
                671: port_open(e, 671), # https://threatfox.abuse.ch/ioc/1252557/
                1337: port_open(e, 1337), # leet h@ck0rz
                2222: port_open(e, 2222), # https://threatfox.abuse.ch/ioc/1252501/
                3333: port_open(e, 3333), # https://threatfox.abuse.ch/ioc/1252536/
                4880: port_open(e, 4880), # https://threatfox.abuse.ch/ioc/1252530/
                5000: port_open(e, 5000), # default port for python flask
                6666: port_open(e, 6666), # https://threatfox.abuse.ch/ioc/1252550/
                7443: port_open(e, 7443), # https://threatfox.abuse.ch/ioc/1252812/
                8000: port_open(e, 8000),
                8080: port_open(e, 8080),
                8081: port_open(e, 8081), # https://threatfox.abuse.ch/ioc/1252815/
                8443: port_open(e, 8443), # https://threatfox.abuse.ch/ioc/1252551/
                8888: port_open(e, 8888), # https://threatfox.abuse.ch/ioc/1252820/
                9090: port_open(e, 9090), # default port for updog
                50000: port_open(e, 50000), # https://threatfox.abuse.ch/ioc/1252509/
            },
            "had_www_on_creation": is_alive(f"www.{e}", False),
            "had_www_on_check": None,
            "tls_info": tls_info,
            "last_commit": last_commit,
            "ip_whois": ip_whois_data
        }
