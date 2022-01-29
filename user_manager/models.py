from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserProfileManager(BaseUserManager):
    """Manages the user profiles"""

    def create_user(self, email, fname, lname, dob, phone_number=None, password=None, profile_pic=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        if profile_pic:
            user = self.model(email=email, fname=fname, lname=lname,
                          dob=dob, phone_number=phone_number, profile_pic=profile_pic)
        else: 
            user = self.model(email=email, fname=fname, lname=lname,
                          dob=dob, phone_number=phone_number)                         
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, lname, dob, password, phone_number=None, profile_pic=None):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, fname, lname,
                                 dob,  phone_number, password, profile_pic)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Database models for users (Making a completely different user model)"""
    email = models.EmailField(max_length=255, unique=True)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    dob = models.DateField()
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/%Y/%m/%d', default='default/images/profile_pic.png')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'dob']

    def get_full_name(self):
        return self.fname + " " + self.lname

    def get_email(self):
        return self.email

    def get_dob(self):
        return self.dob

    def get_profile_pic(self):
        if self.profile_pic:
            return self.profile_pic
        else:
            return 'default/images/profile_pic.png'

    def __str__(self):
        return self.email


class OTP(models.Model):
    """
    Otp model for user. 
    This model is used to store the otp generated for the user.
    Otp should expire after 15 minutes of generation.
    """
    user = models.OneToOneField(
        User, related_name='otp', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.otp


class UserAddress(models.Model):
    user = models.ForeignKey(User,
                             related_name='addresses',
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.TextField(max_length=200)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200, default="India")
    address_type = models.CharField(max_length=20, choices=(
        ("Home", 'Home'), ("Work", 'Work'),
    ), default="Home")

    def __str__(self) -> str:
        return (self.postal_code + " : " + self.address[0:50])

    def get_long_description(self):
        return (self.postal_code + " : " + self.address[0:50])

    def fname(self):
        return (self.first_name + " " + self.last_name)

