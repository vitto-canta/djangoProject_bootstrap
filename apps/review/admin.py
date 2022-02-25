from django.contrib import admin

from apps.review.models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['rate', 'comment', 'made_by', 'addressed_to', 'created_at']
    list_filter = ['rate', 'made_by', 'addressed_to', 'created_at']
    search_fields = ['comment', ]

    class Meta:
        ordering = ['-created_at', 'rate']


admin.site.register(Review, ReviewAdmin)
