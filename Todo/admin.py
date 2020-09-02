from django.contrib import admin
from .models import TodoList, Author, Publisher, Book

def doall(modeladmin, request, queryset):
	queryset.update(
		done = True
	)
doall.short_description = 'Mark done'

def undoall(modeladmin, request, queryset):
	queryset.update(
		done = False
	)
undoall.short_description = 'Mark undo'

class TodoAdmin(admin.ModelAdmin):
	list_display = ('user', 'time', 'done', 'category',)
	list_filter = ('time', 'done', 'category',)
	list_editable= ('done',)
	fieldsets = (
		('User Details', {'fields': ('user',)}),
        ('Todo info', {'fields': ('todo','category',)}),
        ('Todo Config', {'fields': ('time','done','tid',)}),
    )
	actions = [doall, undoall]
# Register your models here.
admin.site.register(TodoList, TodoAdmin)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)