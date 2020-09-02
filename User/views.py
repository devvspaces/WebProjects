import random
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect,get_object_or_404
from django.utils.encoding import force_text,force_bytes
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.views.generic import FormView
from .forms import ChangePassword,RegisterForm,LoginForm, ChangeForm
from .models import User, QA
from .mixins import HandleAjaxMixin
from .utils import crypt, get_key

# from .tokens import acount_confirm_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
acount_confirm_token = PasswordResetTokenGenerator()
# Create your views here.
# def activate_email(request, uidb64, token):
# 	try:
# 		uid=force_text(urlsafe_base64_decode(uidb64))
# 		user=User.objects.get(pk=uid)
# 	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
# 		user=None
# 	if user!=None and acount_confirm_token.check_token(user,token):
# 		user.active=True
# 		user.confirmed_email=True
# 		user.save()
# 		login(request,user)
# 		messages.success(request,f'{user.name}, your account is now activated successfully, you can now shorten your links')
# 		return redirect('dash')
# 	else:
# 		return render(request, "Url/activation_error.html")


from django.http import JsonResponse
import time

# class Verajax(object):
# 	def form_invalid(self,form):
# 		response=super(Verajax,self).form_invalid(form)
# 		if self.request.is_ajax():
# 			return JsonResponse(form.errors, status=400)
# 		else:
# 			return response
# 	def form_valid(self,form):
# 		response=super(Verajax,self).form_valid(form)
# 		if self.request.is_ajax():
# 			print(form.cleaned_data)
# 			data={
# 				'message': 'Your form is successfully recieved'
# 			}
# 			return JsonResponse(data)
# 		else:
# 			return response

def handleAjax(request, context=None, data=None, message='', parent='', status=200, redirectTo=''):
	if data is None:
		data = {}
	if context is None:
		context = {}
	if request.is_ajax():
		data['from'] = parent
		data['message'] = message
		data['redirectTo'] = redirectTo
		return JsonResponse(data, status=status)
	else:
		messages.warning(request,message)
		if redirectTo:
			return redirect(redirectTo)
		return render(request, "User/authentication.html", context)


def Authentication(request, type):
	if request.user.is_authenticated:
		return handleAjax(request, redirectTo='home')
	ajaxdiff=request.POST.get('form')
	if ajaxdiff == 'login':
		if request.method=="POST":
			form=LoginForm(request.POST)
			context={
				"title": "Create an account",
				"type": type
			}
			if form.is_valid():
				context['form']=form
				email=form.cleaned_data.get("email")
				password=form.cleaned_data.get("password")
				user=authenticate(request, username=email, password=password)
				if user.is_active:
					login(request, user)
					return handleAjax(request, context=context,
						message='You have been successfully logged in, you will be redirected home in few seconds', parent='login',
							redirectTo=reverse('home'))
				else:
					# return render(request, "Url/activate_email.html")
					return handleAjax(request, context=context,
						message='You have to activate your account in your email', parent='login', status=400)
			else:
				context['form']=form
				return handleAjax(request, data=form.errors,
					message='Error encountered during verification', parent='login', status=400)
	elif ajaxdiff == 'register':
		if request.method=="POST":
			form=RegisterForm(request.POST)
			form.is_valid()
			context={
				"title": "Create an account",
				"type": type
			}
			if form.is_valid():
				context['form']=form
				user=form.save(commit=True)
				# user.active=True
				# site=get_current_site(request)
				# uid=urlsafe_base64_encode(force_bytes(user.pk))
				# token=acount_confirm_token.make_token(user)
				# subject="{user.name} UrlShortener Account"
				# message=render_to_string("Url/activation_email.html",{
				# 	"user": user,
				# 	"uid": uid,
				# 	"token": token,
				# 	"domail": site.domain
				# })
				# sent=user.email_user(subject,message)
				return handleAjax(request, context=context, 
					message=f'''Account has been created {user.name}
					 successfully, click on the activation link sent to 
					 {user.email} to activate your account, you will be redirected to login in few seconds''',
					parent='signup',
					redirectTo=reverse('authentication', kwargs={'type':'login'}))
			else:
				context['form']=form
				return handleAjax(request, data=form.errors, message='Error encountered, Account has not been created', parent='signup', status=400)
	if type=='register':
		context={
			"title": "Create an account",
			"type": type
		}
		return render(request, "User/authentication.html", context)
	elif type=='login':
		context={
			'title': 'Login',
			"type": type
		}
		return render(request, "User/authentication.html", context)
	else:
		context={
			'title': '404 Page'
		}
		return render(request, "Todo/404.html", context)
def Logout(request):
	logout(request)
	return redirect(reverse('authentication', kwargs={'type':'login'}))

