from django.shortcuts import render, redirect, HttpResponse
from Data_manage.models import WeldSpot, Task
from AppTest.models import AppDataset
import json
import os
from TestModels.app_test import inference
# Create your views here.
DEFECT = ['无', '类型1', '类型2', '类型3', '类型4', '类型5', '类型6']

def apptest(request):
    if request.method == 'GET':
        task_id = request.GET.get('task_id')
        # print(task_id)
        task_list = Task.objects.values('id',
                                        'task_code',
                                        )
        if task_id == None:
            task_id = task_list.first()['id']

        spot_list = WeldSpot.objects.filter(task_code_id=task_id).values(
            'id',
            'spot_code',
            'app_test_status',
        )
        return render(request, 'app_test.html', {'task_list': task_list, 'data_list': spot_list, 'task_id': task_id})
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
        return redirect('/AppTest/apptest/?task_id=' + str(task_id))


def apptest_result_save(request):
    if request.method == 'GET':
        spot_id = request.GET.get('spot_id')
        spot_info = {'spot_id': spot_id,
                     'inspector': '暂无',
                     'spot_code': None,
                     'app_defect_type_0': None,
                     'app_defect_type_1': None,
                     'app_defect_type_2': None,
                     'app_defect_type_3': None,
                     'app_defect_type_4': None,
                     'app_defect_type_5': None,
                     'app_test_result': None,
                     'app_test_notes': None,
                     'img_file_list': [],
                     }
        spot = WeldSpot.objects.filter(pk=spot_id).values('spot_code',
                                                      'app_inspector_code',
                                                      'app_defect_type',
                                                      'app_test_notes',
                                                      'app_test_result',
                                                      'app_defect_type_0',
                                                      'app_defect_type_1',
                                                      'app_defect_type_2',
                                                      'app_defect_type_3',
                                                      'app_defect_type_4',
                                                      'app_defect_type_5',
                                                      ).first()
        spot_info['spot_code'] = spot['spot_code']
        spot_info['inspector'] = spot['app_inspector_code']
        spot_info['app_test_notes'] = spot['app_test_notes']
        spot_info['app_test_result'] = spot['app_test_result']
        spot_info['app_defect_type_0'] = spot['app_defect_type_0']
        spot_info['app_defect_type_1'] = spot['app_defect_type_1']
        spot_info['app_defect_type_2'] = spot['app_defect_type_2']
        spot_info['app_defect_type_3'] = spot['app_defect_type_3']
        spot_info['app_defect_type_4'] = spot['app_defect_type_4']
        spot_info['app_defect_type_5'] = spot['app_defect_type_5']
        spot_info['img_file_list'] = os.listdir(os.path.join('./AppTest/static/app_images', spot_info['spot_code']))
        return HttpResponse(json.dumps(spot_info))
    else:
        spot_id = request.POST.get('spot_id')
        inspector = request.POST.get('inspector')
        defect_type = []
        test_result = request.POST.get('test_result')
        test_notes = request.POST.get('test_notes')
        for e in request.POST.get('defect_types').split():
            if e=='true':
                defect_type.append(True)
            else:
                defect_type.append(False)
        WeldSpot.objects.filter(pk=spot_id).update(
            app_inspector_code=inspector,
            app_test_result=test_result,
            app_test_notes=test_notes,
            app_defect_type_0=defect_type[0],
            app_defect_type_1=defect_type[1],
            app_defect_type_2=defect_type[2],
            app_defect_type_3=defect_type[3],
            app_defect_type_4=defect_type[4],
            app_defect_type_5=defect_type[5],
        )
        return HttpResponse(test_notes)


def start_app_test(request):
    spot_code = request.POST.get('spot_code')
    file_list = os.listdir(os.path.join('./AppTest/static/app_images', spot_code))
    test_result = {
        'img_type_seq': [],
        'type': [0]*6,
        'result': '',
    }
    for e in file_list:
        r = inference.inference(os.path.join('./AppTest/static/app_images', spot_code, e), os.path.join('./AppTest/static/app_test_models', 'model_res18.pkl'))
        test_result['type'][r] += 1
        test_result['img_type_seq'].append(r)
    for i, e in enumerate(test_result['type']):
        if e != 0:
            test_result['result'] += DEFECT[i]+','
    return HttpResponse(json.dumps(test_result))


def app_dataset(request):
    if request.method == 'GET':
        return HttpResponse('请正确操作')
    else:
        # 取post数据
        spot_id = request.POST.get('spot_id')
        img_list = request.POST.getlist('img_list')
        type_list = request.POST.getlist('type_list')
        # 取数据库数据
        spot = WeldSpot.objects.filter(pk=spot_id).values(
            'spot_code'
        ).first()
        folder = spot['spot_code']
        for i in range(len(img_list)):
            a = AppDataset.objects.filter(folder=folder, file_name=img_list[i])
            if len(a)>0:
                a.update(type=type_list[i])
            elif len(a)==0:
                AppDataset.objects.create(folder=folder, file_name=img_list[i], type=type_list[i])
        return HttpResponse('成功')


