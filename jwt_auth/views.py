from django.shortcuts import render
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'base.html')
        else:
            print('Не валидная ')

    return render(request, 'registration.html', {'form': CustomUserCreationForm})
