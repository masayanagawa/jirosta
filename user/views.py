from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.

from userAuth.models import UserMaster
from photo.models import PhotoMaster
from user.models import FollowMaster, FavoriteMaster

import os
from PIL import Image
from PIL import ImageDraw

from collections import OrderedDict


# ユーザページ
def index(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    request.session["upload_path"] = request.path

    p_list = {}
    Photo = {}
    Follow = {}
    Follower = {}
    f_exist = False
    fa_exist = True
    fo = []
    foer = []
    null = False
    

    id = request.session["ID"]

    c_follow = 0
    c_follower = 0

    followcount = FollowMaster.objects.filter(userid=id).count()
    followercount = FollowMaster.objects.filter(followid=id).count()
    Followlist = FollowMaster.objects.all().order_by('date').reverse().filter(userid=id)
    Followerlist = FollowMaster.objects.all().order_by('date').reverse().filter(followid=id)
    user = UserMaster.objects.all().filter(userid=id)
    Photolist = PhotoMaster.objects.all().order_by('date').reverse().filter(userid=id)
    loginid_exist = FollowMaster.objects.all().values('userid').filter(userid=id)
    
    for data in loginid_exist:
        if data:
            f_exist = True

    if Followlist:
        for data in Followlist.values():     
            path = "img/%s/profile.png" % data['followid']
            key = data['id']
            Follow[key] = {"userid": data['followid'], "path": path}
    followlist = sorted(Follow.items(), reverse = True, key=lambda x: x[0])
    follow_desc = OrderedDict(followlist)

    if Followerlist:
        for data in Followerlist.values():     
            path = "img/%s/profile.png" % data['userid']
            key = data['id']
            Follower[key] = {"userid": data['userid'], "path": path}

    followerlist = sorted(Follower.items(), reverse = True, key=lambda x: x[0])
    follower_desc = OrderedDict(followerlist)
        

    for data in loginid_exist:
        if data:
            f_exist = True
    
    if not followcount:
        c_follow = 0
    else:
        c_follow = followcount
    
    if not followercount:
        c_follower = 0
    else:
        c_follower = followercount

    if not PhotoMaster.objects.all().order_by('date').reverse().filter(userid=id).exists():
        null = True

    for v in Photolist.values():
        path = "img/%s/%s" % (v['userid'], v['photo'])
        key = v['id']
        favoritecount = FavoriteMaster.objects.filter(favoriteid=key).count()
        if not FavoriteMaster.objects.filter(favoriteid=key).filter(userid=id).exists():
            fa_exist = False
        Photo[key] = {"id": key, "photo": path, "userid": v['userid'], "text": v['text'], 
                        "date": v['date'], "fa_count": favoritecount, "favorited": fa_exist}

    photolist = sorted(Photo.items(), reverse = True, key=lambda x: x[0])
    photodesc = OrderedDict(photolist)

    for data in user.values():
        path = "img/%s/profile.png" % (data['userid'])
        request.session["search_icon"] = path
        key = data['id']
        p_list[key] = {"icon": path, "userid": data['username'], "profile": data['profile']}

    List = sorted(p_list.items(), reverse = True, key=lambda x: x[0])
    descList = OrderedDict(List)

    search_icon = request.session["search_icon"]
    param = {
        "id": id,
        "list": photodesc,
        "user": descList,
        "follow": follow_desc,
        "follower": follower_desc,
        "followcount": c_follow,
        "followercount": c_follower,
        "f_exist": f_exist,
        "icon": search_icon,
        "null": null

    }
    request.session["path"] = "/app/user/"
    return render(request, "user/index.html", param)

# 検索結果ページ
def search(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    request.session["upload_path"] = request.path


    p_list = {}
    id = request.POST.get('search')

    if not id:
        return HttpResponseRedirect("/app/user/search/")

    searchuser = UserMaster.objects.all().filter(userid=id)
    for data in searchuser.values():
        path = "img/%s/profile.png" % (data['userid'])
        key = data['id']
        p_list[key] = {"icon": path, "userid": data['userid'], "profile": data['profile']}

    List = sorted(p_list.items(), reverse = True, key=lambda x: x[0])
    descList = OrderedDict(List)
    param = {
        "list": descList
    }
    request.session["searchid"] = id
    return render(request, "user/search.html", param)




# 検索結果対象ユーザページ
def searchuser(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    request.session["upload_path"] = request.path

    null = False
    p_list = {}
    Photo = {}
    Follow = {}
    Follower = {}
    f_exist = False
    fa_exist = True
    fo = []
    foer = []
    id = ""

    loginid = request.session["ID"]

    if request.POST.get('searchid'):
        request.session["searchid"] = request.POST.get('searchid')
    
    id = request.session["searchid"]

    if loginid == id:
        return HttpResponseRedirect("/app/user")

    c_follow = 0
    c_follower = 0

    followcount = FollowMaster.objects.filter(userid=id).count()
    followercount = FollowMaster.objects.filter(followid=id).count()
    Followlist = FollowMaster.objects.all().order_by('date').reverse().filter(userid=id)
    Followerlist = FollowMaster.objects.all().order_by('date').reverse().filter(followid=id)
    searchuser = UserMaster.objects.all().filter(userid=id)
    Photolist = PhotoMaster.objects.all().order_by('date').reverse().filter(userid=id)
    loginid_exist = FollowMaster.objects.all().filter(userid=loginid).filter(followid=id)
    
    for data in loginid_exist:
        if data:
            f_exist = True

    if not PhotoMaster.objects.all().order_by('date').reverse().filter(userid=id).exists():
        null = True

    if Followlist:
        for data in Followlist.values():     
            path = "img/%s/profile.png" % data['followid']
            key = data['id']
            Follow[key] = {"userid": data['followid'], "path": path}
    followlist = sorted(Follow.items(), reverse = True, key=lambda x: x[0])
    follow_desc = OrderedDict(followlist)

    if Followerlist:
        for data in Followerlist.values():     
            path = "img/%s/profile.png" % data['userid']
            key = data['id']
            Follower[key] = {"userid": data['userid'], "path": path}

    followerlist = sorted(Follower.items(), reverse = True, key=lambda x: x[0])
    follower_desc = OrderedDict(followerlist)
        

    for data in loginid_exist:
        if data:
            f_exist = True
    
    if not followcount:
        c_follow = 0
    else:
        c_follow = followcount
    
    if not followercount:
        c_follower = 0
    else:
        c_follower = followercount

    for v in Photolist.values():
        path = "img/%s/%s" % (v['userid'], v['photo'])
        key = v['id']
        favoritecount = FavoriteMaster.objects.filter(favoriteid=key).count()
        if not FavoriteMaster.objects.filter(favoriteid=key).filter(userid=id).exists():
            fa_exist = False
        Photo[key] = {"id": key, "photo": path, "userid": v['userid'], "text": v['text'], 
                        "date": v['date'], "fa_count": favoritecount, "favorited": fa_exist}

    photolist = sorted(Photo.items(), reverse = True, key=lambda x: x[0])
    photodesc = OrderedDict(photolist)

    for data in searchuser.values():
        path = "img/%s/profile.png" % (data['userid'])
        request.session["search_icon"] = path
        key = data['id']
        p_list[key] = {"icon": path, "userid": data['username'], "profile": data['profile']}

    List = sorted(p_list.items(), reverse = True, key=lambda x: x[0])
    descList = OrderedDict(List)

    search_icon = request.session["search_icon"]
    param = {
        "id": id,
        "list": photodesc,
        "user": descList,
        "follow": follow_desc,
        "follower": follower_desc,
        "followcount": c_follow,
        "followercount": c_follower,
        "f_exist": f_exist,
        "icon": search_icon,
        "null": null

    }
    request.session["path"] = "/app/user/searchuser"
    return render(request, "user/searchuser.html", param)


# フォロー処理
def follow(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")
    userid = request.session["ID"]
    followid = request.session["searchid"]
    FollowMaster(followid=followid, userid=userid).save()
    return HttpResponseRedirect("/app/user/searchuser/")

# フォロー解除処理
def unfollow(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")
    userid = request.session["ID"]
    followid = request.session["searchid"]
    FollowMaster.objects.get(followid=followid, userid=userid).delete()
    return HttpResponseRedirect("/app/user/searchuser/")

# 豚(いいね)処理
def favorite(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    url = request.session["path"]
    userid = request.session["ID"]
    photoid = request.POST.get('photoid')
    FavoriteMaster(favoriteid=photoid, userid=userid).save()
    co = FavoriteMaster.objects.filter(favoriteid=photoid).count()
    d = {
        'count': co,
    }
    return JsonResponse(d)

#豚(いいね)取り消し処理
def unfavorite(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    url = request.session["path"]
    userid = request.session["ID"]
    photoid = request.POST.get('photoid')
    FavoriteMaster.objects.get(favoriteid=photoid, userid=userid).delete()
    co = FavoriteMaster.objects.filter(favoriteid=photoid).count()
    d = {
        'count': co,
    }
    return JsonResponse(d)