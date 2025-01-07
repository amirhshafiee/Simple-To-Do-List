from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **kwargs):
        if not email:
            raise ValueError('Email must be set ...')
        
        email = self.normalize_email(email)
        user = self.model(email= email, username= username, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password, **kwargs):
        user = self.create_user(email, username, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        return user


