from django.db import models

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('very_happy', 'Very Happy'),
        ('happy', 'Happy'),
        ('neutral', 'Neutral'),
        ('stressed', 'Stressed'),
        ('sad', 'Sad'),
        ('very_sad', 'Very Sad')
    ]

    date = models.DateField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.mood}"

# Create your models here.
