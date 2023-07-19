from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.



# Login class views starts here

class CustomLoginView(LoginView):
    template_name = 'examsolution/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('examsolution:home')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        website_logo = website_pics.objects.get(id=1)
        context['website_logo'] = website_logo
        
        return context
    
    
class RegisterPage(FormView):
    template_name = 'examsolution/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True #Users that are authenticated are redirected
    success_url = reverse_lazy('examsolution:my_to_do_list') #log in the user
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('examsolution:my_to_do_list')
        return super(RegisterPage, self).get(*args, **kwargs) #Means if user not logged in go ahead and do whatever you were up to
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        website_logo = website_pics.objects.get(id=1)
        context['website_logo'] = website_logo
        
        return context
        

# Login class views ends here

# user based views starts here

class UserTaskList(LoginRequiredMixin,ListView):
    model = UserTask
    context_object_name = 'usertasklist'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertasklist'] = context['usertasklist'].filter(user=self.request.user)
        context['count'] = context['usertasklist'].filter(complete=False).count()
        website_logo = website_pics.objects.get(id=1)
        context['website_logo'] = website_logo
        
        search_input = self.request.GET.get('search_area') or ''
        
        if search_input:
            context['usertasklist'] = context['usertasklist'].filter(title__icontains=search_input) #icontains can be used if the title contains that letter
            
        context['search_input'] = search_input
        
        return context
    
# User papers taken list view starts here
class UserProgressList(LoginRequiredMixin,ListView):
    model = UserProgressRecord
    context_object_name = 'user_past_paper_taken_list'
    template_name ='examsolution/userprogress_list.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        website_logo = website_pics.objects.get(id=1)
        context['website_logo'] = website_logo
        context['user_past_paper_taken_list'] = context['user_past_paper_taken_list'].filter(user=self.request.user)
        context['bio_user_past_paper_taken_list'] = context['user_past_paper_taken_list'].filter(subject_of_paper_written='Biology ~ 9700')
        context['chem_user_past_paper_taken_list'] = context['user_past_paper_taken_list'].filter(subject_of_paper_written='Chemistry ~ 9701')
        context['phy_user_past_paper_taken_list'] = context['user_past_paper_taken_list'].filter(subject_of_paper_written='Physics ~ 9702')
        context['econ_user_past_paper_taken_list'] = context['user_past_paper_taken_list'].filter(subject_of_paper_written='Economics ~ 9708')
        
        count = 0
        bio_perce_total = 0
        bio_raw_total = 0
        bio_perce_average = 0
        bio_raw_average = 0
        
        if context['bio_user_past_paper_taken_list']:
            for each_test in context['bio_user_past_paper_taken_list']:
                count = count + 1
                bio_raw_total = int(each_test.raw_mark) + bio_raw_total
                bio_perce_total = float(each_test.percentage) + bio_perce_total
                
            bio_perce_average = round(bio_perce_total/count,1)
            bio_raw_average = round(bio_raw_total/count,1)
            
        count = 0
        chem_perce_total = 0
        chem_raw_total = 0
        chem_perce_average = 0
        chem_raw_average = 0
        
        if context['chem_user_past_paper_taken_list']:
            for each_test in context['chem_user_past_paper_taken_list']:
                count = count + 1
                chem_raw_total = int(each_test.raw_mark) + chem_raw_total
                chem_perce_total = float(each_test.percentage) + chem_perce_total
                
            chem_perce_average = round(chem_perce_total/count,1)
            chem_raw_average = round(chem_raw_total/count,1)
            
        count = 0
        phys_perce_total = 0
        phys_raw_total = 0
        phys_perce_average = 0
        phsy_raw_average = 0
        
        if context['phy_user_past_paper_taken_list']:
            for each_test in context['phy_user_past_paper_taken_list']:
                count = count + 1
                phys_raw_total = int(each_test.raw_mark) + phys_raw_total
                phys_perce_total = float(each_test.percentage) + phys_perce_total
                
            phys_perce_average = round(phys_perce_total/count,1)
            phsy_raw_average = round(phys_raw_total/count,1)
            
        count = 0
        econ_perce_total = 0
        econ_raw_total = 0
        econ_perce_average = 0
        econ_raw_average = 0
        
        if context['econ_user_past_paper_taken_list']:
            for each_test in context['econ_user_past_paper_taken_list']:
                count = count + 1
                econ_raw_total = int(each_test.raw_mark) + econ_raw_total
                econ_perce_total = float(each_test.percentage) + econ_perce_total
                
            econ_perce_average = round(econ_perce_total/count,1)
            econ_raw_average = round(econ_raw_total/count,1)
            

            
        context['bio_perce_average'] = bio_perce_average
        context['bio_raw_average'] = bio_raw_average
        context['chem_perce_average'] = chem_perce_average
        context['chem_raw_average'] = chem_raw_average
        context['phys_perce_average'] = phys_perce_average
        context['phsy_raw_average'] = phsy_raw_average
        context['econ_perce_average'] = econ_perce_average
        context['econ_raw_average'] = econ_raw_average
        
            
        return context


