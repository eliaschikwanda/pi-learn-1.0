from django.urls import path
from . import views


app_name = "examsolution"
urlpatterns = [
    
    path('', views.home, name='home'),
    path('notes/', views.notes, name='notes'),
    path('topicalpastpaper/', views.index_topical_past_paper, name='topical_past_paper'),
    path('topicalpastpaper/<exam_board>', views.subject_topical_past_paper, name='subject_topical_past_paper'),
    path('topicalpastpaper/<exam_board>/<subject_selected>', views.topics_topical_past_paper, name='topics_topical_past_paper'),
    path('topicalpastpaper/<exam_board>/<subject_selected>/<int:topic_id>', views.view_topical_past_paper, name='view_topical_past_paper'),
    path('pastpapers/', views.index_past_papers, name='past_papers'),
    path('pastpapers/<exam_board>',views.subject_past_papers,name='subject_past_papers'),
    path('pastpapers/<exam_board>/<subject_selected>', views.year_past_papers, name='year_past_papers'),
    path('pastpapers/<exam_board>/<subject_selected>/<year>', views.view_past_paper , name='view_past_paper'),
    path('testyourself', views.index_test_yourself, name='test_yourself'),
    path('testyourself/<question_id>/', views.taking_test, name='taking_test'),
    path('testyourself/<question_id>/grading/', views.test_grading, name='test_grading'),
    path('worksheets/', views.worksheets, name='worksheets'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('about_us/',views.about_us,name='about_us'),
    path('privacy/',views.privacy, name='privacy'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),
     
] 



