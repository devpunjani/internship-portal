from django.db import models

#Industry Model
class IndustryModel(models.Model):
    name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.name