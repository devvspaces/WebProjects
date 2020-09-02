from django import forms
from .models import TodoList
from User.models import Profile, QA
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()
class MyForm(forms.Form):
	email = forms.CharField(max_length=10)
	comments = forms.CharField(max_length=100, widget=forms.Textarea())

class TodoForm(forms.ModelForm):
	class Meta:
		model = TodoList
		fields = ('category','todo',)
class QAForm(forms.Form):
	question = forms.CharField(widget=forms.Textarea())
	answer = forms.CharField(max_length=100)
	pk = forms.IntegerField()

	def clean(self):
		self.cleaned_data['question'] = self.data.get('question')
		self.cleaned_data['answer'] = self.data.get('answer')
		test_pk = self.data.get('pk')
		if test_pk:
			self.cleaned_data['pk'] = test_pk
		else:
			self.cleaned_data['pk'] = -1
		self.cleaned_data['user'] = self.data.get('user')
		return self.cleaned_data
	def get_qa_pk(self):
		self.clean()
		pk = self.cleaned_data.get('pk')
		return QA.objects.filter(pk = pk)
	def clean_question(self):
		qa = self.get_qa_pk()
		question = self.cleaned_data.get('question')
		qas=QA.objects.filter(question = question.lower()).exclude(pk=qa.first().pk if qa else None).exists()
		if qas:
			raise forms.ValidationError("Question already exists")
		return question
	def save(self, commit=True):
		qa = self.get_qa_pk().first()
		question = self.cleaned_data.get('question')
		answer = self.cleaned_data.get('answer')
		if not qa:
			user = get_object_or_404(User, pk = self.cleaned_data.get('user'))
			qa=QA(user=user, question=question, answer=answer)
		if commit:
			qa.question = question
			qa.answer = answer
			qa.save()
		return qa
class UserUpdateProfile(forms.ModelForm):
	class Meta:
		model=Profile
		fields=("image",)
class UpdateUser(forms.Form):
	name = forms.CharField(max_length=255)
	email = forms.EmailField()
	pk = forms.IntegerField()

	def clean(self):
		self.cleaned_data['name'] = self.data.get('name')
		self.cleaned_data['email'] = self.data.get('email')
		self.cleaned_data['pk'] = self.data.get('pk')
		return self.cleaned_data

	def get_user_pk(self):
		self.clean()
		pk = self.cleaned_data.get('pk')
		return User.objects.get(pk = pk)
	def clean_email(self):
		user = self.get_user_pk()
		email = self.cleaned_data.get('email')
		if user.email == email:
			return email
		else:
			users = User.objects.filter(email = email).exists()
			if users:
				raise forms.ValidationError("Email already exists")
		return email
	def clean_name(self):
		user = self.get_user_pk()
		name = self.cleaned_data.get('name')
		if user.name == name:
			return name
		else:
			users = User.objects.filter(name = name).exists()
			if users:
				raise forms.ValidationError("Name already exists")
		return name
	def save(self, commit=True):
		user = self.get_user_pk()
		email = self.cleaned_data.get('email')
		name = self.cleaned_data.get('name')
		if commit:
			user.email = email
			user.name = name
			user.save()
		return user
