import json,os,re
from datetime import datetime,timezone
from src.common.config import settings,read_json,write_json
def llm(prompt):
 model=os.getenv("LLM_MODEL_PATH")
 if not model: return None
 try:
  from llama_cpp import Llama
  engine=Llama(model_path=model,n_ctx=4096,verbose=False)
  raw=engine.create_chat_completion(messages=[{"role":"system","content":"Write accurate short video scripts. Return JSON only. Do not invent facts."},{"role":"user","content":prompt}],max_tokens=1200)["choices"][0]["message"]["content"]
  m=re.search(r"\{.*\}",raw,re.S); return json.loads(m.group()) if m else None
 except Exception as e: print("LLM fallback:",e); return None
def fallback(t):
 title=t["title"]; summary=t.get("summary","Explore the original source for more detail.")
 return {"hook":"You probably haven't seen this: "+title,
 "narration":f"Here's something worth discovering. {title}. {summary[:220]}. The details are worth exploring, and the original source is linked for you to check. Follow CurioDaily for more discoveries.",
 "caption":title+" — a CurioDaily discovery. Check the original source.",
 "hashtags":["#CurioDaily","#DidYouKnow","#Discovery"],
 "scenes":[{"text":title,"visual_query":title,"duration":8},{"text":summary[:120],"visual_query":title+" visual","duration":10},{"text":"Explore the original source","visual_query":"cinematic abstract background","duration":8}],
 "claims_to_verify":[title],"sources":[t["url"]],"needs_human_review":True}
def generate(count=3):
 topics=read_json("topics.json",{"topics":[]}); scripts=read_json("scripts.json",{"scripts":[]})
 seen={s["topic_id"] for s in scripts["scripts"]}; candidates=[t for t in sorted(topics["topics"],key=lambda x:x["score"],reverse=True) if t["status"]=="new" and t["id"] not in seen]
 made=[]
 for t in candidates[:count]:
  prompt="Create 35-55 sec vertical video script JSON with hook,narration,caption,hashtags,3-5 scenes(text,visual_query,duration),claims_to_verify,sources,needs_human_review=true. Only use supplied information: "+json.dumps(t)
  s=llm(prompt) or fallback(t)
  s.update({"id":"cd-"+t["id"],"topic_id":t["id"],"created_at":datetime.now(timezone.utc).isoformat(),"status":"draft","category":"curiosity_science"})
  scripts["scripts"].append(s); t["status"]="scripted"; made.append(s)
 write_json("topics.json",topics); write_json("scripts.json",scripts); print("Scripts:",len(made)); return made
