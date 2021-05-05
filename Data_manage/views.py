from django.shortcuts import render, HttpResponse, redirect
from Data_manage.models import WeldSpot, Task


# Create your views here.
def show_table(request):
    task_list = Task.objects.values('id',
                                    'task_code',
                                    'weld_method',
                                    'worker_code',
                                    'machine_code',
                                    'product_code',
                                    'process_card',
                                    'app_test',
                                    'ray_test',
                                    'other_test_method',
                                    )

    return render(request, 'table_file.html', {'data_list': task_list})


def del_data(request):
    id = request.GET.get('id')
    print(id)
    task = Task.objects.get(id=id)
    task.delete()
    return redirect('/Data_manage/table/')


def add_task(request):
    if request.method == 'GET':
        return render(request, 'form_file.html')
    else:
        task_code = request.POST.get('task_code')
        weld_method = request.POST.get('weld_method')
        worker_code = request.POST.get('worker_code')
        machine_code = request.POST.get('machine_code')
        product_code = request.POST.get('product_code')
        process_card = request.POST.get('process_card')

        print(process_card)

        app_test = request.POST.get('app_test')
        if app_test == 'on':
            app_test = True
        else:
            app_test = False

        ray_test = request.POST.get('ray_test')
        if ray_test == 'on':
            ray_test = True
        else:
            ray_test = False

        other_test = request.POST.get('other_test')
        if other_test == '不需要其他检测':
            other_test = None
        task = Task(task_code=task_code,
                    worker_code=worker_code,
                    weld_method=weld_method,
                    machine_code=machine_code,
                    product_code=product_code,
                    process_card=process_card,
                    app_test=app_test,
                    ray_test=ray_test,
                    other_test_method=other_test,
                    )
        task.save()
        return redirect('/Data_manage/table/')


def edit_task(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        task = Task.objects.get(id=id)
        return render(request, 'edit_file.html', {"task": task})
    else:
        nid = request.GET.get('nid')
        task_code = request.POST.get('task_code')
        weld_method = request.POST.get('weld_method')
        worker_code = request.POST.get('worker_code')
        machine_code = request.POST.get('machine_code')
        product_code = request.POST.get('product_code')
        process_card = request.POST.get('process_card')
        app_test = request.POST.get('app_test')
        if app_test == 'on':
            app_test = True
        else:
            app_test = False
        ray_test = request.POST.get('ray_test')
        if ray_test == 'on':
            ray_test = True
        else:
            ray_test = False
        other_test = request.POST.get('other_test')
        if other_test == '不需要其他检测':
            other_test = None

        if process_card == '':
            Task.objects.filter(id=nid).update(
                task_code=task_code,
                worker_code=worker_code,
                weld_method=weld_method,
                machine_code=machine_code,
                product_code=product_code,
                app_test=app_test,
                ray_test=ray_test,
                other_test_method=other_test,
            )
        else:
            Task.objects.filter(id=nid).update(
                task_code=task_code,
                worker_code=worker_code,
                weld_method=weld_method,
                machine_code=machine_code,
                product_code=product_code,
                app_test=app_test,
                ray_test=ray_test,
                other_test_method=other_test,
                process_card=process_card,
            )
        return redirect('/Data_manage/table/')


def show_process(request):
    file_name = request.GET.get('file_name')
    print(file_name)
    return render(request, 'process_card.html', {'image_name': file_name})


def show_spot_table(request):
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
            'app_inspector_code',
            'app_defect_type',
            'app_test_result',
            'app_test_notes',
            'ray_test_status',
            'ray_inspector_code',
            'ray_defect_type',
            'ray_test_result',
            'ray_test_notes',
            'task_code_id',
        )
        return render(request, 'spot_table.html', {'task_list': task_list, 'data_list': spot_list, 'task_id': task_id})
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
        return redirect('/Data_manage/spot_table/?task_id=' + str(task_id))


def del_spot(request):
    id = request.GET.get('id')
    spot = WeldSpot.objects.get(id=id)
    task_id = spot.task_code.id
    spot.delete()
    return redirect('/Data_manage/spot_table/?task_id=' + str(task_id))