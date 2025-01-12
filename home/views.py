from django.shortcuts import render

def home_view(request):
    if request.user.is_authenticated:
        context = {
            "ad": request.user.get_full_name() or request.user.username,
        }
    else:
        context = {
            "ad": "Müşteri",
        }
    return render(request, 'home.html', context)

