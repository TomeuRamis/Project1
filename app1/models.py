from django.db import models

# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=128, default=None)  # Is it secure?

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
    date_of_start = models.DateTimeField(auto_now_add=False)
    date_of_finish = models.DateTimeField(auto_now_add=False)
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '[' + str(self.id) + '] type:' + str(self.type_of_process) + ', topology: ' +str(self.topology) +\
               ', by: ' + str(self.user) + ', time: ' + str(self.time)
