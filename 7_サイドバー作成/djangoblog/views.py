from django.shortcuts import redirect, get_object_or_404
from .models import Post, Category
from django.views.generic import ListView, DetailView
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-id'
    paginate_by = 5
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(get_common_data())
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = self.object.comments.all()
        form = CommentForm()
        context.update({
            'comments': comments, 
            'form': form,
        })
        context.update(get_common_data())
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(data=self.request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()

        return redirect('post_detail', pk=self.object.pk)

class PostListByCategoryView(PostListView):
    template_name = 'post_by_category.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return queryset.filter(categories=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'categories': self.get_queryset().first().categories})
        return context

class PostListByMonthView(PostListView):
    template_name = 'post_by_month.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        if year and month:
            queryset = queryset.filter(created_at__year=year, created_at__month=month)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        context.update({
            'year': year,
            'month': month,
        })
        return context

def get_common_data():
    #サイドバーのカテゴリー一覧
    category_list = Category.objects.all()
    #サイドバーの月別投稿ー一覧
    post_month_list = Post.objects.dates('created_at', 'month', order='DESC')
    return {'category_list': category_list, 'post_month_list': post_month_list}