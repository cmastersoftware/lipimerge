import traceback

class LipimergeException(Exception):
    """Base class for all exceptions raised by Lipimerge."""
    def __init__(self, message: str, errcode: int, details: list[str] = []):
        super().__init__(message)
        self.errcode = errcode
        self.details = details


class Success(LipimergeException):
    """
    Implements the LipimergeException interface for successful operations.

    Do **not** raise. This is technically not an exception but a success status descriptor.
    It is to be **returned** by functions on successful completion.
    """
    def __init__(self, message: str, details: list[str] = []):
        super().__init__(message, 0, details)


class InvalidArguments(LipimergeException):
    def __init__(self):
        super().__init__(
            "Invalid arguments.",
            -1,
            ["Use -h or --help for usage information."]
        )


class ExternalError(LipimergeException):
    """Holder for an error not caused by Lipimerge."""
    def __init__(self, exception):
        super().__init__(
            "External error.",
            1,
            traceback.format_exception(exception)
        )
        self.exception = exception


class InvalidCellIndex(LipimergeException):
    def __init__(self, function: str, icol: int, irow: int, max_col: int, max_row: int):
        super().__init__("Cell index out of range.", 2, details = [
            f"Function: {function}",
            f"Column index: {icol} (max: {max_col})",
            f"Row index: {irow} (max: {max_row})",
        ])
        self.function = function
        self.icol = icol
        self.irow = irow
        self.max_col = max_col
        self.max_row = max_row


class ConsistencyError(LipimergeException):
    def __init__(self, message: str, details: list[str] = []):
        super().__init__(message, 3, details)


class InvalidFile(LipimergeException):
    def __init__(self, message: str, filename: str, details: list[str] = []):
        super().__init__(message, 4, [f"File: {filename}"] + details)
        self.filename = filename
