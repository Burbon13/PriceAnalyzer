class TaskException(Exception):
    def __init__(self, message, errors=None):
        super(TaskException, self).__init__(message)