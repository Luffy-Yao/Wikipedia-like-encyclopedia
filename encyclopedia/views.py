from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
import markdown2
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def random_page(request):
    entries = util.list_entries()
    selected_page = random.choice(entries)
    return redirect('page_content', title=selected_page)
    


def page_content(request, title):
    return render(request, "encyclopedia/page.html", {
        "content": markdown2.markdown(util.get_entry(title)),
        "title": title
    })

def new_page(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    mapped_entries = map(lambda x:x.lower(), entries)
    if query.lower() in mapped_entries:
        return HttpResponse(f"{query} has already been created!") 
    else:
       return render(request, "encyclopedia/new_page.html", {
       "title": query
    })


def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    mapped_entries = map(lambda x:x.lower(), entries)
    if query.lower() in mapped_entries:
         return render(request, "encyclopedia/page.html", {
        "content": markdown2.markdown(util.get_entry(query)),
        "title": query
    })
    else:
        entries_subgroup = []
        for entry in entries:
            if query.lower() in entry.lower():
               entries_subgroup.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries" : entries_subgroup
        })
