import pytz
import datetime

from django.shortcuts import render

from service.models import Timeline
from service.forms import MessageForm, SearchForm

def main_view(request):
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.cleaned_data['message']
            content = Timeline.objects.create(message=msg)
    
    result = Timeline.objects.filter(time__contains=datetime.date.today())
    
    service_time = server_time_check()
    context = {
        'msg_form': form,
        'result': result,
        'service': service_time
    }

    return render(request, 'main.html', context)

def search_view(request):
    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['date']
            result = Timeline.objects.filter(time__contains=query)
            context = {
                'search_form': form,
                'result': result
            }

            return render(request, 'search.html', context)

    return render(request, 'search.html', {'search_form': form})

def server_time_check():
    tz = pytz.timezone('Asia/Seoul')
    seoul = datetime.datetime.now(tz).time()

    service_time = [
        datetime.time(21, 0, 0, tzinfo=tz),
        datetime.time(6, 0, 0, tzinfo=tz)
    ]

    if seoul>service_time[0] or seoul<service_time[1]:
        return True
    else:
        return False
