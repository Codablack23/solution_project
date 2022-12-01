from django.urls import path
from . import views

urlpatterns = [
    path('videos/', views.getVideos, name='cam_video'),
    path('<cam_name>', views.watch, name='cam_name'),
    path('<cam_name>/replay/',views.replay, name='page_number'),
    path('<cam_name>/watch/<watch_link>',views.recordStream, name='page_number'),
    path('<cam_name>/record/',views.recordCamStream, name='page_number'),
    path('<cam_name>/replay/<page_number>',views.replay, name='page_number'),
]