from django.shortcuts import redirect
from .models import Post
from django.views.generic import ListView, DetailView
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-id'

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
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(data=self.request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()

        return redirect('post_detail', pk=self.object.pk)