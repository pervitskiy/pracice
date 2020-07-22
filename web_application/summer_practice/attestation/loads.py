import xlrd
import os, sys
import django
from questionary.models import Student
from django.db.models import Q

os.environ['DJANGO_SETTINGS_MODULE'] = 'taskmanager.setting'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
django.setup()
from .models import Subject, Certification


class UploadingFiles(object):
    def __init__(self, data):
        data = data
        self.error_ = True
        self.eror_heading = False
        self.type_error = False
        self.message_error = ''
        self.list_summa_mark = list()

        self.uploaded_file = data.get("file")
        self.parsing()

    def getting_headers_top(self):
        s = self.s
        headers = dict()
        for column in range(s.ncols):
            value = s.cell(1, column).value
            headers[column] = value
        return headers

    def getting_headers_bt(self):
        s = self.s
        headers = dict()
        for column in range(s.ncols):
            value = s.cell(2, column).value
            headers[column] = value
        return headers

    def transformation(self, row_dict):
        dict_new = {'group': row_dict['group'], 'course': row_dict['course'], 'teacher': row_dict['teacher'],
                    'subject_name': row_dict['subject_name'], 'last_name': ''}
        try:
            if "Ф.И.О".split()[0] in row_dict:
                last_name = row_dict["Ф.И.О"]
                dict_new['last_name'] = last_name.split()[0]

            dict_new['mark1'] = ''
            if "Аттестация:1".split()[0] in row_dict:
                mark1 = row_dict["Аттестация:1".split()[0]]
                if mark1 != '':
                    mark1 = int(mark1)
                    if int(mark1) > 50:
                        self.error_ = False

                dict_new['mark1'] = mark1

            dict_new['mark2'] = ''
            if "Аттестация:2".split()[0] in row_dict:
                mark2 = row_dict["Аттестация:2".split()[0]]
                if mark2 != '':
                    mark2 = int(mark2)
                    if int(mark2) > 50:
                        self.error_ = False

                dict_new['mark2'] = mark2

            dict_new['mark3'] = ''
            if "Аттестация:3 ".split()[0] in row_dict:
                mark3 = row_dict["Аттестация:3 ".split()[0]]
                if mark3 != '':
                    mark3 = int(mark3)
                    if int(mark3) > 50:
                        self.error_ = False

                dict_new['mark3'] = mark3
            return dict_new
        except:
            self.eror_heading = True

    def checking_the_validity(self, s, subject_name, teacher, course, group, headers_bt):
        for row in range(3, s.nrows):
            row_dict = {}
            row_dict['subject_name'] = subject_name
            row_dict['teacher'] = teacher
            row_dict['course'] = course
            row_dict['group'] = group

            for column in range(s.ncols):
                value = s.cell(row, column).value
                field_name = headers_bt[column]
                if field_name == 'id' and not value:
                    continue
                row_dict[field_name] = value

            self.transformation(row_dict)

    def parsing(self):
        uploaded_file = self.uploaded_file

        try:
            wb = xlrd.open_workbook(file_contents=uploaded_file.read())
        except xlrd.XLRDError:
            self.type_error = True
            return

        s = wb.sheet_by_index(0)
        self.s = s

        headers_top = self.getting_headers_top()
        headers_bt = self.getting_headers_bt()

        try:
            course = int(headers_top[0][5:])
            group = int(headers_top[1][7:])
            subject_name = headers_top[2][9:]
            teacher = headers_top[3][15:]
        except ValueError:
            self.eror_heading = True
            return

        if len(Subject.objects.filter(subject_name=subject_name)) == 0:
            Subject.objects.create(
                subject_name=subject_name,
                teacher=teacher
            )

        self.subject_name = subject_name
        self.group = group
        """ Плохая проверка на валидность данных заранее,
            вдруг на последней строчке будут неверные данные,
            а бд мы уже обновили (переписать)
            """
        self.checking_the_validity(
            s, subject_name, teacher, course, group, headers_bt
        )

        for row in range(3, s.nrows):
            row_dict = {}
            row_dict['subject_name'] = subject_name
            row_dict['teacher'] = teacher
            row_dict['course'] = course
            row_dict['group'] = group

            for column in range(s.ncols):
                value = s.cell(row, column).value
                field_name = headers_bt[column]
                if field_name == 'id' and not value:
                    continue
                row_dict[field_name] = value

            dict_new = self.transformation(row_dict)
            summa_mark = 0
            count = 0
            try:
                if dict_new['mark1'] != '':
                    summa_mark += int(dict_new['mark1'])
                    count += 1

                if dict_new['mark2'] != '':
                    summa_mark += int(dict_new['mark2'])
                    count += 1

                if dict_new['mark3'] != '':
                    summa_mark += int(dict_new['mark3'])
                    count += 1

                self.list_summa_mark.append((summa_mark, count))

                if self.error_:
                    try:
                        # Когда в строчке присутствует фамилия, которой еще нет в базе данных:
                        if len(Student.objects.filter(last_name=dict_new['last_name'])) == 0:
                            print('----------')
                            print(1)
                            print(Certification.objects.filter(student__last_name=dict_new['last_name']))
                            print(Certification.objects.filter(subject__subject_name=dict_new['subject_name']))
                            print(Certification.objects.filter(
                                student__last_name=dict_new['last_name'],
                                subject__subject_name=dict_new['subject_name']).distinct())
                            print(Subject.objects.filter(subject_name=dict_new['subject_name']))
                            print(Subject.objects.get(subject_name=dict_new['subject_name']))

                            print('----------')
                            Student.objects.create(
                                last_name=dict_new['last_name'],
                                group=dict_new['group'],
                                course=dict_new['course']
                            )

                            Certification.objects.create(
                                mark1=dict_new['mark1'],
                                mark2=dict_new['mark2'],
                                mark3=dict_new['mark3'],
                                avg_mark= int(summa_mark / count),
                                summa_mark=summa_mark,
                                subject=Subject.objects.get(subject_name=dict_new['subject_name']),
                                student=Student.objects.get(last_name=dict_new['last_name'])
                            )

                        # если у студента по предмету нет оценки, то создать атту с оценками
                        elif len(Certification.objects.filter(
                                student__last_name=dict_new['last_name'],
                                subject__subject_name=dict_new['subject_name']).distinct()) == 0:
                            print('----------')
                            print(2)
                            print(dict_new['last_name'])
                            print(dict_new['subject_name'])
                            print(Certification.objects.filter(
                                student__last_name=dict_new['last_name'],
                                subject__subject_name=dict_new['subject_name']).distinct())
                            print(Certification.objects.filter(student__last_name=dict_new['last_name']))
                            print(Certification.objects.filter(subject__subject_name=dict_new['subject_name']))
                            print(Student.objects.filter(last_name=dict_new['last_name']))
                            print(Subject.objects.filter(subject_name=dict_new['subject_name']))
                            print('----------')
                            Certification.objects.create(
                                mark1=dict_new['mark1'],
                                mark2=dict_new['mark2'],
                                mark3=dict_new['mark3'],
                                summa_mark=summa_mark,
                                avg_mark=int(summa_mark / count),
                                subject=Subject.objects.get(subject_name=dict_new['subject_name']),
                                student=Student.objects.get(last_name=dict_new['last_name'])
                            )



                        # Когда есть фамилия и предмет в базе данных, то тогда просто обновим оценки, если они изменились)
                        else:
                            print('----------')
                            print(3)
                            print(Certification.objects.filter(student__last_name=dict_new['last_name']))
                            print(Certification.objects.filter(subject__subject_name=dict_new['subject_name']))
                            print(Subject.objects.get(subject_name=dict_new['subject_name']))
                            print(Certification.objects.filter(
                                student__last_name=dict_new['last_name'],
                                subject__subject_name=dict_new['subject_name']).distinct())
                            print('----------')
                            Certification.objects.filter(
                                student__last_name=dict_new['last_name'],
                                subject__subject_name=dict_new['subject_name']).update(
                                mark1=dict_new['mark1'],
                                mark2=dict_new['mark2'],
                                mark3=dict_new['mark3'],
                                summa_mark=summa_mark,
                                avg_mark=int(summa_mark / count),

                            )

                    except:
                        self.error_ = False
                        return False
            except:
                self.error_ = False
                return False

    def chek_error(self):
        return self.error_

    def chek_type_error(self):
        return self.type_error

    def chek_error_heading(self):
        return self.eror_heading

    def sum_mark(self):
        print(self.list_summa_mark)
        return self.list_summa_mark

    def number_of_rating_gt_44(self):
        print([el for el in self.list_summa_mark if int(el[0] / el[1]) > 44])
        return len([el for el in self.list_summa_mark if int(el[0] / el[1]) > 44])

        # Не работает, если загрузить повторно файл, но уже с меньшим числом студентов.
        # В базе же данных все равно этот человек числится, а создавать локальную базу данных не имеет смысла. return

    # return len(Certification.objects.filter(subject__subject_name=self.subject_name, student__group=self.group,
    # summa_mark__gt=44))

    def number_of_rating_gt_34(self):
        print([el for el in self.list_summa_mark if 34 <int(el[0] / el[1]) < 45])
        return len([el for el in self.list_summa_mark if 34 < int(el[0] / el[1]) < 45])

        # return len(Certification.objects.filter(subject__subject_name=self.subject_name, student__group=self.group,
        # summa_mark__gt=34, summa_mark__lt=45))

    def number_of_rating_gt_24(self):
        print([el for el in self.list_summa_mark if 24 < int(el[0] / el[1]) < 35])
        return len([el for el in self.list_summa_mark if 24 < int(el[0] / el[1]) < 35])

        # return len(Certification.objects.filter( subject__subject_name=self.subject_name,
        # student__group=self.group, summa_mark__gt=24, summa_mark__lt=35))

    def number_of_rating_lt_25(self):
        print(([el for el in self.list_summa_mark if int(el[0] / el[1]) < 25]))
        return len([el for el in self.list_summa_mark if int(el[0] / el[1]) < 25])

        # return len(Certification.objects.filter(subject__subject_name=self.subject_name, student__group=self.group,
        # summa_mark__lt=25))
