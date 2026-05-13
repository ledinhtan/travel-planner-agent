import os
import logging
from datetime import datetime

# Create a single logs directory in the current working directory
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

# Generate log filename with timestamp
timestamp = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
log_filename = f"{timestamp}.log"

# Full path to the log file (inside the logs directory)
log_file_path = os.path.join(log_dir, log_filename)

# Configure logging
logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)