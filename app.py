from flask import Flask, request, render_template, redirect, url_for
import os
import cv2
import numpy as np
from image_loader import load_images_from_folder
from image_processing import (
    convert_to_grayscale,
    reduce_noise,
    apply_threshold,
    detect_edges,
    apply_morphology
)
from image_saver import save_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['PROCESSED_FOLDER'] = 'static/processed/'

def apply_preprocessing(image, steps):
    processed_image = image.copy()
    for step in steps:
        if step['name'] == 'grayscale':
            if len(processed_image.shape) == 3:  # Check if the image has 3 channels
                processed_image = convert_to_grayscale(processed_image)
        elif step['name'] == 'noise_reduction':
            processed_image = reduce_noise(processed_image, step.get('ksize', (5, 5)))
        elif step['name'] == 'threshold':
            processed_image = apply_threshold(processed_image, step.get('thresh_value', 150))
        elif step['name'] == 'edge_detection':
            processed_image = detect_edges(processed_image, step.get('low_threshold', 100), step.get('high_threshold', 200))
        elif step['name'] == 'morphology':
            processed_image = apply_morphology(processed_image, step.get('operation', 'dilate'), step.get('kernel_size', (5, 5)))
    return processed_image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Read the image
            image = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)  # Read the image unchanged
            
            # Get preprocessing steps
            steps = []
            if request.form.get('grayscale'):
                steps.append({'name': 'grayscale'})
            if request.form.get('noise_reduction'):
                ksize = int(request.form.get('noise_reduction_ksize', 5))
                steps.append({'name': 'noise_reduction', 'ksize': (ksize, ksize)})
            if request.form.get('threshold'):
                thresh_value = int(request.form.get('threshold_value', 150))
                steps.append({'name': 'threshold', 'thresh_value': thresh_value})
            if request.form.get('edge_detection'):
                low_threshold = int(request.form.get('edge_detection_low', 100))
                high_threshold = int(request.form.get('edge_detection_high', 200))
                steps.append({'name': 'edge_detection', 'low_threshold': low_threshold, 'high_threshold': high_threshold})
            if request.form.get('morphology_dilate'):
                kernel_size = int(request.form.get('morphology_dilate_ksize', 5))
                steps.append({'name': 'morphology', 'operation': 'dilate', 'kernel_size': (kernel_size, kernel_size)})
            if request.form.get('morphology_erode'):
                kernel_size = int(request.form.get('morphology_erode_ksize', 5))
                steps.append({'name': 'morphology', 'operation': 'erode', 'kernel_size': (kernel_size, kernel_size)})

            # Apply preprocessing
            processed_image = apply_preprocessing(image, steps)
            processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], f'processed_{file.filename}')
            cv2.imwrite(processed_filepath, processed_image)

            return render_template('index.html', original_image=filepath, processed_image=processed_filepath)

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)
    app.run(debug=True)
