from unicodedata import name
from django.test import TestCase
from .models import Editor, Tag, Article
import datetime as dt

# Create your tests here.
class EditorTestClass(TestCase):
    #SetUp method
    def setUp(self):
         self.james= Editor(first_name = 'James', last_name ='Muriuki', email ='james@moringaschool.com')

    #testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.james, Editor))   
    
    #Testing saving method
    def test_save_method(self):
        self.james.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors)>0)

class TagTestClass(TestCase):
    def setUp(self):
        self.sports = Tag(name = 'sports')

    def test_instance(self):
        self.assertTrue(isinstance(self.sports, Tag))    


class ArticleTestCase(TestCase):
     def setUp(self):
        # Creating a new editor and saving it
        self.james= Editor(first_name = 'James', last_name ='Muriuki', email ='james@moringaschool.com')
        self.james.save_editor()

     # Creating a new tag and saving it
        self.new_tag = Tag(name = 'testing')
        self.new_tag.save()
        self.new_article= Article(title = 'Test Article',post = 'This is a random test Post',editor = self.james)
        self.new_article.save()

        self.new_article.tags.add(self.new_tag)   

     def tearDown(self):
        Editor.objects.all().delete()
        Tag.objects.all().delete()
        Article.objects.all().delete()

     def test_get_news_today(self):
         today_news = Article.today_news()
         self.assertTrue(len(today_news)>0)   

     def test_get_news_by_day(self):
        test_date = '2000-12-30'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date) == 0)

  
    