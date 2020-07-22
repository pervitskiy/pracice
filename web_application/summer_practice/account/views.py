from django.contrib.auth import views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse


class ProfilePage(views.TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            login = request.POST.get('login')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            User.objects.filter(username=login).update(
                email=email, first_name=first_name, last_name=last_name
            )
            return redirect("/")
        return render(request, self.template_name)


class LoggedPage(views.LogoutView):
    template_name = "registration/logout.html"


class RegisterView(views.TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password != password2:
                return render(request, self.template_name, {
                    'error': 'Пароли не совпадают!',
                    'username': username,
                    'email': email
                })
            elif len(User.objects.filter(username=username)) != 0:
                return render(request, self.template_name, {
                    'error': 'Пользователь с таким логином уже существует!',
                    'email': email
                })
            elif len(password) < 8:
                return render(request, self.template_name, {
                    'error': 'Длинна пароля меньше 8 символов ',
                    'username': username,
                    'email': email
                })
            else:
                User.objects.create_user(username, email, password)
                return redirect(reverse("login"))



        return render(request, self.template_name)
