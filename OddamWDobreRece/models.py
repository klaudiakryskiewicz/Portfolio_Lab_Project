from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=120)


class Institution(models.Model):

    class Types(models.TextChoices):
        foundation = 1, _('Foundation')
        non_gov = 2, _('Non-governmental organization')
        local_col = 3, _('Local collection')

    name = models.CharField(max_length=120)
    description = models.TextField()
    year_in_school = models.IntegerField(
        choices=Types.choices,
        default=Types.foundation,
    )
    categories = models.ManyToManyField(Category)

class Donation(models.Model):

    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=120) # ulica + nr domu, czy to powinien być inny typ?
    phone_number = models.PositiveIntegerField(validators=[MaxValueValidator(999999999)])
    city = models.CharField(max_length=60)
    zip_code = models.IntegerField(validators=[MaxValueValidator(99999)])
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)