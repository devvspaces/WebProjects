from django.http import JsonResponse

class Verajax(object):
	def form_invalid(self,form):
		response=super(Verajax,self).form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response
	def form_valid(self,form):
		response=super(Verajax,self).form_valid(form)
		if self.request.is_ajax():
			print(form.cleaned_data)
			data={
				'message': 'Your form is successfully recieved'
			}
			return JsonResponse(data)
		else:
			return response