from django.shortcuts import render,redirect
from .models import Instrument, Entry
from .forms import InstrumentForm, EntryForm
import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.
def index(request):
    """学习笔记的主页"""
    """学习笔记的主页"""
    current_time = datetime.datetime.now()
    context = {'current_time': current_time}
    return render(request, 'investing_logs/index.html',context)

@login_required
def instruments(request):
    """显示所有的主题"""
    instruments = Instrument.objects.filter(owner=request.user).order_by('date_added')
    context = {'instruments': instruments}
    return render(request, 'investing_logs/instruments.html',context)

@login_required
def instrument(request, instrument_id):
    """显示单个主题及其所有的条目"""
    instrument = Instrument.objects.get(id=instrument_id)
    # 确认请求的主题属于当前用户
    if instrument.owner != request.user:
        raise Http404
    entries = instrument.entry_set.order_by('-date_added')
    context = {'instrument': instrument, 'entries': entries}
    return render(request, 'investing_logs/instrument.html',context)

@login_required
def new_instrument(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = InstrumentForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = InstrumentForm(data=request.POST)
        if form.is_valid():
            new_instrument = form.save(commit=False)
            new_instrument.owner = request.user
            new_instrument.save()

            return redirect('investing_logs:instruments')
    # 显示空表单或指出表单数据无效
    context = {'form': form}
    return render(request, 'investing_logs/new_instrument.html',context)

@login_required
def new_entry(request, instrument_id):
    """在特定主题中添加新条目"""
    instrument = Instrument.objects.get(id=instrument_id)
    if request.method != 'POST':
        # 未提交数据：创建一个空表单
        form = EntryForm()
    else:
        # POST 提交的数据：对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.instrument = instrument
            new_entry.save()
            return redirect('investing_logs:instrument', instrument_id=instrument_id)
    # 显示空表单或指出表单数据无效
    context = {'instrument': instrument, 'form': form}
    return render(request, 'investing_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有的条目"""
    entry = Entry.objects.get(id=entry_id)
    instrument = entry.instrument
    if instrument.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # 初次请求：使用当前的条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST 提交的数据：对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('investing_logs:instrument', instrument_id=instrument.id)
    context = {'entry': entry, 'instrument': instrument, 'form': form}
    return render(request, 'investing_logs/edit_entry.html',    context)