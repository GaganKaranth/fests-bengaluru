from django.db import models
from django.db.models import CheckConstraint, Q, F

class College(models.Model):
    CITY_CHOICES=[('BAN','Bangalore')]
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    city=models.CharField(choices=CITY_CHOICES,default='BAN',max_length=10)
    fest_nos=models.IntegerField()
    image=models.ImageField(default='default.jpg',upload_to='college_pics')

    class Meta():
        db_table='college'

    def __str__(self):
        return self.name

class Organizer(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=25)
    phone=models.IntegerField()

    class Meta():
        db_table='organizer'

    def __str__(self):
        return self.name

class Fest(models.Model):
    FEST_CHOICES=[
        ('CUL','Cultural'),
        ('TEC','Technical'),
        ('COL','College'),
        ('SPO','Sports'),
    ]
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    clg_id=models.ForeignKey(College,on_delete=models.CASCADE)
    fest_type=models.CharField(choices=FEST_CHOICES,default='COL',max_length=10)
    fest_desc=models.TextField(default='This is a fest')
    start_date=models.DateField(default='2022-01-01')
    end_date=models.DateField(default='2022-02-01')
    event_nos=models.IntegerField()
    org_id=models.ManyToManyField(Organizer)
    image=models.ImageField(default='default.jpg',upload_to='fest_pics')
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(end_date__gte=F('start_date')), 
                name = 'check_start_date',
            )
        ]
        db_table='fest'

    def __str__(self):
        return self.name

class Event(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=25)
    fest_id=models.ForeignKey(Fest,on_delete=models.PROTECT)
    event_date=models.DateField(default='2022-01-01')
    event_time=models.TimeField(default='11:00')
    event_desc=models.TextField(default='This is an event')
    entry_fee=models.IntegerField()
    org_id=models.ForeignKey(Organizer,on_delete=models.PROTECT)

    class Meta():
        db_table='event'

    def __str__(self):
        return self.name

class Participated(models.Model):
    user=models.IntegerField()
    event=models.IntegerField()

    class Meta():
        db_table='participated'
