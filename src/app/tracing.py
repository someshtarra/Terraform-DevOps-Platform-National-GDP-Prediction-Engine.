from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.core.config import settings
from app.core.logging import logger


def init_tracing(app):
    try:
        provider = TracerProvider()
        processor = BatchSpanProcessor(ConsoleSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        FastAPIInstrumentor.instrument_app(app)
        logger.info("Initialized OpenTelemetry distributed tracing.")
    except Exception as e:
        logger.warning(f"OpenTelemetry initialization skipped: {e}")
