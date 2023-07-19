from django.contrib.sitemaps import Sitemap
from examsolution.models import FullQuestionAnswer

# class YearSiteMap(Sitemap):
#     def items(self):
#         return Year.objects.all()
    
#     def lastmod(self,obj):
#         return obj.updated_at

class FullQuestionAnswersSiteMap(Sitemap):
    def items(self):
        return FullQuestionAnswer.objects.all()
    
    def lastmod(self,obj):
        return obj.updated_at