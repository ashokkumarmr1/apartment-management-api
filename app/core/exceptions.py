
class AppException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ):
        self.message = message
        self.status_code = status_code

class DuplicateEmailException(AppException):
    pass


class DuplicateMobileException(AppException):
    pass


class InvalidCredentialsException(AppException):
    pass


class RoleNotFoundException(AppException):
    pass


class UserNotFoundException(AppException):
    pass


class InvalidPasswordException(AppException):
    pass