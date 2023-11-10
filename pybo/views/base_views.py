import logging

from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from ..models import Question, Comment

logger = logging.getLogger('pybo')


def index(request):
    logger.info("INFO 레벨로 출력")
    # 입력 params
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'pending':
        question_list = Question.objects.filter(status='pending').order_by('-create_date')
    elif so == 'approved':
        question_list = Question.objects.filter(status='approved').order_by('-create_date')
    elif so == 'rejected':
        question_list = Question.objects.filter(status='rejected').order_by('-create_date')
    elif so == 'on_hold':
        question_list = Question.objects.filter(status='holding').order_by('-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')


    # 검색
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw) |# 답변 글쓴이검색
            Q(question_hash__icontains=kw) # 해시값 검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}  # <------ so 추가
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # 질문 댓글 pagination 해야함.
    page = request.GET.get('page', '1')
    question = get_object_or_404(Question, pk=question_id)
    so = request.GET.get('so', 'recent')  # 정렬기준
    basic_comment_list = Comment.objects.filter(question = question)

    # 정렬

    if so == 'pending':
        comment_list = basic_comment_list.filter(status='pending').order_by('-create_date')
    elif so == 'approved':
        comment_list = basic_comment_list.filter(status='approved').order_by('-create_date')
    elif so == 'rejected':
        comment_list = basic_comment_list.filter(status='rejected').order_by('-create_date')
    elif so == 'holding':
        comment_list = basic_comment_list.filter(status='holding').order_by('-create_date')
    else:  # recent
        comment_list = basic_comment_list.order_by('-create_date')

    paginator = Paginator(comment_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question': question, 'comment_list' : page_obj, 'page' : page, 'so' : so}

    return render(request, 'pybo/question_detail.html', context)



