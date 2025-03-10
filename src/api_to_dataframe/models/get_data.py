import requests
import pandas as pd
from api_to_dataframe.utils.logger import logger, telemetry


class GetData:
    @staticmethod
    def get_response(endpoint: str, headers: dict, connection_timeout: int):
        # Start a span for the API request
        with telemetry.traces().span_in_context("http_request") as (span, _):
            span.set_attribute("http.url", endpoint)
            span.set_attribute("http.method", "GET")
            span.set_attribute("http.timeout", connection_timeout)
            
            # Log the request
            telemetry.logs().new_log(
                msg=f"Sending HTTP GET request to {endpoint}",
                tags={
                    "endpoint": endpoint,
                    "timeout": connection_timeout,
                    "component": "GetData",
                    "method": "get_response"
                },
                level=20  # INFO level
            )
            
            try:
                # Make the request
                response = requests.get(endpoint, timeout=connection_timeout, headers=headers)
                
                # Set response attributes on span
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.response_content_length", len(response.content))
                
                # Attempt to raise for status to catch errors
                response.raise_for_status()
                
                # Log successful response
                telemetry.logs().new_log(
                    msg=f"Received HTTP {response.status_code} response from {endpoint}",
                    tags={
                        "endpoint": endpoint,
                        "status_code": response.status_code,
                        "response_size": len(response.content),
                        "component": "GetData",
                        "method": "get_response"
                    },
                    level=20  # INFO level
                )
                
                # Record successful request metric
                telemetry.metrics().metric_increment(
                    name="http.request.success",
                    tags={
                        "endpoint": endpoint,
                        "status_code": response.status_code
                    }
                )
                
                return response
                
            except requests.exceptions.RequestException as e:
                # Record the exception on the span
                span.record_exception(e)
                span.set_attribute("error", True)
                span.set_attribute("error.type", type(e).__name__)
                span.set_attribute("error.message", str(e))
                
                # Log the error
                telemetry.logs().new_log(
                    msg=f"HTTP request failed: {str(e)}",
                    tags={
                        "endpoint": endpoint,
                        "error": str(e),
                        "error_type": type(e).__name__,
                        "component": "GetData",
                        "method": "get_response"
                    },
                    level=40  # ERROR level
                )
                
                # Record failure metric
                telemetry.metrics().metric_increment(
                    name="http.request.failure",
                    tags={
                        "endpoint": endpoint,
                        "error_type": type(e).__name__
                    }
                )
                
                # Re-raise the exception
                raise

    @staticmethod
    def to_dataframe(response):
        # Start a span for dataframe conversion
        with telemetry.traces().span_in_context("convert_to_dataframe") as (span, _):
            # Set attributes about the data
            data_size = len(response) if isinstance(response, list) else 1
            span.set_attribute("data.size", data_size)
            span.set_attribute("data.type", type(response).__name__)
            
            # Log conversion attempt
            telemetry.logs().new_log(
                msg="Converting data to DataFrame",
                tags={
                    "data_size": data_size,
                    "data_type": type(response).__name__,
                    "component": "GetData",
                    "method": "to_dataframe"
                },
                level=20  # INFO level
            )
            
            try:
                # Convert to DataFrame
                df = pd.DataFrame(response)
                
                # Check if DataFrame is empty
                if df.empty:
                    error_msg = "::: DataFrame is empty :::"
                    logger.error(error_msg)
                    
                    # Log the error with OpenTelemetry
                    telemetry.logs().new_log(
                        msg=error_msg,
                        tags={
                            "data_size": data_size,
                            "data_type": type(response).__name__,
                            "component": "GetData",
                            "method": "to_dataframe"
                        },
                        level=40  # ERROR level
                    )
                    
                    # Record empty DataFrame metric
                    telemetry.metrics().metric_increment(
                        name="dataframe.empty",
                        tags={"data_type": type(response).__name__}
                    )
                    
                    # Set span as error
                    span.set_attribute("error", True)
                    span.set_attribute("error.type", "ValueError")
                    span.set_attribute("error.message", error_msg)
                    
                    raise ValueError(error_msg)
                
                # Log success
                telemetry.logs().new_log(
                    msg="Successfully converted data to DataFrame",
                    tags={
                        "rows": len(df),
                        "columns": len(df.columns),
                        "component": "GetData",
                        "method": "to_dataframe"
                    },
                    level=20  # INFO level
                )
                
                # Record dataframe metrics
                telemetry.metrics().record_gauge(
                    name="dataframe.rows",
                    tags={"data_type": type(response).__name__},
                    value=float(len(df))
                )
                
                telemetry.metrics().record_gauge(
                    name="dataframe.columns",
                    tags={"data_type": type(response).__name__},
                    value=float(len(df.columns))
                )
                
                # Set additional span attributes
                span.set_attribute("dataframe.rows", len(df))
                span.set_attribute("dataframe.columns", len(df.columns))
                
                return df
                
            except ValueError:
                # Re-raise ValueErrors (like empty DataFrame)
                raise
                
            except Exception as err:
                # Log the error
                error_msg = f"Invalid response for transform in dataframe: {err}"
                logger.error(error_msg)
                
                # Log with OpenTelemetry
                telemetry.logs().new_log(
                    msg=error_msg,
                    tags={
                        "error": str(err),
                        "error_type": type(err).__name__,
                        "data_type": type(response).__name__,
                        "component": "GetData",
                        "method": "to_dataframe"
                    },
                    level=40  # ERROR level
                )
                
                # Record conversion failure metric
                telemetry.metrics().metric_increment(
                    name="dataframe.conversion.error",
                    tags={"error_type": type(err).__name__}
                )
                
                # Record the exception on the span
                span.record_exception(err)
                span.set_attribute("error", True)
                span.set_attribute("error.type", type(err).__name__)
                span.set_attribute("error.message", str(err))
                
                # Raise TypeError with original error as cause
                raise TypeError(error_msg) from err
