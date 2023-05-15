from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .models import *




# Create your views here.

# Home page view with empty url

def home(request):
    

    
    all_exam_boards = ExamBoard.objects.all()
    
    context = {
        
        'all_exam_boards' : all_exam_boards,
        
        
    }
    
    return render(request, 'examsolution/home.html', context)

# Syllabus page view

def syllabi(request):
   
    context = {

    }
    
    return render(request,'examsolution/syllabi.html',context)

# Notes page view

def notes(request):
    
    context = {
        
    }
    
    return render(request, 'examsolution/notes.html', context)

# Topical Past Paper views starts here

def index_topical_past_paper(request):
    
    exam_board_list = ExamBoard.objects.all()
           
    context = {

        'exam_board_list' : exam_board_list,

    }

    return render(request, 'examsolution/topical_past_paper.html', context)

def subject_topical_past_paper(request,exam_board):
    
    exam_board_selected = get_object_or_404(ExamBoard,exam_board=exam_board)
    
    context = {
        'exam_board_selected' : exam_board_selected,
    }
    
    return render(request,"examsolution/subject_topical_past_paper.html",context)

def topics_topical_past_paper(request,exam_board,subject_selected):
    topic_paper_list = BoardSubTopic.objects.filter(subject_key__subject=subject_selected)
    context = {
        'subject_selected':subject_selected,
        'topic_paper_list':topic_paper_list,
        'exam_board' : exam_board,
    }
    
    return render(request,"examsolution/topics_topical_past_paper.html",context)

def view_topical_past_paper(request,exam_board,subject_selected,topic_id):
    year_set = Year.objects.all()
    session_set = Session.objects.all()
    topic_paper_object = get_object_or_404(BoardSubTopic, pk=topic_id)
    selected_topic_paper_set = topic_paper_object.questionanswer_set.all()
    new_selected_topic_paper_set = topic_paper_object.questionanswer_set.filter(year_key=request.POST.get("year",False), session_key=request.POST.get("session",False))
    

    

    context = {
        'exam_board' : exam_board,
        'subject_selected' :subject_selected,
        'topic_paper_object' : topic_paper_object,
        'selected_topic_paper_set' : selected_topic_paper_set,
        'new_selected_topic_paper_set':new_selected_topic_paper_set,
        'year_set' : year_set,
        'session_set' : session_set,
        
    }

    return render(request,"examsolution/view_topical_past_paper.html",context)
# Topical Past Paper views ends here

# Past Paper view starts here

def index_past_papers(request):
    
    exam_board_list = ExamBoard.objects.all()
    
    context = {
        'exam_board_list': exam_board_list
    }
    
    return render(request, 'examsolution/past_papers.html', context)

def subject_past_papers(request,exam_board):
    
    exam_board_selected = get_object_or_404(ExamBoard,exam_board=exam_board)
    
    context = {
        'exam_board_selected' : exam_board_selected,
    }
    
    return render(request,'examsolution/subject_past_papers.html',context)

def year_past_papers(request,exam_board,subject_selected):
    
    years_available_list = Year.objects.all()
    
    context = {
        'years_available_list':years_available_list,
        'exam_board' : exam_board,
        'subject_selected':subject_selected,
        
    }
    
    return render(request,'examsolution/year_past_papers.html',context)

def view_past_paper(request,exam_board,subject_selected,year):
    
    march_past_papers_selected_list = FullQuestionAnswer.objects.filter(session_key__session='March',year_key__year=year,subject_key__subject=subject_selected).order_by('full_question_name')
    june_past_papers_selected_list = FullQuestionAnswer.objects.filter(session_key__session='June',year_key__year=year,subject_key__subject=subject_selected).order_by('full_question_name')
    november_past_papers_selected_list = FullQuestionAnswer.objects.filter(session_key__session='November',year_key__year=year,subject_key__subject=subject_selected).order_by('full_question_name')
    
    march_extras = ReportThreshPrep.objects.filter(session_key__session='March',year_key__year = year,subject_key__subject=subject_selected).order_by('-extra_name')
    june_extras = ReportThreshPrep.objects.filter(session_key__session='June',year_key__year = year,subject_key__subject=subject_selected).order_by('-extra_name')
    november_extras = ReportThreshPrep.objects.filter(session_key__session='November',year_key__year = year,subject_key__subject=subject_selected).order_by('-extra_name')
   
    context = {
        
        'exam_board' : exam_board,
        'subject_selected' : subject_selected,
        'year':year,
        'march_past_papers_selected_list' : march_past_papers_selected_list,
        'june_past_papers_selected_list':june_past_papers_selected_list,
        'november_past_papers_selected_list':november_past_papers_selected_list,
        'march_extras' : march_extras,
        'june_extras':june_extras,
        'november_extras':november_extras,
       
    }
    
    return render(request,'examsolution/view_past_paper.html',context)

