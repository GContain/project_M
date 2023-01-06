from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..models import Board
from ..forms import BoardForm

@login_required(login_url='common:login')
def board_create(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user # author 속성에 로그인 계정 저장
            board.create_date = timezone.now()
            board.save()
            return redirect('board:index')
    else:
        form = BoardForm()
    context = {'form':form}
    return render(request,'board/board_form.html',{'form':form})

@login_required(login_url='common:login')
def board_modify(request,board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다!')
        return redirect('board:detail',board_id=board.id)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.modify_date = timezone.now() # 수정일시 저장
            board.save()
            return redirect('board:detail',board_id=board.id)
    else:
        form = BoardForm(instance=board)
    context = {'form':form}
    return render(request, 'board/board_form.html', context)

@login_required(login_url='common:login')
def board_delete(request,board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages(request, '삭제권한이 없습니다!')
        return redirect('board:detail', board_id=board.id)
    board.delete()
    return redirect('board:index')

@login_required(login_url='common:login')
def board_vote(request,board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user == board.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다!')
    else:
        board.voter.add(request.user)
    return redirect('board:detail',board_id=board.id) 