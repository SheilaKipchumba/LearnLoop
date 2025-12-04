from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Loop(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Math', 'Mathematics'),
        ('Science', 'Science'),
        ('CS', 'Computer Science'),
        ('Business', 'Business'),
        ('Arts', 'Arts & Humanities'),
        ('Language', 'Languages'),
        ('Engineering', 'Engineering'),
        ('Medicine', 'Medicine'),
        ('Law', 'Law'),
        ('Other', 'Other'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_loops')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Beginner')
    
    # Media fields
    video_url = models.URLField(blank=True, null=True, help_text="Optional YouTube/Vimeo link")
    attachment = models.FileField(upload_to='loop_attachments/', blank=True, null=True)
    
    # Premium content
    is_premium = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    # Stats
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('loop_detail', kwargs={'pk': self.pk})
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loop = models.ForeignKey(Loop, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'loop']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} liked {self.loop.title}"


class Comment(models.Model):
    loop = models.ForeignKey(Loop, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.loop.title}"