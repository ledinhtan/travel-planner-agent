import sys

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Extract detailed error information including file name and line number.
    
    Args:
        error: The original exception
        error_detail: sys module to get traceback details
    
    Returns:
        Formatted error message
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    
    return f"Error occurred in file [{file_name}] at line [{line_number}]: {str(error)}"


class CustomException(Exception):
    """Custom exception that captures file name and line number."""
    
    def __init__(self, error_message: Exception, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
    
    def __str__(self) -> str:
        return self.error_message