class DataException(Exception):
    """Custom exception for dataset handler"""
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"[DataException] {self.message}"
