from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from .utils import create_user_key, crypt, get_key


class UserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, is_active=True, is_staff=False,
                    is_admin=False):
        if not email:
            raise ValueError("User must provide an email")
        if not name:
            raise ValueError("User must provide a name")
        if not password:
            raise ValueError("User must provide a password")

        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.active = is_active
        user.admin = is_admin
        user.staff = is_staff
        user.save(using=self._db)
        return user

    def create_staff(self, email, name=None, password=None):
        user = self.create_user(email=email, name=name, password=password, is_staff=True)
        return user

    def create_superuser(self, email, name=None, password=None):
        user = self.create_user(email=email, name=name, password=password, is_staff=True,
                                is_admin=True)
        return user

    def get_staffs(self):
        return self.filter(staff=True)

    def get_admins(self):
        return self.filter(admin=True)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    confirmed_email = models.BooleanField(default=False)

    REQUIRED_FIELDS = ["name"]
    USERNAME_FIELD = "email"

    objects = UserManager()

    @property
    def named(self):
        return self.name.capitalize()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f'User {self.named}'

    def get_absolute_url(self):
        return reverse('authentication', args=['login'])

    def email_user(self, subject, message, fail=True):
        return send_mail(subject, message, "urlshortener@mail.co.uk", [self.email], fail)

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

class Profile(models.Model):
    image = models.ImageField(upload_to='profiles', default='profiles/profile.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_key = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'User {self.user.name}'

class QA(models.Model):
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    question = models.TextField(unique=True)
    answer = models.CharField(max_length=100)
    time = models.DateField(default=timezone.now)

    def __str__(self):
        return f'QA {self.question}'

