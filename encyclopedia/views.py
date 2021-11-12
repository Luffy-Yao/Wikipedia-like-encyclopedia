from django import forms
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
import markdown2
from . import util
import random


class NewForm(forms.Form):
     New_Entry  = forms.CharField()
     Contents = forms.CharField(widget=forms.Textarea)



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
        "content" : util.get_entry(title),
        "title" : title
    })



def edit(request, title):
    form = NewForm(request.POST)
    if request.method == "POST":
        entryContent = request.POST.get('eContent')
        util.save_entry(title, entryContent)
        return redirect('index')
    else:
        return render(request, "encyclopedia/edit_page.html", {
            "content": markdown2.markdown(util.get_entry(title)),
            "title": title
        })


def new_page(request):
    if request.method == "POST":
            form = NewForm(request.POST)
            if form.is_valid():
                new_entry = form.cleaned_data["New_Entry"]
                content = form.cleaned_data["Contents"]
                mapped_entries = map(lambda x:x.lower(), util.list_entries())
                if new_entry.lower() in mapped_entries:
                    return HttpResponse(f"{new_entry} already exists!")
                util.save_entry(new_entry, content)
                return redirect('index')
            else:
                return render(request, "encyclopedia/new_page.html", {
                    "form": form
                })
    return render(request, "encyclopedia/new_page.html", {
       "form": NewForm()
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
