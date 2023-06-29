import os
from outside.oyt_info import settings

project_folder = os.getcwd()
app_settings_uploaders = settings.SettingsUploaders(
    os.path.join(project_folder, "outside", "oyt_info", "SETTINGS_UPLOADERS.json"))
text_extensions = [".txt"]
video_extensions = [".mp4", ".avi", ".mov", ".mpeg-1", ".mpeg-2", ".mpg", ".wmv",
                    ".mpegps", ".flv", ".3gpp", ".WebM", ".DNxHR", ".ProRes", ".CineForm", ".HEVC"]
image_extensions = [".pjp", ".jpg", ".pjpeg", ".jpeg", ".jfif", ".png"]
