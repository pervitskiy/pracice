from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .loads import UploadingFiles


class CertificationView(LoginRequiredMixin, View):
    def get(self, request):
         return render(request, 'attestation/download.html')

    def post(self, request):
        print(request.POST)
        print(request.FILES)
        file = request.FILES['file']
        uploading_file = UploadingFiles(
            {'file': file}
        )

        if uploading_file.chek_type_error():
            return render(request, 'attestation/download.html', {
                "error": 'Неподдерживаемый формат или поврежденный файл'
            })

        elif uploading_file.chek_error_heading():
            return render(request, 'attestation/download.html', {
                "error": 'Проверьте шапку файла на соответствие примеру'
            })

        elif uploading_file.chek_error():
            number_of_rating_gt_44 = uploading_file.number_of_rating_gt_44()
            number_of_rating_gt_34 = uploading_file.number_of_rating_gt_34()
            number_of_rating_gt_24 = uploading_file.number_of_rating_gt_24()
            number_of_rating_lt_25 = uploading_file.number_of_rating_lt_25()

            uploading_file.sum_mark()

            return render(request, 'attestation/download.html', {
                "message": 'Успешная загрузка',
                "number_of_rating_gt_44": number_of_rating_gt_44,
                "number_of_rating_gt_34": number_of_rating_gt_34,
                "number_of_rating_gt_24": number_of_rating_gt_24,
                "number_of_rating_lt_25": number_of_rating_lt_25
            })

        else:
            return render(request, 'attestation/download.html', {
                "error": 'Некорректные данные в файле'
            })
        return redirect("/")
