import requests
def checkdomain(domain):
  req = requests.get("http://{}".format(domain))
  parkedpattern = ["www.afternic.com/forsale"]
  for pattern in parkedpattern:
    if pattern in req.url:
      return True
  return False
