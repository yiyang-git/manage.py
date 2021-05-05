from django.shortcuts import render, HttpResponse, redirect
from Data_manage.models import WeldSpot, Task
import json
import os
# Create your views here.


def raytest(request):
    if request.method == 'GET':
        task_id = request.GET.get('task_id')
        task_list = Task.objects.values('id',
                                        'task_code',
                                        )
        if task_id == None:
            task_id = task_list.first()['id']

        spot_list = WeldSpot.objects.filter(task_code_id=task_id).values(
            'id',
            'spot_code',
            'ray_test_status',
        )
        return render(request, 'ray_test.html', {'task_list': task_list, 'data_list': spot_list, 'task_id': task_id})
    else:
        task_id = request.POST.get('task_id')
        spot_code = request.POST.get('spot_code')
        if spot_code != '':
            task_obj = Task.objects.filter(pk=task_id).first()
            spot = WeldSpot(
                spot_code=spot_code,
                task_code=task_obj
            )
            spot.save()
        return redirect('/RayTest/raytest/?task_id=' + str(task_id))


def raytest_result_save(request):
    if request.method == 'GET':
        spot_id = request.GET.get('spot_id')
        spot_info = {'spot_id': spot_id,
                     'inspector': '暂无',
                     'spot_code': None,
                     'ray_defect_type_0': [],
                     'ray_test_result': None,
                     'ray_test_notes': None,
                     'img_file_list': [],
                     }
        spot = WeldSpot.objects.filter(pk=spot_id).values('spot_code',
                                                      'ray_inspector_code',
                                                      'ray_defect_type',
                                                      'ray_test_notes',
                                                      'ray_test_result',
                                                      ).first()
        spot_info['spot_code'] = spot['spot_code']
        spot_info['inspector'] = spot['ray_inspector_code']
        spot_info['ray_test_notes'] = spot['ray_test_notes']
        spot_info['ray_test_result'] = spot['ray_test_result']
        return HttpResponse(json.dumps(spot_info))
    else:
        spot_id = request.POST.get('spot_id')
        inspector = request.POST.get('inspector')
        # defect_type = request.POST.get('defect_type')
        test_result = request.POST.get('test_result')
        test_notes = request.POST.get('test_notes')
        WeldSpot.objects.filter(pk=spot_id).update(
            ray_inspector_code=inspector,
            ray_test_result=test_result,
            ray_test_notes=test_notes,
        )
        return HttpResponse(test_notes)