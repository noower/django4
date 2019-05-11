from django.shortcuts import render, get_object_or_404
from vote.models import Question, Choice
from django.contrib.auth.decorators import login_required
'''
데코레이터: 뷰함수가 실행되기 전에 먼저 실행되는 함수
login_required : 뷰함수가 실행되기 전 웹클라이언트의 로그인여부를 파악하고 비로그인 상태인 웹클라이언트에게 로그인페이지를 리다이렉트 해주는 데코레이터

데코레이터를 뷰함수에 적용하는 방법
#@적용할 데코레이터 함수 이름
def 뷰함수()
'''
# Create your views here.

#t설문조사 리스트가 뜨는 메인페이지
def index(request):
    #데이터베이스에 저장된 Question 객체 리스트로추출
    a = Question.objects.all()
    #index.html 전달
    return render(request, 'vote/index.html', {'a': a})
#설문조사 페이지
def detail(request,q_id):
    #Question개체들 중 q_id와 동일한 값을 id변수에 가진 객체 추출
    #또는 조건에 맞는 객체가 없으면 404번에러를 클라이언트에게 전달--
    q = get_object_or_404(Question, id=q_id)
    '''
    get_object_or_404(모델클래스, 조건) : 모델클래스에 조건을 검색해 1개의 객체 추출
    만약 객체가 없는 경우, 클라이언트의 잘못된 접근으로 판단해 뷰함수를 종료하고 404번에러를 전달
    
    현재 Question 모델클래스는 Choice 모델클래스가 외래키로 연결한 상태이므로,
    Question 객체들은 자신과 연결된 Choice 객체들을 추출할 수 있음
    Question객체.choice_set.all(또는 get,filter,exclude)로 데이터베이스에 저장된
    Choice 객체 추출 가능. 모델클래스 이름을 소문자로 작성해야함
    '''
    #Question 객체로 연결된 Choice 객체들을 모두 추출
    c_list = q.choice_set.all()
    #HTML 파일 전달
    return render(request,'vote/detail.html',{'q':q,'c_list':c_list})
    
    
from django.http.response import HttpResponseRedirect
'''
HttpResponseRedirect(URL주소) : 웹클라이언트가 HTML파일받는것이 아닌, 새로운 URL주소를 받아 재요청을 할 수 있도록
처리할 수 있는 클래스

Redirect : 웹서버가 300번대 코드를 전달하면서 더 처리해야할 요청을 웹 클라이언트에게 전달하는 응답

사용방법
return HttpResponseRedirect(이동할 URL주소)

'''
#투표반영
def vote(request):
    #사용자의 요청이 POST방식인지 확인
    #request.method : 웹클라이언트의 요청방식을 저장한 변수
    #"GET", "POST" 문자열을 저장하고 있음
    if request.method == "POST":
        '''
        request.POST 또는 request.GET : 웹클라이언트의 요청과 함께 날라온 데이터를 저장하는 변수
        값을 꺼낼때, HTML코드에 name속성이름으로 값을 추출할 수 있음
        '''
        print(request.POST)
        #사용자가 투표한 Choice객체의 id값을 추출
        c_id = request.POST.get('vote')
        #id값을 바탕으로 데이터베이스에 choice객체 추출
        c = get_object_or_404(Choice, id=c_id)
        #votes 변수에 투표 반영
        c.votes = c.votes +1
        #데이터베이스에 변경사항 저장
        c.save()
        #다른 뷰함수의 URL을 웹클라이언트에게 전달
        #c.q : Choice객체가 연결한 Question객체 변수
        #c.q.id : 연결한 Question객체의 id변수값
        url = "/vote/result/%s/" %c.q.id
        return HttpResponseRedirect(url)

#결과페이지
def result(request,q_id):
    #Question객체를 q_id값으로 한개 추출
    print(request)
    q = get_object_or_404(Question,id=q_id)
    #HTML전달
    return render(request, 'vote/result.html',{'q':q})

#모델폼클래스 임포트
from vote.forms import QuestionForm, ChoiceForm
from _datetime import datetime

