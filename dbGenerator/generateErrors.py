from business.services.genericService import GenericService
from common.exceptions.notValidOrderException import NotValidOrderException
from common.exceptions.notUniqueException import NotUniqueException
from common.exceptions.notValidInputException import NotVaildInputException
from common.constants.enums import Field, Reason, RequiredField


class GenerateErrors:
    @staticmethod
    def get_add_country_error(exception):
        root = GenericService.get_root_exception(exception)
        if isinstance(root, NotUniqueException):
            return Exception('Country rejected because country name already exist in system')
        else:
            return Exception('Country Error, for details contact administrator')

    @staticmethod
    def get_add_administrator(exception):
        root = GenericService.get_root_exception(exception)
        if isinstance(root, NotUniqueException):
            if root.field_name == Field.USER_NAME:
                return Exception('Administrator rejected because administrator-username already exist in system')
            else:
                return Exception('Administrator rejected because administrator already exist in system')
        else:
            return Exception('Administrator Error, for details contact administrator')

    @staticmethod
    def get_add_airline_error(exception):
        root = GenericService.get_root_exception(exception)
        if isinstance(root, NotUniqueException):
            if root.field_name == Field.AIRLINE_COMPANY_NAME:
                return Exception('Airline Company rejected because airline name already exist in system')
            if root.field_name == Field.USER_NAME:
                return Exception('Airline Company rejected because airline-username already exist in system')
            else:
                return Exception('Airline Company rejected because airline already exist in system')
        else:
            return Exception('Airline Company Error, for details contact administrator')

    @staticmethod
    def get_add_flight_error(exception):
        return Exception('flight Error, for details contact administrator')

    @staticmethod
    def get_add_customer_error(exception):
        root = GenericService.get_root_exception(exception)
        if isinstance(root, NotUniqueException):
            if root.field_name == Field.USER_NAME:
                return Exception('Customer rejected because customer-username already exist in system')
            else:
                return Exception('Customer rejected because customer already exist in system')
        else:
            return Exception('Customer Error, for details contact administrator')

    @staticmethod
    def get_add_ticket_error(exception):
        root = GenericService.get_root_exception(exception)
        if isinstance(root, NotValidOrderException):
            return Exception('ticket rejected because all flights avaliable to customer have been sold out.'
                'attention :  flights might be not available bacause they have already departured for current time, or'
                'because they are overlapping with customer other registered flights')
        else:
            return Exception('ticket Error, for details contact administrator')