def full_revision_of_written_paper(request,paper_to_revise):
    mcq_paper_selected_set = FullQuestionAnswer.objects.get(full_question_name=paper_to_revise).paperoneanswers_set.all().order_by('question_number_key__question_number')
    mcq_paper_selected = FullQuestionAnswer.objects.get(full_question_name=paper_to_revise)
    user_answer_input_object = UserProgressRecord.objects.get(paper_written=paper_to_revise)
    website_logo = website_pics.objects.get(id=1)
    
    wrong_question = []
    user_answer_input_list = []
     
    for failed_question in user_answer_input_object.questions_failed.split(','):
        wrong_question.append(failed_question)
    
   
    for each_answer in user_answer_input_object.user_answer_input:
        user_answer_input_list.append(each_answer)
        
    
    context = {
        'score' : user_answer_input_object.raw_mark,
        'grade' : user_answer_input_object.letter_grade,
        'wrong_question':wrong_question,
        'mcq_paper_selected':mcq_paper_selected,
        'mcq_paper_selected_set' : mcq_paper_selected_set,
        'percentage' : user_answer_input_object.percentage,
        'user_answer_input_list' : user_answer_input_list,
        'website_logo':website_logo,
        
    }
    
    return render(request,'examsolution/full_revision_of_written_paper.html',context)
        
# User papers taken list view ends here
    
    
class UserTaskDetail(LoginRequiredMixin,DetailView):
    model = UserTask
    context_object_name = 'eachtask'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        website_logo = website_pics.objects.get(id=1)
        context['website_logo'] = website_logo
        
        return context
    
class UserTaskCreate(LoginRequiredMixin,CreateView):
    model = UserTask
    fields = ['title','description','complete']
    success_url = reverse_lazy('examsolution:my_to_do_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserTaskCreate,self).form_valid(form)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        website_logo = website_pics.objects.get(id=1)
        context['website_logo'] = website_logo
        
        return context
    
# Progress saving view starts here
class UserProgressRecordCreate(LoginRequiredMixin,CreateView):
    model = UserProgressRecord
    fields = []
    success_url = reverse_lazy('examsolution:my_progress')
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.paper_written = self.request.POST.get('paper_written')
        form.instance.raw_mark = self.request.POST.get('raw_mark')
        form.instance.percentage = self.request.POST.get('percentage')
        form.instance.letter_grade = self.request.POST.get('letter_grade')
        form.instance.questions_failed = self.request.POST.get('questions_failed')
        form.instance.subject_of_paper_written = self.request.POST.get('subject_of_paper_written')
        form.instance.user_answer_input = self.request.POST.get('user_answer_input')
        
        form.save()
        
        return super(UserProgressRecordCreate,self).form_valid(form)
    
# Progress saving view ends here
    
    
class UserTaskUpdate(LoginRequiredMixin,UpdateView):
    model = UserTask
    fields = ['title','description','complete']
    success_url = reverse_lazy('examsolution:my_to_do_list')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        website_logo = website_pics.objects.get(id=1)
        context['website_logo'] = website_logo
        
        return context
    
class DeleteView(LoginRequiredMixin,DeleteView):
    model = UserTask
    context_object_name = 'task'
    success_url = reverse_lazy('examsolution:my_to_do_list')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        website_logo = website_pics.objects.get(id=1)
        context['website_logo'] = website_logo
        
        return context
  
# user based views ends here

# Home page view with empty url


def home(request):
    
    website_logo = website_pics.objects.get(id=1) 
    all_exam_boards = ExamBoard.objects.all()
    home_page_img = home_image.objects.get(id=1)
   
    context = {
        
        'all_exam_boards' : all_exam_boards,
        'website_logo' : website_logo,
        'home_page_img': home_page_img,
    }
    
    return render(request, 'examsolution/home.html', context)


# Notes page view

def notes(request):
    
    website_logo = website_pics.objects.get(id=1)
    
    context = {
        'website_logo':website_logo,
    }
    
    return render(request, 'examsolution/notes.html', context)

# Topical Past Paper views starts here

def index_topical_past_paper(request):
    
    website_logo = website_pics.objects.get(id=1)
    exam_board_list = ExamBoard.objects.all()
           
    context = {

        'exam_board_list' : exam_board_list,
        'website_logo':website_logo,

    }

    return render(request, 'examsolution/topical_past_paper.html', context)

def subject_topical_past_paper(request,exam_board):
    
    website_logo = website_pics.objects.get(id=1)
    exam_board_selected = get_object_or_404(ExamBoard,exam_board=exam_board)
    
    context = {
        'exam_board_selected' : exam_board_selected,
        'website_logo':website_logo,
    }
    
    return render(request,"examsolution/subject_topical_past_paper.html",context)

def topics_topical_past_paper(request,exam_board,subject_selected):
    website_logo = website_pics.objects.get(id=1)
    topic_paper_list = BoardSubTopic.objects.filter(subject_key__subject=subject_selected)
    context = {
        'subject_selected':subject_selected,
        'topic_paper_list':topic_paper_list,
        'exam_board' : exam_board,
        'website_logo':website_logo,
    }
    
    return render(request,"examsolution/topics_topical_past_paper.html",context)

def view_topical_past_paper(request,exam_board,subject_selected,topic_id):
    website_logo = website_pics.objects.get(id=1)
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
        'website_logo':website_logo,
        
    }

    return render(request,"examsolution/view_topical_past_paper.html",context)
