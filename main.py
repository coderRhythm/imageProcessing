from image_loader import load_images_from_folder
from image_processing import (
    convert_to_grayscale,
    reduce_noise,
    apply_threshold,
    detect_edges,
    apply_morphology
)
from image_saver import save_image
from logger import setup_logger, log_preprocessing
from visualization import display_images

def get_user_steps():
    print("Choose preprocessing steps (enter the numbers separated by commas):")
    print("1. Grayscale Conversion")
    print("2. Noise Reduction")
    print("3. Thresholding")
    print("4. Edge Detection")
    print("5. Morphological Operations (Dilation)")
    print("6. Morphological Operations (Erosion)")

    choices = input("Enter your choices (1-6): ").split(',')

    steps = []
    for choice in choices:
        choice = choice.strip()
        if choice == '1':
            steps.append({'name': 'grayscale'})
        elif choice == '2':
            ksize = int(input("Enter kernel size for noise reduction (e.g., 5 for 5x5): "))
            steps.append({'name': 'noise_reduction', 'ksize': (ksize, ksize)})
        elif choice == '3':
            thresh_value = int(input("Enter threshold value (e.g., 150): "))
            steps.append({'name': 'threshold', 'thresh_value': thresh_value})
        elif choice == '4':
            low_threshold = int(input("Enter low threshold for edge detection (e.g., 100): "))
            high_threshold = int(input("Enter high threshold for edge detection (e.g., 200): "))
            steps.append({'name': 'edge_detection', 'low_threshold': low_threshold, 'high_threshold': high_threshold})
        elif choice == '5':
            kernel_size = int(input("Enter kernel size for dilation (e.g., 5 for 5x5): "))
            steps.append({'name': 'morphology', 'operation': 'dilate', 'kernel_size': (kernel_size, kernel_size)})
        elif choice == '6':
            kernel_size = int(input("Enter kernel size for erosion (e.g., 5 for 5x5): "))
            steps.append({'name': 'morphology', 'operation': 'erode', 'kernel_size': (kernel_size, kernel_size)})
        else:
            print(f"Invalid choice: {choice}")

    return steps

def apply_preprocessing(image, steps):
    processed_image = image.copy()
    for step in steps:
        if step['name'] == 'grayscale':
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

def main():
    setup_logger()

    folder_path = input("Enter the path to the image folder: ")
    output_folder = input("Enter the path to the output folder: ")
    
    images, filenames = load_images_from_folder(folder_path)

    steps = get_user_steps()
    
    for img, filename in zip(images, filenames):
        processed_img = apply_preprocessing(img, steps)
        
        display_images(img, processed_img)
        
        save_image(processed_img, output_folder, f'processed_{filename}')
        
        log_preprocessing(filename, steps)
    
    print("Processing complete. Check the output folder for processed images and the log file for details.")

if __name__ == '__main__':
    main()
