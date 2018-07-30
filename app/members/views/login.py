from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

__all__ = (
    'login_view',
)


def login_view(request):
    # 1. members.urls <- members 로 include 되도록 config url 에 추가
    # 2. path 구현
    # 3. path 와 view 연결
    # 4. form 작성
    # 5. post 요청을 보내 뷰에서 잘 왔는지 확인
    # URL 'members/login/

    print('출력내용:', request.GET.get('next'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print('성공')

            # authenticate 로 db 와 확인 request 세션값을 주고
            # session_id 값을 django_sessions 테이블에 저장, 데이터는 user 와 연결됨
            # 이 함수 실행 후 돌려줄 HTTP Response 에는 Set-Cookie 헤더를 추가, 내용은 session id= session 값
            login(request, user)

            next = request.GET.get('next')

            if next:
                return redirect(next)

            return redirect('index')

        else:
            print('실패')
            return redirect('members:login')

    return render(request, 'members/login.html')
