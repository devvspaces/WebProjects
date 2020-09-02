from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, FormView
from .models import TodoList, Publisher, Author, Book
from .forms import MyForm, TodoForm, UserUpdateProfile, UpdateUser, QAForm
from .mixins import Verajax
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from User.models import QA as QAModel

# Create your views here.
class Home(LoginRequiredMixin, ListView, FormView):
	template_name = 'Todo/index.html'
	model = TodoList
	context_object_name = 'todos'
	form_class = TodoForm
	message = ''

	def get_queryset(self):
		queryset = super(Home, self).get_queryset()
		queryset=queryset.filter(user=self.request.user)
		return queryset
	def handleAjax(self, context=None, data=None, status=200, redirectTo=''):
		if data is None:
			data = {}
		if context is None:
			context = {}
		if self.request.is_ajax():
			data['from'] = self.request.POST.get('from')
			# data['redirectTo'] = redirectTo
			return JsonResponse(data, status=status)
		else:
			messages.warning(self.request,data.get('data'))
			self.message = data.get('data')
			if redirectTo:
				return redirect(redirectTo)
			return render(self.request, self.template_name, {'todos': self.get_queryset(), 'message': data.get('data')})
	def post(self, request):
		req_from = request.POST.get('from')
		form = self.form_class(request.POST)
		if req_from == 'profile':
			new_post = request.POST.copy()
			form = UserUpdateProfile(request.POST, request.FILES, instance=request.user.profile)
			if new_post['name'] == '':
				new_post['name'] = request.user.name
			if new_post['email'] == '':
				new_post['email'] = request.user.email
			new_post['pk'] = str(request.user.pk)
			form2 = UpdateUser(new_post)
			if form.is_valid():
				d = form.save()
			else:
				error_text = 'Error encountered<br>'
				for i in form.errors:
					error_text+=form.errors[i].as_text()+'<br>'
				return self.handleAjax(data={'data':error_text}, redirectTo='home')
			if form2.is_valid():
				d = form2.save()
			else:
				error_text = 'Error encountered<br>'
				for i in form2.errors:
					error_text+=form2.errors[i].as_text()+'<br>'
				return self.handleAjax(data={'data':error_text}, redirectTo='home')
			return self.handleAjax(data={'data': 'Profile Updated'}, redirectTo='home')
		if request.POST.get('tid'):
			real_todo = get_object_or_404(TodoList, tid = request.POST.get('tid'))
		if form.is_valid():
			try:
				if real_todo.user  == request.user:
					if req_from == 'save':
						todo=form.save(commit=False)
						real_todo.category = todo.category
						real_todo.todo = todo.todo
						real_todo.save()
						return self.handleAjax(data={'data':"Todo saved"})
					if req_from == 'done':
						if real_todo.done:
							real_todo.done = False
							real_todo.save()
							return self.handleAjax(data={'data':"Todo undone"})
						real_todo.done = True
						real_todo.save()
						return self.handleAjax(data={'data':"Todo done"})
					if req_from == 'delete':
						real_todo.delete()
						return self.handleAjax(data={'data':"Todo deleted"})
				else:
					return handleAjax(data={'data':"Permission not allowed"})
			except UnboundLocalError:
				if req_from=='create':
					todo=form.save(commit=False)
					todo.user = request.user
					todo.save()
					data = {'data':"New todo created"}
					data['todo'] = todo.todo
					data['tid'] = todo.tid
					data['date'] = todo.time
					data['category'] = todo.category
					return self.handleAjax(data=data)
		else:
			return self.handleAjax(data=form.errors, status = 400)
		return render(request, self.template_name, {'todos': self.get_queryset()})

class QA(LoginRequiredMixin, ListView, FormView):
	template_name = 'Todo/qa.html'
	model = QAModel
	context_object_name = 'qas'
	form_class = QAForm
	def get_queryset(self):
		queryset = super(QA, self).get_queryset()
		queryset=queryset.filter(user=self.request.user)
		return queryset
	def handleAjax(self, context=None, data=None, status=200, redirectTo=''):
		if data is None:
			data = {}
		if context is None:
			context = {}
		if self.request.is_ajax():
			data['from'] = self.request.POST.get('from')
			# data['redirectTo'] = redirectTo
			return JsonResponse(data, status=status)
		else:
			messages.warning(self.request,data.get('data'))
			self.message = data.get('data')
			if redirectTo:
				return redirect(redirectTo)
			return render(self.request, self.template_name, {'todos': self.get_queryset(), 'message': data.get('data')})
	def post(self,request):
		new_post = request.POST.copy()
		new_post['user'] = request.user.pk
		form = self.form_class(new_post)
		req_from = new_post.get('from')
		pk = new_post.get('pk')
		if pk and pk != '-1':
			real_qa = get_object_or_404(QAModel, pk = pk)
			if new_post['question'] == '':
				new_post['question'] = real_qa.question
			if new_post['answer'] == '':
				new_post['answer'] = real_qa.answer
			form = self.form_class(new_post)
		if new_post.get('from') != 'edit':
			if form.is_valid():
				try:
					if real_qa:
						if req_from == 'save':
							qa=form.save()
							return self.handleAjax(data={'data':"QA updated"})
						if req_from == 'delete':
							real_qa.delete()
							return self.handleAjax(data={'data':"QA deleted"})
				except UnboundLocalError:
					qa=form.save()
					return self.handleAjax(data={'data':"QA created", 'pk': qa.pk})
			else:
				error_text = 'Error encountered<br><br>'
				for i in form.errors:
					error_text+=i.capitalize()+'<br>'+form.errors[i].as_text()+'<br><br>'
				return self.handleAjax(data={'data':error_text}, status = 400)
		return render(request, self.template_name, {'qas': self.get_queryset()})

class PublisherCreate(CreateView, ListView):
	template_name = 'Todo/formview.html'
	model = Publisher
	fields = ['name', 'address', 'city', 'state_province', 'country', 'website']
	success_url = '/pub/'
class AuthorCreate(CreateView, ListView):
	template_name = 'Todo/authorview.html'
	model = Author
	fields = ['salutation', 'name', 'email', 'headshot']
	success_url = '/author/'
class BookCreate(CreateView, ListView):
	template_name = 'Todo/bookview.html'
	model = Book
	fields = ['title', 'authors', 'publisher']
	success_url = '/book/'

decorators=[login_required]
@method_decorator(decorators, name='dispatch')
class Greeting(View):
	greeting='Good day, Dad'
	def get(self, request):
		print(dir(request.session))
		print(request.session.get('passed'))
		return HttpResponse(self.greeting)

class Calling(Greeting):
	greeting='Good day,People'
	def get(self, request):
		if not request.session.get('passed'):
			request.session['passed']=self.greeting
			# request.session.save()
			print('ran')
		return HttpResponse(self.greeting)

@method_decorator(login_required, name='post')
class ShowForm(View):
	form_class = MyForm
	template_name = 'Todo/formview.html'
	initial = {'email': 'netrobeweb@gmail.com', 'comments': 'This is my new comment'}
	def get(self, request):
		form = self.form_class(initial=self.initial)
		return render(request, self.template_name, {'form':form})
	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			print(request.POST)
			return redirect('comments')
		else:
			print('Error found')
		return render(request, self.template_name, {'form':form})
	# @method_decorator(login_required)
	# def dispatch(self, *args, **kwargs):
	# 	return super(ShowForm, self).dispatch(*args, **kwargs)

