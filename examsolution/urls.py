from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LogoutView

app_name = "examsolution"
urlpatterns = [
   
    path('', views.home, name='home'),
    path('site_map', views.site_maps_view),
    path('notes/', views.notes, name='notes'),
    path('topicalpastpaper/', views.index_topical_past_paper, name='topical_past_paper'),
    path('topicalpastpaper/<exam_board>', views.subject_topical_past_paper, name='subject_topical_past_paper'),
    path('topicalpastpaper/<exam_board>/<subject_selected>', views.topics_topical_past_paper, name='topics_topical_past_paper'),
    path('topicalpastpaper/<exam_board>/<subject_selected>/<int:topic_id>', views.view_topical_past_paper, name='view_topical_past_paper'),
    path('pastpapers/', views.index_past_papers, name='past_papers'),
    path('pastpapers/<exam_board>',views.subject_past_papers,name='subject_past_papers'),
    path('pastpapers/<exam_board>/<subject_selected>', views.year_past_papers, name='year_past_papers'),
    path('pastpapers/<exam_board>/<subject_selected>/<year>', views.view_past_paper , name='view_past_paper'),
    path('testyourself/', views.index_test_yourself, name='test_yourself'),
    path('testyourself/<question_id>/', views.taking_test, name='taking_test'),
    path('testyourself/<question_id>/grading/', views.test_grading, name='test_grading'),
    path('worksheets/', views.worksheets, name='worksheets'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us/',views.about_us,name='about_us'),
    path('privacy/',views.privacy, name='privacy'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),
    
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='examsolution:home'),name='logout'),
    path('register/',RegisterPage.as_view(),name='register'),
    
    path('my_to_do_list/',UserTaskList.as_view(),name='my_to_do_list'),
    path('my_to_do_list/<int:pk>/', UserTaskDetail.as_view(),name='task'),
    path('my_to_do_list/create_task/', UserTaskCreate.as_view(),name='create_task'),
    path('my_to_do_list/update_task/<int:pk>/',UserTaskUpdate.as_view(),name='update_task'),
    path('my_to_do_list/delete_task/<int:pk>/',DeleteView.as_view(),name='delete_task'),
    
    path('my_progress/', UserProgressList.as_view(),name='my_progress'),
    path('my_progress_record/', UserProgressRecordCreate.as_view(),name='my_progress_record'),
    path('revision/<paper_to_revise>/', views.full_revision_of_written_paper,name='full_revision_of_written_paper'),

    path('blog/',views.blog_post_home, name='blog_post_home'),
    path("<title>/<int:year>/<int:month>/<int:day>/<int:id>/", views.read_articlet, name="read_article")
    
]


