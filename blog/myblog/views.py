from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import F


class Home(ListView):
	model = Post
	template_name = 'myblog/index.html'
	context_object_name = 'posts'
	paginate_by = 8

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'PYTHON И DJANGO'
		return context



class PostByCategory(ListView):
	template_name = 'myblog/index2.html'	
	context_object_name = 'posts'
	paginate_by = 8
	allow_empty = False

	def get_queryset(self):
		return Post.objects.filter(category__slug=self.kwargs['slug'])
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = Category.objects.get(slug=self.kwargs['slug'])
		return context


class GetPost(DetailView):
	model = Post
	template_name = 'myblog/single.html'
	context_object_name = 'post'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		self.object.views = F('views') + 1
		self.object.save()
		self.object.refresh_from_db()
		return context

class PostByTag(ListView):
	template_name = 'myblog/index.html'	
	context_object_name = 'posts'
	paginate_by = 8
	allow_empty = False

	def get_queryset(self):
		return Post.objects.filter(tags__slug=self.kwargs['slug'])
	
	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Записи по тегу :: ' + str(Tag.objects.get(slug=self.kwargs['slug']))
		return context





class Search(ListView):
	template_name = 'myblog/search.html'
	context_object_name = 'posts'
	paginate_by =  4
	def get_queryset(self):
		return Post.objects.filter(title__icontains=self.request.GET.get('s'))

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['s'] = f"s={self.request.GET.get('s')}&"
		return context 






