from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import Friend, Follower
from posts.forms import PostForm
from posts.models import Post
from django.utils import timezone
from .forms import ProfileForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url = '/')
def user_account(request):
    username = request.user
    user = User.objects.get(username = username)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.post_time = timezone.now()
            new_post.save()
            return HttpResponseRedirect(request.path)
    else:
        form = PostForm()

    user_posts = Post.objects.filter(author = user).order_by("-post_time")
    page = request.GET.get('page', 1)
    paginator = Paginator(user_posts, 10)
    try:
      post_list = paginator.page(page)
    except PageNotAnInteger:
      post_list = paginator.page(1)
    except EmptyPage:
      post_list = paginator.page(paginator.num_pages)



@login_required(login_url = '/')
def friends(request):
    users_friends1 = Friend.objects.filter(user = request.user, confirmed = True)
    users_friends2 = Friend.objects.filter(users_friend = request.user, confirmed = True)
    new_friends = Friend.objects.filter(users_friend = request.user, confirmed = False).count()
    context = {"friends1": users_friends1, "friends2": users_friends2, "not_confirmed_friends_count": new_friends}
    return render(request, 'account/friends.html', context)


@login_required(login_url = '/')
def friend_request(request):
    not_confirmed_friends = Friend.objects.filter(users_friend = request.user, confirmed = False)
    new_friends = Friend.objects.filter(users_friend = request.user, confirmed = False).count()
    context = {"not_confirmed_friends": not_confirmed_friends, "not_confirmed_friends_count": new_friends}
    return render(request, 'account/friend_request.html', context)


@login_required(login_url = '/')
def add_friend(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    is_friend = Friend.objects.filter(user = request.user, users_friend = user)|Friend.objects.filter(user = user, users_friend = request.user)
    if not is_friend:
        add_friend = Friend(user = request.user, users_friend = user)
        add_friend.save()
    return HttpResponseRedirect(reverse('account:account', args = (account_id, )))


@login_required(login_url = '/')
def confirm_friend(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    new_friend = Friend.objects.get(user = user, users_friend = request.user)
    new_friend.confirmed = True
    new_friend.save()
    return HttpResponseRedirect(reverse('account:friends'))


@login_required(login_url = '/')
def delete_friend(request, account_id):
    try:
        user = User.objects.get(id = account_id)
    except:
        raise Http404("Пользователь не найден!")

    new_friend = Friend.objects.filter(user = user, users_friend = request.user)|Friend.objects.filter(user = request.user, users_friend = user )
    new_friend.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