# Topical Past Paper views ends here

# Past Paper view starts here

def index_past_papers(request):
    
    website_logo = website_pics.objects.get(id=1)
    exam_board_list = ExamBoard.objects.all()
    
    context = {
        'exam_board_list': exam_board_list,
        'website_logo':website_logo,
    }
    
    return render(request, 'examsolution/past_papers.html', context)

def subject_past_papers(request,exam_board):
    
    website_logo = website_pics.objects.get(id=1)
    exam_board_selected = get_object_or_404(ExamBoard,exam_board=exam_board)
    
    context = {
        'exam_board_selected' : exam_board_selected,
        'website_logo':website_logo,
    }
    
    return render(request,'examsolution/subject_past_papers.html',context)

def year_past_papers(request,exam_board,subject_selected):
   
    website_logo = website_pics.objects.get(id=1)
    years_available_list = Year.objects.all()
    
    context = {
        'years_available_list':years_available_list,
        'exam_board' : exam_board,
        'subject_selected':subject_selected,
        'website_logo':website_logo,
        
    }
    
    return render(request,'examsolution/year_past_papers.html',context)

def view_past_paper(request,exam_board,subject_selected,year):
    
    website_logo = website_pics.objects.get(id=1)
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
        'website_logo':website_logo,
       
    }
    
    return render(request,'examsolution/view_past_paper.html',context)

# Past Paper view ends here

# Test Yourself starts here

