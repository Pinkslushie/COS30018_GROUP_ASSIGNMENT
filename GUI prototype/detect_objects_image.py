import os
import cv2
import time
import argparse
import tkinter as tk
from tkinter import filedialog

from detector import DetectorTF2

def select_image_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    return file_path

def DetectFromImage(detector, image_path, save_output=False, output_dir='frames/', max_window_size=(800, 600)):
    img = cv2.imread(image_path)

    # Create a copy of the original image for detection
    original_img = img.copy()

    # Resize the image if its dimensions exceed the maximum window size for display
    if img.shape[0] > max_window_size[1] or img.shape[1] > max_window_size[0]:
        img = cv2.resize(img, max_window_size, interpolation=cv2.INTER_AREA)

    det_boxes = detector.DetectFromImage(original_img)
    img_with_detections = detector.DisplayDetections(original_img, det_boxes)

    # Display the resized image with detections
    display_img = img_with_detections
    if img_with_detections.shape[0] > max_window_size[1] or img_with_detections.shape[1] > max_window_size[0]:
        display_img = cv2.resize(img_with_detections, max_window_size, interpolation=cv2.INTER_AREA)

    cv2.imshow('Object Detection Result', display_img)

    screenshot_dir = 'screenshot_of_image/'
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or cv2.getWindowProperty('Object Detection Result', cv2.WND_PROP_VISIBLE) < 1:
            break
        elif key == ord('s'):
            screenshot_path = os.path.join(screenshot_dir, f"screenshot_{time.strftime('%Y%m%d-%H%M%S')}.png")
            cv2.imwrite(screenshot_path, img_with_detections)  # Save the original resolution image with detections
            print(f"Screenshot saved at: {screenshot_path}")

    cv2.destroyAllWindows()

    if save_output:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, os.path.basename(image_path))
        cv2.imwrite(output_path, img_with_detections)
        print("Detection result saved at:", output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Object Detection from Images or Video')
    parser.add_argument('--model_path', help='Path to frozen detection model', default='models/EDD0-Power/saved_model')
    parser.add_argument('--path_to_labelmap', help='Path to labelmap (.pbtxt) file', default='models/edd0_label_map.pbtxt')
    parser.add_argument('--class_ids', help='id of classes to detect, expects string with ids delimited by ","', type=str, default=None)  # example input "1,3" to detect person and car
    parser.add_argument('--threshold', help='Detection Threshold', type=float, default=0.2)
    parser.add_argument('--output_directory', help='Path to output images and video', default='frames/')
    parser.add_argument('--save_output', help='Flag for save images and video with detections visualized, default: False', action='store_true')  # default is false
    args = parser.parse_args()

    id_list = None
    if args.class_ids is not None:
        id_list = [int(item) for item in args.class_ids.split(',')]

    if args.save_output:
        if not os.path.exists(args.output_directory):
            os.makedirs(args.output_directory)

    # Instance of the class DetectorTF2
    detector = DetectorTF2(args.model_path, args.path_to_labelmap, class_id=id_list, threshold=args.threshold)

    image_path = select_image_file()  # Select image file using file explorer dialog
    if image_path:
        DetectFromImage(detector, image_path, save_output=args.save_output, output_dir=args.output_directory)

    print("Done ...")
