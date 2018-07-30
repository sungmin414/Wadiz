from django.shortcuts import redirect

__all__ = (
    'withdraw',
)


def withdraw(request):

    request.user.delete()

    return redirect('index')
