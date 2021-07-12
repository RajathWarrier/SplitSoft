from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=30)
    total_expense = models.FloatField()

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class User(models.Model):
    fName = models.CharField(max_length=20)
    lName = models.CharField(max_length=20)
    groups = models.ManyToManyField(Group)

    class Meta:
        ordering = ['fName']
    def __str__(self):
        return self.fName + " " + self.lName

class Owe(models.Model):
    amount = models.FloatField()
    group = models.ForeignKey(Group, on_delete=CASCADE, null=True)
    who = models.ForeignKey(User, related_name='who_owes', on_delete=CASCADE)
    whom = models.ForeignKey(User, related_name='owe_whom', on_delete=CASCADE)
    def __str__(self):
        return self.who.fName + " owes " + self.whom.fName + " $" + str(self.amount)

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    group = models.ForeignKey(Group, on_delete=CASCADE)
    payer = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name + " ($" + str(self.amount) + ")"