# Past Paper view ends here

# Test Yourself starts here

def index_test_yourself(request):
    
    multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1')
    
    context = {
        'multiple_choice_available_list' : multiple_choice_available_list,
    }
    
    return render(request, 'examsolution/test_yourself.html', context)

def taking_test(request,question_id):
    
    mcq_paper_selected = FullQuestionAnswer.objects.get(id=question_id)
    mcq_paper_selected_set = FullQuestionAnswer.objects.get(id=question_id).paperoneanswers_set.all()
    possible_answer1 = PossibleLetters.objects.get(pk=1)
    possible_answer2 = PossibleLetters.objects.get(pk=2)
    possible_answer3 = PossibleLetters.objects.get(pk=3)
    possible_answer4 = PossibleLetters.objects.get(pk=4)
    
    context = {
        'mcq_paper_selected' : mcq_paper_selected,
        'mcq_paper_selected_set' : mcq_paper_selected_set,
        'possible_answer1':possible_answer1,
        'possible_answer2' : possible_answer2,
        'possible_answer3' : possible_answer3,
        'possible_answer4' : possible_answer4,
        'question_id' : question_id,
        
        
    }
    
    return render(request,'examsolution/taking_test.html',context)

def test_grading(request,question_id):
    mcq_paper_selected = get_object_or_404(FullQuestionAnswer,pk=question_id)
    mcq_paper_selected_set = FullQuestionAnswer.objects.get(id=question_id).paperoneanswers_set.all()
    score = 0
    wrong_question = []
    
    submitted_answer1 = PossibleLetters.objects.get(pk=request.POST['1']).letter
    question_1 = mcq_paper_selected_set.get(question_number_key__question_number = 1)
    if str(submitted_answer1) == str(question_1.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_1.question_number_key.question_number)
    
    submitted_answer2 = PossibleLetters.objects.get(pk=request.POST['2']).letter
    question_2 = mcq_paper_selected_set.get(question_number_key__question_number = 2)
    if str(submitted_answer2) == str(question_2.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_2.question_number_key.question_number)
        
    submitted_answer3 = PossibleLetters.objects.get(pk=request.POST['3']).letter
    question_3 = mcq_paper_selected_set.get(question_number_key__question_number = 3)
    if str(submitted_answer3) == str(question_3.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_3.question_number_key.question_number)
    
    submitted_answer4 = PossibleLetters.objects.get(pk=request.POST['4']).letter
    question_4 = mcq_paper_selected_set.get(question_number_key__question_number = 4)
    if str(submitted_answer4) == str(question_4.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_4.question_number_key.question_number)
        
    submitted_answer5 = PossibleLetters.objects.get(pk=request.POST['5']).letter
    question_5 = mcq_paper_selected_set.get(question_number_key__question_number = 5)
    if str(submitted_answer5) == str(question_5.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_5.question_number_key.question_number)
        
    submitted_answer6 = PossibleLetters.objects.get(pk=request.POST['6']).letter
    question_6 = mcq_paper_selected_set.get(question_number_key__question_number = 6)
    if str(submitted_answer6) == str(question_6.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_6.question_number_key.question_number)
        
    submitted_answer7 = PossibleLetters.objects.get(pk=request.POST['7']).letter
    question_7 = mcq_paper_selected_set.get(question_number_key__question_number = 7)
    if str(submitted_answer7) == str(question_7.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_7.question_number_key.question_number)
        
    submitted_answer8 = PossibleLetters.objects.get(pk=request.POST['8']).letter
    question_8 = mcq_paper_selected_set.get(question_number_key__question_number = 8)
    if str(submitted_answer8) == str(question_8.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_8.question_number_key.question_number)
        
    submitted_answer9 = PossibleLetters.objects.get(pk=request.POST['9']).letter
    question_9 = mcq_paper_selected_set.get(question_number_key__question_number = 9)
    if str(submitted_answer9) == str(question_9.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_8.question_number_key.question_number)
        
    submitted_answer10 = PossibleLetters.objects.get(pk=request.POST['10']).letter
    question_10 = mcq_paper_selected_set.get(question_number_key__question_number = 10)
    if str(submitted_answer10) == str(question_10.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_10.question_number_key.question_number)
        
    submitted_answer11 = PossibleLetters.objects.get(pk=request.POST['11']).letter
    question_11 = mcq_paper_selected_set.get(question_number_key__question_number = 11)
    if str(submitted_answer11) == str(question_11.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_11.question_number_key.question_number)
        
    submitted_answer12 = PossibleLetters.objects.get(pk=request.POST['12']).letter
    question_12 = mcq_paper_selected_set.get(question_number_key__question_number = 12)
    if str(submitted_answer12) == str(question_12.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_12.question_number_key.question_number)
        
    submitted_answer13 = PossibleLetters.objects.get(pk=request.POST['13']).letter
    question_13 = mcq_paper_selected_set.get(question_number_key__question_number = 13)
    if str(submitted_answer13) == str(question_13.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_13.question_number_key.question_number)
        
    submitted_answer14 = PossibleLetters.objects.get(pk=request.POST['14']).letter
    question_14 = mcq_paper_selected_set.get(question_number_key__question_number = 14)
    if str(submitted_answer14) == str(question_14.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_14.question_number_key.question_number)
        
    submitted_answer15 = PossibleLetters.objects.get(pk=request.POST['15']).letter
    question_15 = mcq_paper_selected_set.get(question_number_key__question_number = 15)
    if str(submitted_answer15) == str(question_15.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_15.question_number_key.question_number)
        
    submitted_answer16 = PossibleLetters.objects.get(pk=request.POST['16']).letter
    question_16 = mcq_paper_selected_set.get(question_number_key__question_number = 16)
    if str(submitted_answer16) == str(question_16.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_16.question_number_key.question_number)
    
    submitted_answer17 = PossibleLetters.objects.get(pk=request.POST['17']).letter
    question_17 = mcq_paper_selected_set.get(question_number_key__question_number = 17)
    if str(submitted_answer17) == str(question_17.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_17.question_number_key.question_number)
        
    
        
    submitted_answer18 = PossibleLetters.objects.get(pk=request.POST['18']).letter
    question_18 = mcq_paper_selected_set.get(question_number_key__question_number = 18)
    if str(submitted_answer18) == str(question_18.question_answer_key):
        score += 1
        
    else:
        wrong_question.append(question_18.question_number_key.question_number)
        
        
        
    submitted_answer19 = PossibleLetters.objects.get(pk=request.POST['19']).letter
    question_19 = mcq_paper_selected_set.get(question_number_key__question_number = 19)
    if str(submitted_answer19) == str(question_19.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_19.question_number_key.question_number)
        
        
        
    submitted_answer20 = PossibleLetters.objects.get(pk=request.POST['20']).letter
    question_20 = mcq_paper_selected_set.get(question_number_key__question_number = 20)
    if str(submitted_answer20) == str(question_20.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_20.question_number_key.question_number)
        
        
        
    submitted_answer21 = PossibleLetters.objects.get(pk=request.POST['21']).letter
    question_21 = mcq_paper_selected_set.get(question_number_key__question_number = 21)
    if str(submitted_answer21) == str(question_21.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_21.question_number_key.question_number)
        
        
        
    submitted_answer22 = PossibleLetters.objects.get(pk=request.POST['22']).letter
    question_22 = mcq_paper_selected_set.get(question_number_key__question_number = 22)
    if str(submitted_answer22) == str(question_22.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_22.question_number_key.question_number)
        
        
        
    submitted_answer23 = PossibleLetters.objects.get(pk=request.POST['23']).letter
    question_23 = mcq_paper_selected_set.get(question_number_key__question_number = 23)
    if str(submitted_answer23) == str(question_23.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_23.question_number_key.question_number)
        
    
        
    submitted_answer24 = PossibleLetters.objects.get(pk=request.POST['24']).letter
    question_24 = mcq_paper_selected_set.get(question_number_key__question_number = 24)
    if str(submitted_answer24) == str(question_24.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_24.question_number_key.question_number)
        
        
        
    submitted_answer25 = PossibleLetters.objects.get(pk=request.POST['25']).letter
    question_25 = mcq_paper_selected_set.get(question_number_key__question_number = 25)
    if str(submitted_answer25) == str(question_25.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_25.question_number_key.question_number)
        
        
        
    submitted_answer26 = PossibleLetters.objects.get(pk=request.POST['26']).letter
    question_26 = mcq_paper_selected_set.get(question_number_key__question_number = 26)
    if str(submitted_answer26) == str(question_26.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_26.question_number_key.question_number)
        
        
        
    submitted_answer27 = PossibleLetters.objects.get(pk=request.POST['27']).letter
    question_27 = mcq_paper_selected_set.get(question_number_key__question_number = 27)
    if str(submitted_answer27) == str(question_27.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_27.question_number_key.question_number)
        
        
        
    submitted_answer28 = PossibleLetters.objects.get(pk=request.POST['28']).letter
    question_28 = mcq_paper_selected_set.get(question_number_key__question_number = 28)
    if str(submitted_answer28) == str(question_28.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_28.question_number_key.question_number)
        
        
        
    submitted_answer29 = PossibleLetters.objects.get(pk=request.POST['29']).letter
    question_29 = mcq_paper_selected_set.get(question_number_key__question_number = 29)
    if str(submitted_answer29) == str(question_29.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_29.question_number_key.question_number)
        
        
        
        
    submitted_answer30 = PossibleLetters.objects.get(pk=request.POST['30']).letter
    question_30 = mcq_paper_selected_set.get(question_number_key__question_number = 30)
    if str(submitted_answer30) == str(question_30.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_30.question_number_key.question_number)
        
        
        
    submitted_answer31 = PossibleLetters.objects.get(pk=request.POST['31']).letter
    question_31 = mcq_paper_selected_set.get(question_number_key__question_number = 31)
    if str(submitted_answer31) == str(question_31.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_31.question_number_key.question_number)
        
        
        
    submitted_answer32 = PossibleLetters.objects.get(pk=request.POST['32']).letter
    question_32 = mcq_paper_selected_set.get(question_number_key__question_number = 32)
    if str(submitted_answer32) == str(question_32.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_32.question_number_key.question_number)
        
        
        
    submitted_answer33 = PossibleLetters.objects.get(pk=request.POST['33']).letter
    question_33 = mcq_paper_selected_set.get(question_number_key__question_number = 33)
    if str(submitted_answer33) == str(question_33.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_33.question_number_key.question_number)
        
        
        
    submitted_answer34 = PossibleLetters.objects.get(pk=request.POST['34']).letter
    question_34 = mcq_paper_selected_set.get(question_number_key__question_number = 34)
    if str(submitted_answer34) == str(question_34.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_34.question_number_key.question_number)
        
        
        
    submitted_answer35 = PossibleLetters.objects.get(pk=request.POST['35']).letter
    question_35 = mcq_paper_selected_set.get(question_number_key__question_number = 35)
    if str(submitted_answer35) == str(question_35.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_35.question_number_key.question_number)
        
        
        
    submitted_answer36 = PossibleLetters.objects.get(pk=request.POST['36']).letter
    question_36 = mcq_paper_selected_set.get(question_number_key__question_number = 36)
    if str(submitted_answer36) == str(question_36.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_36.question_number_key.question_number)
        
        
        
    submitted_answer37 = PossibleLetters.objects.get(pk=request.POST['37']).letter
    question_37 = mcq_paper_selected_set.get(question_number_key__question_number = 37)
    if str(submitted_answer37) == str(question_37.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_37.question_number_key.question_number)
        
        
        
    submitted_answer38 = PossibleLetters.objects.get(pk=request.POST['38']).letter
    question_38 = mcq_paper_selected_set.get(question_number_key__question_number = 38)
    if str(submitted_answer38) == str(question_38.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_38.question_number_key.question_number)
        
        
        
    submitted_answer39 = PossibleLetters.objects.get(pk=request.POST['39']).letter
    question_39 = mcq_paper_selected_set.get(question_number_key__question_number = 39)
    if str(submitted_answer39) == str(question_39.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_39.question_number_key.question_number)
        
        
        
        
    submitted_answer40 = PossibleLetters.objects.get(pk=request.POST['40']).letter
    question_40 = mcq_paper_selected_set.get(question_number_key__question_number = 40)
    if str(submitted_answer40) == str(question_40.question_answer_key):
        score += 1
    else:
        wrong_question.append(question_40.question_number_key.question_number)
        
    context = {
        'score' : score,
        'wrong_question':wrong_question,
    }
            
    return render(request,'examsolution/test_grading.html',context)


# Test Yourself ends here

# College view

def college(request):

    
    context = {
        
    }
    
    return render(request, 'examsolution/college.html', context)

# Contact PiiLearn view

def contactpiilearn(request):
    
    context = {
       
    }
    
    return render(request, 'examsolution/contact_piilearn.html', context)

def exam_board(request):
    
    context = {

    }
    
    return render(request,'examsolution/exam_board.html',context)