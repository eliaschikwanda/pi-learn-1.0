

# from django import forms
# from django.forms import ModelForm
# from .models import *
# from .views import *


# question_answer = QuestionAnswer.objects.all()

# questions_available = []
# for x in question_answer:
#     questions_available.append(x.question_name)

# QUESTION_AVAILABLE_CHOICES = []

# QUESTION_AVAILABLE_CHOICES.insert(0,('None',''))

# number_of_questions_available = len(questions_available)
# for x in range(number_of_questions_available):
#     array_index_needed = x + 1
#     QUESTION_AVAILABLE_CHOICES.insert(array_index_needed,(questions_available[x],questions_available[x]))



# class QuestionSearchForm(forms.Form):
#     question_search = forms.ChoiceField(choices=QUESTION_AVAILABLE_CHOICES, widget=forms.Select(attrs={'onchange': 'submit();'}))
    
    
# # Exam Board Search starts here

# # Below

# exam_board_choices = ExamBoard.objects.all()
# exam_board_available = []
# for exam_baord in exam_board_choices:
#     exam_board_available.append(exam_baord.exam_board)

# EXAM_BOARD_CHOICES = []
# EXAM_BOARD_CHOICES.insert(0,('None',''))
# exam_baord_num = len(exam_board_available)

# for x in range(exam_baord_num):
#     index_needed = x + 1
#     EXAM_BOARD_CHOICES.insert(index_needed,(exam_board_available[x],exam_board_available[x]))
    
# # Exam Board Search ends here
# # Subject Search starts here
    
# subject_choices = Subject.objects.all()
# subject_available = []
# for subject in subject_choices:
#     subject_available.append(subject.subject)
    
# SUBJECT_CHOICES = []
# SUBJECT_CHOICES.insert(0,('None',''))
# subject_num = len(subject_available)


# for x in range(subject_num):
#     index_needed = x + 1
#     SUBJECT_CHOICES.insert(index_needed,(subject_available[x],subject_available[x]))

# # Subject Search starts here
# # Paper Search starts here

# paper_choices = Paper.objects.all()
# paper_available = []
# for paper in paper_choices:
#     paper_available.append(paper.paper_num)
    
# PAPER_NUMBER_CHOICES  = []
# PAPER_NUMBER_CHOICES.insert(0,('None',''))
# paper_number = len(paper_available)

# for x in range(paper_number):
#     index_needed = x + 1
#     PAPER_NUMBER_CHOICES.insert(index_needed,(str(paper_available[x]),str(paper_available[x])))

# # Paper Search ends here
# # Topic Search starts here
# topic_choices = BoardSubTopic.objects.all()
# topics_available = []
# for topic in topic_choices:
#     topics_available.append(topic.topic)
    
# TOPIC_CHOICES = []
# TOPIC_CHOICES.insert(0,('None',''))
# topics_len = len(topics_available)

# for x in range(topics_len):
#     index_needed = x + 1
#     TOPIC_CHOICES.insert(index_needed,(topics_available[x],topics_available[x]))

# # Topic Search end here
# # Year Search starts here
# year_choices = Year.objects.all()
# years_available = []
# for year in year_choices:
#     years_available.append(year.year)
    
# YEAR_CHOICES = []
# YEAR_CHOICES.insert(0,('None',''))
# years_len = len(years_available)

# for x in range(years_len):
#     index_needed = x + 1
#     YEAR_CHOICES.insert(index_needed,(str(years_available[x]),str(years_available[x])))
# # Year Search ends here
# # Session Search starts here
# session_choices = Session.objects.all()
# session_available = []
# for session in session_choices:
#     session_available.append(session.session)
    
# SESSION_CHOICES = []
# SESSION_CHOICES.insert(0,('None',''))
# session_len = len(session_available)

# for x in range(session_len):
#     index_needed = x + 1
#     SESSION_CHOICES.insert(index_needed,(str(session_available[x]),str(session_available[x])))
# # Session Search ends here


# class SearchForm(forms.Form):
#     subject_search = forms.ChoiceField(choices=SUBJECT_CHOICES, label='Subject',required=False, widget=forms.Select(attrs={'onchange': 'submit();'}))
#     paper_search = forms.ChoiceField(choices=PAPER_NUMBER_CHOICES, label='Paper', required=False, widget=forms.Select(attrs={'onchange':'submit()'}))
#     topic_search = forms.ChoiceField(choices=TOPIC_CHOICES, label='Topic', required=False , widget=forms.Select(attrs={'onchange':'submit()'}))
#     year_search = forms.ChoiceField(choices=YEAR_CHOICES, label='Year', required=False, widget=forms.Select(attrs={'onchange':'submit()'}))
#     session_search = forms.ChoiceField(choices=SESSION_CHOICES, label='Session', required=False, widget=forms.Select(attrs={'onchange':'submit()'}))


# class ExamBoardSearchForm(forms.Form):
#     exam_board_search = forms.ChoiceField(choices=EXAM_BOARD_CHOICES, label='Exam Board', required=True)



##### Views part
    # question_search_form = SearchForm(request.POST or None)
    # subject_searched = ''
    # paper_searched = ''
    # topic_searched = ''
    # year_searched = ''
    # session_searched = ''

    
    # if question_search_form.is_valid():
    #     subject_searched = question_search_form.cleaned_data.get('subject_search')
    #     paper_searched = question_search_form.cleaned_data.get('paper_search')
    #     topic_searched = question_search_form.cleaned_data.get('topic_search')
    #     year_searched = question_search_form.cleaned_data.get('year_search')
    #     session_searched = question_search_form.cleaned_data.get('session_search')
        