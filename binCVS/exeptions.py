import os
from binCVS.ClassCVS import my_cvs


# Проверяет есть ли файлы для отслеживания
def track_files_is_empty():
    if len(my_cvs.track_files) == 0:
        print('Добавьте файлы для отслеживания')
        raise SystemExit()


# Проверка версии проекта на существование
def incorrect_prj_ver(ver):
    try:
        ver = int(ver)
    except ValueError:
        print('Неккоректная версия проекта')
        raise SystemExit

    if ver < 1 or my_cvs.last_project_version < ver:
        print(str(ver) + ' версии проекта не существует')
        raise SystemExit


# Проверяет инициализирован ли .cvs
def check_initialized():
    if not os.path.exists(my_cvs.way_to_cvs):
        print('Неинициализирован .cvs')
        raise SystemExit
    if not os.path.exists(my_cvs.way_to_cvs_data):
        print('Не удалось найти .cvs\\cvsData\n')
        print('Переинициализируйте .cvs')
        raise SystemExit
    if not os.path.exists(my_cvs.way_to_prj_ver):
        print('Не удалось найти .cvs\\prjVer\n')
        print('Переинициализируйте .cvs')
        raise SystemExit
