# Image Dataset Overview

## Datasets

- We have approximately 150 images featuring out-of-stock scenarios.
- There are about 150 images depicting misplacement scenarios.
- Some images may exhibit both out-of-stock and misplacement conditions, leading to a total of 267 images instead of 300.

### Case 1 (C1)
- **Images:** Approximately 250 images.

### Case 2 (C2)
- **Images:** Approximately 250 images.
- **Perfect Images:** An additional 150 perfect images.

### Case 3 (C3)
- **Images:** Approximately 250 images.
- **Perfect Images:** An additional 150 perfect images.
- **Original Images:** An additional 75 original images, making up 50% of the dataset.

## Extensions

### Angled Images
- A set of images captured from various angles to supplement the primary datasets.

### Ablation Study

#### Images_C1 (More Bounding Boxes)
- This dataset is part of the ablation study described in section 6.6 of the report. It contains images with additional bounding boxes for more detailed analysis.

### Original Images
- A collection of unmodified original images that have not been combined with other datasets.

## Data Splitting

For data splitting, we use an 8:2 ratio, where 80% of the dataset is used for training and 20% for testing. There is no validation set. The split is done randomly, but after splitting, we keep a copy of the output so all team members use the same split images for training and testing to ensure consistency. The splitting is done using a Python script that only accepts images in jpg, jpeg, and png formats.

```bash
python scripts\partition_dataset.py -x -i images\ -r 0.2
```

## Data Pre-processing

- Data labels are generated in .xml format during the splitting process. These labels contain information about the bounding boxes, including the file name, width, height, class (out-of-stock or misplacement), and coordinates (xmin, ymin, xmax, ymax).
- The data is then converted to .csv format to make it more human-readable and easier to stream than XML, especially for larger datasets.

```bash
python scripts\xml_to_csv.py -i images\train -o annotations\train_labels.csv
python scripts\xml_to_csv.py -i images\test -o annotations\test_labels.csv
```

- The .csv files are then converted to TFRecord Format (.record), which is required by TensorFlow for more efficient training.

```bash
python scripts\generate_tfrecord.py -c annotations/test_labels.csv -i images/test -x images/test -o annotations/test.tfrecord -l annotations/label_map.pbtxt
python scripts\generate_tfrecord.py -c annotations/train_labels.csv -i images/train -x images/train -o annotations/train.tfrecord -l annotations/label_map.pbtxt
```

- The models use an image resizer to 512x512, maintaining its aspect ratio, with the remaining space filled with black pixels.
- Single Class Models (CenterNet Resnet50 V2 512x512 and CenterNet Resnet101 V1 FPN 512x512): Data augmentation techniques include random horizontal flipping, scaling, cropping, and padding.
- Multi Class Model (EfficientDet D0 512x512): Data augmentation techniques include random cropping with variable aspect ratios and sizes, and random padding.

## Model Training

The model is trained using TensorFlow 2’s main training script, model_main_tf2.py. The training command also requires the pipeline.config, which includes the configurations specific to the model. The model’s checkpoints and training logs are saved inside the training directory.

```bash
python C:\Users\Public\COS30082\Tensorflow\models\research\object_detection\model_main_tf2.py --pipeline_config_path="models\[model name]\pipeline.config" --model_dir="training" –alsologtostderr
```

- Single Class – CenterNet Resnet101 V1 FPN 512x512: Uses ResNet-v1-101 feature extractor.
- Single Class – CenterNet Resnet50 V2 512x512: Uses ResNet-50 V2 feature extractor.
- Multi Class – EfficientDet D0 512x512: Uses SSD EfficientNet-B0 BiFPN feature extractor.

## Model Exportation

The model is exported using exporter_main_v2.py, which is part of the TensorFlow Object Detection API. The model accepts images in tensor format. We need to provide the directory to the pipeline.config used and the directory of the model’s checkpoint, which is training, and save it in a directory called exported-models.

```bash
python C:\Users\Public\COS30082\models-master\research\object_detection\exporter_main_v2.py --input_type image_tensor --pipeline_config_path="models\[model name]\pipeline.config" --trained_checkpoint_dir="training" --output_directory="exported-models"
```
