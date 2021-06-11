from django.shortcuts import render, get_object_or_404
from itertools import chain
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from . import forms

# Create your views here.
# from .models import Course, Step
from . import models


def course_list(request):
    # courses = Course.objects.all()
    # output = ','.join(courses)
    # output = ", ".join([str(course) for course in courses])
    courses = models.Course.objects.all()
    email = 'questions@learning_site.com'
    return render(request, 'courses/course_list.html', {'courses': courses,
                                                        'email': email})


def course_detail(request, pk):
    # course = Course.objects.get(pk=pk)
    course = get_object_or_404(models.Course, pk=pk)
    steps = sorted(chain(course.text_set.all(), course.quiz_set.all()),  # 2.3
                         key=lambda step: step.order)
    return render(request, 'courses/course_detail.html',
                  {'course': course,
                   'steps': steps})


# 2.3 def step_detail(request, course_pk, step_pk):
def text_detail(request, course_pk, step_pk):
    # step = get_object_or_404(models.Step, course_id=course_pk, pk=step_pk)
    step = get_object_or_404(models.Text, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/text_detail.html', {'step': step})


# 2.3
def quiz_detail(request, course_pk, step_pk):
    step = get_object_or_404(models.Quiz, course_id=course_pk, pk=step_pk)
    return render(request, 'courses/quiz_detail.html', {'step': step})


# 处理quizzes的视图--添加一个quiz
@login_required
def quiz_create(request, course_pk):
    course = get_object_or_404(models.Course, pk=course_pk)
    form = forms.QuizForm()

    if request.method == 'POST':
        form = forms.QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Quiz added!')
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': course})


# 处理quizzes的视图--编辑一个quiz
@login_required
def quiz_edit(request, course_pk, quiz_pk):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk, course_id=course_pk)
    form = forms.QuizForm(instance=quiz)    # 实例化
    # 处理点击保存键后不会跳转到到同一页面,而是真的将编辑好的内容保存的操作
    # POST是提交request
    if request.method == 'POST':
        form = forms.QuizForm(instance=quiz, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Update {}'.format(form.cleaned_data['title']))
            return HttpResponseRedirect(quiz.get_absolute_url())
    return render(request, 'courses/quiz_form.html', {'form': form, 'course': quiz.course})


@login_required
def create_question(request, quiz_pk, question_type):
    quiz = get_object_or_404(models.Quiz, pk=quiz_pk)
    if question_type == 'tf':                       # 这里我们要知道应该用哪一种form
        form_class = forms.TrueFalseQuestionForm
    else:
        form_class = forms.MultipleChoiceQuestionForm

    form = form_class()
    answer_forms = forms.AnswerInlineFormSet(
        queryset=models.Answer.objects.none()   # 4.4因为我们是创建一个question,这个question没有答案,要一个空的queryset
    )

    if request.method == 'POST':         # 这个部分跟我们在创建quizzes的视图中做得是一样的
        form = form_class(request.POST)  # 如果上面实例化了, 这里就不能这样做了
        answer_forms = forms.AnswerInlineFormSet(  # 4.4
            request.POST,
            queryset=models.Answer.objects.none()
        )
        if form.is_valid() and answer_forms.is_valid():  # 4.4 answer_forms也是valid的话
        # if form.is_valid():
            question = form.save(commit=False)           # 创建一个问题
            question.quiz = quiz
            question.save()
            answers = answer_forms.save(commit=False)    # 4.4
            for answer in answers:                       # 4.4
                answer.question = question               # 4.4
                answer.save()                            # 4.4
            messages.success(request, 'Added question')
            return HttpResponseRedirect(quiz.get_absolute_url())

    return render(request, 'courses/question_form.html', {'quiz': quiz,
                                                          'form': form,
                                                          'formset': answer_forms})


@login_required
def edit_question(request, quiz_pk, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk, quiz_id=quiz_pk)
    if hasattr(question, 'truefalsequestion'):
        form_class = forms.TrueFalseQuestionForm
        question = question.truefalsequestion               #这个确保编辑问题是保存了shuffle answer这个选项
    else:
        form_class = forms.MultipleChoiceQuestionForm
        question = question.multiplechoicequestion
    form = form_class(instance=question)
    answer_forms = forms.AnswerInlineFormSet(  # 4.4
        queryset=form.instance.answer_set.all()
    )

    # 保存
    if request.method == 'POST':
        form = form_class(request.POST, instance=question)
        answer_forms = forms.AnswerInlineFormSet(    # 4.4
            request.POST,
            queryset=form.instance.answer_set.all()
        )
        #if form.is_valid():
        if form.is_valid() and answer_forms.is_valid():    # 4.4 answer_forms也是valid的
            form.save()
            answers = answer_forms.save(commit=False)      # 4.4
            for answer in answers:                         # 4.4
                answer.question = question                 # 4.4
                answer.save()                              # 4.4
            # for answer in answer_forms.deleted_objects:    # 4.6
            #     answer.delete()
            messages.success(request, 'Updated question')
            return HttpResponseRedirect(question.quiz.get_absolute_url())
    return render(request, 'courses/question_form.html', {
        'form': form,
        'quiz': question.quiz,
        'formset': answer_forms})                          # 4.4


@login_required
def answer_form(request, question_pk, answer_pk=None):
    question = get_object_or_404(models.Question, pk=question_pk)
    formset = forms.AnswerFormSet(queryset=question.answer_set.all())

    if request.method == 'POST':
        formset = forms.AnswerFormSet(request.POST, queryset=question.answer_set.all())

        if formset.is_valid():
            answers = formset.save(commit=False)  # from here course_id

            for answer in answers:
                answer.question = question
                answer.save()                    # to here,  =  formset.save()
        
            messages.success(request, 'added answers')
            return HttpResponseRedirect(question.quiz.get_absolute_url())

    return render(request, 'courses/answer_form.html', {'question': question, 'formset': formset})

    # form = forms.AnswerForm()  # 改成formset

    # # 这个if POST部分在4.1视频之前如下, 上面那样
    # if request.method == 'POST':
    #     form = forms.AnswerForm(request.POST)
    #
    #     if form.is_valid():
    #         answer = form.save(commit=False)
    #         answer.question = question
    #         answer.save()
    #         messages.success(request, 'Answer Added!')
    #         return HttpResponseRedirect(question.get_absolute_url())

    # 在3.9中并没有这部份, 以及上面answer_pk=None这个部分, 但是4.1的视频中出现了
    # 但是4.1视频去把这部个去掉了, 因为我们要编辑一堆答案而不是一个答案
    # 然后再去掉一整部分
    # if answer_pk:
    #     answer = get_object_or_404(models.Answer, pk=answer_pk)
    #     form = forms.AnswerForm(instance=answer)
    #
    # if request.method == 'POST':
    #     if answer_pk:
    #         form = forms.AnswerForm(request.POST, instance=answer)
    #     else:
    #         form = forms.AnswerForm(request.POST)
    #     if form.is_valid():
    #         answer = form.save(commit=False)
    #         answer.question = question
    #         answer.save()
    #         messages.success(request, 'Answer Added!')
    #         return HttpResponseRedirect(question.get_absolute_url())

    # return render(request, 'courses/answer_form.html', {'question': question, 'form': form})