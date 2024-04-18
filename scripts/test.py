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
