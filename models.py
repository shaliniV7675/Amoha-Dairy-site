from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name
        from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=100)
    phone     = models.CharField(max_length=10)
    email     = models.EmailField(unique=True)
    password  = models.CharField(max_length=100)   # plain-text (no extra packages needed)

    def __str__(self):
        return self.email


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('processing', 'Processing'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_id     = models.CharField(max_length=30, unique=True)
    items        = models.JSONField()          # list of cart item dicts
    shipping     = models.JSONField()          # shipping address dict
    payment_method = models.CharField(max_length=30)
    items_total  = models.PositiveIntegerField(default=0)
    delivery_fee = models.PositiveIntegerField(default=0)
    discount     = models.PositiveIntegerField(default=0)
    grand_total  = models.PositiveIntegerField(default=0)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    placed_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-placed_at']

    def __str__(self):
        return f"{self.order_id} — {self.user.email}"

    
