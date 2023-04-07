import os
from outside.oyt_info import settings

project_folder = os.getcwd()
app_settings = settings.Settings(os.path.join(project_folder, "outside", "oyt_info", "SETTINGS.json"))
