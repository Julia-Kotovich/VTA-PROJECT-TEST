from django.urls import path
from . import views

urlpatterns = [
    path("routes/",views.getRoutes,name="routes"),
    path("home/",views.index,name="index"),
    path("vta-answer/",views.getAnswer,name="vtaResponse"),
    path("vta/like/",views.likeResponse,name="likeResponse"),
    path("vta/dislike/",views.dislikeResponse,name="dislikeResponse"),
    path("vta/feedback/",views.feedback,name="sendfeedback"),
]