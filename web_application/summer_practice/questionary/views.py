from django.shortcuts import render, redirect
from django.views import View
from .models import Student
from attestation.models import Subject, Certification
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# Create your views here.


class FormView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'questionary/create_profile.html')

    def post(self, request):
        firstName = request.POST.get('firstName').strip()
        lastName = request.POST.get('lastName').strip()
        patronymic = request.POST.get('patronymic')
        email = request.POST.get('email')
        address = request.POST.get('address')
        country = request.POST.get('country')
        numberFromGroup = request.POST.get('numberFromGroup')
        specialty = request.POST.get('specialty')
        form_group = request.POST.get('form-of-training')
        telephone = request.POST.get('telephone')
        course = request.POST.get('course')
        print(Student.objects.filter(last_name=lastName, group=numberFromGroup))
        try:
            if len(Student.objects.filter(last_name=lastName)) == 0:
                Student.objects.create(
                    first_name=firstName, last_name=lastName,
                    patronymic=patronymic, email=email, address=address,
                    country=country, group=numberFromGroup, specialty=specialty,
                    form_group=form_group, telephone=telephone,
                    course=course
                )
            else:
                Student.objects.filter(last_name=lastName, group=numberFromGroup).update(
                    first_name=firstName,
                    patronymic=patronymic, email=email, address=address,
                    country=country, group=numberFromGroup,
                    specialty=specialty,
                    form_group=form_group, telephone=telephone,
                    course=course
                )
            return render(request, 'questionary/create_profile.html', {
                'message': 'Данные успешно сохранены!'
            })
        except Exception:
            return render(request, 'questionary/create_profile.html', {
                'errors': 'Некорректные данные!'
            })


def show_the_list_of_students(request):
    students = Student.objects.all()
    if request.POST:
        if not request.POST.get('sort_course') and not request.POST.get('sort_group') and not request.POST.get(
                'sort_last_name'):
            students = Student.objects.all()
        elif not request.POST.get('sort_course') and not request.POST.get('sort_group') and request.POST.get(
                'sort_last_name'):
            students = Student.objects.all().order_by('last_name')
        elif not request.POST.get('sort_course') and request.POST.get('sort_group') and request.POST.get(
                'sort_last_name'):
            students = Student.objects.all().order_by('-group', 'last_name')
        elif request.POST.get('sort_course') and not request.POST.get('sort_group') and not request.POST.get(
                'sort_last_name'):
            students = Student.objects.all().order_by('-course')
        elif request.POST.get('sort_course') and not request.POST.get('sort_group') and request.POST.get(
                'sort_last_name'):
            students = Student.objects.all().order_by('-course', 'last_name')
        elif request.POST.get('sort_course') and request.POST.get('sort_group') and not request.POST.get(
                'sort_last_name'):
            students = Student.objects.all().order_by('-course', '-group')
        elif request.POST.get('sort_course') and request.POST.get('sort_group') and request.POST.get('sort_last_name'):
            students = Student.objects.all().order_by('-course', '-group', 'last_name')
        else:
            students = Student.objects.all().order_by('-group')
    return render(request, 'questionary/show_student.html', {
        'students': students
    })


def detail_student(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        certification = Certification.objects.filter(student__last_name=student.last_name,
                                                     student__group=student.group
                                                     )
        print(certification)
        if request.POST:
            firstName = request.POST.get('firstName').strip()
            lastName = request.POST.get('lastName').strip()
            patronymic = request.POST.get('patronymic')
            email = request.POST.get('email')
            address = request.POST.get('address')
            country = request.POST.get('country')
            numberFromGroup = request.POST.get('numberFromGroup')
            specialty = request.POST.get('specialty')
            form_group = request.POST.get('form-of-training')
            telephone = request.POST.get('telephone')
            course = request.POST.get('course')

            try:
                if len(Student.objects.filter(last_name=lastName)) == 0:
                    Student.objects.create(
                        first_name=firstName, last_name=lastName,
                        patronymic=patronymic, email=email, address=address,
                        country=country, group=numberFromGroup, specialty=specialty,
                        form_group=form_group, telephone=telephone,
                        course=course
                    )
                else:
                    Student.objects.filter(last_name=lastName).update(
                        first_name=firstName,
                        patronymic=patronymic, email=email, address=address,
                        country=country, group=numberFromGroup,
                        specialty=specialty,
                        form_group=form_group, telephone=telephone,
                        course=course
                    )
                return render(request, 'questionary/create_profile.html', {
                    'message': 'Данные успешно сохранены!'
                })
            except Exception:
                return render(request, 'questionary/create_profile.html', {
                    'errors': 'Некорректные данные!'
                })
    except:
        raise Http404("Студент не найден!")

    return render(request, 'questionary/create_profile.html', {
        'student': student,
        'certification': certification
    })
