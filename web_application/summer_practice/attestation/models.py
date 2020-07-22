from django.db import models


class Subject(models.Model):
    subject_name = models.CharField('название предмета', max_length=25, null=True, blank=True)
    teacher = models.CharField('Ф.И.О', null=True, blank=True, max_length=25)

    def __str__(self):
        return self.subject_name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Certification(models.Model):
    mark1 = models.CharField('оценка за первую аттестацию', null=True, blank=True, max_length=2)
    mark2 = models.CharField('оценка за вторую аттестацию', null=True, blank=True, max_length=2)
    mark3 = models.CharField('оценка за третью аттестацию', null=True, blank=True, max_length=2)

    summa_mark = models.IntegerField('общая оценка', null=True, blank=True)
    avg_mark = models.IntegerField('средняя оценка', null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="предмет", related_name='subject')
    student = models.ForeignKey('questionary.Student', on_delete=models.CASCADE, verbose_name="студент",
                                related_name='student')

    def __str__(self):
        return "Аттестация№" + str(self.pk)

    class Meta:
        verbose_name = 'Аттестация'
        verbose_name_plural = 'Аттестации'
