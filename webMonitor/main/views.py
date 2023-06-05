import json
import statistics

from django.core.serializers import serialize
from django.shortcuts import render
from .models import CpuData
from datetime import datetime, timedelta


def index(request):
    last_hour = datetime.now() - timedelta(hours=1)
    data = CpuData.objects.filter(dateTime__range=[last_hour, datetime.now()])
    serialized_data = serialize("json", data)
    serialized_data = json.loads(serialized_data)

    output = []
    output_avg = []

    temp_output_avg = []
    for i in range(0, 60 * 60, 5):
        date_time_delta = last_hour + timedelta(seconds=i)

        cpu_data = CpuData()
        cpu_data.id = -1
        cpu_data.percent = 0.0
        cpu_data.dateTime = date_time_delta

        for s in serialized_data:
            cpu_load_date_time = datetime.strptime(s['fields']['dateTime'], '%Y-%m-%dT%H:%M:%S.%f')
            distinction_date_time = (date_time_delta - cpu_load_date_time).total_seconds()
            if distinction_date_time < 0.0:
                distinction_date_time = (cpu_load_date_time - date_time_delta).total_seconds()
            if distinction_date_time < 4.0:
                cpu_data.id = s['pk']
                cpu_data.percent = s['fields']['percent']

        if len(temp_output_avg) < 12:
            temp_output_avg.append(cpu_data.percent)
        else:
            avg_percent = statistics.mean(temp_output_avg)
            cpu_avg_data = CpuData()
            cpu_avg_data.id = -1
            cpu_avg_data.percent = avg_percent
            cpu_avg_data.dateTime = date_time_delta
            output_avg.append(cpu_avg_data)
            temp_output_avg.clear()
        output.append(cpu_data)

    context = {
        'data': output,
        'avg_data': output_avg
    }
    return render(request, 'main/index.html', context)
