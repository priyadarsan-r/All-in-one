import os
from src.common.config import ROOT,env_bool,read_json,write_json
from src.publishing.youtube import upload
from src.publishing.meta import instagram,facebook
def publish(platform,limit=3):
 if not env_bool("ENABLE_PUBLISHING",False):print("Publishing disabled; set ENABLE_PUBLISHING=true after validation.");return []
 dry=env_bool("DRY_RUN",True);q=read_json("publishing_queue.json",{"items":[]});scripts=read_json("scripts.json",{"scripts":[]})["scripts"];pub=read_json("published.json",{"items":[]})
 done={(x.get("script_id"),x.get("platform")) for x in pub["items"]};results=[]
 for item in q["items"]:
  sid=item["script_id"]
  if len(results)>=limit:break
  if (sid,platform) in done or item["status"] not in ("approved","review_required"):continue
  s=next((x for x in scripts if x["id"]==sid),None);video=ROOT/item["video"]
  if not s or not video.exists():continue
  if platform=="youtube":res=upload(str(video),s["hook"],s["caption"],s.get("hashtags"),dry)
  else:
   url=os.getenv("PUBLIC_VIDEO_URL")
   if not url:raise RuntimeError("Set PUBLIC_VIDEO_URL to public HTTPS MP4")
   res=instagram(url,s["caption"],dry) if platform=="instagram" else facebook(url,s["caption"],s["hook"],dry)
  row={"script_id":sid,"platform":platform,"result":res,"dry_run":dry};pub["items"].append(row);results.append(row)
 write_json("published.json",pub);return results
