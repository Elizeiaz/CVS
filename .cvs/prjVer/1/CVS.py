import sys
import argparse
import os
import ctypes
import difflib
import shutil

from help import *


# Объявление ожидаемых аргументов командной строки
def checkArgs():
    parse_Args = argparse.ArgumentParser(add_help=False, conflict_handler='resolve')
    parse_Args.add_argument('command', nargs='?', default='--about')
    parse_Args.add_argument('value', nargs='?')
    parse_Args.add_argument('-h', '--help', action="store_true")
    parse_Args.add_argument('-a', '--about', action="store_true")
    parse_Args.add_argument('-i', '--info', action="store_true")

    return parse_Args


# Функция служит выводом на консоль информации для -h и -a
def printHelp(args):
    if args.help:
        h_help()
    else:
        if args.about or command == '--about':
            h_about()


# Создание основных директорий
def initDir(cur_dir):
    main_folder = cur_dir + '\\.cvs'

    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        ret = ctypes.windll.kernel32.SetFileAttributesW(main_folder, 0x02)
        os.makedirs(main_folder + '\\prjVer')
        os.makedirs(main_folder + '\\cvsData')
        print('.cvs успешно инициализирован в ' + cur_dir + '\\.cvs')
    else:
        print('.cvs уже инициализирован в ' + cur_dir + '\\.cvs')


# Функция ищет все файлы в dir, которых нет в .cvsignore.txt
def find_all_files(cur_dir):
    files = os.listdir(cur_dir)
    ignore_files = ['.cvs']
    return_files = []

    if os.path.exists(cur_dir + '\\.cvsignore.txt'):
        with open(cur_dir + '\\.cvsignore.txt', encoding='utf-8-sig') as ignore:
            ignore_files += ignore.read().splitlines()

    for file in files:
        if os.path.isfile(cur_dir + '\\' + file):
            if file not in ignore_files:
                return_files.append(file)
        elif file not in ignore_files:
            other_files = find_all_files(cur_dir + '\\' + file)
            for f in other_files:
                if f not in ignore_files:
                    return_files.append(file + '\\' + f)
    return return_files


# Возвращает отслеживаемые файлы
def return_track_files(cur_dir):
    if os.path.exists(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'):
        with open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'r', encoding='utf-8-sig') as f:
            track_files = f.read().splitlines()
            return track_files
    return []


# Удаляет "лишние" отслеживаемые файлы, возвращает True, если такие файлы имеются
def add_deleted_files(cur_dir):
    files = find_all_files(cur_dir)
    track_files = return_track_files(cur_dir)
    f = open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'w', encoding='utf-8-sig')
    count = 0

    for t_file in track_files:
        if t_file not in files:
            print('    - ' + t_file)
            count += 1
        else:
            f.write(t_file + '\n')
    f.close()

    if count < 1:
        return False
    return True


# Добавляет файл(ы) в отслеживаемые
def add_track_files(cur_dir, files, found_change_track_files):
    files_for_txt = []
    mode = 0
    track_files = return_track_files(cur_dir)
    way_to_trackFiles = cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'
    if isinstance(files, str):
        files = [files, '']
        del files[1]
        mode = 1

    if not os.path.exists(way_to_trackFiles):
        open(way_to_trackFiles, 'w+', encoding='utf-8-sig').close()

    if mode == 0:
        for file_s in files:
            files_for_txt.append(file_s)
            if file_s not in track_files:
                found_change_track_files = True
                print('    + ' + file_s)

        with open(way_to_trackFiles, 'w', encoding='utf-8-sig') as f:
            for file_str in files_for_txt:
                f.write(file_str + '\n')
    else:
        if files[0] not in track_files:
            with open(way_to_trackFiles, 'a', encoding='utf-8-sig') as f:
                f.write(files[0] + '\n')
                found_change_track_files = True
                print('    + ' + files[0])

    if not found_change_track_files:
        print("Файл(ы) уже отслеживаются")


