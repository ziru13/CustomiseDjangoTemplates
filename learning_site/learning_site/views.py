from django.contrib import messages
from django.core.mail import send_mail
# from django.core.urlresolvers import reverse  # django2.0以上删除了
from django.urls import reverse                 # 改用了这个
from django.http import HttpResponseRedirect

from django.shortcuts import HttpResponse, render

# from .forms import SuggestionForm
from . import forms


def hello_world(request):
    return render(request, 'home.html')


def suggestion_view(request):
    form = forms.SuggestionForm()    # 1.4 实例化我们SuggestionForm中的实例
    if request.method == 'POST':  # 1.6 全大写,如果是一个POST,
        form = forms.SuggestionForm(request.POST)  # 1.6 我们给form从request.POST中得到的数据,此时request.POST就像一个字典
        if form.is_valid():     # 1.6 验证数据是有效的
            send_mail(          # 1.6 当别人创建一个suggestion时,给他发一个email,在setting中使用EMAIL_BACKEND和EMAIL_FILE_PATH
                'Suggestion from {}'.format(form.cleaned_data['name']),    # 1.6 subject-对象, cleaned_data时valid之后好的data
                form.cleaned_data['suggestion'],  # 1.6 邮件的body
                '{name} < {email}>'.format(**form.cleaned_data),  # 1.6 邮件发件人
                ['ziru.fish@gmail.com']  # 1.6 邮件收件人
            )
            messages.add_message(request, messages.SUCCESS,  # 1.6 提交后网站的提示信息
                                 'Thanks for your suggestion!')
            return HttpResponseRedirect(reverse('suggestion'))  # 1.6 回到suggestion这个url,redirect是一个get request,所以得到的是一个空的form
    return render(request, 'suggestion_form.html', {'form': form})  # 1.4一个普通的render
