from django.shortcuts import render
from .models import HigherGoal, Goal


# Create your views here.

# send a list of goals and higher goals
goals = Goal.objects.all()
context = {"goals":goals}


def home_view(request):
    return render(request,'goals/home.html', context)

