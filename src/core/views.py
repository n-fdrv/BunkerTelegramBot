from os import listdir
from os.path import isfile, join

from django.shortcuts import render


def show_admin_logs(request):
    """View to show admin logs."""
    logs_path = "logs/"
    logs_files = [f for f in listdir(logs_path) if isfile(join(logs_path, f))]
    data = {"files": logs_files}
    return render(request, "admin_logs.html", data)


def show_admin_log_file(request, log_name):
    """View to show admin_log_file."""
    logs_path = "logs/"
    file_data = []
    with open(f"{logs_path}{log_name}", "r", encoding="utf-8") as file:
        for line in file:
            row_data = line.strip()
            file_data.append(row_data.split(" | "))
    data = {"data": file_data}
    return render(request, "admin_log_file.html", data)
