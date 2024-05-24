import os
import cv2
import time
import argparse
from detector import DetectorTF2

def DetectFromCamera(detector, save_output=False, output_dir='Screenshot/'):
    # Create output directory if it does not exist
    if save_output and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Output directory created: {output_dir}")

    cap = cv2.VideoCapture(0)  # Accessing the default camera (0)
    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return

    frame_count = 0
    last_save_time = time.time()
    save_image = False

    while True:
        ret, img = cap.read()
        if not ret:
            print("Error: Unable to read frame from the camera")
            break

        timestamp1 = time.time()
        det_boxes = detector.DetectFromImage(img)
        elapsed_time = round((time.time() - timestamp1) * 1000)  # ms
        img_with_detections = detector.DisplayDetections(img, det_boxes, det_time=elapsed_time)

        cv2.imshow('Real Time Object Detection', img_with_detections)
        
        # Check for ESC key press or window close event
        key = cv2.waitKey(1)
        if key == 27 or cv2.getWindowProperty('Real Time Object Detection', cv2.WND_PROP_VISIBLE) < 1:
            print("Exiting loop")
            break
        elif key == ord('s') and not save_image:  # Press 's' to save image if not already saved
            save_image = True
            print("Image saved")

        if save_output and save_image:
            frame_count += 1
            frame_output_path = os.path.join(output_dir, f'frame_{frame_count}.jpg')
            print(f"Saving frame: {frame_output_path}")
            cv2.imwrite(frame_output_path, img_with_detections)  # Save the annotated frame
            save_image = False  # Reset save_image to False after saving

    cap.release()
    cv2.destroyAllWindows()
    print("Camera released and windows destroyed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Object Detection from Images or Video')
    parser.add_argument('--model_path', help='Path to frozen detection model', default='models/EDD0-Power/saved_model')
    parser.add_argument('--path_to_labelmap', help='Path to labelmap (.pbtxt) file', default='models/edd0_label_map.pbtxt')
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

    # Instance of the class DetectorTF2
    detector = DetectorTF2(args.model_path, args.path_to_labelmap, class_id=id_list, threshold=args.threshold)

    print("Starting detection...")
    DetectFromCamera(detector, save_output=args.save_output, output_dir=args.output_directory)
    print("Detection finished.")