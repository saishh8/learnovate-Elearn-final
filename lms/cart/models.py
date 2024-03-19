from django.db import models
from accounts.models import User
from courses.models import Course

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(course.price for course in self.courses.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='course_thumbnails')

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order-{self.pk} ({self.user.username})"