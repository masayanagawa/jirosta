from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
# Create your views here.

from userAuth.models import UserMaster
from photo.models import PhotoMaster
from user.models import FollowMaster, FavoriteMaster

import os
import shutil
from PIL import Image
from PIL import ImageDraw

def index(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    request.session["upload_path"] = request.path

    user = []

    userid = request.session["ID"]
    id = UserMaster.objects.values('userid').filter(userid=userid)
    username = UserMaster.objects.values('username').filter(userid=userid)
    profile = UserMaster.objects.values('profile').filter(userid=userid)

    path = "img/%s/profile.png" % userid
    
    for v in id:
        for data in v.values():
            user.append(data)

    for v in username:
        for data in v.values():
            user.append(data)
    
    for v in profile:
        for data in v.values():
            user.append(data)

    request.session["userid"] = user[0]
    request.session["username"] = user[1]
    request.session["profile"] = user[2]
    request.session["path"] = path

    param = {
        "id": user[0],
        "username": user[1],
        "profile": user[2],
        "path": path
    }
        
    return render(request, "setting/index.html", param)

def post(request, *args, **kwargs):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")

    userid = request.session["ID"]
    num = UserMaster.objects.values('id').filter(userid=userid)
    id = request.POST.get("id")
    username = request.POST.get("username")
    profile = request.POST.get("profile")
    img = request.FILES.get('img')
    size = ""

    if id and username:
        if img:
            with open(os.path.join(settings.MEDIA_ROOT, userid, 'profile.png'), 'wb+') as dest:
                for chunk in img.chunks():
                    dest.write(chunk)

            path = "./static/img/%s/profile.png" % userid
            
            offset = 0
            img2 = Image.open(path)

            if img2.width != img2.height:
                offset = 0

                new_size = 400

                # 中心座標を計算
                center_x = int(img2.width / 2)
                center_y = int(img2.height / 2)

                # トリミング
                img2 = img2.crop((center_x - new_size / 2, center_y - new_size / 2, center_x + new_size / 2, center_y + new_size / 2))
                            
                img2.save("./static/img/%s/profile.png" % userid)

            mask = Image.new("L", img2.size)
            draw = ImageDraw.Draw(mask)
            draw.ellipse([(offset, offset), (img2.size[0] - offset, img2.size[1] - offset)], 255)
            del draw

            img2.putalpha(mask)

            img2.save("./static/img/%s/profile.png" % userid)

        path = "img/%s/profile.png" % userid

        for v in num:
            for data in v.values():
                UserMaster.objects.values().filter(id=data).update(userid=id, username=username, profile=profile)

        request.session["ID"] = id

        sucsess = "設定を変更しました。"
        param = {
            "id": id,
            "username": username,
            "profile": profile,
            "sucsess": sucsess,
            "path": path,

        }
        return render(request, "setting/index.html", param)
    else:
        errmsg = []
        if not id:
            errmsg.append("IDが未入力です。")
        if not username:
            errmsg.append("ユーザーネームが未入力です。")
        if not img.name:
            errmsg.append("ファイルを選択してください")

        id = request.session["userid"]
        username = request.session["username"]
        profile = request.session["profile"]
        path = request.session["path"]
        param = {
            "id": id,
            "username": username,
            "profile": profile,
            "path": path,
            "error": errmsg,
            
        }
        return render(request, "setting/index.html", param)

def password(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")
    request.session["upload_path"] = request.path
    
    return render(request, "setting/password.html")

def postpassword(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")
    pw = request.POST.get("pw")
    pw2 = request.POST.get("pw2")

    userid = request.session["ID"]
    num = UserMaster.objects.values('id').filter(userid=userid)

    if pw and pw2 and pw == pw2:
        for v in num:
            for data in v.values():
                UserMaster.objects.values().filter(id=data).update(password=pw)

        sucsess = "パスワードを変更しました。"
        param = {
                'sucsess': sucsess
        }
        return render(request, "setting/password.html", param)
    else:
        errmsg = []
        if not pw or not pw2:
            errmsg.append("パスワードが未入力です。")
        elif pw != pw2:
            errmsg.append("パスワードが一致しません。")
        else:
            errmsg.append("原因不明のエラー")
        param = {
            'error': errmsg
        }
        return render(request, "setting/password.html", param)

def unregister(request):
    if not 'ID' in request.session:
        request.session["path"] = request.path
        return HttpResponseRedirect("/userAuth/login/")
    errmsg = []
    id = request.session["userid"]
    username = request.session["username"]
    profile = request.session["profile"]
    path = request.session["path"]
    pw = request.POST.get('pw')

    if not pw:
        errmsg.append("退会不可:パスワードが未入力です。")
        param = {
            "id": id,
            "username": username,
            "profile": profile,
            "path": path,
            "error": errmsg,
        }
        return render(request, 'setting/index.html', param)

    id = request.session["ID"]
    datapw = UserMaster.objects.all().values('password').filter(userid=id)


    for d in datapw:
        if pw == d['password']:
            UserMaster.objects.filter(userid=id).delete()
            PhotoMaster.objects.filter(userid=id).delete()
            FollowMaster.objects.filter(userid=id).delete()
            FollowMaster.objects.filter(followid=id).delete()
            FavoriteMaster.objects.filter(userid=id).delete()
            shutil.rmtree("./static/img/%s" % id)
            return HttpResponseRedirect("/")
        else:
            errmsg.append("退会不可:パスワードが違います。")
            param = {
                "id": id,
                "username": username,
                "profile": profile,
                "path": path,
                "error": errmsg,
            }
            return render(request, 'setting/index.html', param)