from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from deposit.models import Deposit, Mydepositlist
from deposit.deposit_read import deposit_crawler
from member.models import Member

def test(request):
    return render(request, 'deposit/test.html')

def search(request):
    # Deposit.objects.all().delete()
    deposit_list = deposit_crawler()
    # for items in deposit_list:
    #     Deposit(**items).save()
    return render(request, 'deposit/deposit_search.html',{'deposit_list':deposit_list})

def search_result(request):
    dmoney = request.POST.get('money')
    dperiod = request.POST.get('month')
    dtype = request.POST.get('rate_type')

    deposit_list = Deposit.objects.all()

    if dtype == '단리':
        deposit_list = Deposit.objects.filter(rate_type='단리')
    elif dtype == '복리':
        deposit_list = Deposit.objects.filter(rate_type='복리')

    if dperiod == '6':
        deposit_list = deposit_list.exclude(rate_6 = '-').order_by('-rate_6')
    elif dperiod == '12':
        deposit_list = deposit_list.exclude(rate_12= '-').order_by('-rate_12')
    elif dperiod == '24':
        deposit_list = deposit_list.exclude(rate_24= '-').order_by('-rate_24')
    elif dperiod == '36':
        deposit_list = deposit_list.exclude(rate_36= '-').order_by('-rate_36')

    data = list(deposit_list.values())
    for d in data:
        if d['rate_type'] == '단리':
            # money = 100000
            money = int(dmoney) *(1 + 0.01 * float(d['rate_'+dperiod]) * 0.846 * int(dperiod) /12)
            d['money'] = format(int(money),',')
        else:
            money = int(dmoney) * pow(1 + 0.01 * float(d['rate_'+dperiod])* 0.846,int(dperiod)/12)
            d['money'] = format(int(money),',')

    return JsonResponse(data, safe=False)

def my_deposit(request):
    my_list = request.POST.getlist('my_list[]')
    id = request.POST.get('my_id')
    for product in my_list:
        Mydepositlist(member_id_id = id, product_name= product).save()
    return HttpResponse("저장완료")


def my_deposit_list(request):
    id_value = request.session['id']
    company_list = list(Member.objects.filter(id=id_value).values())
    product_list = list(Mydepositlist.objects.filter(member_id_id=id_value).values())
    name_list = []
    for item in product_list:
        name_list.append(item['product_name'])
    name_set = set(name_list)
    return render(request, 'deposit/mydeposit_list.html',{'name_list':name_set,'company_list':company_list})


def detail(request, d_name):
    print(d_name)
    data = list(Deposit.objects.filter(product=d_name).values())
    print(data[0])
    return render(request, 'deposit/detail.html',{'data':data[0]})

def delete(request):
    delete_list = request.POST.getlist('delete_list[]')
    id = request.POST.get('my_id')
    for product in delete_list:
        Mydepositlist.objects.filter(member_id_id=id).filter(product_name=product).delete()
    return render(request,'deposit/mydeposit_list.html')