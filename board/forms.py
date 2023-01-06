from django import forms
from .models import Board, Reply

class BoardForm(forms.ModelForm):

    class Meta:
        model = Board # 사용할 모델
        fields = ['subject','content'] # BoardForm에서 사용할 Board 모델의 속성

        labels = {
            'subject':'제목',
            'content':'내용',
        }

class ReplyForm(forms.ModelForm):

    class Meta:
        model = Reply
        fields = ['content']

        labels = {
            'content':'답글내용'
        }