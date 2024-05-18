import logging
import sys


console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('.log')
file_handler.setLevel(logging.DEBUG)

handlers = [file_handler, console_handler]
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-6s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=handlers
    )

logger = logging.getLogger(__name__)