from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.

from userAuth.models import UserMaster
from photo.models import PhotoMaster
from user.models import FollowMaster, FavoriteMaster

from datetime import datetime

import os
from PIL import Image
from PIL import ImageDraw

from collections import OrderedDict

def top(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    p_list = {}
    List = ""
    descList = ""
    tl = []
    fa_exist = True
    null = False
    errmsg = ""

    scroll = 0

    u_list = {}
    Follow = {}
    Follower = {}

    loginid = request.session["ID"]

    user = UserMaster.objects.all().filter(userid=loginid)
    followcount = FollowMaster.objects.filter(userid=loginid).count()
    followercount = FollowMaster.objects.filter(followid=loginid).count()
    Followlist = FollowMaster.objects.all().order_by('date').reverse().filter(userid=loginid)
    Followerlist = FollowMaster.objects.all().order_by('date').reverse().filter(followid=loginid)

    Followlist = FollowMaster.objects.all().values('followid').filter(userid=loginid)
    tl.append(loginid)

    for data in user.values():
        path = "img/%s/profile.png" % (data['userid'])
        key = data['id']
        u_list[key] = {"icon": path, "userid": data['userid'], "path": path, "follow": followcount, "follower": followercount}

    user_profile = sorted(u_list.items(), reverse = True, key=lambda x: x[0])
    userdesc = OrderedDict(user_profile)

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

    if Followlist:
        for v in Followlist:
            for data in v.values():
                tl.append(data)        
    for v in tl:
        photo = PhotoMaster.objects.all().order_by('date').reverse().filter(userid=v)
        for data in photo.values():
            path = "img/%s/profile.png" % (data['userid'])
            photo_path = "img/%s/%s" % (data['userid'], data['photo'])
            key = data['id']
            favoritecount = FavoriteMaster.objects.filter(favoriteid=key).count()
            log_userfavoritecount = FavoriteMaster.objects.filter(favoriteid=key).filter(userid=loginid).count()
            if log_userfavoritecount == 0:
                fa_exist = False
            
            p_list[key] = {"id": key, "photo": photo_path, "text": data['text'], "date": data['date'], "userid": data['userid'], "path": path, "fa_count": favoritecount, "favorited": log_userfavoritecount}
    List = sorted(p_list.items(), reverse = True, key=lambda x: x[0])
    descList = OrderedDict(List)

    if 'null' in request.session:
        null = True
        errmsg = request.session['null']
        del request.session['null']


    param = {
        "list": descList,
        "user": userdesc,
        "follow": follow_desc,
        "follower": follower_desc,
        "scroll": scroll,
        "null": null,
        "msg": errmsg
    }
    request.session["path"] = "/app/top"
    return render(request, "app/top.html", param)


def upload(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    return render(request, "app/upload.html")

def uploadpost(request, *args, **kwargs):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")
    try:
        img = request.FILES.get('uploadimg')
        text = request.POST.get('text')
        
        if img:
            userid = request.session["ID"]
            date = datetime.now().strftime("%Y%m%d%H%M%S")
            new_path = date + img.name
            PhotoMaster(photo=new_path, text=text, userid=userid).save()
                
            with open(os.path.join(settings.MEDIA_ROOT, userid, new_path), 'wb+') as dest:
                for chunk in img.chunks():
                    dest.write(chunk)
                
            offset = 0

            new_size = 750


            img_copy = Image.open("./static/img/%s/%s" % (userid, new_path))
            # 中心座標を計算
            center_x = int(img_copy.width / 2)
            center_y = int(img_copy.height / 2)

            # トリミング
            img_crop = img_copy.crop((center_x - new_size / 2, center_y - new_size / 2, center_x + new_size / 2, center_y + new_size / 2))

                
            img_crop.save("./static/img/%s/%s" % (userid, new_path))

            request.session["path"] = "/app/top"
            return HttpResponseRedirect("/app/top")
        else:
            request.session['null'] = "画像を選択してください"
            return HttpResponseRedirect("/app/top")
    except PhotoMaster.DoesNotExist:
        request.session['null'] = "登録エラー"
        return HttpResponseRedirect("/app/top")
