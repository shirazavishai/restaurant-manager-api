import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
import os 

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define log file path
log_file = 'restaurant_logs.log'

# Create a file handler for logging to a file
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Create a console handler for logging to stdout
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

if (os.getenv('APPLICATION_INSIGHTS_INSTRUMENTATION_KEY')):
    instrumentation_key = os.getenv('APPLICATION_INSIGHTS_INSTRUMENTATION_KEY')  # Add to environment variables or secrets
    azure_handler = AzureLogHandler(connection_string=f'InstrumentationKey={instrumentation_key}')
    logger.addHandler(azure_handler)
