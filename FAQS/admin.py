from django.contrib import admin
from .models import FAQ

class FAQAdmin(admin.ModelAdmin):
    fields = ['question', 'answer']

    list_display = ['Question', 'Answer']
    
    list_display_links = ['Question', 'Answer']
    
    def Question(self, obj):
        return obj.question[:50] + '...' if len(obj.question) > 50 else obj.question
    
    def Answer(self, obj):
        return obj.answer[:50] + '...' if len(obj.answer) > 50 else obj.answer

    def get_fields(self, request, obj=None):
        return ['question', 'answer']

admin.site.register(FAQ, FAQAdmin)
