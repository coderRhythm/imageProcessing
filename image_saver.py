import cv2
import os

def save_image(image, output_path, filename):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    cv2.imwrite(os.path.join(output_path, filename), image)
