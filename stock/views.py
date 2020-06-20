# Create your views here.
import pandas as pd
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView
from plotly.offline import offline
from stock.models import Company
from member.models import Member
import plotly.graph_objs as go


def update(request):
    id_value = request.session['id']
    my_stock = request.POST.get('play')
    result = Member.objects.filter(id=id_value).update(stock_list=my_stock)
    print(result)
    company_list = Member.objects.all()
    print(company_list)
    return render(request, 'deposit/mydeposit_list.html', {'company_list':company_list})


# 회사 별 정보 조회
def filter(request):
    d = request.POST.get('search_key')
    print(d)
    list = Company.objects.filter(company_name__contains=d) #SQL like or '%a%' 써서 다 가져오기
    # return render(request, "{% url 'stock:company_detail' %}", {'d': d, 'list': list})
    return render(request, 'stock/companyFilter_list.html', {'d': d, 'list': list})

# 전체 회사 조회
class CompanyList(ListView):
    model = Company
    paginate_by = 25

def detail(request, a):  #회사 별 주식 정보 크롤링

    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

    print(type(code_df))  # <class 'pandas.core.frame.DataFrame'>
    print(code_df.head())  # 데이터를 확인

    # code_df에 있는 '종목코드' 컬럼을 0을 채운 6자리 포멧으로 맞춰준다.
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

    # code_df를 회사명과 종목코드 컬럼만 뽑아낸다.

    #    ***참고*** pandas에서 컬럼을 선택 할 때

    #                   단일개 선택: df['컬럼명']   or   df.컬럼명

    #                   여러개 선택: df[['컬럼명', ... ,'컬럼명']]

    code_df = code_df[['회사명', '종목코드']]

    excel = code_df[['회사명', '종목코드', ]]

    print(code_df)  # 데이터를 확인

    # 한글로된 컬럼명을 영어로 바꿔준다.

    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    item_name = a # 파라미터 a 입력, 주식회사 크롤링 para

    url = get_url(item_name, code_df) #주식회사 정보 크롤링

    df = pd.DataFrame() #데이터 프레임 생성

    # 크롤링. 페이지 20까지 크롤링을 한다.

    for page in range(1, 21):
    # 위에서 얻은 url에 page를 붙여줘서 url 포멧을 만들어준다.

        pg_url = '{url}&page={page}'.format(url=url, page=page)

    # pandas의 df에 위에서 얻은 url을 넣어줘서 우리가 구하고자 하는 데이터프레임을 만든다.

    # 데이터프레임을 만들 때 리스트에 [0]을 붙여줘서 만들 수 있음을 다시 확인.

        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    return HttpResponseRedirect(url)

def get_url(item_name, code_df): #일일 주식 회사 크롤링 조회
        # 코드를 가져오기 위한 처리.

        # 먼저 .query("name=='{}'".format(item_name))['code']는 name 컬럼에 item_name과 동일한 값의 code값을 반환한다는 뜻.

        # 즉, .query("쿼리".format(쿼리에 넣을 데이터))[얻을 자료]

        # .to_string(index = False)로 위에서 얻어진 값에 index를 빼고 string타입으로 바꿔준다.

        code = (code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)).strip()

        # url은 일일 종가 시가 고가 저가 거래량을 보여주는 표이다.

        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)

        print("요청 URL={}".format(url))

        return url

        f = df.dropna()

        # 상위 5개 데이터 확인하기

        print(df.head())
        print("---------------head 이후 경계선------------")
        # print(df.readline)

        # 한글로 된 컬럼명을 영어로 바꿔준다.

        df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff',

                                '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

        # 데이터의 타입을 int형으로 바꿔줌. \(역슬래쉬)는 뒤에 데이터가 이어진다는 의미이다. 한줄로 쓰면 \ 필요없음.

        df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
            = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

        # 컬럼명 'date'의 타입을 date로 바꿔줌

        df['date'] = pd.to_datetime(df['date'])

        #  일자(date)를 기준으로 오름차순 정렬

        df = df.sort_values(by=['date'], ascending=False)

        print('---최근날짜것만 가져옴----')
        myDate = df.iloc[0]
        print(myDate)
        print(myDate.close)

        # 상위 5개 데이터 확인

        print(df.head())

