import os,shutil,subprocess
from pathlib import Path
def narrate(text,output):
 exe=shutil.which("piper"); model=os.getenv("PIPER_VOICE_MODEL")
 if not exe or not model:
  print("Piper or PIPER_VOICE_MODEL unavailable");return False
 Path(output).parent.mkdir(parents=True,exist_ok=True)
 with open(output,"wb") as f: subprocess.run([exe,"--model",model,"--output_file",str(output)],input=text.encode(),stdout=subprocess.DEVNULL,check=True)
 return Path(output).stat().st_size>1000
