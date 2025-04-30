from django.shortcuts import render
from .models import Project, Progress #, progressを入れた4/23【⑥−２】ビューを追加（詳細ページの処理）
from .forms import ProjectForm, ProgressForm
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from datetime import date
from decimal import Decimal
from calendar import monthrange

def project_list(request):
    projects = Project.objects.all().order_by('deadline') #.all()で終わらせてたけどorderbyしたくて追加。締切早い順。('-deadline')にすれば遅い順に、('-progress_rate')にすれば進捗高い順になるけど今回の実装では進捗高い順は多分バグる
    return render(request, 'manga/project_list.html', {'projects': projects})

def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'manga/project_form.html', {'form': form})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    progresses = Progress.objects.filter(project=project).order_by('date')

    #カレンダー追加実装
    today = date.today()
    year = today.year
    month = today.month
    days_in_month = monthrange(year, month)[1] #今月の日数

    #日毎に進捗入力があるかチェック
    progress_dates = progresses.values_list('date', flat=True)
    calender = []
    for day in range(1, days_in_month + 1):
        d = date(year, month, day)
        calender.append({
            'date': d,
            'has_progress': d in progress_dates,
            'color': project.color #プロジェクトに設定された色
        })

    return render(request, 'manga/project_detail.html', {
        'project': project,
        'progresses': progresses,
        'calender': calender,
    })


def progress_add(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.project = project
            progress.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProgressForm()
    return render(request, 'manga/progress_form.html', {
        'form': form,
        'project': project
    })

def progress_today(request, pk):
    project = get_object_or_404(Project, pk=pk)
    today = date.today()

    #すでに今日の分送信済みの場合は追加しない
    if Progress.objects.filter(project=project, date=today).exists():
        #とりあえずリダイレクトだけ。後で覚えてればすでに登録済みのメッセージ出してもいいね
        return redirect('project_detail', pk=project.pk)

    #今日のノルマを自動登録
    Progress.objects.create(
        project=project,
        date=today,
        pages_done=project.today_target_pages
    )
    return redirect('project_detail', pk=project.pk)

def progress_today_confirm(request, pk):
    project = get_object_or_404(Project, pk=pk)
    today = date.today()

    if Progress.objects.filter(project=project, date=today).exists():
        return redirect('project_detail', pk=project.pk)

    try:
        if project.remaining_days == 0:
            floor_value = Decimal(str(project.remaining_pages))
        else:
            floor_value = Decimal(str(project.remaining_pages)) / Decimal(str(project.remaining_days))
    except ZeroDivisionError:
        floor_value = Decimal('0')

    return render(request, 'manga/progress_confirm.html', {
        'project': project,
        'floor_value':floor_value
    })

def progress_today_save(request, pk):
    project = get_object_or_404(Project, pk=pk)
    today = date.today()

    if request.method == 'POST':
        mode = request.POST.get('mode')
        custom_pages = request.POST.get('custom_pages')

        if Progress.objects.filter(project=project, date=today).exists():
            return redirect('project_detail', pk=project.pk)

        if mode == 'ceil':
            pages = Decimal(str(project.today_target_pages))
        elif mode == 'floor':
            pages = Decimal(str(project.remaining_pages)) / Decimal(str(project.remaining_days))
        elif mode == 'custom':
            if custom_pages:
                pages = Decimal(str(custom_pages))
            else:
                pages = Decimal('0')

        Progress.objects.create(project=project, date=today, pages_done=pages)

    return redirect('project_detail', pk=project.pk)

def progress_delete(request, progress_id):
    progress = get_object_or_404(Progress, pk=progress_id)
    project_pk = progress.project.pk
    progress.delete()
    return redirect('project_detail', pk=project_pk)

def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'manga/project_form.html', {'form':form, 'project':project})

def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project_list')


# Create your views here.
