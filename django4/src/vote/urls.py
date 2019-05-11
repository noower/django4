'''
Created on 2019. 4. 21.

@author: 평일오후
'''
'''
어플리케이션 별로 별도의 URL Conf를 만들 수 있음
단, app_name와 urlpatterns 변수를 정의해야함(이름이 들리면 URL Conf가 설정되지 않음)
app_name : 이 파일에 정의한 URL들의 그룹이름(문자열)
urlpatterns : path함수를 이용해 뷰함수를 등록하는 변수(리스트)
이렇게 만들어진 urls.py를 메인프로젝트폴더의 urls.py에 알려줘야함
'''
from django.urls import path
from vote.views import *

app_name = 'vote'

#기본 도메인 주소 : 127.0.0.1:8000/vote/
urlpatterns =[
    path('', index),
    #127.0.0.1:8000/숫자값 요청이 들어오면 deatil함수 호출
    #숫자값은 q_id매개변수에 값으로 사용됨
    path('<int:q_id>/', detail),
    #127.0.0.1/vote/vote
    path('vote/', vote),
    #127.0.0.1/vote/result
    path('result/<int:q_id>/',result),
    #127.0.0.1:8000/vote/qr/ -> qregiste호출
    #파이썬코드나 HTML에서 vote:qr 별칭으로 URL을 찾을 수 있음
    path('qr/',qregiste, name='qr'),
    #127.0.0.1:8000/vote/cr/ -> cregiste호출
    #파이선코드나 HTML에서 vote:cr 별칭으로 URL을 찾을 수 있음
    path('cr/',cregiste, name='cr'),
    #127.0.0.1:8000/vote/qu/
    path('<int:q_id>/change/',qupdate, name='qu'),
    #
    path('<int:q_id>/delete/',qdelete, name='qd'),
    #
    path('<int:c_id>/cdelete/',cdelete, name='cd'),
    #
    path('<int:c_id>/cchange/', cupdate, name='cu'),
              ]