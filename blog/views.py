from django.shortcuts import render,get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.core.mail import send_mail
from .forms import EmailPostForm,CommentPostForm


def post_comment(request, post_id):
    post = get_object_or_404( Post,id=post_id,status=Post.Status.PUBLISHED)
    comment = None
    form = CommentPostForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,'blog/comment.html',{'post': post,'form': form,'comment': comment})


def post_share(request, post_id):
    post = get_object_or_404(Post,id=post_id,status=Post.Status.PUBLISHED)
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        
        if form.is_valid():# Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = (f"{cd['name']} ({cd['email']}) "f"recommends you read {post.title}")
            
            message = (f"Read {post.title} at {post_url}\n\n"f"{cd['name']}\'s comments: {cd['comments']}")
            send_mail(subject=subject,message=message,from_email=None,recipient_list=[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request,'blog/share.html',{'post': post,'form': form,'sent': sent})

def home(request):
    return render(request,'blog/home.html')

def about(request):
    return render(request,'blog/about.html')

class PostListView(ListView):
    paginate_by = 3
    context_object_name = 'posts'
    template_name = 'blog/post_details.html'

    def get_queryset(self):
        show_draft = self.request.GET.get('draft') == 'true'
        if show_draft:
            return Post.objects.filter(status=Post.Status.DRAFT).order_by('-publish')
        return Post.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_draft'] = self.request.GET.get('draft') == 'true'
        return context
    
#def post_details(request):
    #show_draft = request.GET.get('draft')
    #if show_draft == "true":
    #    post = Post.objects.filter(status=Post.Status.DRAFT)
    # else:
    #    post = Post.objects.filter(status=Post.Status.PUBLISHED)
    # paginator=Paginator(post,3)
    # page_number=request.GET.get('page',1)
    #posts=paginator.page(page_number)
    # return render(request, 'blog/post_details.html', {'posts': posts,'show_draft': show_draft})   
def post_detail(request, id, year, month, date):
    post = Post.published.get(id=id, created_at__year=year, created_at__month=month, created_at__day=date)
    return render(request, 'blog/post_list.html', {'post': post})
