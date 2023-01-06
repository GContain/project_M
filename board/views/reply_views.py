from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone

from ..models import Board, Reply
from ..forms import ReplyForm

@login_required(login_url='common:login')
def reply_create(request,board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.method == "POST":
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.author = request.user # author 속성에 로그인 계정 저장
                reply.create_date = timezone.now()
                reply.board = board
                reply.save()
                return redirect('{}#reply_{}'.format(resolve_url('board:detail', board_id=board.id), reply.id))
                    
    else:
        form = ReplyForm()
    context = {'board': board, 'form': form}
    return render(request, 'board/board_detail.html', context)

@login_required(login_url='common:login')
def reply_modify(request,reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user != reply.author:
        messages(request, '수정권한이 없습니다!')
        return redirect('board:detail', board_id=reply.board.id)
    if request.method == "POST":
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.modify_date = timezone.now()
            reply.save()
            return redirect('{}#reply_{}'.format(resolve_url('board:detail', board_id=reply.board.id), reply.id))
    else:
        form = ReplyForm(instance=reply)
    context = {'reply':reply, 'form':form}
    return render(request, 'board/board_form.html', context)

@login_required(login_url='common:login')
def reply_delete(request,reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user != reply.author:
        messages(request, '삭제권한이 없습니다!')
        return redirect('board:detail', board_id=reply.board.id)
    else:
        reply.delete()
    return redirect('board:detail', board_id=reply.board.id)

@login_required(login_url='common:login')
def reply_vote(request,reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    if request.user == reply.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다!')
    else:
        reply.voter.add(request.user)
    return redirect('{}#reply_{}'.format(resolve_url('board:detail', board_id=reply.board.id), reply.id))