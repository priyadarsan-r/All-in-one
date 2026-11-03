import json, os
from pathlib import Path
from dotenv import load_dotenv
ROOT=Path(__file__).resolve().parents[2]
load_dotenv(ROOT/".env")
def settings(): return json.loads((ROOT/"config/settings.json").read_text())
def read_json(name, default):
 p=ROOT/"data"/name
 try: return json.loads(p.read_text())
 except (OSError,json.JSONDecodeError): return default
def write_json(name,value):
 p=ROOT/"data"/name; p.parent.mkdir(exist_ok=True)
 t=p.with_suffix(p.suffix+".tmp"); t.write_text(json.dumps(value,indent=2,ensure_ascii=False)); t.replace(p)
def env_bool(k,default=False): return os.getenv(k,str(default)).lower() in ("1","true","yes","on")