def index_test_yourself(request):
    
    website_logo = website_pics.objects.get(id=1)
    
    # Chemistry ~ 9701 filters 
    Chem_9701_2022_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2022',session_key__session='March').order_by('full_question_name')
    Chem_9701_2022_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2022',session_key__session='June').order_by('full_question_name')
    Chem_9701_2022_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2022',session_key__session='November').order_by('full_question_name')
    Chem_9701_2021_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2021',session_key__session='March').order_by('full_question_name')
    Chem_9701_2021_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2021',session_key__session='June').order_by('full_question_name')
    Chem_9701_2021_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2021',session_key__session='November').order_by('full_question_name')
    Chem_9701_2020_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2020',session_key__session='March').order_by('full_question_name')
    Chem_9701_2020_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2020',session_key__session='June').order_by('full_question_name')
    Chem_9701_2020_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Chemistry ~ 9701',year_key__year='2020',session_key__session='November').order_by('full_question_name')
    
    # Physic ~ 9702 filters
    Phy_9702_2022_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2022',session_key__session='March').order_by('full_question_name')
    Phy_9702_2022_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2022',session_key__session='June').order_by('full_question_name')
    Phy_9702_2022_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2022',session_key__session='November').order_by('full_question_name')
    Phy_9702_2021_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2021',session_key__session='March').order_by('full_question_name')
    Phy_9702_2021_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2021',session_key__session='June').order_by('full_question_name')
    Phy_9702_2021_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2021',session_key__session='November').order_by('full_question_name')
    Phy_9702_2020_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2020',session_key__session='March').order_by('full_question_name')
    Phy_9702_2020_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2020',session_key__session='June').order_by('full_question_name')
    Phy_9702_2020_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Physics ~ 9702',year_key__year='2020',session_key__session='November').order_by('full_question_name')
    
    #Biology filters
    Bio_9700_2022_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2022',session_key__session='March').order_by('full_question_name')
    Bio_9700_2022_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2022',session_key__session='June').order_by('full_question_name')
    Bio_9700_2022_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2022',session_key__session='November').order_by('full_question_name')
    Bio_9700_2021_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2021',session_key__session='March').order_by('full_question_name')
    Bio_9700_2021_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2021',session_key__session='June').order_by('full_question_name')
    Bio_9700_2021_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2021',session_key__session='November').order_by('full_question_name')
    Bio_9700_2020_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2020',session_key__session='March').order_by('full_question_name')
    Bio_9700_2020_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2020',session_key__session='June').order_by('full_question_name')
    Bio_9700_2020_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Biology ~ 9700',year_key__year='2020',session_key__session='November').order_by('full_question_name')
    
    # Economics filters
    Econ_9708_2022_March_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Economics ~ 9708',year_key__year='2022',session_key__session='March').order_by('full_question_name')
    Econ_9700_2022_June_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Economics ~ 9708',year_key__year='2022',session_key__session='June').order_by('full_question_name')
    Econ_9700_2022_November_multiple_choice_available_list = FullQuestionAnswer.objects.filter(paper_number__paper_num='1',subject_key__subject='Economics ~ 9708',year_key__year='2022',session_key__session='November').order_by('full_question_name')
    
   
   
   
   
    context = {
        'website_logo':website_logo,
        'Chem_9701_2022_March_multiple_choice_available_list':Chem_9701_2022_March_multiple_choice_available_list,
        'Chem_9701_2022_June_multiple_choice_available_list' : Chem_9701_2022_June_multiple_choice_available_list,
        'Chem_9701_2022_November_multiple_choice_available_list' : Chem_9701_2022_November_multiple_choice_available_list,
        'Chem_9701_2021_March_multiple_choice_available_list' : Chem_9701_2021_March_multiple_choice_available_list,
        'Chem_9701_2021_June_multiple_choice_available_list' : Chem_9701_2021_June_multiple_choice_available_list,
        'Chem_9701_2021_November_multiple_choice_available_list' : Chem_9701_2021_November_multiple_choice_available_list,
        'Chem_9701_2020_March_multiple_choice_available_list' : Chem_9701_2020_March_multiple_choice_available_list,
        'Chem_9701_2020_June_multiple_choice_available_list' : Chem_9701_2020_June_multiple_choice_available_list,
        'Chem_9701_2020_November_multiple_choice_available_list' : Chem_9701_2020_November_multiple_choice_available_list,
        'Phy_9702_2022_March_multiple_choice_available_list' : Phy_9702_2022_March_multiple_choice_available_list,
        'Phy_9702_2022_June_multiple_choice_available_list' : Phy_9702_2022_June_multiple_choice_available_list,
        'Phy_9702_2022_November_multiple_choice_available_list' : Phy_9702_2022_November_multiple_choice_available_list,
        'Phy_9702_2021_March_multiple_choice_available_list' : Phy_9702_2021_March_multiple_choice_available_list,
        'Phy_9702_2021_June_multiple_choice_available_list' : Phy_9702_2021_June_multiple_choice_available_list,
        'Phy_9702_2021_November_multiple_choice_available_list' : Phy_9702_2021_November_multiple_choice_available_list,
        'Phy_9702_2020_March_multiple_choice_available_list' : Phy_9702_2020_March_multiple_choice_available_list,
        'Phy_9702_2020_June_multiple_choice_available_list' : Phy_9702_2020_June_multiple_choice_available_list,
        'Phy_9702_2020_November_multiple_choice_available_list' : Phy_9702_2020_November_multiple_choice_available_list,
        'Bio_9700_2022_March_multiple_choice_available_list' : Bio_9700_2022_March_multiple_choice_available_list,
        'Bio_9700_2022_June_multiple_choice_available_list' : Bio_9700_2022_June_multiple_choice_available_list,
        'Bio_9700_2022_November_multiple_choice_available_list' : Bio_9700_2022_November_multiple_choice_available_list,
        'Bio_9700_2021_March_multiple_choice_available_list' : Bio_9700_2021_March_multiple_choice_available_list,
        'Bio_9700_2021_June_multiple_choice_available_list' : Bio_9700_2021_June_multiple_choice_available_list,
        'Bio_9700_2021_November_multiple_choice_available_list' : Bio_9700_2021_November_multiple_choice_available_list,
        'Bio_9700_2020_March_multiple_choice_available_list' : Bio_9700_2020_March_multiple_choice_available_list,
        'Bio_9700_2020_June_multiple_choice_available_list' : Bio_9700_2020_June_multiple_choice_available_list,
        'Bio_9700_2020_November_multiple_choice_available_list' : Bio_9700_2020_November_multiple_choice_available_list,
        'Econ_9708_2022_March_multiple_choice_available_list' : Econ_9708_2022_March_multiple_choice_available_list,
        'Econ_9700_2022_June_multiple_choice_available_list' : Econ_9700_2022_June_multiple_choice_available_list,
        'Econ_9700_2022_November_multiple_choice_available_list' :Econ_9700_2022_November_multiple_choice_available_list,
    }
    
    
    
    return render(request, 'examsolution/test_yourself.html', context)
    

    
    

