import logging
from logging.handlers import RotatingFileHandler


# Define the format for the logs
class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.levelname = record.levelname.lower()
        return super().format(record)


# Function to set up logging
def setup_logging():
    # Create a custom logger
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)

    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)

    # Set level for handlers
    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    console_format = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_format = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
