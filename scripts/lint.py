"""Verify the syntax of my antimalware list and verify there are no legit domains in it"""
# note: this does include allowlisting trackers, as this is just for my antimalware list. This will NOT prevent other lists from blocking these domains

# domains which are good & should never be blocked in this list (includes trackers and ads)
gooddomains = ["google.com","www.google.com","duckduckgo.com","www.duckduckgo.com","safeweb.norton.com","mywot.com","www-amazon-com.customer.fastly.net","adguardteam.github.io","iam-py-test.github.io","example.com","r3.o.lencr.org","mozilla.org","www.mozilla.org","www.mozorg.moz.works","github.community","github.githubassets.com","somepythonthings.tk","letsencrypt.org","easylist.to","ublockorigin.com","microsoft.com","amazon.com","mcafee.com","norton.com","msedge.api.cdp.microsoft.com","config.edge.skype.com","msedge.f.tlu.dl.delivery.mp.microsoft.com","msedge.f.dl.delivery.mp.microsoft.com","msedge.b.tlu.dl.delivery.mp.microsoft.com","msedge.b.dl.delivery.mp.microsoft.com","msedge.sf.tlu.dl.delivery.mp.microsoft.com","msedge.sf.dl.delivery.mp.microsoft.com","msedge.sb.tlu.dl.delivery.mp.microsoft.com","msedge.sb.dl.delivery.mp.microsoft.com","msedgeextensions.f.tlu.dl.delivery.mp.microsoft.com","msedgeextensions.f.dl.delivery.mp.microsoft.com","msedgeextensions.b.tlu.dl.delivery.mp.microsoft.com","msedgeextensions.b.dl.delivery.mp.microsoft.com","msedgeextensions.sf.tlu.dl.delivery.mp.microsoft.com","msedgeextensions.sf.dl.delivery.mp.microsoft.com","msedgeextensions.sb.tlu.dl.delivery.mp.microsoft.com","msedgeextensions.sb.dl.delivery.mp.microsoft.com","do.dsp.mp.microsoft.com","edge-enterprise.activity.windows.com","edge.activity.windows.com","api.aadrm.com","api.aadrm.de","api.aadrm.cn","notify.windows.com","wns.windows.com","notify.live.net","login.microsoftonline.com","login.live.com","edge.microsoft.com","goto.target.com","goto-target-com.customtraffic.impactradius.com","admin.microsoft.com","iyec.omni7.jp","hackerone-us-west-2-production-attachments.s3.us-west-2.amazonaws.com","hackerone.com","tryhackme.com","static-labs.tryhackme.cloud","tryhackme.cloud","cdc.gov","google.org","dns.msftncsi.com","131.107.255.255","content-system.gog.com","gamesdb.gog.com","notifications.gog.com","marketing-sections.gog.com","api.gogalaxy.com","auth.gog.com","users.gog.com","cdn-akamai-ec.gog-services.com","cdn.gog.com","presence.gog.com","gameplay.gog.com","insights-collector.gog.com","external-accounts.gog.com","aus5.mozilla.org","forums.malwarebytes.com","www.bleepingcomputer.com","bleepingcomputer.com","cdn.mwbsys.com","cloud.malwarebytes.com","download.toolslib.net","keystone-akamai.mwbsys.com","keystone.mwbsys.com","malwarebytes.com","mb-cosmos.com","mbamupdates.com","mwbsys.com","sirius.mwbsys.com",'guard.io','pgl.yoyo.org',"koyu.space","joinmastodon.org","wiki.koyu.space","docs.joinmastodon.org","blog.joinmastodon.org","tails.boum.org","app.slack.com","l-dc-msedge.net","pipelines.actions.githubusercontent.com","d1f8f9xcsvx3ha.cloudfront.net","activate.adobe.com","practivate.adobe.com","adobe.com","www.adobe.com","lmlicenses.wip4.adobe.com","lm.licenses.adobe.com","na1r.services.adobe.com","hlrcv.stage.adobe.com","media-amazon.com","ssl-images-amazon.com","ark.mwbsys.com","blitz.mb-cosmos.com","data-cdn.mbamupdates.com","data-cdn-static.mbamupdates.com","detect-remediate.cloud.malwarebytes.com","hubble.mb-cosmos.com","nebula-agent-installers-mb-prod.s3.amazonaws.com","nebula-diagnostics-mb-prod.s3.amazonaws.com","nebula-helix-syslog-mb-prod.s3.amazonaws.com","socket.cloud.malwarebytes.com","storage.gra.cloud.ovh.net","telemetry.malwarebytes.com","downloads.malwarebytes.com","links.malwarebytes.com","meps.mwbsys.com","ars.cloud.malwarebytes.com","api.malwarebytes.com","oneview.malwarebytes.com"]
# domains which are used for hosting or contain User Generated Content, and should only have subdomains/specific urls listed
hosting = ["duckdns.org","appspot.com","blogspot.com","raw.githubusercontent.com","githubusercontent.com","github.com","www.gitlab.com","gitlab.com","github.io","storage.cloud.google.com","mediafire.com","archive.org",'web.archive.org',"fastly.net","addons.mozilla.org","sites.google.com","ips-cic-filestore.s3.amazonaws.com","s3.amazonaws.com","amazonaws.com","pp.ua","avatars.githubusercontent.com","cdn.discordapp.com","media.discordapp.net"]
# social media and email
social = ["reddit.com","twitter.com","slack.com","meet.google.com","mail.google.com","gmail.com","chat.google.com","discord.gift","discord.com","protonmail.com","outlook.com","www.facebook.com","facebook.com","old.reddit.com","slack.com","youtube.com","www.youtube.com","youtubekids.com","discordapp.com"]
# url shorteners which should only have specific urls blocked
urlshorteners = ["bit.ly","x.co","tinyurl.com","t.co","t.ly","urldefense.proofpoint.com","clickagy.com","www.clickagy.com","shorte.st","tinyurl.hu"]
# websites for sharing malware, phishing, and scams with the security community
malshare = ["virustotal.com","www.virustotal.com","support.virustotal.com","api.virustotal.com","vxvault.net","abuse.ch","urlhaus.abuse.ch","threatfox.abuse.ch","bazaar.abuse.ch","phishtank.com","openphish.com","www.hybrid-analysis.com","hybrid-analysis.com","malshare.com","mb-api.abuse.ch","threatfox-api.abuse.ch","otx.alienvault.com","alienvault.com","malpedia.caad.fkie.fraunhofer.de","www.threatcrowd.org","threatcrowd.org","api.tria.ge","tria.ge"]
# nsfw
nsfw = ["fullxh.com","megaxh.com","unlockxh4.com","xhamster46.com","xhday1.com","xhday.com","xhplanet1.com","xhtab2.com","xhwebsite.com","xhwide1.com","hamsterix.com"]
# invalid syntax
invalidsyntax = ["$$","$docment","$alll","^all","$docs","$scripted","$alls","$documentall","$allall","$all$all","$all.","$docments","$doc$doc","|*$","$documentP","$window","$document$document"]

legitdomains = gooddomains + hosting + social + urlshorteners + malshare + nsfw

# the main text
lines = open("antimalware.txt","r",encoding="UTF-8").read().split("\n")
# a list of invalid lines/good domains found
invalidlines = []
# log
log = ""
totalscanned = 0

for line in lines:
    if line.startswith("!"):
        continue
    try:
      domain = line.split("^$")[0][2:]
      if domain in legitdomains:
        invalidlines.append(line)
        print("False positive detected: WARNING")
      for syntax in invalidsyntax:
        if syntax in line:
          invalidlines.append(line)
      totalscanned += 1
    except:
      continue

with open("invalidlines.md","w") as f:
  f.write("## Lines detected by Lint (out of {})".format(totalscanned))
  for line in invalidlines:
    f.write("\n{}<br>".format(line))
  f.close()
