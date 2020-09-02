from django.urls import path
from .views import Home, Greeting, Calling, ShowForm, PublisherCreate, AuthorCreate, BookCreate, QA

urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('qa/', QA.as_view(), name='qa'),
	path('greet/', Greeting.as_view()),
	path('call/', Calling.as_view()),
	path('kill/', Calling.as_view(greeting='Killed ya all')),
	path('comment/', ShowForm.as_view(), name='comments'),
	path('pub/', PublisherCreate.as_view(), name='pub'),
	path('author/', AuthorCreate.as_view(), name='author'),
	path('book/', BookCreate.as_view(), name='book'),
]