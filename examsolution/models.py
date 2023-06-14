from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Year(models.Model):
    year = models.IntegerField()
 
    def __str__(self):
        return str(self.year)
    
    class Meta:
        ordering = ['-year']
    
class ExamBoard(models.Model):
    exam_board = models.CharField(max_length=200)
    
    def __str__(self):
        return self.exam_board
    
class Session(models.Model):
    session = models.CharField(max_length=200)
    
    def __str__(self):
        return self.session
    
class Paper(models.Model):
    paper_num = models.IntegerField()
    
    def __str__(self):
        return str(self.paper_num)
    
class Subject(models.Model):
    exam_board_key = models.ForeignKey(ExamBoard, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    
    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ['subject']
    
class BoardSubTopic(models.Model):
    subject_key = models.ForeignKey(Subject, on_delete=models.CASCADE, null='False')
    paper_num_key = models.ForeignKey(Paper, on_delete=models.CASCADE, null='False')
    topic = models.CharField(max_length=200)
    
    def __str__(self):
        return self.subject_key.subject + " " + self.topic + "(" + str(self.paper_num_key.paper_num) + ")" 
    
    
class QuestionAnswer(models.Model):
    board_sub_topic_key = models.ForeignKey(BoardSubTopic, on_delete=models.CASCADE)
    year_key = models.ForeignKey(Year, on_delete=models.CASCADE)
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=200)
    question_directory = models.FileField(null=True,upload_to='TopicalQuestions')
    answer_name = models.CharField(max_length=200)
    answer_directory = models.FileField(null=True,upload_to='TopicalAnswers')
    detailed_answer_link = models.CharField(max_length=500, blank=True, null=True)
    video_explanation_link = models.CharField(max_length=500, blank=True, null=True)
    exam_report_comment = models.CharField(max_length=20000, blank=True)

    
    def __str__(self):
        return self.board_sub_topic_key.subject_key.exam_board_key.exam_board + " " + self.board_sub_topic_key.subject_key.subject + " " + str(self.year_key.year) + " " + self.session_key.session + " " + str(self.board_sub_topic_key.paper_num_key.paper_num) + " " + self.board_sub_topic_key.topic + " (" + self.question_name + ") " + " (" + self.answer_name + ") "
    

class FullQuestionAnswer(models.Model):
    subject_key = models.ForeignKey(Subject, on_delete=models.CASCADE, null='False')
    year_key = models.ForeignKey(Year, on_delete=models.CASCADE)
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)
    full_question_name = models.CharField(max_length=200)
    google_drive_question_link = models.URLField(max_length=200,null=True, blank=True)
    full_question_directory = models.FileField(null=True,upload_to='FullQuestionPaper')
    full_answersheet_name = models.CharField(max_length=200)
    google_drive_answer_link = models.URLField(max_length=200,null=True, blank=True)
    full_answersheet_directory = models.FileField(null=True,upload_to='FullMarkScheme')
    paper_number = models.ForeignKey(Paper,on_delete=models.CASCADE,blank=True,null=True)
    A_raw_mark_req = models.IntegerField(blank=True, null=True)
    B_raw_mar_req = models.IntegerField(blank=True, null=True)
    C_raw_mar_req = models.IntegerField(blank=True, null=True)
    D_raw_mar_req = models.IntegerField(blank=True, null=True)
    E_raw_mar_req = models.IntegerField(blank=True, null=True)
    general_exam_report_cmnt = models.CharField(max_length=20000,blank=True, null=True)
    
    class Meta:
        ordering = ['full_question_name']
    
    
    def __str__(self):
        return str(self.year_key.year) + " ("+ self.session_key.session + ") "+ " " + self.subject_key.subject + " " + " (" + self.full_question_name + ") " + " (" + self.full_answersheet_name + ") "

    
class ReportThreshPrep(models.Model):
    subject_key = models.ForeignKey(Subject,on_delete=models.CASCADE)
    year_key = models.ForeignKey(Year, on_delete=models.CASCADE)
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)
    extra_name = models.CharField(max_length=500)
    extra_directory = models.FileField(null=True,upload_to='ReportThreshPrep')
    
    def __str__(self):
        return self.extra_name + " " + str(self.year_key.year) + " ("+ self.session_key.session + ") "+ " " + self.subject_key.subject + " "
    
class PossibleLetters(models.Model):
    letter = models.CharField(max_length=1)
    
    def __str__(self):
        return self.letter
    
class PossibleQuestionNumber(models.Model):
    question_number = models.IntegerField()
    
    def __str__(self):
        return str(self.question_number)
    
class PaperOneAnswers(models.Model):
    paper_one_name_key = models.ForeignKey(FullQuestionAnswer,on_delete=models.CASCADE)
    question_number_key = models.ForeignKey(PossibleQuestionNumber,on_delete=models.CASCADE)
    question_answer_key = models.ForeignKey(PossibleLetters,on_delete=models.CASCADE)
    question_category = models.CharField(max_length=500,null=True,blank=True)
    question_examreportcmt = models.CharField(max_length=20000,null=True,blank=True)
    question_video_explanation = models.URLField(max_length=1000,null=True,blank=True)
    
    def __str__(self):
        return str(self.question_number_key.question_number) + " ("+ self.question_answer_key.letter +") " +" ("+ self.paper_one_name_key.full_question_name + ") "
    
class website_pics(models.Model):
    website_logo = models.ImageField(null=True,upload_to='WesbitePics')

class home_image(models.Model):
    home_logo = models.ImageField(null=True,upload_to='WesbitePics')


class people_image(models.Model):
    name_of_pic = models.CharField(max_length=2000)
    picture = models.ImageField(null=True,upload_to='WesbitePics')
    
    def __str__(self):
        return self.name_of_pic
    
# user related tables

class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']
    
class UserProgressRecord(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject_of_paper_written = models.CharField(max_length=200,null=True,blank=True)
    paper_written = models.CharField(max_length=200)
    raw_mark = models.IntegerField(null=True, blank=True)
    percentage = models.CharField(max_length=50,null=True, blank=True)
    letter_grade = models.CharField(max_length=1,null=True, blank=True)
    hours_taken = models.IntegerField(null=True, blank=True)
    minutes_taken = models.IntegerField(null=True, blank=True)
    questions_failed = models.CharField(max_length=2000,null=True, blank=True)
    date_completed = models.DateTimeField(auto_now_add=True)
    subject_of_paper_written = models.CharField(max_length=200,null=True,blank=True)
    user_answer_input = models.CharField(max_length=2000,null=True,blank=True)
    
    def __str__(self):
        return self.paper_written
    
    class Meta:
        ordering = ['-date_completed']

class ContactUsInfo(models.Model):
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    sender_message = models.TextField()
    
    def __str__(self):
        return self.sender_name