import subprocess
import sys
import os
import json

print("Hack --- Installing dependencies")
subprocess.call([sys.executable, "-m", "pip", "install", "pillow"])
subprocess.call([sys.executable, "-m", "pip", "install", "pandas"])
print("Hack --- Dependencies successfully installed")

output_file = os.path.join(
    "..",
    "outputs",
    "0",
    "0"
)

print(" --- Collecting paths ---")
with open("../task.json") as f:
    manifest = json.load(f)
    try:
        model_path = manifest['inputs'][0]['connections'][0]['file']
        images_path = manifest['inputs'][1]['connections'][0]['file']
    except (KeyError, IndexError) as e:
        input_path = None
print("Model path is: {}".format(model_path))
print("Images folder is: {}".format(images_path))


subprocess.call([sys.executable, "object_detection.py",
                 "--od_m", model_path,
                 "--images", images_path,
                 "--results", output_file,
                 "--od_thres", "0.7",
                 "--od_target", "1"])

