from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from .forms import PostForm
from .models import *
from .filters import NewsFilter


class ViewNews(ListView):
    model = Post
    ordering = '-post_in'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='Author').exists()
        return context


class OneViewNews(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}',
                        None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class SearchView(FilterView):
    model = Post
    filterset_class = NewsFilter
    template_name = 'news/search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/new_create.html'
    permission_required = ('News.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'NE'
        return super().form_valid(form)


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/article_create.html'
    permission_required = ('News.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type_post = 'AR'
        return super().form_valid(form)


class NewEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/new_edit.html'
    permission_required = ('News.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.type_post == 'AR':
            return HttpResponse('Такой статьи не существует')
        post.save()
        return super().form_valid(form)


class ArticleEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/article_edit.html'
    permission_required = ('News.change_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.type_post == 'NE':
            return HttpResponse('Такой статьи не существует')
        post.save()
        return super().form_valid(form)


class NewDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/new_delete.html'
    success_url = reverse_lazy("news")
    permission_required = ('News.delete_post',)


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy("news")
    permission_required = ('News.delete_post',)


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='Author')
    if not request.user.groups.filter(name='Author').exists():
        author_group.user_set.add(user)
    return redirect('/news/')


class CategoryListView(ViewNews):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-post_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
