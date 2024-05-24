# interface.py
import tkinter as tk
import subprocess
import os
from tkinter import messagebox

def run_detection_script():
    try:
        subprocess.Popen(['python', 'detect_objects_camera.py', '--save_output'])
        messagebox.showinfo("Info", "Object detection on cam is running.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run detection script: {e}")

def select_video():
    try:
        subprocess.Popen(['python', 'detect_objects_video.py'])
        messagebox.showinfo("Info", "Object detection on video is running.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run detection script: {e}")

def detect_objects_image():
    try:
        subprocess.Popen(['python', 'detect_objects_image.py'])
        messagebox.showinfo("Info", "Object detection on image is running.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run detection script: {e}")
        
def run_warp_image_script():
    try:
        subprocess.Popen(['python', 'warp_image.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run warp image script: {e}")

# Create the main window
root = tk.Tk()
root.title("Object Detection GUI")
root.geometry('1280x760')

# Create a frame for the left side buttons
left_frame = tk.Frame(root, width=200, bg="lightgrey")
left_frame.pack(side="left", fill="y")

# Create and place the button to run object detection
run_button = tk.Button(left_frame, text="Activate Cam for Real Time Object Detection", command=run_detection_script, padx=20, pady=20, font=('Arial', 14))
run_button.pack(pady=10)

# Create and place the button to select video for object detection
select_video_button = tk.Button(left_frame, text="Select Video for Object Detection", command=select_video, padx=20, pady=20, font=('Arial', 14))
select_video_button.pack(pady=10)

# Create a button to run object detection on an image
detect_image_button = tk.Button(left_frame, text="Select Image for Object Detection", command=detect_objects_image, padx=20, pady=20, font=('Arial', 14))
detect_image_button.pack(pady=10)

# Create and place the button to run warp_image.py script
warp_image_button = tk.Button(left_frame, text="Select Image to Warp", command=run_warp_image_script, padx=20, pady=20, font=('Arial', 14))
warp_image_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
