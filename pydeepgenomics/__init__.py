import os
import shutil

# If custom version of params doesn't exist, copy template
path_params = os.path.join(
	os.path.dirname(os.path.abspath(__file__)), "preprocess")
if not os.path.isfile(os.path.join(path_params, "settings.py")):
	shutil.copy(
			os.path.join(path_params, "settings_template.py"),
			os.path.join(path_params, "settings.py"))
