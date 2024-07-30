import cv2

def convert_to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def reduce_noise(image, ksize=(5, 5)):
    return cv2.GaussianBlur(image, ksize, 0)

def apply_threshold(image, thresh_value=150):
    _, thresh = cv2.threshold(image, thresh_value, 255, cv2.THRESH_BINARY)
    return thresh

def detect_edges(image, low_threshold=100, high_threshold=200):
    return cv2.Canny(image, low_threshold, high_threshold)

def apply_morphology(image, operation='dilate', kernel_size=(5, 5)):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    if operation == 'dilate':
        return cv2.dilate(image, kernel, iterations=1)
    elif operation == 'erode':
        return cv2.erode(image, kernel, iterations=1)
    return image
