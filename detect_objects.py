import subprocess
import sys

print("[Hack] --- Installing dependencies")
subprocess.call([sys.executable, "-m", "pip", "install", "pillow"])
subprocess.call([sys.executable, "-m", "pip", "install", "pandas"])
subprocess.call([sys.executable, "-m", "pip", "install", "tensorflow"])
print("[Hack] --- Dependencies successfully installed")

from PIL import Image, ImageFont, ImageDraw

import os
import argparse
import numpy as np
from pathlib import Path
from ai.object_detection import CocoDetectorAPI
import pandas as pd
import json

output_file = os.path.join(
    "..",
    "outputs",
    "0",
    "0"
)

print("[INFO] --- Collecting paths ---")
with open("../task.json") as f:
    manifest = json.load(f)
    try:
        model_path = manifest['inputs'][0]['connections'][0]['file']
        images_path = manifest['inputs'][1]['connections'][0]['file']
    except (KeyError, IndexError) as e:
        input_path = None
print("[INFO] Model path is: {}".format(model_path))
print("[INFO] Images folder is: {}".format(images_path))


def object_detection(cod, img_base_path, target, hd_threshold=0.7):

    im = Image.open(img_base_path)
    img_base = np.asarray(im)

    obj_boxes, obj_scores, classes, num = cod.process_frame(img_base, hd_threshold, target)
    pil_image_detections = tag_detections(img_base, obj_boxes, obj_scores)

    df = pd.DataFrame(obj_scores, columns=classes)

    return pil_image_detections, df


def tag_detections(img, obj_boxes, scores):

    pil_image = Image.fromarray(img)
    img_draw = ImageDraw.Draw(pil_image)

    for i in range(len(scores[0])):
        box = obj_boxes[i]

        #font = ImageFont.truetype("arial", 20)
        #text = "Person: " + str(scores[0][i])

        #img_draw.text((int(box[1]), int(box[0])), text, font=font)
        img_draw.rectangle((int(box[1]), int(box[0]), int(box[3]), int(box[2])), fill=None, outline=(255, 0, 0))

    return pil_image


if __name__ == "__main__":

    print("--- Initiating Object Detection ---")

    # parser = argparse.ArgumentParser()
    #
    # parser.add_argument("--od_m", type=str, required=True)
    # parser.add_argument("--od_thres", type=float, required=True)
    # parser.add_argument("--od_target", type=str, required=True)
    # parser.add_argument("--images", type=str, required=True)
    # parser.add_argument("--results", type=str, required=True)
    # args = parser.parse_args()

    print("[INFO] Loading images from: " + images_path)
    images = Path(images_path).glob("*.jpg")

    print("[INFO] Loading model from: " + model_path)
    cod_api = CocoDetectorAPI(model_path)

    for image in images:

        image_name = Path(image).resolve().stem

        image_with_det, image_data_df = object_detection(cod_api,
                                                         str(image),
                                                         int(1),
                                                         float(0.7))

        image_det_path = os.path.join(
            output_file,
            "{}_tagged.jpg".format(image_name)
        )

        results_path = os.path.join(
            output_file,
            "{}_data.pkl".format(image_name)
        )

        print("[INFO] Saving tagged image to: " + image_det_path)
        print("[INFO] Saving data to: " + results_path)

        # save in new file
        image_with_det.save(image_det_path, "JPEG")
        image_data_df.to_pickle(results_path)
