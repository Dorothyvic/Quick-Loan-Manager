import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', blank=True, null=True, unique=True)
    username = None
    is_staff = models.BooleanField(default=False)
    is_contact = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Business(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True, max_length=200)
    phone = models.CharField(null=True, blank=True, max_length=20)
    address = models.CharField(null=True, blank=True, max_length=50)


class Customers(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    gender = models.CharField(null=True, blank=True, max_length=10)
    phone = models.CharField(null=True, blank=True, max_length=50)
    email = models.EmailField(null=True, blank=True, max_length=200)
    place_of_work = models.CharField(null=True, blank=True, max_length=200)
    next_of_kin = models.CharField(null=True, blank=True, max_length=200)


class LoanRequests(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('disbursed', 'disbursed'),
        ('paid', 'paid'),
        ('cancelled', 'cancelled')
    )

    customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    amount_requested = models.IntegerField()
    interest_rate = models.FloatField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    approved_amount = models.FloatField(null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, null=True, blank=True, max_length=200)


class SupportingDocuments(models.Model):
    loan_request = models.ForeignKey(LoanRequests, on_delete=models.CASCADE)
    title = models.CharField(null=True, blank=True, max_length=100)
    file = models.FileField(upload_to='loan documents')
    description = models.CharField(null=True, blank=True, max_length=200)
    uploaded_date = models.DateField()
    value = models.CharField(null=True, blank=True, max_length=100)


class Transactions(models.Model):
    TRANSACTION_TYPE = (
        ('disbursed', 'disbursed'),
        ('payback', 'payback'),
    )
    CHANEL_TYPE = (
        ('cash', 'cash'),
        ('mobile_money', 'mobile_money'),
        ('bank', 'bank'),
    )
    loan_request = models.ForeignKey(LoanRequests, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, null=True, blank=True, max_length=200)
    amount = models.FloatField()
    chanel = models.CharField(choices=CHANEL_TYPE, null=True, blank=True, max_length=200)
    date = models.DateField(auto_now_add=True)