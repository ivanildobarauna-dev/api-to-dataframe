import pytest
import logging
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_logger(monkeypatch):
    """
    Mock the logger to prevent test failures.
    """
    # Create a proper logger with a handler that won't cause errors
    test_logger = logging.getLogger("test-logger")
    test_logger.setLevel(logging.INFO)
    handler = logging.NullHandler()
    handler.setLevel(logging.INFO)
    test_logger.addHandler(handler)
    test_logger.propagate = False
    
    # Replace the real logger with our test logger
    monkeypatch.setattr("api_to_dataframe.utils.logger.logger", test_logger)
    monkeypatch.setattr("api_to_dataframe.models.retainer.logger", test_logger)
    
    yield test_logger

@pytest.fixture(autouse=True)
def mock_otel_wrapper():
    """
    Mock the OpenTelemetry wrapper to prevent test failures.
    This is applied to all tests automatically.
    """
    # Create mock objects for each component
    mock_span = MagicMock()
    mock_context = MagicMock()
    
    # Configure the traces mock
    mock_traces = MagicMock()
    mock_traces.span_in_context.return_value.__enter__.return_value = (mock_span, mock_context)
    mock_traces.get_tracer.return_value = MagicMock()
    
    # Configure the logs mock
    mock_logs = MagicMock()
    mock_logs.new_log.return_value = None
    mock_logs.get_logger.return_value = MagicMock()
    
    # Configure the metrics mock
    mock_metrics = MagicMock()
    
    # Configure the main telemetry object
    mock_wrapper = MagicMock()
    mock_wrapper.traces.return_value = mock_traces
    mock_wrapper.logs.return_value = mock_logs
    mock_wrapper.metrics.return_value = mock_metrics
    
    # Apply the patch to the wrapper_builder function
    with patch('otel_wrapper.deps_injector.wrapper_builder', return_value=mock_wrapper):
        yield mock_wrapper