def stock_detail(request, s):  # 주식 그래프 생성
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

    # 타입을 확인

    print(type(code_df))  # <class 'pandas.core.frame.DataFrame'>
    print(code_df.head())  # 데이터를 확인


    # code_df에 있는 '종목코드' 컬럼을 0을 채운 6자리 포멧으로 맞춰준다.

    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

    # code_df를 회사명과 종목코드 컬럼만 뽑아낸다.

    #    ***참고*** pandas에서 컬럼을 선택 할 때

    #                   단일개 선택: df['컬럼명']   or   df.컬럼명

    #                   여러개 선택: df[['컬럼명', ... ,'컬럼명']]

    code_df = code_df[['회사명', '종목코드']]

    excel = code_df[['회사명', '종목코드', ]]

    print(code_df)  # 데이터를 확인

    print('----------배열만들기-----------')
    code_df.to_csv("test.csv", encoding="UTF-8")#csv로 저장해놓음
    first_test = code_df[['회사명', '종목코드']] #호사명과 종목코드가 들어간것

    # 한글로된 컬럼명을 영어로 바꿔준다.

    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})


    def get_url(s, code_df): #s 파라미터로, 데이터 프레임 반환

        # 코드를 가져오기 위한 처리.

        # 먼저 .query("name=='{}'".format(item_name))['code']는 name 컬럼에 item_name과 동일한 값의 code값을 반환한다는 뜻.

        # 즉, .query("쿼리".format(쿼리에 넣을 데이터))[얻을 자료]

        # .to_string(index = False)로 위에서 얻어진 값에 index를 빼고 string타입으로 바꿔준다.

        code = (code_df.query("name=='{}'".format(s))['code'].to_string(index = False)).strip()

        # url은 일일 종가 시가 고가 저가 거래량을 보여주는 표이다.

        url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code = code)

        print("요청 URL={}".format(url))

        return url

    print('----------------------------')


    # 회사명 입력 -> 그 회사 주식 가져옴.

    item_name = s

    url = get_url(item_name, code_df)

    df = pd.DataFrame()


    # 크롤링. 페이지 20까지 크롤링을 한다. 1->20 페이지 생성

    for page in range(1, 21):

        # 위에서 얻은 url에 page를 붙여줘서 url 포멧을 만들어준다.

        pg_url = '{url}&page={page}'.format(url = url, page = page)

        # pandas의 df에 위에서 얻은 url을 넣어줘서 우리가 구하고자 하는 데이터프레임을 만든다.

        # 데이터프레임을 만들 때 리스트에 [0]을 붙여줘서 만들 수 있음을 다시 확인.

        df = df.append(pd.read_html(pg_url, header = 0)[0], ignore_index= True)


    # df.dropna()를 이용해 결측값(NaN) 있는 행을 제거한다.

    df = df.dropna()

    # 상위 5개 데이터 확인하기

    print(df.head())
    print("---------------head 이후 경계선------------")


    # 한글로 된 컬럼명을 영어로 바꿔준다.

    df = df.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff',

        '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

    # 데이터의 타입을 int형으로 바꿔줌. \(역슬래쉬)는 뒤에 데이터가 이어진다는 의미이다. 한줄로 쓰면 \ 필요없음.

    df[['close', 'diff', 'open', 'high', 'low', 'volume']]\
        = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

    # 컬럼명 'date'의 타입을 date로 바꿔줌

    df['date'] = pd.to_datetime(df['date'])

    #  일자(date)를 기준으로 오름차순 정렬

    df = df.sort_values(by=['date'], ascending=False)

    print('---최근날짜것만 가져옴----')
    myDate = df.iloc[0]
    print(myDate)
    print(myDate.close)



    # 상위 5개 데이터 확인

    print(df.head())

    # plotly 라이브러리 사용법은 ' Python ▒ plotly 라이브러리 ' 참고

    trace = go.Scatter(x=df.date, y=df.close, name=item_name)
    data = [trace]


    # 그래프의 레이아웃을 설정한다. - 딕셔너리 타입으로 작성
    layout = dict(
        title='{}의 종가 시간 흐름'.format(item_name),
        xaxis=dict(rangeselector=
        dict(buttons=list(
            [dict(count=1, label='1m', step='month', stepmode='backward'),
             dict(count=3, label='3m', step='month', stepmode='backward'),
             dict(count=6, label='6m', step='month', stepmode='backward'),
             dict(step='all')]
        )),
            rangeslider=dict(), type='date'))

    fig = go.Figure(data=data, layout=layout)
    # stock_img = offline.plot(fig, filename="C:/Users/Administrator/PycharmProjects/Crawling/img/inqury.html")
    stock_img = offline.plot(fig, filename="E:/ksy/python_project/bankproject/static/inqury.html")

    return redirect('stock:company_list2')