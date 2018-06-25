from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .. models import Users
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.core.paginator import Paginator
import os
# Create your views here.
def index(request):
    return render(request,'selfadmin/users/index.html')

def ulist(request):
    types = request.GET.get('type',None)
    keywords = request.GET.get('keywords',None)
    # 根据条件判断需要查找的数据
    if types:
        if types == 'all':
            userlist = Users.objects.filter(
                Q(username__contains=keywords)|
                Q(address__contains=keywords)|
                Q(email__contains=keywords)|
                Q(phone__contains=keywords)|
                Q(sex__contains=keywords)
            )
        elif types == 'username':
            userlist = Users.objects.filter(username__contains=keywords)
        elif types == 'address':
            userlist = Users.objects.filter(address__contains=keywords)
        elif types == 'email':
            userlist = Users.objects.filter(email__contains=keywords)
        elif types == 'phone':
            userlist = Users.objects.filter(phone__contains=keywords)
        elif types == 'sex':
            if keywords == '男':
                userlist = Users.objects.filter(sex=1)
            elif keywords == '女':
                userlist = Users.objects.filter(sex=0)
    else:
        userlist = Users.objects.all()

    # 分页 返回当前页数据
    paginator = Paginator(userlist, 10)
    p = request.GET.get('p',1)
    ulist = paginator.page(p)
    context = {'userlist':ulist}

    return render(request,'selfadmin/users/ulist.html',context)


def delete(request):
    uid = request.GET.get('uid',None)
    ob = Users.objects.get(id=uid)
    # print(ob.username)
    try:
        if ob.pic!='':
            os.remove('.'+ob.pic)
        ob.delete()
        data = {'msg':'删除成功','code':0}
    except:
        data = {'msg':'删除失败','code':1}
    return JsonResponse(data)

def edit(request):
    uid = request.GET.get('uid',None)
    # print(uid)
    ob = Users.objects.get(id=uid)
    context = {'userlist':ob}
    return render(request,'selfadmin/users/edit.html',context)

def insert(request):
    data = request.POST.copy().dict()
    del data['csrfmiddlewaretoken']
    ob = Users.objects.get(id=data['id'])
    # print(ob.username,data['username'])
    # for i in data:
    #     print(i)
    if data['sex']:
        ob.sex = data['sex']
    if data['name']:
        ob.name = data['name']
    if request.FILES.get('pic'):
        os.remove('.'+ob.pic)
        res = upload(request)
        ob.pic = res
    if data['code']:
        ob.code = data['code']
    if data['phone']:
        ob.phone = data['phone']
    if data['address']:
        ob.address = data['address']
    if data['username']:
        ob.username = data['username']
    if data['email']:
        ob.email = data['email']
    ob.save()
        
    return HttpResponse('<script>alert("修改成功");location.href="'+reverse("selfadmin_ulist")+'"</script>')





def add(request):
    if request.method == 'POST':
        data = request.POST.copy().dict()
        del data['csrfmiddlewaretoken']
        # print(data)
        
        data['password'] = make_password(data['password'], None, 'pbkdf2_sha256')

        res = ''
        if request.FILES.get('pic',None):
            res = upload(request)
            if res[0:8] == '<script>':
                return HttpResponse(res)
        data['pic'] = res
        # print(data)

        obj = Users.objects.create(**data)

        return HttpResponse('<script>alert("添加成功");location.href="'+reverse("selfadmin_ulist")+'"</script>')
    return render(request,'selfadmin/users/add.html')


def upload(request):
    ofile = request.FILES.get('pic',None)
    # print(filename)
    if not ofile:
        # print('qing xuan ze wen jian')
        return 
    fed = ofile.name.split('.').pop()
    arr = ['jpg','png','jpeg','gif']
    if fed not in arr:
        # print('type confirm')
        return '<script>alert("格式不正确");location.href="'+reverse("selfadmin_add")+'"</script>'

    import time,random
    newfilename = str(int(time.time())) + str(random.randint(1,100000)) + '.' + fed
    
    destination = open("./static/pics/"+newfilename,"wb+")

    # 分块写入文件  
    for chunk in ofile.chunks():      
       destination.write(chunk)  
    # 关闭文件
    destination.close()

    return '/static/pics/'+newfilename