import os,time,requests
def graph(path,method="GET",data=None):
 url=f"https://graph.facebook.com/{os.getenv('META_GRAPH_VERSION','v23.0')}/{path.lstrip('/')}"
 payload=dict(data or {});payload["access_token"]=os.getenv("META_ACCESS_TOKEN","")
 r=requests.request(method,url,data=payload,timeout=60);r.raise_for_status();return r.json()
def instagram(url,caption,dry=True):
 if dry:print("[DRY RUN] Instagram",url);return {"id":"DRY_RUN"}
 uid=os.getenv("META_IG_USER_ID")
 if not uid or not os.getenv("META_ACCESS_TOKEN"):raise RuntimeError("Meta credentials missing")
 c=graph(f"{uid}/media","POST",{"media_type":"REELS","video_url":url,"caption":caption,"share_to_feed":"true"});cid=c["id"]
 for _ in range(30):
  st=graph(cid,data={"fields":"status_code"})
  if st.get("status_code")=="FINISHED":break
  if st.get("status_code")=="ERROR":raise RuntimeError(str(st))
  time.sleep(10)
 else:raise TimeoutError("Meta processing timed out")
 return graph(f"{uid}/media_publish","POST",{"creation_id":cid})
def facebook(url,caption,title,dry=True):
 if dry:print("[DRY RUN] Facebook Reel",url);return {"id":"DRY_RUN"}
 page=os.getenv("META_PAGE_ID")
 if not page:raise RuntimeError("META_PAGE_ID missing")
 start=graph(f"{page}/video_reels","POST",{"upload_phase":"start"});vid=start["video_id"]
 data=requests.get(url,timeout=90);data.raise_for_status()
 up=requests.post(start["upload_url"],headers={"Authorization":"OAuth "+os.environ["META_ACCESS_TOKEN"],"file_size":str(len(data.content)),"Content-Type":"application/octet-stream"},data=data.content,timeout=180);up.raise_for_status()
 done=graph(f"{page}/video_reels","POST",{"upload_phase":"finish","video_id":vid,"video_state":"PUBLISHED","description":caption,"title":title})
 return {"id":vid,"result":done}
