import subprocess
import sys
import os
import json

print("Hack --- Installing dependencies")
subprocess.call([sys.executable, "-m", "pip", "install", "pillow"])
subprocess.call([sys.executable, "-m", "pip", "install", "pandas"])
print("Hack --- Dependencies successfully installed")



args = [sys.executable, "./detect_objects.py",
                        "--od_m", model_path,
                        "--images", images_path,
                        "--results", output_file,
                        "--od_thres", "0.7",
                        "--od_target", "1"]

#os.execlp("python", *args)

print("About to execute: {}".format(args))

subprocess.call(args)
