"""定义 learning_logs 的 URL 模式"""
from django.urls import path
from . import views


app_name = 'investing_logs'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    # 显示所有主题的页面
    path('instruments/', views.instruments, name='instruments'),
    # 特定主题的详细页面
    path('instruments/<int:instrument_id>/', views.instrument, name='instrument'),
    # 用于添加新主题的网页
    path('new_instrument/', views.new_instrument, name='new_instrument'),
    # 用于添加新条目的页面
    path('new_entry/<int:instrument_id>/', views.new_entry, name='new_entry'),
    # 用于编辑条目的页面
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]