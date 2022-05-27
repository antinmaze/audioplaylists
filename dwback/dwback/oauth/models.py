from django.db import models
from django.db.models import JSONField

# Create your models for oauth_session Table

class Session(models.Model):
    client_id = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    #token = models.CharField(max_length=1000)
    token = JSONField(null=True)
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        """Fonction requise par Django pour manipuler les objets Book dans la base de données."""
        return f'{self.id} ({self.state})'