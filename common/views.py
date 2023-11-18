from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import UserForm
import secrets
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def generate_symmetric_key(key_length=16):
    key = secrets.token_hex(key_length)
    return key

pos = {"외부인" : 0, "사원" : 1, "대리" : 2, "과장" : 3, "차장": 4, "부장": 5}


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            position = request.POST.get("position")
            user = form.save(commit=False)

            if position in pos:
                user.last_name = pos[position]
            else:
                user.last_name = pos["등록되지않음"]

            # 공개 키 생성 및 설정
            symmetric_key = generate_symmetric_key()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # user.first_name = symmetric_key
            user.first_name = f"{symmetric_key} {raw_password}"
            subject = "대칭키 공유"  # 타이틀
            to = [user.email]  # 수신할 이메일 주소
            from_email = "qudrb24@naver.com"  # 발신할 이메일 주소
            message = symmetric_key

            email = EmailMessage()
            email.subject = subject
            email.body = f"{user.username}님의 대칭키 : {message}"
            email.from_email = from_email
            email.to = to
            email.send()



            user.save()
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, "common/signup.html", { 'form' : form })