def taking_test(request,question_id):
    
    website_logo = website_pics.objects.get(id=1)
    mcq_paper_selected = FullQuestionAnswer.objects.get(id=question_id)
    mcq_paper_selected_set = FullQuestionAnswer.objects.get(id=question_id).paperoneanswers_set.all().order_by('question_number_key__question_number')
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
        'website_logo':website_logo,
        
        
    }
    
    
    return render(request,'examsolution/taking_test.html',context)
    


def test_grading(request,question_id):
    
    website_logo = website_pics.objects.get(id=1)
    mcq_paper_selected = get_object_or_404(FullQuestionAnswer,pk=question_id)
    mcq_paper_selected_set = FullQuestionAnswer.objects.get(id=question_id).paperoneanswers_set.all()
    score = 0
    wrong_question = []
    user_answer_input = []
    count_question = 0
    
    
    if mcq_paper_selected.subject_key.subject == "Economics ~ 9708":
        print("this is working")
        for count_question in range(1,31):
            print(count_question)
            count_question = str(count_question)
            submitted_answer = PossibleLetters.objects.get(pk=request.POST.get(count_question)).letter
            user_answer_input.append(submitted_answer)
            question = mcq_paper_selected_set.get(question_number_key__question_number = count_question)
            if str(submitted_answer) == str(question.question_answer_key):
                score += 1
            else:
                wrong_question.append(question.question_number_key.question_number)
            
        
            
        percentage = ''
        percentage = round((score/30)*100,1)
        
        
        
    else:
            
             
        submitted_answer1 = PossibleLetters.objects.get(pk=request.POST['1']).letter
        user_answer_input.append(submitted_answer1)
        question_1 = mcq_paper_selected_set.get(question_number_key__question_number = 1)
        if str(submitted_answer1) == str(question_1.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_1.question_number_key.question_number)
        
        submitted_answer2 = PossibleLetters.objects.get(pk=request.POST['2']).letter
        user_answer_input.append(submitted_answer2)
        question_2 = mcq_paper_selected_set.get(question_number_key__question_number = 2)
        if str(submitted_answer2) == str(question_2.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_2.question_number_key.question_number)
            
        submitted_answer3 = PossibleLetters.objects.get(pk=request.POST['3']).letter
        user_answer_input.append(submitted_answer3)
        question_3 = mcq_paper_selected_set.get(question_number_key__question_number = 3)
        if str(submitted_answer3) == str(question_3.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_3.question_number_key.question_number)
        
        submitted_answer4 = PossibleLetters.objects.get(pk=request.POST['4']).letter
        user_answer_input.append(submitted_answer4)
        question_4 = mcq_paper_selected_set.get(question_number_key__question_number = 4)
        if str(submitted_answer4) == str(question_4.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_4.question_number_key.question_number)
            
        submitted_answer5 = PossibleLetters.objects.get(pk=request.POST['5']).letter
        user_answer_input.append(submitted_answer5)
        question_5 = mcq_paper_selected_set.get(question_number_key__question_number = 5)
        if str(submitted_answer5) == str(question_5.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_5.question_number_key.question_number)
            
        submitted_answer6 = PossibleLetters.objects.get(pk=request.POST['6']).letter
        user_answer_input.append(submitted_answer6)
        question_6 = mcq_paper_selected_set.get(question_number_key__question_number = 6)
        if str(submitted_answer6) == str(question_6.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_6.question_number_key.question_number)
            
        submitted_answer7 = PossibleLetters.objects.get(pk=request.POST['7']).letter
        user_answer_input.append(submitted_answer7)
        question_7 = mcq_paper_selected_set.get(question_number_key__question_number = 7)
        if str(submitted_answer7) == str(question_7.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_7.question_number_key.question_number)
            
        submitted_answer8 = PossibleLetters.objects.get(pk=request.POST['8']).letter
        user_answer_input.append(submitted_answer8)
        question_8 = mcq_paper_selected_set.get(question_number_key__question_number = 8)
        if str(submitted_answer8) == str(question_8.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_8.question_number_key.question_number)
            
        submitted_answer9 = PossibleLetters.objects.get(pk=request.POST['9']).letter
        user_answer_input.append(submitted_answer9)
        question_9 = mcq_paper_selected_set.get(question_number_key__question_number = 9)
        if str(submitted_answer9) == str(question_9.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_8.question_number_key.question_number)
            
        submitted_answer10 = PossibleLetters.objects.get(pk=request.POST['10']).letter
        user_answer_input.append(submitted_answer10)
        question_10 = mcq_paper_selected_set.get(question_number_key__question_number = 10)
        if str(submitted_answer10) == str(question_10.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_10.question_number_key.question_number)
            
        submitted_answer11 = PossibleLetters.objects.get(pk=request.POST['11']).letter
        user_answer_input.append(submitted_answer11)
        question_11 = mcq_paper_selected_set.get(question_number_key__question_number = 11)
        if str(submitted_answer11) == str(question_11.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_11.question_number_key.question_number)
            
        submitted_answer12 = PossibleLetters.objects.get(pk=request.POST['12']).letter
        user_answer_input.append(submitted_answer12)
        question_12 = mcq_paper_selected_set.get(question_number_key__question_number = 12)
        if str(submitted_answer12) == str(question_12.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_12.question_number_key.question_number)
            
        submitted_answer13 = PossibleLetters.objects.get(pk=request.POST['13']).letter
        user_answer_input.append(submitted_answer13)
        question_13 = mcq_paper_selected_set.get(question_number_key__question_number = 13)
        if str(submitted_answer13) == str(question_13.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_13.question_number_key.question_number)
            
        submitted_answer14 = PossibleLetters.objects.get(pk=request.POST['14']).letter
        user_answer_input.append(submitted_answer14)
        question_14 = mcq_paper_selected_set.get(question_number_key__question_number = 14)
        if str(submitted_answer14) == str(question_14.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_14.question_number_key.question_number)
            
        submitted_answer15 = PossibleLetters.objects.get(pk=request.POST['15']).letter
        user_answer_input.append(submitted_answer15)
        question_15 = mcq_paper_selected_set.get(question_number_key__question_number = 15)
        if str(submitted_answer15) == str(question_15.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_15.question_number_key.question_number)
            
        submitted_answer16 = PossibleLetters.objects.get(pk=request.POST['16']).letter
        user_answer_input.append(submitted_answer16)
        question_16 = mcq_paper_selected_set.get(question_number_key__question_number = 16)
        if str(submitted_answer16) == str(question_16.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_16.question_number_key.question_number)
        
        submitted_answer17 = PossibleLetters.objects.get(pk=request.POST['17']).letter
        user_answer_input.append(submitted_answer17)
        question_17 = mcq_paper_selected_set.get(question_number_key__question_number = 17)
        if str(submitted_answer17) == str(question_17.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_17.question_number_key.question_number)
            
        
            
        submitted_answer18 = PossibleLetters.objects.get(pk=request.POST['18']).letter
        user_answer_input.append(submitted_answer18)
        question_18 = mcq_paper_selected_set.get(question_number_key__question_number = 18)
        if str(submitted_answer18) == str(question_18.question_answer_key):
            score += 1
            
        else:
            wrong_question.append(question_18.question_number_key.question_number)
            
            
            
        submitted_answer19 = PossibleLetters.objects.get(pk=request.POST['19']).letter
        user_answer_input.append(submitted_answer19)
        question_19 = mcq_paper_selected_set.get(question_number_key__question_number = 19)
        if str(submitted_answer19) == str(question_19.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_19.question_number_key.question_number)
            
            
            
        submitted_answer20 = PossibleLetters.objects.get(pk=request.POST['20']).letter
        user_answer_input.append(submitted_answer20)
        question_20 = mcq_paper_selected_set.get(question_number_key__question_number = 20)
        if str(submitted_answer20) == str(question_20.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_20.question_number_key.question_number)
            
            
            
        submitted_answer21 = PossibleLetters.objects.get(pk=request.POST['21']).letter
        user_answer_input.append(submitted_answer21)
        question_21 = mcq_paper_selected_set.get(question_number_key__question_number = 21)
        if str(submitted_answer21) == str(question_21.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_21.question_number_key.question_number)
            
            
            
        submitted_answer22 = PossibleLetters.objects.get(pk=request.POST['22']).letter
        user_answer_input.append(submitted_answer22)
        question_22 = mcq_paper_selected_set.get(question_number_key__question_number = 22)
        if str(submitted_answer22) == str(question_22.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_22.question_number_key.question_number)
            
            
            
        submitted_answer23 = PossibleLetters.objects.get(pk=request.POST['23']).letter
        user_answer_input.append(submitted_answer23)
        question_23 = mcq_paper_selected_set.get(question_number_key__question_number = 23)
        if str(submitted_answer23) == str(question_23.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_23.question_number_key.question_number)
            
        
            
        submitted_answer24 = PossibleLetters.objects.get(pk=request.POST['24']).letter
        user_answer_input.append(submitted_answer24)
        question_24 = mcq_paper_selected_set.get(question_number_key__question_number = 24)
        if str(submitted_answer24) == str(question_24.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_24.question_number_key.question_number)
            
            
            
        submitted_answer25 = PossibleLetters.objects.get(pk=request.POST['25']).letter
        user_answer_input.append(submitted_answer25)
        question_25 = mcq_paper_selected_set.get(question_number_key__question_number = 25)
        if str(submitted_answer25) == str(question_25.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_25.question_number_key.question_number)
            
            
            
        submitted_answer26 = PossibleLetters.objects.get(pk=request.POST['26']).letter
        user_answer_input.append(submitted_answer26)
        question_26 = mcq_paper_selected_set.get(question_number_key__question_number = 26)
        if str(submitted_answer26) == str(question_26.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_26.question_number_key.question_number)
            
            
            
        submitted_answer27 = PossibleLetters.objects.get(pk=request.POST['27']).letter
        user_answer_input.append(submitted_answer27)
        question_27 = mcq_paper_selected_set.get(question_number_key__question_number = 27)
        if str(submitted_answer27) == str(question_27.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_27.question_number_key.question_number)
            
            
            
        submitted_answer28 = PossibleLetters.objects.get(pk=request.POST['28']).letter
        user_answer_input.append(submitted_answer28)
        question_28 = mcq_paper_selected_set.get(question_number_key__question_number = 28)
        if str(submitted_answer28) == str(question_28.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_28.question_number_key.question_number)
            
            
            
        submitted_answer29 = PossibleLetters.objects.get(pk=request.POST['29']).letter
        user_answer_input.append(submitted_answer29)
        question_29 = mcq_paper_selected_set.get(question_number_key__question_number = 29)
        if str(submitted_answer29) == str(question_29.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_29.question_number_key.question_number)
            
            
            
            
        submitted_answer30 = PossibleLetters.objects.get(pk=request.POST['30']).letter
        user_answer_input.append(submitted_answer30)
        question_30 = mcq_paper_selected_set.get(question_number_key__question_number = 30)
        if str(submitted_answer30) == str(question_30.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_30.question_number_key.question_number)
            
            
            
        submitted_answer31 = PossibleLetters.objects.get(pk=request.POST['31']).letter
        user_answer_input.append(submitted_answer31)
        question_31 = mcq_paper_selected_set.get(question_number_key__question_number = 31)
        if str(submitted_answer31) == str(question_31.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_31.question_number_key.question_number)
            
            
            
        submitted_answer32 = PossibleLetters.objects.get(pk=request.POST['32']).letter
        user_answer_input.append(submitted_answer32)
        question_32 = mcq_paper_selected_set.get(question_number_key__question_number = 32)
        if str(submitted_answer32) == str(question_32.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_32.question_number_key.question_number)
            
            
            
        submitted_answer33 = PossibleLetters.objects.get(pk=request.POST['33']).letter
        user_answer_input.append(submitted_answer33)
        question_33 = mcq_paper_selected_set.get(question_number_key__question_number = 33)
        if str(submitted_answer33) == str(question_33.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_33.question_number_key.question_number)
            
            
            
        submitted_answer34 = PossibleLetters.objects.get(pk=request.POST['34']).letter
        user_answer_input.append(submitted_answer34)
        question_34 = mcq_paper_selected_set.get(question_number_key__question_number = 34)
        if str(submitted_answer34) == str(question_34.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_34.question_number_key.question_number)
            
            
            
        submitted_answer35 = PossibleLetters.objects.get(pk=request.POST['35']).letter
        user_answer_input.append(submitted_answer35)
        question_35 = mcq_paper_selected_set.get(question_number_key__question_number = 35)
        if str(submitted_answer35) == str(question_35.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_35.question_number_key.question_number)
            
            
            
        submitted_answer36 = PossibleLetters.objects.get(pk=request.POST['36']).letter
        user_answer_input.append(submitted_answer36)
        question_36 = mcq_paper_selected_set.get(question_number_key__question_number = 36)
        if str(submitted_answer36) == str(question_36.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_36.question_number_key.question_number)
            
            
            
        submitted_answer37 = PossibleLetters.objects.get(pk=request.POST['37']).letter
        user_answer_input.append(submitted_answer37)
        question_37 = mcq_paper_selected_set.get(question_number_key__question_number = 37)
        if str(submitted_answer37) == str(question_37.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_37.question_number_key.question_number)
            
            
            
        submitted_answer38 = PossibleLetters.objects.get(pk=request.POST['38']).letter
        user_answer_input.append(submitted_answer38)
        question_38 = mcq_paper_selected_set.get(question_number_key__question_number = 38)
        if str(submitted_answer38) == str(question_38.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_38.question_number_key.question_number)
            
            
            
        submitted_answer39 = PossibleLetters.objects.get(pk=request.POST['39']).letter
        user_answer_input.append(submitted_answer39)
        question_39 = mcq_paper_selected_set.get(question_number_key__question_number = 39)
        if str(submitted_answer39) == str(question_39.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_39.question_number_key.question_number)
            
            
            
            
        submitted_answer40 = PossibleLetters.objects.get(pk=request.POST['40']).letter
        user_answer_input.append(submitted_answer40)
        question_40 = mcq_paper_selected_set.get(question_number_key__question_number = 40)
        if str(submitted_answer40) == str(question_40.question_answer_key):
            score += 1
        else:
            wrong_question.append(question_40.question_number_key.question_number)
            
            
        percentage = ''
        percentage = round((score/40)*100,1)
        
    grade = ''
    
    if mcq_paper_selected.A_raw_mark_req:
            
        if score >= mcq_paper_selected.A_raw_mark_req:
            grade = 'A'
            
        elif score >= mcq_paper_selected.B_raw_mar_req:
            grade = 'B'
            
        elif score >= mcq_paper_selected.C_raw_mar_req:
            grade = 'C'
        
        elif score >= mcq_paper_selected.D_raw_mar_req:
            grade = 'D'
            
        elif score >= mcq_paper_selected.E_raw_mar_req:
            grade = 'E'
            
        else:
            grade = 'Ungraded'
        

    

           
    context = {
        'score' : score,
        'grade' : grade,
        'wrong_question':wrong_question,
        'website_logo':website_logo,
        'mcq_paper_selected':mcq_paper_selected,
        'mcq_paper_selected_set':mcq_paper_selected_set,
        'percentage': percentage,
        'user_answer_input':user_answer_input,
        
    }
            
    return render(request,'examsolution/test_grading.html',context)