# Работа с коммандой add
def command_add(value, args_info):
    found_change_track_files = add_deleted_files(cur_dir)
    if not value and not args_info:
        h_add()

    elif not value and args_info:
        print('Отслеживаемые файлы:')
        if os.path.exists(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'):
            with open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'r', encoding='utf-8-sig') as f:
                track_files = f.read().splitlines()
            for file in track_files:
                print('   ' + file)
        else:
            print('Нет отслеживаемых файлов\n')
            print('Введите CVS.py add для получения справки')

    elif value == '.' and not args_info:
        file_list = find_all_files(cur_dir)
        add_track_files(cur_dir, file_list, found_change_track_files)

    elif not args_info:
        file_list = find_all_files(cur_dir)

        if value in file_list:
            add_track_files(cur_dir, value, found_change_track_files)
        else:
            print("Не удалось найти файл " + value)


# Ищет номер последнего коммита
def find_last_ver(cur_dir):
    way_to_prjVer = cur_dir + '\\.cvs\\prjVer'
    folders = os.listdir(way_to_prjVer)
    last_ver = int(0)

    for folder in folders:
        if os.path.isdir(way_to_prjVer + '\\' + folder):
            try:
                if int(last_ver) < int(folder):
                    last_ver = folder
            except ValueError:
                pass
    return int(last_ver)


# Создаёт новую директорию для commit
def create_new_prjver_dir(cur_dir):
    way_to_prjVer = cur_dir + '\\.cvs\\prjVer'
    files = os.listdir(way_to_prjVer)
    folders = []
    for file in files:
        if os.path.isdir(way_to_prjVer + '\\' + file):
            folders.append(file)

    last_ver = find_last_ver(cur_dir) + 1
    os.makedirs(way_to_prjVer + '\\' + str(last_ver))


def build_file(cur_dir):
    last_ver = find_last_ver(cur_dir) + 1
    for i in range(last_ver):
        print(i)


# Построчное сравнение двух файлов, если изменения были, то выводит True
def make_diff(cur_dir, file_name):
    last_ver = find_last_ver(cur_dir)
    check_diff = False

    f1 = open(cur_dir + '\\' + file_name, 'r', encoding='utf-8-sig')
    # f2 = open(cur_dir + '\\.cvs\\prjVer\\' + str(last_ver - 1) + '\\' + file_name, 'r', encoding='utf-8-sig')
    file1_text, file2_text = f1.read().splitlines(), f2.read().splitlines()
    f1.close(), f2.close()

    d = difflib.Differ()
    diff = d.compare(file1_text, file2_text)
    count_str = 0
    finished_file = open(cur_dir + '\\.cvs\\prjVer\\' + str(last_ver) + '\\' + file_name, 'w', encoding='utf-8-sig')

    for diff_str in diff:
        count_str += 1
        if diff_str[0] == '+' or diff_str[0] == '-':
            check_diff = True

            finished_file.write(str(count_str) + diff_str + '\n')

    finished_file.close()
    if not check_diff:
        os.remove(cur_dir + '\\.cvs\\prjVer\\' + str(last_ver) + '\\' + file_name)
    return check_diff


if __name__ == "__main__":
    cur_dir = os.getcwd()
    build_file(cur_dir)
    add_deleted_files(cur_dir)

    args = checkArgs().parse_args()
    command, value = args.command, args.value

    printHelp(args)

    if command == 'init':
        initDir(cur_dir)

    elif command == 'add':
        command_add(value, args.info)

    elif command == 'commit':
        last_ver = find_last_ver(cur_dir)
        track_files = return_track_files(cur_dir)
        create_new_prjver_dir(cur_dir)

        if last_ver == 0:
            for t_file in track_files:
                open(cur_dir + '\\.cvs\\prjVer\\' + str(last_ver + 1) + '\\' + t_file, 'w').close()
                shutil.copy(cur_dir + '\\' + t_file, cur_dir + '\\.cvs\\prjVer\\' + str(last_ver + 1) + '\\' + t_file)
        else:
            for t_file in track_files:
                #make_diff(cur_dir, t_file)
                pass