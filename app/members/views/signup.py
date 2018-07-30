from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect, render

from members.forms import SignupForm


User = get_user_model()

__all__ = (
    'signup',
)


def signup(request):

    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        # 에러메시지가 없음
        if form.is_valid():
            user = form.signup()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    # get 요청일 때 빈 form 을 전달해서 렌더링
    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'members/signup.html', context)