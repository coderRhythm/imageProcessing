import cv2
import numpy as np
from matplotlib import pyplot as plt

def display_images(original, processed):
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    
    plt.subplot(1, 2, 2)
    plt.title('Processed Image')
    plt.imshow(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB))
    
    plt.show()
