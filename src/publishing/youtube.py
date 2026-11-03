import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
def upload(video,title,description,tags=None,dry_run=True):
 if dry_run:print("[DRY RUN] YouTube",video);return {"id":"DRY_RUN"}
 keys=["YOUTUBE_CLIENT_ID","YOUTUBE_CLIENT_SECRET","YOUTUBE_REFRESH_TOKEN"]
 if not all(os.getenv(k) for k in keys):raise RuntimeError("YouTube OAuth secrets missing")
 c=Credentials(None,refresh_token=os.environ[keys[2]],token_uri="https://oauth2.googleapis.com/token",client_id=os.environ[keys[0]],client_secret=os.environ[keys[1]],scopes=["https://www.googleapis.com/auth/youtube.upload"])
 yt=build("youtube","v3",credentials=c);body={"snippet":{"title":title[:100],"description":description,"tags":tags or [],"categoryId":"22"},"status":{"privacyStatus":"public","selfDeclaredMadeForKids":False}}
 req=yt.videos().insert(part="snippet,status",body=body,media_body=MediaFileUpload(video,chunksize=-1,resumable=True));status,response=None,None
 while response is None:status,response=req.next_chunk()
 return response
