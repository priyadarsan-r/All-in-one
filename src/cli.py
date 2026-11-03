import argparse,shutil
from src.discovery.run import discover
from src.scripting.generate import generate
from src.video.render import produce
from src.publishing.runner import publish
from src.analytics.collect import collect
from src.common.config import read_json,settings
def main():
 p=argparse.ArgumentParser();sub=p.add_subparsers(dest="cmd",required=True)
 sub.add_parser("discover")
 g=sub.add_parser("generate");g.add_argument("--count",type=int,default=3)
 v=sub.add_parser("produce");v.add_argument("--count",type=int,default=3)
 u=sub.add_parser("publish");u.add_argument("--platform",choices=["youtube","instagram","facebook"],required=True);u.add_argument("--limit",type=int,default=3)
 sub.add_parser("analytics");sub.add_parser("validate")
 a=p.parse_args()
 if a.cmd=="discover":discover()
 elif a.cmd=="generate":generate(a.count)
 elif a.cmd=="produce":produce(a.count)
 elif a.cmd=="publish":publish(a.platform,a.limit)
 elif a.cmd=="analytics":collect()
 elif a.cmd=="validate":
  assert settings()["target_videos_per_day"]==3
  for n,k in [("topics.json","topics"),("scripts.json","scripts"),("publishing_queue.json","items")]:assert k in read_json(n,{})
  assert shutil.which("ffmpeg"),"Install FFmpeg"
  print("Validation passed")
if __name__=="__main__":main()
