from werkzeug.security import generate_password_hash, check_password_hash


class User:

    is_active = True
    is_anonymous = False
    is_admin = False
    id = -1
    firstname = ""
    lastname = ""
    email = ""
    password = ""

    def __init__(self, id, firstname, lastname, email):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.id

