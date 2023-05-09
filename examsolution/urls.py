from django.urls import path
from . import views


app_name = "examsolution"
urlpatterns = [
    
    path('', views.home, name='home'),
    path('syllabi', views.syllabi, name='syllabi'),
    path('notes', views.notes, name='notes'),
    path('topicalpastpaper', views.index_topical_past_paper, name='topical_past_paper'),
    path('topicalpastpaper/<exam_board>', views.subject_topical_past_paper, name='subject_topical_past_paper'),
    path('topicalpastpaper/<exam_board>/<subject_selected>', views.topics_topical_past_paper, name='topics_topical_past_paper'),
    path('topicalpastpaper/<exam_board>/<subject_selected>/<int:topic_id>', views.view_topical_past_paper, name='view_topical_past_paper'),
    path('pastpapers', views.past_papers, name='past_papers'),
    path('testyourself', views.test_yourself, name='test_yourself'),
    path('college', views.college, name='college'),
    path('contactpiilearn', views.contactpiilearn, name='contact_piilearn'),
     
] 




