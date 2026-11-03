from datetime import datetime,timezone
from src.common.config import read_json,write_json
def collect():
 p=read_json("published.json",{"items":[]});a=read_json("analytics.json",{"items":[]})
 a["items"].append({"collected_at":datetime.now(timezone.utc).isoformat(),"published_count":len(p["items"]),"note":"No platform performance metrics queried yet; add Insights/YouTube Analytics scopes."})
 write_json("analytics.json",a);print("Publication inventory recorded.")
