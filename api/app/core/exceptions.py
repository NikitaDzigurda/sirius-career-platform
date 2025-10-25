"""
Кастомные исключения приложения
"""
from fastapi import HTTPException, status


class SiriusCareerException(Exception):
    """Базовое исключение приложения"""
    pass


class UserNotFoundError(SiriusCareerException):
    """Пользователь не найден"""
    pass


class InvalidCredentialsError(SiriusCareerException):
    """Неверные учетные данные"""
    pass


class OTPExpiredError(SiriusCareerException):
    """OTP код истек"""
    pass


class OTPInvalidError(SiriusCareerException):
    """Неверный OTP код"""
    pass


class TestNotFoundError(SiriusCareerException):
    """Тест не найден"""
    pass


class CompanyNotFoundError(SiriusCareerException):
    """Компания не найдена"""
    pass


class VacancyNotFoundError(SiriusCareerException):
    """Вакансия не найдена"""
    pass


# Admin domain exceptions
class TestNotFoundException(SiriusCareerException):
    """Тест не найден"""
    pass


class TestSlugAlreadyExistsException(SiriusCareerException):
    """Тест с таким slug уже существует"""
    pass


class TestHasResultsException(SiriusCareerException):
    """Нельзя удалить тест, у которого есть результаты"""
    pass


class InvalidQuestionConfigException(SiriusCareerException):
    """Неверная конфигурация вопроса"""
    pass


class InvalidQuestionOrderException(SiriusCareerException):
    """Неверный порядок вопросов"""
    pass


# HTTP исключения
def raise_user_not_found():
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Пользователь не найден"
    )


def raise_invalid_credentials():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверные учетные данные"
    )


def raise_otp_expired():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="OTP код истек"
    )


def raise_otp_invalid():
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Неверный OTP код"
    )
