from django.shortcuts import render, redirect
from .models import Record, Item
from .forms import RecordForm
from django.http import JsonResponse


# Create your views here.





# def home_view(request):
#     records =  Record.objects.all()
#     items = Item.objects.all()

#     context = {"records":records,"items":items}


#     return render(request, "tracker/home.html", context)


# def records_view(request):
#     return render(request, "tracker/records.html")



def item_api(request, pk):
    item = Item.objects.get(pk=pk)
    return JsonResponse({
        "item_type": item.item_type
    })


def get_all(target):
    return target.objects.all()

def get_all_records_for_item(target_item):
    all_records = target_item.record_set

def get_all_items():
    all_items = get_all(Item)
    return all_items

def get_all_item_records(item):
    pass

def get_all_item_goals(item):
    pass

def home_context():
    all_items = get_all_items()
    context = {}


def home(request):
    context= {}
    items = get_all_items()
    for item in items:
        context[item.name] = {}
        context[item.name]['object'] = item
        context[item.name]['records'] = item.record_set.values()
        context[item.name]['goals'] = item.goal_set.values()
    print(context)
    return render(request, "index.html", {"items":context})
# def home(request):
#     form = RecordForm()

#     if request.method == "POST":
#         form = RecordForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("home")

#     recent_records = Record.objects.select_related("related_item")[:15]

#     return render(request, "tracker/home.html", {
#         "form": form,
#         "records": recent_records
#     })


