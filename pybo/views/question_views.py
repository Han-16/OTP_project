from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.utils import timezone
import hashlib
from ..forms import QuestionForm
from ..models import Question
import hmac
from ..ocra import OCRA
import random
from django.http import JsonResponse
from datetime import datetime


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        key = request.user.first_name.split()[0]
        subject = request.POST.get("subject")
        content = request.POST.get("content")
        cli_hmac = request.POST.get('cli_hmac')
        srv_hmac = hmac.new(bytes(key, 'utf-8'), f"{subject}{content}".encode('utf-8'), hashlib.sha256).hexdigest()

        if srv_hmac == cli_hmac:
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user  # 추가한 속성 author 적용
                question.create_date = datetime.now()
                date = question.create_date.strftime('%Y-%m-%d %I:%M')
                sha256_hash = hashlib.sha256()
                data = f"{question.subject}{question.content}{question.author}{date}"
                sha256_hash.update(data.encode('utf-8'))
                question.question_hash = sha256_hash.hexdigest()
                question.save()
                return redirect('pybo:index')
        else:
            messages.error(request, "HMAC값 불일치")
            return render(request, 'pybo/question_form.html', {'form': form})
    else:
        form = QuestionForm()
    context = { 'form': form }
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
            date = question.modify_date.strftime('%Y-%m-%d %I:%M')
            question.modify_count += 1
            sha256_hash = hashlib.sha256()

            data = f"{question.subject}{question.content}{question.author}{date}"
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
        if request.user.is_staff:
            pass
        else:
            messages.error(request, "결재할 수 있는 권한이 없습니다.")
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

def question_ocra(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    key = request.user.first_name.split()[0]

    cli_ocra = request.POST.get('ocra')
    status = request.POST.get('modalButtonClicked')
    pw = request.user.first_name.split()[1]
    t = datetime.now().strftime("%Y-%m-%d %H:%M")
    C = request.POST.get("challengeValue")
    p_h = hashlib.sha1(bytes(pw, 'utf-8')).digest()
    m = question.question_hash
    S_check = bytes(f'{C}{p_h}{m}{t}',encoding='utf8')
    srv_ocra = str(OCRA(key, S_check))
    print(f"t is : {t}")
    print(f"srv_orca : {srv_ocra}")
    print(f"cli_ocra : {cli_ocra}")
    print(f"C : {C}, type : {type(C)}")
    print(f"p_h is : {p_h}")
    print(f"m is : {m}")

    if srv_ocra == cli_ocra:
        print("같음")
        if request.user.last_name <= question.author.last_name:
            if request.user.is_staff:
                pass
            else:
                messages.error(request, "결재할 수 있는 권한이 없습니다.")
                return redirect('pybo:index')

        question.status = status
        question.save()
        return redirect("pybo:index")
    print("안같음")
    messages.error(request, "결재할 수 있는 권한이 없습니다.")
    return redirect('pybo:index')

def determine_qc(request):
    qs = random.randint(1, 100)
    response_data = {'qs' : qs}
    return JsonResponse(response_data)

def open_question_modal(request, question_id):
    challenge_value = random.randint(1000, 9999)  # 랜덤한 챌린지 값 생성
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "pybo:detail", {'question_id' : question.id, 'challenge_value' : challenge_value})

def open_question_modal(request):
    if request.method == 'GET':
        challenge_value = random.randint(1, 9999)
        return JsonResponse({'challenge_value': challenge_value})