from cgitb import html
from email import message
from django.http import Http404, HttpResponse, HttpResponseRedirect
import datetime as dt
from django.shortcuts import render, redirect
from .models import Article, NewsLetterRecepients
from .forms import NewsLetterForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required


# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')

def news_of_day(request):
    date = dt.date.today()
    news = Article.today_news()
    print(news)

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecepients(name = name, email = email)
            recipient.save()
            HttpResponseRedirect('news_of_day')
            send_welcome_email(name, email )
    else:
        form = NewsLetterForm()    
 
    return render(request, 'all-news/today_news.html', {"date":date, "news": news, "letterForm":form}) 

def convert_dates(dates):
    #Function that gets the weekday number of the date
    day_number = dt.date.weekday(dates)

    days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',"Sunday"]  
    #Returning the actual day of the week
    day = days[day_number] 
    return day  

def past_days_news(request, past_date):
    #Converts data from the string url
    try:
        date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
    except:
        #Raise 404 error when ValueError is thrown
        raise Http404()    

    if date == dt.date.today():
        return redirect(news_of_day)

    news = Article.day_news(date) 
    return render(request, 'all-news/past_news.html', {"date": date, "news": news})

def search_results(request):

    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'all-news/search.html',{"message":message,"articles": searched_articles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})

@login_required(login_url='/accounts/login/')
def article(request, article_id):
        try:
            article = Article.objects.get(id = article_id)

        except:
            raise Http404()

        return render(request, 'all-news/article.html', {"article":article})    
