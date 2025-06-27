from fastapi import HTTPException, status

class UserAlreadyExists(HTTPException):
    def __init__(self, detail: str = "User with this email or username already exists."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Not authorized to perform this action."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

# Add more specific exceptions as needed