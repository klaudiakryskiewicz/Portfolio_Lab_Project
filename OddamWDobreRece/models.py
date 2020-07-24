from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name}"


class Institution(models.Model):
    class Types(models.TextChoices):
        foundation = 1, _('Foundation')
        non_gov = 2, _('Non-governmental organization')
        local_col = 3, _('Local collection')

    name = models.CharField(max_length=120)
    description = models.TextField()
    type = models.IntegerField(
        choices=Types.choices,
        default=Types.foundation,
    )
    categories = models.ManyToManyField(Category)

    def no_of_helped(self):
        return Institution.objects.filter(donation__isnull=False).distinct().count()

    def __str__(self):
        return f"{self.name}"


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=12)
    city = models.CharField(max_length=60)
    zip_code = models.CharField(max_length=8)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    is_taken = models.BooleanField(default=False)
