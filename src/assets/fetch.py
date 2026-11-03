import os,requests
from pathlib import Path
from src.common.config import ROOT
WORK=ROOT/"work/assets"; WORK.mkdir(parents=True,exist_ok=True)
def pexels(query):
 key=os.getenv("PEXELS_API_KEY")
 if not key:return None
 r=requests.get("https://api.pexels.com/v1/search",headers={"Authorization":key},params={"query":query,"per_page":5,"orientation":"portrait"},timeout=25);r.raise_for_status()
 photos=r.json().get("photos",[])
 if not photos:return None
 p=photos[0]; url=p["src"].get("large2x") or p["src"]["large"]
 b=requests.get(url,timeout=30);b.raise_for_status(); path=WORK/f"{p['id']}.jpg";path.write_bytes(b.content)
 return {"path":str(path),"provider":"Pexels","url":p["url"],"creator":p.get("photographer"),"license":"Pexels License; verify current terms"}
def commons(query):
 api="https://commons.wikimedia.org/w/api.php"
 r=requests.get(api,params={"action":"query","generator":"search","gsrsearch":query+" filetype:bitmap","gsrnamespace":6,"gsrlimit":6,"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":1200,"format":"json"},headers={"User-Agent":"CurioDaily/0.1"},timeout=25);r.raise_for_status()
 for p in r.json().get("query",{}).get("pages",{}).values():
  i=(p.get("imageinfo") or [{}])[0]; url=i.get("thumburl") or i.get("url")
  if not url:continue
  b=requests.get(url,timeout=30);b.raise_for_status();path=WORK/f"commons-{p['pageid']}.jpg";path.write_bytes(b.content)
  meta=i.get("extmetadata",{})
  val=lambda k:(meta.get(k) or {}).get("value","")
  return {"path":str(path),"provider":"Wikimedia Commons","url":i.get("descriptionurl",url),"creator":val("Artist"),"license":val("LicenseShortName")}
 return None
def get_visual(q): return pexels(q) or commons(q)
