from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Sentence(models.Model):
    sen_text = models.TextField(max_length=100)
    def __str__(self):
        return self.sen_text