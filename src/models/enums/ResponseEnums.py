from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "File Type not Supported"
    FILE_SIZE_EXCEEDED = "File Size Exceeded"
    FILE_UPLOADED_SUCCESSFULLY = "File Uploaded Successfully"
    FILE_UPLOAD_FAIL = "File Upload Failed"
    PROCESSING_FAILED = "Processing Failed"
    PROCESSING_SUCCEEDED = "processing Succeeded"