# Test Yourself ends here

# College view

def worksheets(request):

    website_logo = website_pics.objects.get(id=1)
    context = {
        'website_logo':website_logo,
    }
    
    return render(request, 'examsolution/worksheet.html', context)

# Contact PiiLearn view

def contact_us(request):
    website_logo = website_pics.objects.get(id=1)
    
    if request.method == "POST":
        contact_instance = ContactUsInfo()
        sender_name = request.POST.get('sender_name')
        sender_email = request.POST.get('sender_email')
        sender_message = request.POST.get('sender_message')
        
        contact_instance.sender_name = sender_name
        contact_instance.sender_email = sender_email
        contact_instance.sender_message = sender_message
        
        contact_instance.save()
        
        return render(request,'examsolution/message_sent_confrimation.html',{'sender_name':sender_name,'website_logo':website_logo})
        
    
    
    context = {
       'website_logo':website_logo,
    }
    
    return render(request, 'examsolution/contact_us.html', context)

def about_us(request):
  
    website_logo = website_pics.objects.get(id=1)
    placeholderpic = people_image.objects.get(name_of_pic='placeholder')
    
    context = {
       'website_logo':website_logo,
       'placeholderpic' :placeholderpic,
    }
    
    return render(request,'examsolution/about_us.html',context)

def privacy(request):
    
    website_logo = website_pics.objects.get(id=1)
    context = {
       'website_logo':website_logo,
    }
    
    return render(request,'examsolution/privacy.html', context)

def terms_of_use(request):
    
    website_logo = website_pics.objects.get(id=1)
    context = {
       'website_logo':website_logo,
    }
    
    return render(request, 'examsolution/terms_of_use.html',context)

def site_maps_view(request):
    return render(request,'examsolution/sitemap.xml')