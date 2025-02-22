from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=False)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    is_teacher = models.BooleanField(default=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text='Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )

    def save(self, *args, **kwargs):
        """Ensure username is auto-generated if not provided."""
        if not self.username:
            base_username = self.email.split("@")[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        if not self.name:
            self.name = self.username
        super().save(*args, **kwargs)



class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.SET_NULL, null=True) 
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # for arrangement of order - is used to do order in decreasing order 
    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class AIResponse(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='ai_responses')
    response_text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']

class Quiz(models.Model):
    quiz_id = models.CharField(max_length=10, unique=True)
    topic = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_number = models.IntegerField()
    question_text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_answer = models.CharField(max_length=1)  # 'A', 'B', 'C', or 'D'
    explanation = models.TextField()