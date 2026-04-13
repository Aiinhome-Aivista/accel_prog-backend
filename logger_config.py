import logging
import os
from dotenv import load_dotenv

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from azure.monitor.opentelemetry.exporter import AzureMonitorLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
# from logger_config import logger

load_dotenv()
connection_string = os.getenv("YOUR_CONNECTION_STRING")

# ✅ TRACE SETUP
tracer_provider = TracerProvider()
tracer_provider.add_span_processor(
    BatchSpanProcessor(
        AzureMonitorTraceExporter(connection_string=connection_string)
    )
)
trace.set_tracer_provider(tracer_provider)

# ✅ LOG SETUP
logger_provider = LoggerProvider()
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(
        AzureMonitorLogExporter(connection_string=connection_string)
    )
)

handler = LoggingHandler(logger_provider=logger_provider)

# ✅ LOGGER
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# 👉 FORMATTER ADD (IMPORTANT)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

# Console log
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.propagate = False

print("✅ Azure Monitor configured", flush=True)