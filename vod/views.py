from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.template import RequestContext
from mysite.settings import STATIC_URL
from .forms import PostForm
from django.contrib import messages
from filer.models import Image
from .models import Post
from django.core import serializers
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def gallery(request):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    print('get form ok!')
    if  form.is_valid():
        image_file = form.cleaned_data['image']
        Image.save()
        instance = form.save()
        # instance = request.user
        instance.save()
        # message success
        messages.success(request, "Successfully Created")
        print('form valid')
        # return render(request, "vod/gallery.html")
    # context = {
    #     "form": form,
    # }
    else:
        print('form is invalid')
    return render(request, "vod/gallery.html")
    # if request.method == 'POST' and request.FILES:
        # myfile=request.FILES['name_file']
        # print('file:'+myfile.name)
        # form=DocumentForm(request.POST,request.FILES)
        # print('form OK!')
        # if form.is_valid():
        #     print('Save OK!')
        #     form.save()
        #     return HttpResponseRedirect('homepage')

    # return render(request,'vod/gallery.html')


def image_redirect(request,filename):
    print('filename:'+filename)
    return HttpResponseRedirect(STATIC_URL+'images/'+filename)


def homepage(request):
    user = request.user
    content = None
    if request.user.is_authenticated():
        content = {
            # 'active_menu': 'homepage',
            'user': user.username,
        }
        print('user:'+user.username)
    return render(request,'vod/basic.html',content)


# Create your views here.
def login(request):
    state = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('username:'+username)
        print('password:'+password)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    print('retry')
    return render(request,'vod/login.html',content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))

# divide data into few pages
def listing(request):
    video_list = Post.objects.all()
    video_page = Paginator(video_list,6)
    # print('total pages:'+str(video_page.count))
    page=request.GET.get('page')
    try:
        videos = video_page.page(page)
    except PageNotAnInteger:
        videos = video_page.page(1)
    except EmptyPage:
        videos = video_page.page(video_page.num_pages)
    content={
        'videos':videos,
    }
    return render(request,'vod/list.html',content)

# @login_required
def ajax_get_data(request):
       json_data = serializers.serialize("json", Post.objects.all())
       return HttpResponse(json_data,content_type="application/json")