from common.entities.Customer import Customer
from common.entities.User import User
from common.exceptions.notValidInputException import NotVaildInputException
from common.constants.enums import Reason, Field, Entity, Actions, UserRoles
from business.services.validationService import ValidationService
from common.exceptions.notUniqueException import NotUniqueException
from common.exceptions.notFoundException import NotFoundException


class CustomerService:
    def __init__(self, local_session, repository):
        self.local_session = local_session
        self._repository = repository

    def validate_customer(self, customer):
        # is empty
        empty_first_name = not ValidationService.validate_not_empty(customer.first_name)
        if empty_first_name:
            raise NotVaildInputException('Must Enter Valid First Name', Reason.EMPTY, Field.CUSTOMER_FIRST_NAME)
        empty_last_name = not ValidationService.validate_not_empty(customer.last_name)
        if empty_last_name:
            raise NotVaildInputException('Must Enter Valid Last Name', Reason.EMPTY, Field.CUSTOMER_LAST_NAME)
        empty_address = not ValidationService.validate_not_empty(customer.address)
        if empty_address:
            raise NotVaildInputException('Must Enter Valid Adress', Reason.EMPTY, Field.CUSTOMER_ADDRESS_NAME)
        empty_phone = not ValidationService.validate_not_empty(customer.phone_number)
        if empty_phone:
            raise NotVaildInputException('Must Enter Valid Phone Number', Reason.EMPTY, Field.CUSTOMER_PHONE_NAME)
        empty_credit_card_number = not ValidationService.validate_not_empty(customer.credit_card_number)
        if empty_credit_card_number:
            raise NotVaildInputException('Must Enter Valid CreditCard', Reason.EMPTY, Field.CUSTOMER_CREDIT_CARD)

        # to_long not  valid
        first_name_too_long = not ValidationService.validate_max_lenght(customer.first_name, Customer.MAX_FIRST_NAME)
        if first_name_too_long:
            raise NotVaildInputException('First Name too long', Reason.TOO_LONG, Field.CUSTOMER_FIRST_NAME)
        last_name_too_long = not ValidationService.validate_max_lenght(customer.last_name, Customer.MAX_LAST_NAME)
        if last_name_too_long:
            raise NotVaildInputException('Last Name too long', Reason.TOO_LONG, Field.CUSTOMER_LAST_NAME)
        adress_too_long = not ValidationService.validate_max_lenght(customer.address, Customer.MAX_ADDRESS)
        if adress_too_long:
            raise NotVaildInputException('Address too long', Reason.TOO_LONG, Field.CUSTOMER_ADDRESS_NAME)
        phone_too_long = not ValidationService.validate_max_lenght(customer.phone_number, Customer.MAX_PHONE)
        if phone_too_long:
            raise NotVaildInputException('Phone too long', Reason.TOO_LONG, Field.CUSTOMER_PHONE_NAME)
        credit_card_too_long = not ValidationService.validate_max_lenght(customer.credit_card_number, Customer.MAX_CREDIT_CARD)
        if credit_card_too_long:
            raise NotVaildInputException('Credit Card too long', Reason.TOO_LONG, Field.CUSTOMER_CREDIT_CARD)

        # not formatted
        phone_not_formatted = not ValidationService.validate_phone(customer.phone_number)
        if phone_not_formatted:
            raise NotVaildInputException('Phone is Not Formatted Correctly', Reason.NOT_FORMATTED,
                                         Field.CUSTOMER_PHONE_NAME)
        credit_card_not_formatted = not ValidationService.validate_credit_card(customer.credit_card_number)
        if credit_card_not_formatted:
            raise NotVaildInputException('Credit Card is Not Formatted Correctly', Reason.NOT_FORMATTED,
                                         Field.CUSTOMER_CREDIT_CARD)
        # unique constraint
        customer_by_phone_cond = (lambda query: query.filter(Customer.phone_number == customer.phone_number,
                                                             Customer.id != customer.id))
        customer_by_phone = self._repository.get_all_by_condition(Customer, customer_by_phone_cond)
        if len(customer_by_phone) > 0:
            if customer.id is None:
                raise NotUniqueException('Phone Allready Exists',  Actions.ADD_CUSTOMER, Field.CUSTOMER_PHONE_NAME,
                                         customer.phone_number)
            else:
                raise NotUniqueException('Phone Allready Exists', Actions.UPDATE_CUSTOMER, Field.CUSTOMER_PHONE_NAME,
                                         customer.phone_number)

        customer_by_credit_card_cond = \
            (lambda query: query.filter(Customer.credit_card_number == customer.credit_card_number,
                                        Customer.id != customer.id))
        customer_by_credit_card = self._repository.get_all_by_condition(Customer, customer_by_credit_card_cond)
        if len(customer_by_credit_card) > 0:
            if customer.id is None:
                raise NotUniqueException('Credit-Card Allready Exist!', Actions.ADD_CUSTOMER,
                                         Field.CUSTOMER_CREDIT_CARD, customer.credit_card_number)
            else:
                raise NotUniqueException('Credit-Card Allready Exist!', Actions.UPDATE_CUSTOMER,
                                         Field.CUSTOMER_CREDIT_CARD, customer.credit_card_number)
        # CHECK USER ID ===> ONLY ON UPDATE
        if customer.id is not None:
            user_by_cust_user_id_cond = (lambda query: query.filter(User.id == customer.user_id))
            user_by_cust_user_id = self._repository.get_all_by_condition(User, user_by_cust_user_id_cond)
            if len(user_by_cust_user_id) == 0:
                raise NotFoundException('User Id Not Found!', Entity.USER, customer.user_id)

    def add_customer(self, customer, user):
        self._repository.add_customer(customer, user)

    # def add_customer(self, customer):
    #     self._repository.add(customer)

    def update_customer(self, customer_id, customer):
        customer_updated_data = {
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'address': customer.address,
            'phone_number': customer.phone_number,
            'credit_card_number': customer.credit_card_number
        }
        self._repository.update(Customer, 'id', customer_id, customer_updated_data)

    def remove_customer(self, customer_id):
        customer = self.get_customer_by_id(customer_id)
        if customer is None:
            raise NotFoundException('Customer Not Found', Entity.CUSTOMER, customer_id)
        self._repository.remove_customer(customer_id, customer.user_id)

    def get_all_customers(self):
        customers = self._repository.get_all(Customer)
        return customers

    def get_customer_by_id(self, customer_id):
        customer = self._repository.get_by_id(Customer, customer_id)
        return customer

    def get_flights_by_customer(self, customer_id):
        customer_flights = self._repository.get_flights_by_customer(customer_id)
        return customer_flights

    def get_customer_by_user_id(self, user_id):
        user_id_filter = (lambda query: query.filter(Customer.user_id == user_id))
        entries = self._repository.get_all_by_condition(Customer, user_id_filter)
        if len(entries) == 0:
            return None
        customer = entries[0]
        return customer

