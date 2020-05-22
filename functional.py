import argparse
import os
import ctypes
import shutil
import datetime

from help import *
from ClassCVS import my_cvs
from work_with_files import find_all_files, add_track_files, create_new_prj_ver_dir
from build_files import make_diff, make_file
from exeptions import incorrect_prj_ver


# Объявление ожидаемых аргументов командной строки
def check_args():
    parse_args = argparse.ArgumentParser(add_help=False, conflict_handler='resolve')
    parse_args.add_argument('command', nargs='?', default='--about')
    parse_args.add_argument('value', nargs='?')
    parse_args.add_argument('value_plus', nargs='?')
    parse_args.add_argument('-h', '--help', action="store_true")
    parse_args.add_argument('-a', '--about', action="store_true")
    parse_args.add_argument('-i', '--info', action="store_true")

    return parse_args


# Функция служит выводом на консоль информации для -h и -a
def print_help(args, command):
    if args.help:
        h_help()
    else:
        if args.about or command == '--about':
            h_about()


# Функционал для команды init
def command_init():
    main_folder = my_cvs.cur_dir + '\\.cvs'

    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        ctypes.windll.kernel32.SetFileAttributesW(main_folder, 0x02)
        os.makedirs(main_folder + '\\prjVer')
        os.makedirs(main_folder + '\\cvsData')
        print('.cvs успешно инициализирован в ' + my_cvs.cur_dir + '\\.cvs')
    else:
        print('.cvs уже инициализирован в ' + my_cvs.cur_dir + '\\.cvs')


# Функционал для команды add
def command_add(value, args_info):
    if not value and not args_info:
        h_add()

    elif not value and args_info:
        print('Отслеживаемые файлы:')
        if os.path.exists(my_cvs.cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'):
            with open(my_cvs.cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'r', encoding='utf-8-sig') as f:
                track_files = f.read().splitlines()
            for file in track_files:
                print('   ' + file)
        else:
            print('Нет отслеживаемых файлов\n')
            print('Введите CVS.py add для получения справки')

    elif value == '.' and not args_info:
        file_list = find_all_files(my_cvs.cur_dir)
        add_track_files(file_list)

    elif not args_info:
        file_list = find_all_files(my_cvs.cur_dir)

        if value in file_list:
            add_track_files(value)
        else:
            print("Не удалось найти файл " + value)


# Обрабатывает название файла на поддиректории, создаёт их и выводит путь к файлу
def way_to(way_dir, file_name):
    reversed_file = file_name[::-1]
    splited_file = reversed_file.split('\\', 1)
    splited_file[0] = splited_file[0][::-1]
    if len(splited_file) == 1:
        return way_dir + '\\' + file_name

    splited_file[1] = splited_file[1][::-1]
    if not os.path.exists(way_dir + '\\' + splited_file[1]):
        os.mkdir(way_dir + '\\' + splited_file[1])
    return way_dir + '\\' + splited_file[1] + '\\' + splited_file[0]


# Функционал для команды commit
def command_commit(value):
    create_new_prj_ver_dir()
    way_to_new_prjver = my_cvs.cur_dir + '\\.cvs\\prjVer\\' + str(my_cvs.last_project_version + 1)

    if not os.path.exists(my_cvs.cur_dir + '\\.cvs\\prjVer\\.addedFiles'):
        open(my_cvs.cur_dir + '\\.cvs\\prjVer\\.addedFiles', 'w', encoding='utf-8-sig').close()

    with open(my_cvs.cur_dir + '\\.cvs\\prjVer\\.addedFiles', 'r', encoding='utf-8-sig') as a_files:
        added_files = a_files.read().splitlines()

    for t_file in my_cvs.track_files:
        if t_file not in added_files:
            way_to_t_file = way_to(way_to_new_prjver, t_file)
            open(way_to_t_file, 'w').close()
            way_to_first_file = way_to(my_cvs.cur_dir, t_file)
            shutil.copy(way_to_first_file, way_to_t_file)
            with open(my_cvs.cur_dir + '\\.cvs\\prjVer\\.addedFiles', 'a', encoding='utf-8-sig') as a_files:
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
            with open(way_to_new_prjver + '\\.comment', 'w', encoding='utf-8-sig') as f:
                f.write(value)

        with open(way_to_new_prjver + '\\.date', 'w', encoding='utf-8-sig') as f:
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
            with open(my_cvs.cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'w', encoding='utf-8-sig') as f:
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
    way_to_prj_ver = my_cvs.cur_dir + '\\.cvs\\prjVer'
    folders = os.listdir(way_to_prj_ver)
    if not len(folders) == 0:
        for folder in folders:
            if os.path.isdir(way_to_prj_ver + '\\' + folder):
                with open(way_to_prj_ver + '\\' + folder + '\\.date', encoding='utf-8-sig') as f_date:
                    return_log += '   ' + folder + ' версия от ' + f_date.read() + '\n'
                if os.path.exists(way_to_prj_ver + '\\' + folder + '\\.comment'):
                    with open(way_to_prj_ver + '\\' + folder + '\\.comment', encoding='utf-8-sig') as f_comment:
                        return_log += '   Комментарий: ' + f_comment.read() + '\n'
                return_log += '\n'
    else:
        print('Отсутствуют сохранённые версии проекта')
        raise SystemExit
    print(return_log)
