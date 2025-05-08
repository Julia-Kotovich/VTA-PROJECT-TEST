from django.contrib import admin
from .models import Chat, LikeResponse, DislikeResponse, Feedback

@admin.register(LikeResponse)
class LikeResponseAdmin(admin.ModelAdmin):
    list_display = ('userText', 'VTAText', 'userId', 'likeStatus')
    list_filter = ('likeStatus',)
    search_fields = ('userText', 'VTAText', 'userId')
    ordering = ('-id',)  # Сортировка по id в обратном порядке

@admin.register(DislikeResponse)
class DislikeResponseAdmin(admin.ModelAdmin):
    list_display = ('userText', 'VTAText', 'userId', 'likeStatus')
    list_filter = ('likeStatus',)
    search_fields = ('userText', 'VTAText', 'userId')
    ordering = ('-id',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('userFeedback', 'userId')
    search_fields = ('userFeedback', 'userId')
    ordering = ('-id',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('query', 'response', 'created')
    search_fields = ('query', 'response')
    ordering = ('-created',)
