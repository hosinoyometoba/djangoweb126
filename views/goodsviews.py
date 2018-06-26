from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Goods,Types

def gettypesorder():
    # 获取所有的分类信息
    # tlist = Types.objects.all()

    # select *,concat(path,id) as paths from myadmin_types order by paths;
    tlist = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')

    for x in tlist:
        if x.pid == 0:
            x.pname = '顶级分类'
        else:
            t = Types.objects.get(id=x.pid)
            x.pname = t.name
        num  = x.path.count(',')-1
        x.name = (num*'_~^~')+x.name


    return tlist

def upload(request):
    ofile = request.FILES.get('pics',None)
    # print(filename)
    if not ofile:
        # print('qing xuan ze wen jian')
        return '<script>alert("图片不能为空,请选择图片!");location.href="'+reverse("selfadmin_goods_add")+'"</script>'
    fed = ofile.name.split('.').pop()
    arr = ['jpg','png','jpeg','gif']
    if fed not in arr:
        # print('type confirm')
        return '<script>alert("格式不正确");location.href="'+reverse("selfadmin_goods_add")+'"</script>'

    import time,random
    newfilename = str(int(time.time())) + str(random.randint(1,100000)) + '.' + fed
    
    destination = open("./static/pics/"+newfilename,"wb+")

    # 分块写入文件  
    for chunk in ofile.chunks():      
       destination.write(chunk)  
    # 关闭文件
    destination.close()

    return '/static/pics/'+newfilename

def list1(request):
    return HttpResponse('list1')

def delete(request):
    return HttpResponse('delete')

def add(request):
    if request.method == 'GET':
        alltype = gettypesorder()
        context = {'alltype':alltype}
        return render(request,'selfadmin/goods/add.html',context)
    elif request.method == 'POST':
        data = request.POST.copy().dict()
        del data['csrfmiddlewaretoken']
        res = ''
        if request.FILES.get('pics',None):
            res = upload(request)
            if res[0:8] == '<script>':
                return HttpResponse(res)
        data['pics'] = res
        data['typeid_id'] = Types.objects.get(id = data['typeid_id'])
        print(data)
        obj = Types.objects.create(**data)

        return HttpResponse('1')
def edit(request):
    return HttpResponse('edit')