import logging
from otel_wrapper.deps_injector import wrapper_builder

# Configure logging once at the start of your program
logging.basicConfig(
    encoding="utf-8",
    format="%(asctime)s :: api-to-dataframe[%(levelname)s] :: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z",
    level=logging.INFO,
)

# Initialize traditional logger
logger = logging.getLogger("api-to-dataframe")

# Initialize OpenTelemetry wrapper
telemetry = wrapper_builder("api-to-dataframe")