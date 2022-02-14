from datetime import datetime
from common.constants.settings import EMPTY


class ValidationService:
    @staticmethod
    def validate_date(date: str):
        try:
            parse_date = datetime.strptime(date, '%d/%m/%Y')
            return True
        except ValueError as exc:
            return False

    @staticmethod
    def validate_not_empty(string: str):
        return string != EMPTY

    @staticmethod
    def validate_not_null(value):
        return value is not None

    @staticmethod
    def validate_max_lenght(string: str, max_lenght):
        if len(string) > max_lenght:
            return False
        return True

    @staticmethod
    def validate_min_lenght(string: str, min_lenght):
        if len(string) < min_lenght:
            return False
        return True

    @staticmethod
    def validate_minimum(number_input, minimum):
        if number_input < minimum:
            return False
        return True

    @staticmethod
    def validate_maximum(number_input, maximum):
        if number_input > maximum:
            return False
        return True

    @staticmethod
    def validate_phone(phone):
        return True

    @staticmethod
    def validate_credit_card(credit_card_number):
        return True
