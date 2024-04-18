import dns, dns.resolver
import os, sys, json, datetime, socket, random, publicsuffixlist, ssl, requests, time

p = publicsuffixlist.PublicSuffixList(only_icann=True)
resolver = dns.resolver.Resolver()
resolver.nameservers = ["https://unfiltered.adguard-dns.com/dns-query","94.140.14.140", "8.8.8.8","1.1.1.1"]
