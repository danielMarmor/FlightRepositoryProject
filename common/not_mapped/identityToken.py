class IdentityToken:
    def __init__(self, user_name, user_role_id, identity_id):
        self.user_name = user_name
        self.user_role_id = user_role_id
        self.identity_id = identity_id

    def __eq__(self, other):
        return isinstance(other, IdentityToken) \
            and self.user_name == other.user_name \
            and self.user_role_id == other.user_role_id \
            and self.identity_id == other.identity_id

    def __str__(self):
        return f'<IdentityToken> user_name:{self.user_name}, user_role_id:{self.user_role_id} '\
               f'identity_id:{self.identity_id}'

    def __repr__(self):
        return f'<IdentityToken> user_name:{self.user_name}, user_role_id:{self.user_role_id} ' \
               f'identity_id:{self.identity_id}'

    @property
    def serialize(self):
        data = {'user_name': self.user_name,
                'user_role_id': self.user_role_id,
                'identity_id': self.identity_id}
        return data

