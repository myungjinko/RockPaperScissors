from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_games(self):
        return self.wins + self.losses + self.draws

    @property
    def win_percentage(self):
        total = self.total_games()
        if total == 0:
            return 0
        return round((self.wins / total) * 100, 1)

    def __str__(self):
        return f"{self.name} ({self.win_percentage}%)"

    class Meta:
        ordering = ['name']
