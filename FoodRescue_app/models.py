from django.db import models

# Create your models here.
from django.db import models

class Register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


    role = models.CharField(
    max_length=20,
    choices=[
        ('hotel', 'Hotel'),
        ('customer', 'Customer'),
        ('delivery', 'Delivery Partner'),
    ],
    default='customer'
)


    def __str__(self):
        return self.name

    

class Food(models.Model):
    hotel = models.ForeignKey(
        Register,
        on_delete=models.CASCADE,
        related_name='foods',
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_time = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='food_images/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Order(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    delivery_partner = models.ForeignKey(
        Register,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries'
    )

    def __str__(self):
        return self.customer_name
