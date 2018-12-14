from django.db import models

# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)

    def __str__(self):
        return str(self.user_name)


class Request(models.Model):
    TYPE_OF_PROCESS = (
        ('fibonacci', 'fibonacci'),
        ('wait', 'wait')
    )
    STATUS = (
        ('P', 'pending'),
        ('S', 'started'),
        ('F', 'finished')
    )
    type_of_process = models.CharField(max_length=20, choices=TYPE_OF_PROCESS)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    pid = models.IntegerField(default=-1)
    status = models.CharField(max_lenght=1, choices=STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '['+str(self.id)+'] ' + str(self.type_of_process)
