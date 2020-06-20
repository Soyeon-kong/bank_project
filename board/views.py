import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import *
from board.models import Board, UpdateForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator
# Create your views here.

class BoardList(ListView):
    model= Board

class BoardCreate(CreateView):
    model = Board
    fields = ['b_writer','b_title','b_content']
    template_name_suffix = '_create'
    success_url = reverse_lazy('boardlist')

class BoardDetail(DetailView):
    model = Board
    template_name = 'board/board_detail.html'


class BoardUpdate(UpdateView):
    model = Board
    form_class = UpdateForm
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save(update_fields=list(form.fields))
        return HttpResponseRedirect(self.get_success_url())
    template_name = 'board/board_update.html'
    success_url =  reverse_lazy('boardlist')

def deleteboard(request):
    num = request.GET.get('b_number')
    board = Board.objects.get(b_number=num)
    board.delete()
    return render(request , 'board/board_list.html')

def index(request):
    page = request.GET.get('page','1')

    board_list = Board.objects.order_by('-create_date')

    paginator = Paginator(board_list,10)
    page_obj =Paginator.get_page(page)

    context= {'page_list':page_obj}

    return render(request, 'board/board_list.html',context)