#Question 객체 추가
@login_required
def qregiste(request):
    #웹클라이언트의 요청방식 구분
    #-> 하나의 뷰에 두가지 기능을 구현하고자 함
    #GET 방식요청
    if request.method == "GET":
        #폼클래스 객체를 생성 및 HTML파일 전달
        #폼클래스 객체 생성시, 매개변수를 입력하지 않으면,
        #<input>태그에 아무런 값도 채워져있지 않은 상태로 생성됨
        obj = QuestionForm()
        '''
        form 객체를 기반으로 HTML 코드에 들어갈 <input>태그를 생성할 때,
        as_p(), as_table(), as_ul() 함수를 사용할 수 있음.
        as_p : 설명과 입력공간이 <p>태그로 묶여잇는 HTML코드로 변환
        as_table : 설명과 입력공간이 한 행(<tr>)에 묶여있는 HTML코드로 변환
        as_ul : 설명과 입력공간이 리스트아이템(<li>)에 묶여있는 HTMl코드로 변환
        '''
        print('as_table()결과 : ', obj.as_table())
        return render(request,'vote/qregiste.html', {'form':obj.as_table()})
    #POST 방식요청
    elif request.method == "POST":
        #q = Question(name = request.POST.get('name') , pub_date = datetime.now())
        #q.save()

        #사용자 입력 기반으로 폼클래스객체를 생성
        #request.POST : POST요청 시 동봉된 사용자의 입력데이터
        obj = QuestionForm(data=request.POST)
        #폼클래스 객체를 연동된 모델클래스 객체로 변환
        #q : 사용자 입력으로 name변수에 값이 채워져있는 Question객체
        #폼객체.save() : 데이터베이스에 사용자입력기반의 새로운 객체가 저장되면서 새로운 객체를 반환하는 함수
        #사용자는 pub_date변수에 값을 입력할수없기때문에, 폼객체를 바로 데이터베이스에 저장할 수 없음(pub_date변수의 값이 없는 상태)
        #따라서 Question객체로 변환한 뒤, 비어있는 변수를 채워줘야함
        #->폼객체.save(commit=False) 
        q = obj.save(commit=False)
        print('저장전 id변수값: ',q.id) #데이터베이스에 저장되지않은 변수의 id값은 None이뜸
        #값이 채워져있지 않은 변수에 값을 채움
        q.pub_date = datetime.now() #컴퓨터의 현재날짜/시간을 대입
        #데이터베이스에 새로만든 모델객체 저장
        #모델객체.save() : 새로운객체를 저장하거나 기존객체의 변수값변경을 데이터베이스에 저장할 수 있음
        q.save()
        print('저장후 id변수값: ',q.id)
        #다른 URL로 이동
        return HttpResponseRedirect('/vote/%s/' % q.id)
        
#Question 객체 수정
@login_required
def qupdate(request,q_id):
    #수정할 대상의 객체 추출
    q = get_object_or_404(Question, id=q_id)
    #GET 방식요청
    if request.method == "GET":
        #수정할 객체를 기반으로 QuestionForm 객체를 생성
        obj = QuestionForm(instance = q)
        #HTML 파일 전달
        return render(request, 'vote/qupdate.html', {'form':obj.as_p()})
    #POST 방식요청
    elif request.method == "POST":
        #사용자입력+수정할객체를 기반으로 QuestionForm 객체를 생성
        obj = QuestionForm(request.POST, instance = q)
        #수정을 하는 객체를 바탕으로 QuestionForm 객체가 생성됬기때문에
        #pub_date 변수는 이미 값이 채워져있음
        #->바로 데이터베이스에 저장
        w = obj.save()
        print('수정할 객체 q의 id:', q.id)
        print('폼객체가 준 객체의 id:',w.id)
        #다른 URL 전달 detail 페이지
        return HttpResponseRedirect('/vote/%s/' % w.id)

#Question 객체 삭제
@login_required
def qdelete(request,q_id):
    q = get_object_or_404(Question,id=q_id)
    print('삭제전 id: ',q.id)
    q.delete() #데이터베이스에서 삭제됨
    print('삭제후 id: ',q.id)
    return render(request,'vote/delete_com.html',{'title' : q.name,'type':1})
#Choice 객체 추가
@login_required
def cregiste(request):
    #GET 요청
    if request.method=="GET":
        #ChoiceForm 객체 생성 및 HTML('vote/cregiste.html') 전달
        obj = ChoiceForm()
        return render(request,'vote/cregiste.html', {'form': obj.as_table()})
    #POST 요청
    elif request.method=="POST":
        #사용자입력기반으로 ChoiceForm 객체 생성
        obj = ChoiceForm(request.POST)
        #ChoiceForm객체를 기반으로 Choice객체 생성 및 데이터베이스 저장
        #->값이 비어있는 변수가 없기때문(votes는 기본값 설정이 되있음)
        c = obj.save()
        #다른 페이지로 이동(index나 detail로 이동)
        #return HttpResponseRedirect('/vote/')
        return HttpResponseRedirect('/vote/%s/' %c.q.id)
#Choice 객체 수정
@login_required
def cupdate(request, c_id):
    c=get_object_or_404(Choice,id=c_id)
    if request.method == "GET":
        obj = ChoiceForm(instance = c)
        return render(request, 'vote/cupdate.html', {'obj':obj})
    elif request.method == "POST":
        obj = ChoiceForm(request.POST, instance=c)
        obj.save()
        #detail View의 URL을 전달
        return HttpResponseRedirect('/vote/%s/' %c.q.id)
    
    
#Choice 객체 삭제
@login_required
def cdelete(request, c_id):
    #Choice 객체 찾기
    c = get_object_or_404(Choice,id=c_id)
    #데이터베이스에서 삭제
    c.delete()
    #HTML 파일 or URL주소 전달
    return render(request, 'vote/delete_com.html', {'title':c.name, 'type':2})