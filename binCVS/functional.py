import os
import ctypes
import shutil
import datetime
import re

from binCVS.ClassCVS import my_cvs
from binCVS.build_files import make_diff, make_file, way_to
from binCVS.exeptions import incorrect_prj_ver
from binCVS.work_with_files import find_all_files, create_file, write_file, rewrite_file, read_file


# Функционал для команды init
def command_init():
    if not os.path.exists(my_cvs.way_to_cvs):
        os.makedirs(my_cvs.way_to_cvs)
        ctypes.windll.kernel32.SetFileAttributesW(my_cvs.way_to_cvs, 0x02)

        os.makedirs(my_cvs.way_to_prj_ver)
        os.makedirs(my_cvs.way_to_cvs_data)
        print(my_cvs.track_files)
        create_file(my_cvs.track_files)
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
        write_file(my_cvs.track_files, new_track_files)

    return new_track_files


# Функционал для команды commit
def command_commit(value):
    create_new_prj_ver_dir()
    way_to_new_prjver = os.path.join(my_cvs.way_to_prj_ver, str(my_cvs.last_project_version + 1))

    create_file(my_cvs.way_to_added_file)

    added_files = read_file(my_cvs.way_to_added_file)

    for t_file in my_cvs.track_files:
        if t_file not in added_files:
            way_to_t_file = way_to(way_to_new_prjver, t_file)
            open(way_to_t_file, 'w').close()
            way_to_first_file = way_to(my_cvs.cur_dir, t_file)
            shutil.copy(way_to_first_file, way_to_t_file)
            with open(my_cvs.way_to_added_file, 'a', encoding='utf-8-sig') as a_files:
                a_files.write(t_file + '\n')
        else:
            make_diff(t_file)

    cur_files = find_all_files(way_to_new_prjver)
    if len(cur_files) == 0:
        shutil.rmtree(way_to_new_prjver)

    if os.path.exists(way_to_new_prjver):
        print("Успешно добавлены файлы:")
        files = find_all_files(way_to_new_prjver)
        for file in files:
            print('   ' + file)

        if value:
            with open(os.path.join(way_to_new_prjver, '.comment'), 'w', encoding='utf-8-sig') as f:
                f.write(value)

        with open(os.path.join(way_to_new_prjver, '.date'), 'w', encoding='utf-8-sig') as f:
            d = datetime.datetime.now()
            f.write(str(d.date()) + ' ' + str(d.hour) + ':' + str(d.minute))
    else:
        print('Нет изменённых файлов')


# Функционал для команды reset
def command_reset(args, value, value_plus):
    if not value:
        print('Введите версию проекта')
        raise SystemExit

    if not args.value_plus:
        incorrect_prj_ver(value)

        for t_file in my_cvs.track_files:
            make_file(t_file, value)
        print("Откат на версию " + value + " произошёл успешно")
    else:
        value, args.value_plus = value_plus, value
        incorrect_prj_ver(value)
        t_file = value_plus
        make_file(t_file, value)
        print("Откат файла " + t_file + " на версию " + value + " произошёл успешно")


# Функционал для командыв delete
def command_delete(value):
    if value:
        track_files = my_cvs.track_files

        if value in track_files:
            track_files.remove(value)
            with open(my_cvs.way_to_track_file, 'w', encoding='utf-8-sig') as f:
                for t_file in track_files:
                    f.write(t_file + '\n')
            print('Файл ' + value + ' больше не отслеживается')
        else:
            print('Файл ' + value + ' ещё не отслеживается')
    else:
        print('Вы не ввели название файла')


# Функционал для команды log
def command_log():
    return_log = 'Версии проекта:\n'
    folders = os.listdir(my_cvs.way_to_prj_ver)
    if not len(folders) == 0:
        for folder in folders:
            if os.path.isdir(os.path.join(my_cvs.way_to_prj_ver, folder)):
                with open(os.path.join(my_cvs.way_to_prj_ver, folder, '.date'), encoding='utf-8-sig') as f_date:
                    return_log += '   ' + folder + ' версия от ' + f_date.read() + '\n'
                if os.path.exists(os.path.join(my_cvs.way_to_prj_ver, folder, '.comment')):
                    with open(os.path.join(my_cvs.way_to_prj_ver, folder, '.comment'),
                              encoding='utf-8-sig') as f_comment:
                        return_log += '   Комментарий: ' + f_comment.read() + '\n'
                return_log += '\n'
    else:
        print('Отсутствуют сохранённые версии проекта')
        raise SystemExit
    print(return_log)


# Создаёт новую директорию для commit
def create_new_prj_ver_dir():
    os.makedirs(os.path.join(my_cvs.way_to_prj_ver, str(my_cvs.last_project_version + 1)))


# Добавляет файл(ы) в отслеживаемые
def add_track_files(files):
    added_files = []

    way_to_track_files = my_cvs.way_to_track_file

    if not os.path.exists(way_to_track_files):
        open(way_to_track_files, 'w+', encoding='utf-8-sig').close()

    if isinstance(files, str):
        added_files.append(files)
    else:
        for new_file in files:
            if new_file not in my_cvs.track_files:
                added_files.append(new_file)

    with open(way_to_track_files, 'a', encoding='utf-8-sig') as f:
        for new_file in added_files:
            f.write(new_file + '\n')
