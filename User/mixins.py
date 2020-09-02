from django.http import JsonResponse

class HandleAjaxMixin(object):
	def handleAjax(self, context=None, data=None, status=200, redirectTo=''):
		if data is None:
			data = {}
		if context is None:
			context = {}
		if self.request.is_ajax():
			data['from'] = self.request.POST.get('from')
			if redirectTo:
				data['redirectTo'] = redirectTo
			return JsonResponse(data, status=status)
		else:
			messages.warning(self.request,data.get('data'))
			self.message = data.get('data')
			if redirectTo:
				return redirect(redirectTo)
			return render(self.request, self.template_name, {'todos': self.get_queryset(), 'message': data.get('data')})