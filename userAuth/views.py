from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

# Create your views here.

from .models import UserMaster

import os
from PIL import Image
from PIL import ImageDraw
class registerView(TemplateView):
    template_name = "userAuth/register.html"
    def post(self, request, *args, **kwargs):
        try:
            userid = request.POST.get('id')
            pw = request.POST.get('pw')
            pw2 = request.POST.get('pw2')

            another = UserMaster.objects.filter(userid=userid)

            for i in another:
                errmsg = []
                if i:
                    errmsg.append("そのIDは既に存在します。")
                    param = {
                        'error': errmsg
                    }
                    return render(request, 'userAuth/register.html', param)


            if userid and pw and pw2 and pw == pw2:
                request.session["id"] = userid
                request.session["pw"] = pw
                return HttpResponseRedirect('/userAuth/createuser')
            else:
                errmsg = []
                if not userid:
                    errmsg.append("IDが未入力です。")
                if not pw or not pw2:
                    errmsg.append("パスワードが未入力です。")
                elif pw != pw2:
                    errmsg.append("パスワードが一致しません。")
                else:
                    errmsg.append("原因不明のエラー")
                param = {
                        'error': errmsg
                }
            return render(request, 'userAuth/register.html', param)
        except UserMaster.DoesNotExist:
            param = {
                'error': "登録エラー"
            }
            return render(request, 'userAuth/register.html', param)       

register = registerView.as_view()

class loginView(TemplateView):
    template_name = "userAuth/login.html"
    def post(self, request, *args, **kwargs):
        errmsg = []
        try:
            userid = request.POST.get('id')
            pw = request.POST.get('pw')

            if not userid or not pw:
                if not userid:
                    errmsg.append("・IDが未入力です。")
                if not pw:
                    errmsg.append("・パスワードが未入力です。")
                param = {
                    'error': errmsg
                }
                return render(request, 'userAuth/login.html', param)

            UserMaster.objects.get(userid=userid)
            UserMaster.objects.get(password=pw)
            request.session['ID'] = userid
                
            return HttpResponseRedirect("/app/top")
        except UserMaster.DoesNotExist:
            errmsg.append("・IDかパスワードが間違ってます。")
            param = {
                'error': errmsg
            }
            return render(request, 'userAuth/login.html', param)

login = loginView.as_view()

class createView(TemplateView):
    template_name = "userAuth/createuser.html"
    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            profile = request.POST.get('profile')
            if username and profile:
                userid = request.session["id"]
                pw = request.session["pw"]
                UserMaster(userid=userid, password=pw, username=username, profile=profile).save()
                request.session['ID'] = userid
                img_path = './static/img/' + userid
                os.makedirs(img_path)
                path = "./static/img/default.jpg"
                offset = 0
                img2 = Image.open(path)
                mask = Image.new("L", img2.size)
                draw = ImageDraw.Draw(mask)
                draw.ellipse([(offset, offset), (img2.size[0] - offset, img2.size[1] - offset)], 255)
                del draw

                img2.putalpha(mask)

                img2.save("./static/img/%s/profile.png" % userid)
                try:
                    userid = request.session['id']
                    pw = request.session['pw']
                    UserMaster.objects.get(userid=userid)
                    UserMaster.objects.get(password=pw)
                    request.session['ID'] = userid
                    return HttpResponseRedirect("/app/top")
                except UserMaster.DoesNotExist:
                    param = {
                        'error': "IDかパスワードが間違ってます。"
                    }
                    return render(request, 'userAuth/login.html', param)
            else:
                errmsg = []
                if not username:
                    errmsg.append("ユーザーネームが未入力です。")
                else:
                    errmsg.append("原因不明のエラー")
                param = {
                        'error': errmsg
                }
            return render(request, 'userAuth/createuser.html', param)
        except UserMaster.DoesNotExist:
            param = {
                'error': "登録エラー"
            }
            return render(request, 'userAuth/createuser.html', param)

create = createView.as_view()