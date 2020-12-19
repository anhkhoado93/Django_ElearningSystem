from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Office'),
        (2, 'Department'),
        (3, 'Lecturer'),
        (4, 'Student'),
        (5, 'Admin'),
    )
    user_id = models.DecimalField(max_digits=7,decimal_places=0,unique=True,default=Decimal(0000000))
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)