
class UserDetails:
    def __init__(self, token, identity):
        self.user_role_id = token.user_role_id
        self.token = token
        self.identity = identity

    @property
    def serialize(self):
        data = {'token': self.token,
                'identity': self.identity,
                'user_role_id': self.user_role_id
        }
        return data
