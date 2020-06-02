import os
from binCVS.ClassCVS import my_cvs


# Проверяет есть ли файлы для отслеживания
def track_files_is_empty():
    if len(my_cvs.track_files) == 0:
        return True
    return False


# Проверка версии проекта на существование
def incorrect_prj_ver(ver):
    try:
        ver = int(ver)
    except ValueError:
        return True

    if ver < 1 or my_cvs.last_project_version < ver:
        return True

    return False


# Проверяет инициализирован ли .cvs
def check_initialized():
    if not os.path.exists(my_cvs.way_to_cvs):
        print(my_cvs.way_to_cvs)
        return False
    return True