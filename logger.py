import logging

def setup_logger():
    logging.basicConfig(
        filename='preprocessing.log',
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s:%(message)s'
    )

def log_preprocessing(filename, steps):
    logging.info(f'File: {filename}, Steps: {steps}')
