import cv2
import numpy as np
import json
import os
from tkinter import Tk, filedialog

def main():
    # Initialize Tkinter root
    root = Tk()
    root.withdraw()  # Hide the root window

    # Prompt user to select an image file
    img_file = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    
    # Ensure an image file was selected
    if not img_file:
        print("No image file selected. Exiting...")
        return

    # Derive the JSON file name from the selected image file
    base_name = os.path.basename(img_file)
    json_file = os.path.splitext(base_name)[0] + ".json"

    # Ensure the JSON file exists in the same directory
    img_dir = os.path.dirname(img_file)
    json_file_path = os.path.join(img_dir, json_file)
    if not os.path.exists(json_file_path):
        print(f"JSON file not found: {json_file_path}. Exiting...")
        return

    # Create the "warped" folder if it doesn't exist
    if not os.path.exists('warped image'):
        os.makedirs('warped image')

    try:
        # Load JSON data
        with open(json_file_path) as f:
            data = json.load(f)

        # Extract quadrilateral points
        points = data['shapes'][0]['points']
        quadrilateral = np.array(points, dtype=np.float32)

        # Load the original image
        img = cv2.imread(img_file)

        # Calculate the bounding rectangle for the quadrilateral
        rect = cv2.boundingRect(quadrilateral)

        # Calculate the aspect ratio of the bounding rectangle
        aspect_ratio = rect[2] / rect[3]

        # Set the desired output image size (maintaining aspect ratio)
        w, h = 640, int(640 / aspect_ratio)  # Width is fixed, height is calculated based on aspect ratio

        # Prepare destination points for the resized and centered warped image
        dst_points = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)

        # Calculate perspective transformation matrix
        M = cv2.getPerspectiveTransform(quadrilateral, dst_points)

        # Calculate the desired scaling factor
        scale_factor = 2

        # Calculate the new output image size
        new_w = int(w * scale_factor)
        new_h = int(h * scale_factor)

        # Apply perspective transformation and resize the warped image
        warped_img = cv2.warpPerspective(img, M, (w, h))

        # Create a white background image of the desired size
        white_bg = np.full((h, w, 3), 255, dtype=np.uint8)

        # Calculate the offset to center the resized warped image on the white background
        offset_x = (w - warped_img.shape[1]) // 2
        offset_y = (h - warped_img.shape[0]) // 2

        # Paste the resized warped image onto the white background at the calculated offset
        white_bg[offset_y:offset_y + warped_img.shape[0], offset_x:offset_x + warped_img.shape[1]] = warped_img

        # Save the filled warped image in the "warped" folder
        warped_file = os.path.join('warped image', os.path.basename(img_file))
        cv2.imwrite(warped_file, white_bg)

        print('Process complete.')

    except FileNotFoundError:
        print(f"File not found: {json_file_path}. Exiting...")

if __name__ == "__main__":
    main()
