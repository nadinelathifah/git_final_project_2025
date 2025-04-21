class UserNotFoundError(Exception):
    def __init__(self, message="User does not exist. Please Sign Up to create a My Home Heroes account."):
        super().__init__(message)
