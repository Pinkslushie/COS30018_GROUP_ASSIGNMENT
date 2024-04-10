# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os

### Set configurations

# Repo URL
# repo_url = 'https://github.com/yuki678/driving-object-detection'

# Models
MODELS_CONFIG = {
    'ssd_mobilenet_v2': {
        'model_name': 'ssd_mobilenet_v2_320x320_coco17_tpu-8',
        'model_path': r'\models\ssd_mobilenet_v2',
        'pipeline_file': '\pipeline.config'
    },
    # 'ssd_mobilenet_v2_fpn': {
    #     'model_name': 'ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8',
    #     'model_path': r'\models\tf2\my_ssd_mobilenet_v2_fpnlite',
    #     'pipeline_file': '\pipeline.config'
    # },
    # 'my_centernet_resnet50_v1_fpn': {
    #     'model_name': 'centernet_resnet50_v1_fpn_512x512_coco17_tpu-8',
    #     'model_path': r'\models\tf2\my_centernet_resnet50_v1_fpn',
    #     'pipeline_file': '\pipeline.config'
    # },
    # 'my_centernet_resnet101_v1_fpn': {
    #     'model_name': 'centernet_resnet101_v1_fpn_512x512_coco17_tpu-8',
    #     'model_path': r'\models\tf2\my_centernet_resnet101_v1_fpn',
    #     'pipeline_file': '\pipeline.config'
    # }
}

# Select a model to use.
selected_model = 'ssd_mobilenet_v2'

model_name = MODELS_CONFIG[selected_model]['model_name']
model_path = MODELS_CONFIG[selected_model]['model_path']
pipeline_file = MODELS_CONFIG[selected_model]['pipeline_file']

# Set Repository Home Directory
repo_dir_path = r'C:\Users\Public\COS30018\COS30018_GROUP_ASSIGNMENT-main' #os.path.abspath(os.path.join('.', os.path.basename(repo_url)))

# Set Label Map (.pbtxt) path and pipeline.config path
label_map_pbtxt_fname = repo_dir_path + r'\annotations\label_map.pbtxt'
pipeline_fname = repo_dir_path + model_path + pipeline_file

# Set .record path
test_record_fname = repo_dir_path + r'\annotations\test.tfrecord'
train_record_fname = repo_dir_path + r'\annotations\train.tfrecord'

# Set output directories and clean up
model_dir = repo_dir_path + r'\training'
output_dir = repo_dir_path + r'\exported-models'

os.makedirs(model_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)


#### Download Pretrained Model
import os
import shutil
import glob
import urllib.request
import tarfile
MODEL_FILE = model_name + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/'
DEST_DIR = 'pretrained_model'

if not (os.path.exists(MODEL_FILE)):
    urllib.request.urlretrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)

tar = tarfile.open(MODEL_FILE)
tar.extractall()
tar.close()

os.remove(MODEL_FILE)
if (os.path.exists(DEST_DIR)):
    shutil.rmtree(DEST_DIR)
os.rename(model_name, DEST_DIR)


# Set fine tune checkpoint
fine_tune_checkpoint = os.path.join(DEST_DIR, "checkpoint\ckpt-0")
print("fine_tune_checkpoint: ", fine_tune_checkpoint)


#### change the pipeline.config
# import re

# batch_size =  3

# def get_num_classes(pbtxt_fname):
#     from object_detection.utils import label_map_util
#     label_map = label_map_util.load_labelmap(pbtxt_fname)
#     categories = label_map_util.convert_label_map_to_categories(
#         label_map, max_num_classes=90, use_display_name=True)
#     category_index = label_map_util.create_category_index(categories)
#     return len(category_index.keys())

# num_classes = get_num_classes(label_map_pbtxt_fname)
# with open(pipeline_fname) as f:
#     s = f.read()
# with open(pipeline_fname, 'w') as f:
    
#     # fine_tune_checkpoint
#     s = re.sub('fine_tune_checkpoint: ".*?"',
#                 'fine_tune_checkpoint: "{}"'.format(fine_tune_checkpoint), s)
    
#     # tfrecord files train and test.
#     s = re.sub(
#         '(input_path: ".*?)(train.record)(.*?")', 'input_path: "{}"'.format(train_record_fname), s)
#     s = re.sub(
#         '(input_path: ".*?)(val.record)(.*?")', 'input_path: "{}"'.format(test_record_fname), s)

#     # label_map_path
#     s = re.sub(
#         'label_map_path: ".*?"', 'label_map_path: "{}"'.format(label_map_pbtxt_fname), s)

#     # # Set training batch_size.
#     # s = re.sub('batch_size: [0-9]+',
#     #             'batch_size: {}'.format(batch_size), s)

#     # # Set training steps, num_steps
#     # s = re.sub('num_steps: [0-9]+',
#     #             'num_steps: {}'.format(num_steps), s)
    
#     # # Set number of classes num_classes.
#     # s = re.sub('num_classes: [0-9]+',
#     #             'num_classes: {}'.format(num_classes), s)
#     f.write(s)


