import os
from outside.oyt_info import settings

project_folder = os.getcwd()
app_settings_uploaders = settings.SettingsUploaders(
    os.path.join(project_folder, "outside", "oyt_info", "SETTINGS_UPLOADERS.json"))