class ChangePasswordView(HandleAjaxMixin,FormView):
	model = User
	template_name = 'User/verification.html'
	form_class = ChangeForm
	def post(self,request):
		new_post = request.POST.copy()
		form = self.form_class(new_post)
		req_from = new_post.get('from')
		if req_from == 'qas':
			user = get_object_or_404(User, email=crypt(get_key('TODOAPP_KEY')
				,encrypted=request.session.get('qa_email')))
			# if not user:
			# 	return self.handleAjax(data={'data':"Email is unaccepted"}) 
			for a,b in request.session.items():
				if a.startswith('qx'):
					# Getting questions from session store and verifying with answer from post
					question = crypt(
						crypt(get_key('TODOAPP_KEY'), encrypted=user.profile.user_key),
						encrypted = b)
					qxx = get_object_or_404(QA, question = question)
					answer = new_post.get(a).lower()
					if qxx.answer != answer:
						return self.handleAjax(data={'data':"Verification failed"}, redirectTo=reverse('change-password'), status=400)
			uid=urlsafe_base64_encode(force_bytes(user.pk))
			token=acount_confirm_token.make_token(user=user)
			link = reverse('password_reset_confirm',
				kwargs={'uidb64':uid,
				'token':token})
			return self.handleAjax(data={'data':"Verification successful"}, redirectTo=link)
		
		if form.is_valid():
			if req_from == 'qa_email':
				# Analyse data for qa to send through ajax
				user = User.objects.get(email=new_post.get('email'))
				qas = random.sample(list(QA.objects.filter(user = user)), 2)
				data = {'data':"Email Verified"}
				data['questions'] = {'qx'+str(n):i for n,i in enumerate([i.question for i in qas])}
				request.session['qa_email'] = crypt(get_key('TODOAPP_KEY'),
					message = new_post.get('email'))
				# request.session['qa_email'] = new_post.get('email')
				for n,i in data['questions'].items():
					request.session[n] = crypt(crypt(get_key('TODOAPP_KEY'),
						encrypted=user.profile.user_key),
						message = i)
				return self.handleAjax(data=data)
			if req_from == 'link':
				return self.handleAjax(data={'data':"Email Verified"})
				# Sending password verification link here
		else:
			error_text = 'Error encountered<br><br>'
			for i in form.errors:
				error_text+=i.capitalize()+'<br>'+form.errors[i].as_text()+'<br><br>'
			return self.handleAjax(data={'data':error_text}, status = 400)
		return render(request, self.template_name, {'qas': self.get_queryset()})

class ResetPasswordView(LoginRequiredMixin,HandleAjaxMixin,FormView):
	model = User
	template_name = 'User/verification.html'
	form_class = ChangeForm
	def post(self,request):
		new_post = request.POST.copy()
		form = self.form_class(new_post)
		req_from = new_post.get('from')
		if req_from == 'qas':
			user = get_object_or_404(User, email=crypt(get_key('TODOAPP_KEY')
				,encrypted=request.session.get('qa_email')))
			# if not user:
			# 	return self.handleAjax(data={'data':"Email is unaccepted"}) 
			for a,b in request.session.items():
				if a.startswith('qx'):
					# Getting questions from session store and verifying with answer from post
					question = crypt(
						crypt(get_key('TODOAPP_KEY'), encrypted=user.profile.user_key),
						encrypted = b)
					qxx = get_object_or_404(QA, question = question)
					answer = new_post.get(a).lower()
					if qxx.answer != answer:
						return self.handleAjax(data={'data':"Verification failed"}, status=400)
			return self.handleAjax(data={'data':"Verification successful"})
		
		if form.is_valid():
			if req_from == 'qa_email':
				# Analyse data for qa to send through ajax
				user = User.objects.get(email=new_post.get('email'))
				qas = random.sample(list(QA.objects.filter(user = user)), 2)
				data = {'data':"Email Verified"}
				data['questions'] = {'qx'+str(n):i for n,i in enumerate([i.question for i in qas])}
				request.session['qa_email'] = crypt(get_key('TODOAPP_KEY'),
					message = new_post.get('email'))
				# request.session['qa_email'] = new_post.get('email')
				for n,i in data['questions'].items():
					request.session[n] = crypt(crypt(get_key('TODOAPP_KEY'),
						encrypted=user.profile.user_key),
						message = i)
				return self.handleAjax(data=data)
			if req_from == 'link':
				return self.handleAjax(data={'data':"Email Verified"})
				# Sending password verification link here
		else:
			error_text = 'Error encountered<br><br>'
			for i in form.errors:
				error_text+=i.capitalize()+'<br>'+form.errors[i].as_text()+'<br><br>'
			return self.handleAjax(data={'data':error_text}, status = 400)
		return render(request, self.template_name, {'qas': self.get_queryset()})

# @login_required
	# def resetPass(request):
	# 	form=ChangePassword()
	# 	if request.method=="POST":
	# 		form=ChangePassword(request.POST)
	# 		if form.is_valid():
	# 			#Checking if old password is correct
	# 			password=form.cleaned_data.get("password_old")
	# 			user=request.user
	# 			if user.check_password(password):
	# 				#Setting new password now
	# 				new_password=form.cleaned_data.get("password1")
	# 				user.set_password(new_password)
	# 				messages.success("Your password is now successfully changed")
	# 				return redirect("profile")
	# 			else:
	# 				messages.warning("Your Old password is incorrect, you can reset your password with the link below change password form")
	# 	context={
	# 		"form": form
	# 	}
	# 	return render(request,"Url/change_password.html", context)