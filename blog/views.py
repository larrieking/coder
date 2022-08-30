#from django.shortcuts import render

# Create your views here.
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import  render, get_object_or_404
from .models import Post, Category, Comment
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import EmailPostForms
def post_list(request):
    cat = request.GET.get('cat')
    print(cat)
    if cat != None:
        posts = Post.published.filter(category = cat)
    else:
        posts = Post.published.all()



    paginator = Paginator(posts,4)
    page = request.GET.get('page')
    cover = posts[len(posts)-1]


    try:
        postss = paginator.page(page)
    except PageNotAnInteger:
        postss = paginator.page(1)
    except EmptyPage:
        postss = paginator.page(paginator.num_pages)


    return render(request, 'list.html', {'posts':postss, 'cover':cover,  'page':page})

def post_details(request, year, month, day, post):
    name = request.POST.get('name')
    email = request.POST.get('email')
    body = request.POST.get('body')



    post = get_object_or_404(Post, slug = post, status='published', publish__year=year, publish__month=month, publish__day=day )
    comments = post.comments.filter(active=True)
    new_comment = None



    if request.method == "POST":
        c1 = Comment(name=name, email=email, body=body, post = post)

        c1.save()
        print(comments)


    return render(request, 'detail.html', {'post':post,  "comments":comments})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status = 'published')
    post_url = request.build_absolute_uri(post.get_absolute_url())
    to_mail = ""
    if request.method == 'POST':
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')
        from_mail = request.POST.get('from')
        to_mail = request.POST.get('to')
        meassage = request.POST.get('body')


        try:


            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{first_name} {last_name} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{first_name}'s comments: {meassage}"

            send_mail(subject, message, 'info@adventurecapital.com.ng', [to_mail,])
            print(to_mail)
            sent = True


        except Exception as e:

            print(e)
            sent = False

    else:
        sent = False
    return render(request, 'share.html', {'post':post, "post_url":post_url, "sent":sent, 'to':to_mail})


def home(request):
    return render(request, 'home.html')

def contact(request):
    if request.method =='POST':
        return HttpResponse('<div class = "alert alert-success">done</div>')
    else:
        return render(request, 'contact.html')