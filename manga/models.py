from django.db import models
from datetime import date
from math import ceil
from decimal import Decimal

class Project(models.Model):
    title = models.CharField(max_length=100)
    total_pages = models.PositiveIntegerField()
    start_date = models.DateField()
    deadline = models.DateField()
    color = models.CharField(max_length=20, default="blue") #カレンダー用

    def __str__(self):
        return self.title
    
    @property
    def progress_rate(self):
        total_done = sum(p.pages_done for p in self.progress_set.all())
        if self.total_pages == 0:
            return
        return round((total_done / self.total_pages) * 100)
    
    @property
    def remaining_days(self):
        today = date.today()
        delta = (self.deadline - today).days
        return max(delta, 0)

    @property
    def remaining_pages(self):
        total_done = sum(p.pages_done for p in self.progress_set.all())
        return max(self.total_pages - total_done, 0)
    
    @property
    def estimated_total_hours(self):
        #1pあたりの作業時間も出す、0.5は30分扱い、30分で1pはアホの所業なので後で個々で変えられるようにしたい
        return round(self.remaining_pages * 0.5, 1)
    
    @property
    def can_finish_on_time(self):
        if self.remaining_days == 0:
            return False
        return self.remaining_pages / self.remaining_days <= 1 #1日1pで間に合うか？
    
    @property
    def today_target_pages(self):
        if self.remaining_days == 0:
            return Decimal(str(self.remaining_pages)) #今日中に全部やるパターン（修羅場とか）
        return Decimal(str(self.remaining_pages / self.remaining_days))

class Progress(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    date = models.DateField()
    pages_done = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.project.title} - {self.date}: {self.pages_done}ページ"


# Create your models here.
