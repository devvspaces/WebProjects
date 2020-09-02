from django.db import models
from django.db.models.signals import pre_save
from django.db import models
from django.utils import timezone
from .utils import create_tid


# Create your models here.
class TodoList(models.Model):
	CATEGORY = (
		('LT', 'Long Term',),
		('ST', 'Short Term',),
	)
	user = models.ForeignKey('User.User', on_delete=models.CASCADE)
	todo = models.TextField()
	time = models.DateField(default=timezone.now)
	done = models.BooleanField(default=False)
	tid = models.CharField(max_length=255, blank = True)
	category = models.CharField(choices=CATEGORY, max_length=2)

	def __str__(self):
		return f'TodoList {self.todo[0:20]}'
	class  Meta:
		ordering = ['-time']
			

class Publisher(models.Model):
	name = models.CharField(max_length=30, default='John Doe')
	address = models.CharField(max_length=50, default='Nalla jaguar')
	city = models.CharField(max_length=60, default='Toronto')
	state_province = models.CharField(max_length=30, default='Vancouver')
	country = models.CharField(max_length=50, default='USA')
	website = models.URLField(default='https://www.google.com')

	class Meta:
		ordering = ['-name']

	def __str__(self):
		return self.name.capitalize()

class Author(models.Model):
	salutation = models.CharField(max_length=10, default='Mr')
	name = models.CharField(max_length=200, default='John Doe')
	email = models.EmailField(default='johnnydoe@gmail.com')
	headshot = models.ImageField(upload_to = 'author_headshots')
	def __str__(self):
		return self.name.capitalize()
		

class Book(models.Model):
	title = models.CharField(max_length=100)
	authors = models.ManyToManyField('Author')
	publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
	publisher_date = models.DateField(auto_now_add=True)
	def __str__(self):
		return self.title.capitalize()


def pre_save_link(sender, instance, *args, **kwargs):
	if len(instance.tid)==0:
		instance.tid = create_tid(instance)
	instance.todo=instance.todo.replace('<div>','<br>').replace('</div>','').replace('</span>','').replace('</span>','')

pre_save.connect(pre_save_link, TodoList)