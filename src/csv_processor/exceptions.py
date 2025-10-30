class CSVProcessorError(Exception):
    pass


class FileValidationError(CSVProcessorError):
    pass


class ReportNotFoundError(CSVProcessorError):
    pass


class InvalidCSVFormatError(CSVProcessorError):
    pass