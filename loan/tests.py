import uuid

# from django.core.mail import send_mail
from django.test import TestCase

from quick_loan_manager.loan.emails import send_email

# Create your tests here.
send_email("Hey", "dorothyvic24@gmail.com", "Dorothy", "Test")