from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from ..models import Board

def index(request):
    page = request.GET.get('page','1') # 페이지
    kw = request.GET.get('kw','') # 검색어
    board_list = Board.objects.order_by('-create_date')
    if kw:
        board_list = board_list.filter(
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) | # 내용 검색
            Q(reply__content__icontains=kw) | # 댓글 내용 검색
            Q(author__username__icontains=kw) | # 게시판 글쓴이 검색
            Q(reply__author__username__icontains=kw)  # 댓글 글쓴이 검색
        ).distinct()
    paginator = Paginator(board_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'board_list':page_obj, 'page':page, 'kw':kw}
    return render(request,'board/board_list.html', context)

def detail(request,board_id):
    board = get_object_or_404(Board, pk=board_id)
    context = {'board':board,}
    return render(request,'board/board_detail.html', context)