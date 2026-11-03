import hashlib,re
from datetime import datetime,timezone
from urllib.parse import urlparse
import feedparser
from src.common.config import settings,read_json,write_json
def clean(s): return re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",s or "")).strip()
def score(title,summary):
 text=(title+" "+summary).lower()
 terms={"curiosity":["why","how","secret","hidden","strange","surprising","discovered"],
 "visual_potential":["photo","video","space","ocean","island","architecture","robot","animal","design"],
 "broad_appeal":["people","life","world","food","travel","money","home","science"],
 "shareability":["amazing","useful","beautiful","unusual","incredible","free","tips"],
 "brand_fit":["product","app","tool","device","design","travel","website"]}
 vals={k:min(100,20+15*sum(w in text for w in ws)) for k,ws in terms.items()}
 vals["timeliness"]=65
 weights=settings()["scoring_weights"]
 return round(sum(vals[k]*weights[k] for k in weights)/sum(weights.values()),1)
def discover():
 cfg=settings()["discovery"]; state=read_json("topics.json",{"topics":[]})
 seen={x.get("id") for x in state["topics"]}; fresh=[]
 for url in cfg["feeds"]:
  try:
   feed=feedparser.parse(url,request_headers={"User-Agent":"CurioDaily/0.1"})
   for e in feed.entries[:25]:
    title=clean(e.get("title")); link=e.get("link",""); summary=clean(e.get("summary") or e.get("description"))
    if not title or not link: continue
    uid=hashlib.sha1((title.lower()+link).encode()).hexdigest()[:16]
    if uid in seen: continue
    fresh.append({"id":uid,"title":title,"summary":summary[:1200],"url":link,
      "source":urlparse(link).netloc,"published":e.get("published",""),
      "discovered_at":datetime.now(timezone.utc).isoformat(),"score":score(title,summary),"status":"new"})
  except Exception as ex: print("Feed error",url,ex)
 fresh.sort(key=lambda x:x["score"],reverse=True)
 state["topics"]=(state["topics"]+fresh[:cfg["max_topics_per_run"]])[-1000:]
 write_json("topics.json",state); print("New topics:",min(len(fresh),cfg["max_topics_per_run"]))
 return fresh
if __name__=="__main__": discover()
