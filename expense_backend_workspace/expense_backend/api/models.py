from django.db import models
from django.contrib.auth.models import User


# PUBLIC_INTERFACE
class Category(models.Model):
    """Expense category for user-defined grouping."""

    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


# PUBLIC_INTERFACE
class Expense(models.Model):
    """Expense record with category and user association."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name='expenses'
    )
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Trimmed for line length
        return f"{self.user.username}: {self.amount} on {self.date}"
