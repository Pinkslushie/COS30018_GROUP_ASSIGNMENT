import os
import cv2
import time
import argparse
import tkinter as tk
from tkinter import filedialog

from detector import DetectorTF2

def select_video_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4 *.avi")])
    return file_path

def DetectFromCamera(detector, video_path, save_output=False, output_dir='frames/', window_width=1920, window_height=1080):

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    screenshot_dir = 'screenshot_of_video'

    # Create Screenshot directory if it doesn't exist
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    while True:
        ret, img = cap.read()
        if not ret:
            break

        timestamp1 = time.time()
        det_boxes = detector.DetectFromImage(img)
        elapsed_time = round((time.time() - timestamp1) * 1000)  # ms
        img_with_detections = detector.DisplayDetections(img, det_boxes, det_time=elapsed_time)

        # Resize image to fit the window
        scaled_img = cv2.resize(img_with_detections, (window_width, window_height))

        cv2.imshow('Object Detection From Video', scaled_img)
        
        key = cv2.waitKey(1)
        if key == 27:  # Esc key
            break
        elif key == ord('s'):  # 's' key for saving screenshot
            screenshot_path = os.path.join(screenshot_dir, f'screenshot_{time.strftime("%Y%m%d-%H%M%S")}.jpg')
            print("Saving screenshot:", screenshot_path)
            cv2.imwrite(screenshot_path, img_with_detections)

        if save_output:
            frame_count += 1
            frame_output_path = os.path.join(output_dir, f'frame_{frame_count}.jpg')
            print("Saving frame:", frame_output_path)
            cv2.imwrite(frame_output_path, img_with_detections)  # Save the annotated frame
            
    # Release VideoCapture and destroy windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Object Detection from Video')
    parser.add_argument('--model_path', help='Path to frozen detection model',
                        default='models/EDD0-Power/saved_model')
    parser.add_argument('--path_to_labelmap', help='Path to labelmap (.pbtxt) file',
                        default='models/edd0_label_map.pbtxt')
    parser.add_argument('--class_ids', help='id of classes to detect, expects string with ids delimited by ","',
                        type=str, default=None)  # example input "1,3" to detect person and car
    parser.add_argument('--threshold', help='Detection Threshold', type=float, default=0.5)
    parser.add_argument('--output_directory', help='Path to output images and video', default='frames/')
    parser.add_argument('--save_output', help='Flag for save images and video with detections visualized, default: False',
                        action='store_true')  # default is false
    args = parser.parse_args()

    id_list = None
    if args.class_ids is not None:
        id_list = [int(item) for item in args.class_ids.split(',')]

    if args.save_output:
        if not os.path.exists(args.output_directory):
            os.makedirs(args.output_directory)

    # Instance of the class DetectorTF2
    detector = DetectorTF2(args.model_path, args.path_to_labelmap, class_id=id_list, threshold=args.threshold)

    video_path = select_video_file()  # Select video file using file explorer dialog
    if video_path:
        DetectFromCamera(detector, video_path, save_output=args.save_output, output_dir=args.output_directory, window_width=1000, window_height=768)

    print("Done ...")