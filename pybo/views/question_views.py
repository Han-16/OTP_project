from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.utils import timezone
import hashlib
from ..forms import QuestionForm
from ..models import Question
import qrcode


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # 추가한 속성 author 적용
            question.create_date = timezone.now()
            sha256_hash = hashlib.sha256()
            data = f"{question.subject}||{question.content}"
            sha256_hash.update(data.encode('utf-8'))
            question.question_hash = sha256_hash.hexdigest()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.modify_count += 1
            sha256_hash = hashlib.sha256()
            data = f"{question.subject}||{question.content}||{question.author}||{question.create_date}||{question.modify_date}"
            sha256_hash.update(data.encode('utf-8'))
            question.question_hash = sha256_hash.hexdigest()


            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')




@login_required(login_url="common:login")
def question_decision(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.user.last_name <= question.author.last_name:
        messages.error(request, "권한이 없습니다.")
        return redirect('pybo:index')

    status = request.GET.get('status')

    if status not in ['approved', 'rejected', 'holding']:
        return HttpResponseBadRequest("Invalid status parameter")

    question.status = status
    question.save()
    return redirect('pybo:index')


@login_required(login_url="common:login")
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return redirect('pybo:detail', question_id=question.id)
