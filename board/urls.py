from django.urls import path
from .views import base_views, board_views, reply_views

app_name = 'board'
urlpatterns = [
    # base_views
    path('',base_views.index,name='index'),
    path('<int:board_id>/',base_views.detail,name='detail'),

    # board_views
    path('board/create/',board_views.board_create,name='board_create'),
    path('board/modify/<int:board_id>/',board_views.board_modify,name='board_modify'),
    path('board/delete/<int:board_id>/',board_views.board_delete,name='board_delete'),
    path('board/vote/<int:board_id>/',board_views.board_vote,name='board_vote'),

    # reply_views
    path('reply/create/<int:board_id>/',reply_views.reply_create,name='reply_create'),
    path('reply/modify/<int:reply_id>/',reply_views.reply_modify,name='reply_modify'),
    path('reply/delete/<int:reply_id>/',reply_views.reply_delete,name='reply_delete'),
    path('reply/vote/<int:reply_id>/',reply_views.reply_vote,name='reply_vote'),

]