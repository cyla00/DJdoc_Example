from django.db import models

# Create your models here.
class Product(models.Model):

    CATEGORIES = (
    ('category 1', 'category 1'),
    ('category 2', 'category 2'),
    ('category 3', 'category 3'),
    ('category 4', 'category 4'),
    ('category 5', 'category 5'),
    )

    prod_title = models.CharField(max_length=200, null=True)
    prod_category = models.CharField(max_length=100, choices=CATEGORIES)
    prod_price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    prod_description = models.TextField(default='null', null=True)
    
    # def __str__(self):
    #     return self.prod_title