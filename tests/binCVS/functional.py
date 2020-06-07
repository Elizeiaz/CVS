import os
import ctypes
import shutil
import datetime
import re

from binCVS.classes import my_cvs
from binCVS.build_files import make_diff, make_file, make_subdirectory
from binCVS.work_with_files import find_all_files
from binCVS.base_work_with_files import create_file, write_file, rewrite_file, read_file


# Функционал для команды init
def command_init():
    if not os.path.exists(my_cvs.path.way_to_cvs):
        os.makedirs(my_cvs.path.way_to_cvs)
        ctypes.windll.kernel32.SetFileAttributesW(my_cvs.path.way_to_cvs, 0x02)

        os.makedirs(my_cvs.path.way_to_prj_ver)
        os.makedirs(my_cvs.path.way_to_cvs_data)
        create_file(my_cvs.path.way_to_track_file)
        create_file(my_cvs.path.way_to_added_file)
        return True

    return False


# Функционал для команды add
def command_add(file_name):
    all_files = find_all_files(my_cvs.cur_dir)
    is_reg = False
    new_track_files = []

    if file_name[0] == '*':
        file_name = '.' + file_name + '$'
        is_reg = True
    elif file_name[0] == '.' and len(file_name) == 1:
        file_name = file_name + '*[^\n]'
        is_reg = True

    if is_reg:
        for cur_file in all_files:
            if cur_file not in my_cvs.track_files:
                matched_file = re.findall(file_name, cur_file)
                if len(matched_file) > 0:
                    new_track_files.append(matched_file[0])
    else:
        if file_name in all_files and file_name not in my_cvs.track_files:
            new_track_files.append(file_name)

    if len(new_track_files) > 0:
        write_file(my_cvs.path.way_to_track_file, new_track_files)

    return new_track_files


# Функционал для команды commit
def command_commit(value):
    create_new_prj_ver_dir()
    way_to_new_prjver = os.path.join(my_cvs.path.way_to_prj_ver, str(my_cvs.last_project_version + 1))
    commited_files = []

    for t_file in my_cvs.track_files:
        if t_file not in my_cvs.added_files:
            way_to_t_file = make_subdirectory(way_to_new_prjver, t_file)
            create_file(way_to_t_file)
            shutil.copy(os.path.join(my_cvs.cur_dir, t_file), way_to_t_file)
            write_file(my_cvs.path.way_to_added_file, t_file)
            commited_files.append(t_file)
        else:
            commited_file = make_diff(t_file)
            if commited_file:
                commited_files.append(commited_file)

    if commited_files:
        write_file(os.path.join(way_to_new_prjver, '.comment'), value)
        d = datetime.datetime.now()
        write_file(os.path.join(way_to_new_prjver, '.date'), str(d.date()) + ' ' + str(d.hour) + ':' + str(d.minute))

    return commited_files


# Функционал для команды reset
def command_reset(version=my_cvs.last_project_version, file_name=None):
    if file_name:
        make_file(file_name, version)
    else:
        for t_file in my_cvs.track_files:
            make_file(t_file, version)

    return version


# Функционал для командыв delete
def command_delete(file_name):
    track_files = my_cvs.track_files
    is_reg = False
    deleted_files = []
    matched_files = []

    if file_name[0] == '*':
        file_name = '.' + file_name + '$'
        is_reg = True
    elif file_name[0] == '.' and len(file_name) == 1:
        file_name = file_name + '*[^\n]'
        is_reg = True

    if is_reg:
        for t_file in track_files:
            matched_files.append(re.findall(file_name, t_file))
        if len(matched_files) > 0:
            for matched_file in matched_files:
                if matched_file:
                    if matched_file[0] in track_files:
                        track_files.remove(matched_file[0])
                        deleted_files.append(matched_file[0])
    else:
        if file_name in track_files:
            track_files.remove(file_name)
            deleted_files.append(file_name)

    rewrite_file(my_cvs.path.way_to_track_file, track_files)

    return deleted_files


# Возвращает отслеживаемые файлы
def command_track():
    return my_cvs.track_files


# Функционал для команды log
def command_log():
    log = 'Версии проекта:\n'
    folders = os.listdir(my_cvs.path.way_to_prj_ver)

    if not len(folders) == 0:
        for folder in folders:
            if os.path.isdir(os.path.join(my_cvs.path.way_to_prj_ver, folder)):
                log += 'Версия : ' + folder + '\n'
                log += 'Дата: ' + str(read_file(os.path.join(my_cvs.path.way_to_prj_ver, folder, '.date'))) + '\n'
                log += 'Комментарий: ' + str(
                    read_file(os.path.join(my_cvs.path.way_to_prj_ver, folder, '.comment'))) + '\n'
                log += '\n'
    else:
        log += 'Отсутствуют версии проекта'

    return log


# Создаёт новую директорию для commit
def create_new_prj_ver_dir():
    os.makedirs(os.path.join(my_cvs.path.way_to_prj_ver, str(my_cvs.last_project_version + 1)))


# Добавляет файл(ы) в отслеживаемые
def add_track_files(files):
    added_files = []
    if isinstance(files, str):
        added_files.append(files)
    else:
        for new_file in files:
            if new_file not in my_cvs.track_files:
                added_files.append(new_file)

    write_file(my_cvs.path.way_to_track_file, added_files)

    return added_files
