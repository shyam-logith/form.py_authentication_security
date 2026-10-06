from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.EmailField()
    course = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.name

