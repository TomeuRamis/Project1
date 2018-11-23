from django.db import models

# Create your models here.

class Request(models.Model):
    TYPE_OF_PROCESS = (
        ('fib', 'fibonacci'),
        ('wait', 'wait30')
    )
    type_of_process = models.CharField(max_length=20, choices=TYPE_OF_PROCESS)
    date_of_creation = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.type_of_process + self.date_of_creation)
