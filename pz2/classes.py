import hashlib
import datetime

class User:
    def __init__(self, username, password, is_active):
        self.username = username
        self._password_hash = self._hash_password(password)
        self.is_active = is_active
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self._password_hash == self._hash_password(password)
    

class Administrator(User):
    def __init__(self, username, password, is_active = True, permissions = None):
        super().__init__(username, password, is_active)
        if permissions is None:
            self.permissions = set()
        else:
            self.permissions = set(permissions)

    def has_permission(self, permission):
        return permission in self.permissions
            
    def grant_permission(self, permission):
        self.permissions.add(permission)
    
    def revoke_permission(self, permission):
        self.permissions.discard(permission)

    def __str__(self):
        return (f"Administrator '{self.username}', is_active={self.is_active}, permissions={list(self.permissions)})")
    

class RegularUser(User):
    def __init__(self, username, password, is_active, last_login_date = None):
        super().__init__(username, password, is_active)
        self.last_login_date = last_login_date

    def update_last_login(self):
        self.last_login_date = datetime.datetime.now()

    def __str__(self):
        return (f"RegularUser '{self.username}', is_active={self.is_active}, last_login='{self.last_login_date}')")

class GuestUser(User):
    def __init__(self):
        super().__init__(username = 'Guest', password = '', is_active = True)
        self.session_expires = datetime.datetime.now() + datetime.timedelta(hours=1)

    def verify_password(self, password):
        return False
    
    def is_session_active(self):
        return self.session_expires > datetime.datetime.now()
    
    def __str__(self):
        return (f"GuestUser, session_expires='{self.session_expires}'")
    

class AccessControl:
    def __init__(self, *users):
        self.users = {}
        for user in users:
            self.users[user.username] = user
        
    def add_user(self, user):
        if user.username not in self.users:
            self.users[user.username] = user
        else: print('The user already exists')

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password) and user.is_active:
            if isinstance(user, RegularUser):
                user.update_last_login()
            return user
        else: return None
