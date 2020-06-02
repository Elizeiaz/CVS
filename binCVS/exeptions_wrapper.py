from binCVS.exeptions import track_files_is_empty, check_initialized, incorrect_prj_ver


def track_files_is_empty_wrapper():
    if track_files_is_empty():
        print('!Нет файлов для отслеживания')
        raise SystemExit


def incorrect_prj_ver_wrapper(ver):
    if incorrect_prj_ver(ver):
        print('!Некорректная версия проекта')
        raise SystemExit


def check_initialized_wrapper():
    if not check_initialized():
        print('.cvs неинициализирована')
        raise SystemExit
