from django.db import models

# Create your models here.

class Year(models.Model):
    year = models.IntegerField()
 

    def __str__(self):
        return str(self.year)
    
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
    question_directory = models.FileField(null=True)
    answer_name = models.CharField(max_length=200)
    answer_directory = models.FileField(null=True)
    detailed_answer_link = models.CharField(max_length=500, blank=True, null=True)
    video_explanation_link = models.CharField(max_length=500, blank=True, null=True)
    exam_report_comment = models.CharField(max_length=2000, blank=True)

    
    def __str__(self):
        return self.board_sub_topic_key.subject_key.exam_board_key.exam_board + " " + self.board_sub_topic_key.subject_key.subject + " " + str(self.year_key.year) + " " + self.session_key.session + " " + str(self.board_sub_topic_key.paper_num_key.paper_num) + " " + self.board_sub_topic_key.topic + " (" + self.question_name + ") " + " (" + self.answer_name + ") "
    

class FullQuestionAnswer(models.Model):
    subject_key = models.ForeignKey(Subject, on_delete=models.CASCADE, null='False')
    year_key = models.ForeignKey(Year, on_delete=models.CASCADE)
    session_key = models.ForeignKey(Session, on_delete=models.CASCADE)
    full_question_name = models.CharField(max_length=200)
    full_question_link = models.CharField(max_length=500)
    full_answersheet_name = models.CharField(max_length=200)
    full_answersheet_link = models.CharField(max_length=500)
    
    def __str__(self):
        return str(self.year_key.year) + " (" + self.full_question_name + ") " + " (" + self.full_answersheet_name + ") "


