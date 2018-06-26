from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Types,Goods



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


def list1(request):
    tlist = gettypesorder()
    context = {'tlist':tlist}
    return render(request,'selfadmin/types/list.html',context)

def delete(request):
    tid = request.GET.get('tid',None)
    # print(tid)
    sontype = Types.objects.filter(pid=tid)
    type1 = Types.objects.filter(id=tid)
    # print(bool(sontype))
    if sontype:
        data = {'msg':'所选对象有下级类别,不能删除','code':0}
    else:
        type1.delete()
        data = {'msg':'删除成功','code':1}
    return JsonResponse(data)

def add(request):
    alltype = gettypesorder()
    context = {'alltype':alltype}
    return render(request,'selfadmin/types/add.html',context)


def edit(request):

    return HttpResponse('<script>alert("请删除原有类型并重新添加");location.href="'+reverse("selfadmin_type_list")+'"</script>')

def insert(request):
    ob = Types()
    ob.name = request.POST['name']
    ob.pid = request.POST['pid']
    # print(ob.name,ob.pid)
    if ob.pid == 0:
        ob.path = '0,'
    else:
        p = Types.objects.get(id=ob.pid)
        ob.path = p.path +str(p.id)+','
        # print(ob.path)
    ob.save()
    
    return HttpResponse('<script>alert("添加成功");location.href="'+reverse("selfadmin_type_list")+'"</script>')