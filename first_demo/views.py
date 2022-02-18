from django.shortcuts import render


def home(request):

    if request.user.is_authenticated:
        user_id = request.user.id
        print("=========>>>>>>>>",request.user.id)

        return render(request, 'home.html')