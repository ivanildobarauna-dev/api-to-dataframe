import pytest
import logging
import contextlib
from unittest.mock import patch, MagicMock

# Create a simple context manager to replace span_in_context
@contextlib.contextmanager
def mock_span_in_context(name, kind=None, attributes=None):
    mock_span = MagicMock()
    mock_context = MagicMock()
    yield (mock_span, mock_context)

@pytest.fixture(autouse=True)
def patch_otel_for_tests(monkeypatch):
    """
    Completely disable and replace OpenTelemetry to prevent test failures.
    This is a more aggressive approach that should work even with coverage.
    """
    # Create a proper logger with a handler that won't cause errors
    test_logger = logging.getLogger("test-logger")
    test_logger.setLevel(logging.INFO)
    handler = logging.NullHandler()
    handler.setLevel(logging.INFO)
    test_logger.addHandler(handler)
    test_logger.propagate = False
    
    # Mock telemetry components
    mock_traces = MagicMock()
    mock_traces.span_in_context.side_effect = mock_span_in_context
    mock_traces.get_tracer.return_value = MagicMock()
    mock_traces.new_span.return_value = MagicMock()
    
    mock_logs = MagicMock()
    mock_logs.new_log.return_value = None
    mock_logs.get_logger.return_value = test_logger
    
    mock_metrics = MagicMock()
    mock_metrics.metric_increment.return_value = None
    mock_metrics.record_gauge.return_value = None
    mock_metrics.record_histogram.return_value = None
    
    # Mock main telemetry object
    mock_telemetry = MagicMock()
    mock_telemetry.traces.return_value = mock_traces
    mock_telemetry.logs.return_value = mock_logs
    mock_telemetry.metrics.return_value = mock_metrics
    
    # Apply all patches
    monkeypatch.setattr("api_to_dataframe.utils.logger.telemetry", mock_telemetry)
    monkeypatch.setattr("api_to_dataframe.utils.logger.logger", test_logger)
    monkeypatch.setattr("api_to_dataframe.models.retainer.logger", test_logger)
    monkeypatch.setattr("api_to_dataframe.models.retainer.telemetry", mock_telemetry)
    monkeypatch.setattr("api_to_dataframe.controller.client_builder.telemetry", mock_telemetry)
    monkeypatch.setattr("api_to_dataframe.models.get_data.telemetry", mock_telemetry)
    
    # Also patch the wrapper_builder function in case it's used directly
    monkeypatch.setattr("otel_wrapper.deps_injector.wrapper_builder", lambda app_name: mock_telemetry)