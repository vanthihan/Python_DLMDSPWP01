class DataException:
    """Custom exception for dataset handler"""
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"[DataException] {self.message}"


class FileNotFoundException:
    """Custom exception for missing files"""
    
    def __init__(self, filepath):
        self.filepath = filepath

    def __str__(self):
        return f"[FileNotFoundException] File not found: {self.filepath}"

class VisualizationException:
    """Custom exception for visualization errors"""
    
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return f"[VisualizationException] {self.error_message}"
