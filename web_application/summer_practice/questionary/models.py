from django.db import models


class Student(models.Model):
    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    patronymic = models.CharField('Отчество', max_length=30)
    email = models.EmailField('Почта', null=True, blank=True)
    address = models.CharField('Адрес', max_length=50)
    country = models.CharField('Страна', max_length=40)
    group = models.IntegerField('Номер группы')
    course = models.IntegerField('Номер курса', null=True, blank=True)
    telephone = models.CharField('Номер телефона', max_length=13, null=True, blank=True)
    specialty = models.CharField('Специальность', max_length=100)
    form_group = models.CharField('Форма обучения', max_length=20)

    def __str__(self):
        return self.last_name + ":" + str(self.group) + "группа"

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
