import logging

# Configure logging once at the start of your program
logging.basicConfig(
    encoding="utf-8",
    format="%(asctime)s :: api-to-dataframe[%(levelname)s] :: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    level=logging.INFO,
)

logger = logging.getLogger("api-to-dataframe")