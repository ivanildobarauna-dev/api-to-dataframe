import time
from enum import Enum

from requests.exceptions import RequestException
from api_to_dataframe.utils.logger import logger, telemetry
from api_to_dataframe.utils import Constants


class Strategies(Enum):
    NO_RETRY_STRATEGY = 0
    LINEAR_RETRY_STRATEGY = 1
    EXPONENTIAL_RETRY_STRATEGY = 2


def retry_strategies(func):
    def wrapper(*args, **kwargs):  # pylint: disable=inconsistent-return-statements
        retry_number = 0
        
        # Get the endpoint for better observability context
        endpoint = args[0].endpoint if hasattr(args[0], 'endpoint') else 'unknown'
        
        # Start a span for this entire retry operation
        with telemetry.traces().span_in_context("retry_operation") as (span, _):
            span.set_attribute("endpoint", endpoint)
            span.set_attribute("retry_strategy", args[0].retry_strategy.name)
            span.set_attribute("max_retries", args[0].retries)
            
            while retry_number < args[0].retries:
                try:
                    # Log retry attempt if not the first attempt
                    if retry_number > 0:
                        # Log using traditional logger
                        logger.info(f"Trying for the {retry_number} of {Constants.MAX_OF_RETRIES} retries. Using {args[0].retry_strategy}")
                        
                        # Log using OpenTelemetry
                        telemetry.logs().new_log(
                            msg=f"Retry attempt {retry_number} of {args[0].retries}",
                            tags={
                                "endpoint": endpoint,
                                "retry_number": retry_number,
                                "max_retries": args[0].retries,
                                "retry_strategy": args[0].retry_strategy.name,
                                "component": "RetryStrategy"
                            },
                            level=20  # INFO level
                        )
                        
                        # Record retry metric
                        telemetry.metrics().metric_increment(
                            name="api.request.retry",
                            tags={
                                "endpoint": endpoint,
                                "retry_strategy": args[0].retry_strategy.name
                            }
                        )
                        
                        # Update span with current retry count
                        span.set_attribute("current_retry", retry_number)
                    
                    # Execute the wrapped function
                    result = func(*args, **kwargs)
                    
                    # If we got here, it succeeded - record success metric after retries
                    if retry_number > 0:
                        telemetry.metrics().metric_increment(
                            name="api.request.retry.success",
                            tags={
                                "endpoint": endpoint,
                                "retry_count": retry_number,
                                "retry_strategy": args[0].retry_strategy.name
                            }
                        )
                        
                        telemetry.logs().new_log(
                            msg=f"Request succeeded after {retry_number} retries",
                            tags={
                                "endpoint": endpoint,
                                "retry_count": retry_number,
                                "retry_strategy": args[0].retry_strategy.name,
                                "component": "RetryStrategy"
                            },
                            level=20  # INFO level
                        )
                    
                    return result
                    
                except RequestException as e:
                    retry_number += 1
                    
                    # Record exception in the span
                    span.record_exception(e)
                    span.set_attribute("failed_attempt", retry_number)
                    
                    # Handle different retry strategies
                    if args[0].retry_strategy == Strategies.NO_RETRY_STRATEGY:
                        # Log failure with OpenTelemetry
                        telemetry.logs().new_log(
                            msg=f"Request failed with {type(e).__name__}, no retry strategy configured",
                            tags={
                                "endpoint": endpoint,
                                "error": str(e),
                                "error_type": type(e).__name__,
                                "component": "RetryStrategy"
                            },
                            level=40  # ERROR level
                        )
                        
                        # Record failure metric
                        telemetry.metrics().metric_increment(
                            name="api.request.failure",
                            tags={
                                "endpoint": endpoint,
                                "error_type": type(e).__name__,
                                "retry_strategy": "none"
                            }
                        )
                        
                        raise e
                        
                    # Apply delay based on strategy
                    if args[0].retry_strategy == Strategies.LINEAR_RETRY_STRATEGY:
                        delay = args[0].delay
                        strategy_name = "linear"
                    elif args[0].retry_strategy == Strategies.EXPONENTIAL_RETRY_STRATEGY:
                        delay = args[0].delay * retry_number
                        strategy_name = "exponential"
                    
                    # Log retry delay
                    telemetry.logs().new_log(
                        msg=f"Request failed, retrying in {delay}s (strategy: {strategy_name})",
                        tags={
                            "endpoint": endpoint,
                            "retry_count": retry_number,
                            "delay": delay,
                            "strategy": strategy_name,
                            "error": str(e),
                            "error_type": type(e).__name__,
                            "component": "RetryStrategy"
                        },
                        level=30  # WARNING level
                    )
                    
                    # Record the delay time in metrics
                    telemetry.metrics().record_gauge(
                        name="api.retry.delay",
                        tags={
                            "endpoint": endpoint,
                            "retry_count": retry_number,
                            "strategy": strategy_name
                        },
                        value=float(delay)
                    )
                    
                    # Sleep for the calculated delay
                    time.sleep(delay)
                    
                    # Check if we've reached max retries
                    if retry_number in (args[0].retries, Constants.MAX_OF_RETRIES):
                        # Log final failure
                        error_msg = f"Failed after {retry_number} retries"
                        logger.error(error_msg)
                        
                        telemetry.logs().new_log(
                            msg=error_msg,
                            tags={
                                "endpoint": endpoint,
                                "retry_count": retry_number,
                                "max_retries": args[0].retries,
                                "error": str(e),
                                "error_type": type(e).__name__,
                                "component": "RetryStrategy"
                            },
                            level=40  # ERROR level
                        )
                        
                        # Record final failure metric
                        telemetry.metrics().metric_increment(
                            name="api.request.retry.exhausted",
                            tags={
                                "endpoint": endpoint,
                                "retry_strategy": args[0].retry_strategy.name,
                                "error_type": type(e).__name__
                            }
                        )
                        
                        raise e

    return wrapper
