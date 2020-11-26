from django.db import models


RATING_CHOICES = (
    ('5', '5 Star'),
    ('4', '4 Star'),
    ('3', '3 Star'),
    ('2', '2 Star'),
    ('1', '1 Star'),
)

COLOR_CHOICES = (
    ('Blue', 'Blue Color'),
    ('Green', 'Green Color'),
    ('Red', 'Red Color'),
    ('Yellow', 'Yellow Color'),
    ('Black', 'Black Color'),
)

class CommonField(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(CommonField):
	name = models.CharField(max_length=100, unique=True)

	def __str__(self):
		return str(self.name)


class Product(CommonField):
    name = models.CharField(max_length=100, blank=False)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, blank=True)
    price = models.DecimalField(default=1.00, max_digits=5, decimal_places=2)
    discount = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default=COLOR_CHOICES[0][0])

    def __str__(self):
        return "{0},{1}".format(self.name, self.price)