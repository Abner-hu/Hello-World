# -*- coding: utf-8 -*-
 
import datetime
from django.http import HttpResponse
 
from reportlab.pdfgen import canvas

from django.http import HttpResponse

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import Context, loader
from poll.models import Poll,Choice
from django.core.urlresolvers import reverse

def index(request):
    latest_poll_list = Poll.objects.order_by('-pub_date')[:5]  #  读取近5个更新的问题
    template = loader.get_template('poll/index.html')
    context = Context({
        'latest_poll_list': latest_poll_list,
    })                                              
    return HttpResponse(template.render(context))   # 调用index.html模板

def detail(request,poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)         # 读取指定对象
    template = loader.get_template('poll/detail.html') 
    context = Context({
        'poll': poll,
    })
    return HttpResponse(template.render(context))     # 调用detail.html （1）
        
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)    
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice']) 
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
        })  # 调用detail.html进行返回 （2）
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('poll:result', args=(poll.id,)))   # 重定向到poll:result  reverse(根据命名url和参数拼装出一个url请求)

def result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'poll/result.html', {'poll': poll})   # 调用result.html模板

def hello_pdf(request):

    # Create the HttpResponse object with the appropriate PDF headers.
#    response = HttpResponse(mimetype='application/pdf')
    response = HttpResponse()

    response['Content-Disposition'] = 'attachment; filename=hello.pdf'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()

    p.save()

    return response

def first_page(request):
    now = datetime.datetime.now()
    #now = "Hello World"

    html = "<html><body>It is: %s.</body></html>" % now

    #return HttpResponse("&lt;p&gt;Hello World&lt;/p&gt;")
    return HttpResponse(html)

def login(request):

    try:

        m = Member.objects.get(username__exact=request.POST['username'])

        if m.password == request.POST['password']:

            request.session['member_id'] = m.id

            return HttpResponse("You're logged in.")

    except Member.DoesNotExist:

        return HttpResponse("Your username and password didn't match.")

