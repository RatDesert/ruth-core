from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """ Custom User model manager. """

    def create_user(self, **kwargs):
        """ Parameters
            ----------
            **kwargs
                Keyword arguments that corresponds to User model fields

            Returns
            -------
            object

        """
        email, password = kwargs.get('email'), kwargs.get('password')
        if not email:
            raise ValueError('The Email must be set')
        if not password:
            raise ValueError('The password must be set')

        email = self.normalize_email(email)
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, **kwargs):
        is_superuser, is_staff = kwargs.get('is_superuser', False), kwargs.get('is_staff', False)
        if not is_superuser:
            raise ValueError('The Email must be set')
        if not is_staff:
            raise ValueError('The password must be set')

        return self.create_user(**kwargs)