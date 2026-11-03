import json,shutil,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from src.common.config import ROOT,read_json,write_json
from src.assets.fetch import get_visual
from src.audio.tts import narrate
OUT=ROOT/"output";WORK=ROOT/"work"
def cmd(args):subprocess.run(args,check=True)
def make_card(text,path,bg=None):
 im=Image.new("RGB",(1080,1920),(20,25,38))
 if bg and Path(bg).exists():
  src=Image.open(bg).convert("RGB"); ratio=max(1080/src.width,1920/src.height);src=src.resize((int(src.width*ratio),int(src.height*ratio)))
  x=(src.width-1080)//2;y=(src.height-1920)//2;im.paste(src.crop((x,y,x+1080,y+1920)))
 im=im.convert("RGBA");im.alpha_composite(Image.new("RGBA",im.size,(0,0,0,115)))
 d=ImageDraw.Draw(im)
 fp="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
 f=ImageFont.truetype(fp,65) if Path(fp).exists() else ImageFont.load_default()
 words=text.split();lines=[];line=""
 for w in words:
  trial=(line+" "+w).strip()
  if d.textbbox((0,0),trial,font=f)[2]>920 and line:lines.append(line);line=w
  else:line=trial
 if line:lines.append(line)
 y=750-len(lines)*45
 for ln in lines:
  box=d.textbbox((0,0),ln,font=f);d.text(((1080-(box[2]-box[0]))//2,y),ln,font=f,fill="white");y+=90
 d.text((55,1800),"CURIO DAILY  •  DISCOVER MORE",font=ImageFont.load_default(),fill="white")
 im.convert("RGB").save(path,quality=92)
def produce_one(s):
 if not shutil.which("ffmpeg"):raise RuntimeError("FFmpeg is required")
 OUT.mkdir(exist_ok=True);WORK.mkdir(exist_ok=True);clips=[];credits=[]
 scenes=s.get("scenes") or [{"text":s["hook"],"visual_query":s["hook"],"duration":10}]
 for i,scene in enumerate(scenes):
  v=get_visual(scene.get("visual_query") or s["hook"]);bg=v["path"] if v else None
  if v:credits.append({k:x for k,x in v.items() if k!="path"})
  card=WORK/f"{s['id']}-{i}.jpg";make_card(scene.get("text") or s["hook"],card,bg)
  clip=WORK/f"{s['id']}-{i}.mp4";duration=max(4,int(scene.get("duration",8)))
  cmd(["ffmpeg","-y","-loop","1","-i",str(card),"-t",str(duration),"-vf","scale=1080:1920,fps=30,format=yuv420p","-an","-c:v","libx264","-preset","ultrafast","-crf","24",str(clip)])
  clips.append(clip)
 concat=WORK/f"{s['id']}.txt";concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips))
 silent=WORK/f"{s['id']}-silent.mp4";cmd(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(silent)])
 audio=WORK/f"{s['id']}.wav";has_audio=narrate(s["narration"],audio)
 final=OUT/(s["id"]+".mp4" if has_audio else s["id"]+"-SILENT-REVIEW.mp4")
 if has_audio:cmd(["ffmpeg","-y","-i",str(silent),"-i",str(audio),"-map","0:v","-map","1:a","-c:v","libx264","-preset","veryfast","-crf","22","-c:a","aac","-b:a","128k","-shortest",str(final)])
 else:shutil.copy2(silent,final)
 manifest={"script_id":s["id"],"video":str(final.relative_to(ROOT)),"narration_present":has_audio,"sources":s.get("sources",[]),"claims_to_verify":s.get("claims_to_verify",[]),"assets":credits,"needs_human_review":True}
 (OUT/(s["id"]+".manifest.json")).write_text(json.dumps(manifest,indent=2))
 return final
def produce(count=3):
 state=read_json("scripts.json",{"scripts":[]});queue=read_json("publishing_queue.json",{"items":[]});done={x["script_id"] for x in queue["items"]}
 todo=[s for s in state["scripts"] if s["status"]=="draft" and s["id"] not in done][:count]
 for s in todo:
  p=produce_one(s);queue["items"].append({"script_id":s["id"],"video":str(p.relative_to(ROOT)),"status":"review_required"});s["status"]="rendered"
 write_json("scripts.json",state);write_json("publishing_queue.json",queue);print("Rendered",len(todo))
