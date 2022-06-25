class RequestValidation:
    STRING = type('string')
    INTEGER = type(1)

    @staticmethod
    def validate_form(request, requested_values):
        if not request.form:
            return False
        for prop in [name_value for name_value in requested_values]:
            prop_name = prop[0]
            prop_type = prop[1]
            if prop_name not in request.form.keys():
                return False
            reuqest_value = request.form[prop_name]
            match prop_type:
                case RequestValidation.STRING:
                    continue
                case RequestValidation.INTEGER:
                    if not str(reuqest_value).isnumeric():
                        return False

        return True

    @staticmethod
    def validate_query(request, requested_values):
        if not request.args:
            return False
        for prop in [name_value for name_value in requested_values]:
            prop_name = prop[0]
            prop_type = prop[1]
            if prop_name not in request.args.keys():
                return False
            reuqest_value = request.args[prop_name]
            match prop_type:
                case RequestValidation.STRING:
                    continue
                case RequestValidation.INTEGER:
                    if not str(reuqest_value).isnumeric():
                        return False

    @staticmethod
    def validate_integer(value: str):
        is_number = value.isnumeric()
        return is_number

