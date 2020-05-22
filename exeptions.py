import os
from ClassCVS import CVS


# Проверяет есть ли файлы для отслеживания
def track_files_is_empty():
    if len(CVS.track_files) == 0:
        print('Добавьте файлы для отслеживания')
        raise SystemExit()


# Проверка версии проекта на существование
def incorrect_prj_ver(ver):
    try:
        ver = int(ver)
    except ValueError:
        print('Неккоректная версия проекта')
        raise SystemExit

    if ver < 1 or CVS.last_project_version < ver:
        print(str(ver) + ' версии проекта не существует')
        raise SystemExit


# Проверяет инициализирован ли .cvs
def check_initialized():
    if not os.path.exists(CVS.cur_dir + '\\.cvs'):
        print('Неинициализирован .cvs')
        raise SystemExit
    if not os.path.exists(CVS.cur_dir + '\\.cvs\\cvsData'):
        print('Не удалось найти .cvs\\cvsData\n')
        print('Переинициализируйте .cvs')
        raise SystemExit
    if not os.path.exists(CVS.cur_dir + '\\.cvs\\prjVer'):
        print('Не удалось найти .cvs\\prjVer\n')
        print('Переинициализируйте .cvs')
        raise SystemExit
