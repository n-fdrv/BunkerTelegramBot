from datetime import datetime
from os import listdir
from os.path import isfile, join

from django.apps import apps
from django.shortcuts import render

from bot.models import User


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


def send_message_view(request):
    """View to show send_message page."""
    data = {}
    if request.method == "POST":
        text = request.POST["text"]
        app_config = apps.get_app_config("bot")
        app = app_config.bot
        scheduler = app.get_scheduler()
        bot = app.get_bot()
        users = User.objects.all()
        for user in users:
            scheduler.add_job(
                bot.send_message,
                "date",
                run_date=datetime.now(),
                args=[user.telegram_id, text],
            )
        data = {"success": True, "text": text}
    return render(request, "send_message.html", data)
