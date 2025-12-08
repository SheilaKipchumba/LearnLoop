from django.db import models
from django.contrib.auth.models import User
from loops.models import Loop

class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    loop = models.ForeignKey(Loop, on_delete=models.CASCADE, related_name='payments')
    phone_number = models.CharField(max_length=15)
    amount = models.PositiveIntegerField()
    
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.loop.title} - {self.status}"
