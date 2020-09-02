from .models import Profile, User, QA
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .utils import crypt, get_key, create_user_key

@receiver(post_save, sender=User)
def create_profile(sender, instance,created,**kwargs ):
	if created:
		Profile.objects.create(user=instance)
		
@receiver(post_save, sender=User)
def save_profile(sender, instance,**kwargs ):
	instance.profile.save()

@receiver(pre_save, sender=QA)
def pre_save_qa(sender, instance, *args, **kwargs):
    instance.question = instance.question.lower()
    instance.answer = instance.answer.lower()

@receiver(post_save, sender=Profile)
def post_save_profile(sender, instance, *args, **kwargs):
	print('IIIII')
	if not instance.user_key:
		instance.user_key = crypt(get_key('TODOAPP_KEY'),message=create_user_key(instance))
		instance.save()

# def post_save_user(sender, instance, *args, **kwargs):
#     try:
#         instance.profile
#     if not instance.profile:
#         print(instance)
#         instance.profile = Profile(user=instance)
#         instance.save()

# post_save.connect(post_save_user, User)