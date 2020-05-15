import sys
import argparse
import os
import ctypes
import difflib
import shutil
import datetime

from help import *


# Объявление ожидаемых аргументов командной строки
def checkArgs():
    parse_Args = argparse.ArgumentParser(add_help=False, conflict_handler='resolve')
    parse_Args.add_argument('command', nargs='?', default='--about')
    parse_Args.add_argument('value', nargs='?')
    parse_Args.add_argument('value_plus', nargs='?')
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
    ignore_files = ['.cvs', '.cvsignore.txt']
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
def command_add(cur_dir, value, args_info):
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


# Собирает файл с учётом изменений всех версий
def build_file(cur_dir, file_name, ver=None):
    first_ver = True

    if not ver:
        last_ver = find_last_ver(cur_dir)
    else:
        last_ver = int(ver)
        last_ver = int(ver)

    builded_file = []

    for i in range(1, last_ver + 1):
        way_to_file = way_to(cur_dir + '\\.cvs\\prjVer\\' + str(i), file_name)
        if os.path.exists(way_to_file):
            if first_ver == True:
                with open(way_to_file, 'r', encoding='utf-8-sig') as f:
                    builded_file = f.read().splitlines()

                    first_ver = False
            else:
                if os.path.exists(way_to_file):
                    with open(way_to_file, 'r', encoding='utf-8-sig') as f:
                        changes_str = f.read().splitlines()
                        check_minus = 0

                        for change_str in changes_str:
                            change_str = change_str.split(' ', 1)
                            if change_str[0][-1] == '+':
                                builded_file.insert(int(change_str[0][0:-1]) - 1, change_str[1])
                            else:
                                builded_file.pop(int(change_str[0][0:-1]) - 1 - check_minus)
                                check_minus += 1
    return builded_file


# Заменяет файлы в основной директории
def make_file(cur_dir, file_name, ver=None):
    files = file_name
    way_to_file = way_to(cur_dir, file_name)

    if not ver:
        builded_file = build_file(cur_dir, files)
    else:
        builded_file = build_file(cur_dir, files, ver)

    with open(way_to_file, 'w', encoding='utf-8-sig') as f:
        for file_str in builded_file:
            f.write(file_str + '\n')

# Построчное сравнение двух файлов, если изменения были, то выводит True
def make_diff(cur_dir, file_name):
    last_ver = find_last_ver(cur_dir)
    check_diff = False
    way_to_f1 = way_to(cur_dir, file_name)

    f1 = open(way_to_f1, 'r', encoding='utf-8-sig')
    file1_text = f1.read().splitlines()
    file2_text = build_file(cur_dir, file_name)
    f1.close()

    d = difflib.Differ()
    diff = d.compare(file2_text, file1_text)
    count_str = 0
    way_to_finished_file = way_to(cur_dir + '\\.cvs\\prjVer\\' + str(last_ver), file_name)
    finished_file = open(way_to_finished_file, 'w', encoding='utf-8-sig')

    for diff_str in diff:
        count_str += 1
        if diff_str[0] == '+' or diff_str[0] == '-':
            check_diff = True

            finished_file.write(str(count_str) + diff_str + '\n')

    finished_file.close()
    if not check_diff:
        way_to_remove_file = way_to(cur_dir + '\\.cvs\\prjVer\\' + str(last_ver), file_name)
        os.remove(way_to_remove_file)
    return check_diff


# Проверяет есть ли файлы для отслеживания
def track_files_is_empty(cur_dir):
    track_files = return_track_files(cur_dir)
    if len(track_files) == 0:
        print('Добавьте файлы для отслеживания')
        raise SystemExit()


# Проверка версии проекта на существование
def incorrect_prjver(cur_dir, ver):
    last_ver = find_last_ver(cur_dir)
    try:
        ver = int(ver)
    except ValueError:
        print('Неккоректная версия проекта')
        raise SystemExit

    if ver < 1 or last_ver < ver:
        print(str(ver) + ' версии проекта не существует')
        raise SystemExit


# Проверяет инициализирован ли .cvs
def check_initialized(cur_dir):
    if not os.path.exists(cur_dir + '\\.cvs'):
        print('Неинициализирован .cvs')
        raise SystemExit
    if not os.path.exists(cur_dir + '\\.cvs\\cvsData'):
        print('Не удалось найти .cvs\\cvsData\n')
        print('Переинициализируйте .cvs')
        raise SystemExit
    if not os.path.exists(cur_dir + '\\.cvs\\prjVer'):
        print('Не удалось найти .cvs\\prjVer\n')
        print('Переинициализируйте .cvs')
        raise SystemExit


# Функционал для команды commit
def command_commit(cur_dir, value):
    last_ver = find_last_ver(cur_dir)
    track_files = return_track_files(cur_dir)
    create_new_prjver_dir(cur_dir)
    way_to_new_prjver = cur_dir + '\\.cvs\\prjVer\\' + str(last_ver + 1)

    if not os.path.exists(cur_dir + '\\.cvs\\prjVer\\.addedFiles'):
        open(cur_dir + '\\.cvs\\prjVer\\.addedFiles', 'w', encoding='utf-8-sig').close()

    with open(cur_dir + '\\.cvs\\prjVer\\.addedFiles', 'r', encoding='utf-8-sig') as a_files:
        added_files = a_files.read().splitlines()

    for t_file in track_files:
        if t_file not in added_files:
            way_to_t_file = way_to(way_to_new_prjver, t_file)
            open(way_to_t_file, 'w').close()
            way_to_first_file = way_to(cur_dir, t_file)
            shutil.copy(way_to_first_file, way_to_t_file)
            with open(cur_dir + '\\.cvs\\prjVer\\.addedFiles', 'a', encoding='utf-8-sig') as a_files:
                a_files.write(t_file + '\n')
        else:
            make_diff(cur_dir, t_file)

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
def command_reset(cur_dir, value, value_plus):
    if not value:
        print('Введите версию проекта')
        raise SystemExit

    if not args.value_plus:
        incorrect_prjver(cur_dir, value)
        track_files = return_track_files(cur_dir)

        for t_file in track_files:
            make_file(cur_dir, t_file, value)
        print("Откат на версию " + value + " произошёл успешно")
    else:
        value, args.value_plus = value_plus, value
        incorrect_prjver(cur_dir, value)
        t_file = value_plus
        make_file(cur_dir, t_file, value)
        print("Откат файла " + t_file + " на версию " + value + " произошёл успешно")


# Функционал для командыв delete
def command_delete(cur_dir, value):
    if value:
        track_files = return_track_files(cur_dir)
        if value in track_files:
            track_files.remove(value)
            with open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'w', encoding='utf-8-sig') as f:
                for t_file in track_files:
                    f.write(t_file + '\n')
            print('Файл ' + value + ' больше не отслеживается')
        else:
            print('Файл ' + value + ' ещё не отслеживается')
    else:
        print('Вы не ввели название файла')


# Возвращает информацию о всех сохранениях проекта
def command_log(cur_dir):
    return_log = 'Версии проекта:\n'
    way_to_prjVer = cur_dir + '\\.cvs\\prjVer'
    folders = os.listdir(way_to_prjVer)
    if not len(folders) == 0:
        for folder in folders:
            if os.path.isdir(way_to_prjVer + '\\' + folder):
                with open(way_to_prjVer + '\\' + folder + '\\.date', encoding='utf-8-sig') as f_date:
                    return_log += '   ' + folder + ' версия от ' + f_date.read() + '\n'
                if os.path.exists(way_to_prjVer + '\\' + folder + '\\.comment'):
                    with open(way_to_prjVer + '\\' + folder + '\\.comment', encoding='utf-8-sig') as f_comment:
                        return_log += '   Комментарий: ' + f_comment.read() + '\n'
                return_log += '\n'
    else:
        print('Отсутствуют сохранённые версии проекта')
        raise SystemExit
    print(return_log)


if __name__ == "__main__":
    cur_dir = os.getcwd()
    if os.path.exists(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'):
        add_deleted_files(cur_dir)

    args = checkArgs().parse_args()
    command, value, value_plus = args.command, args.value, args.value_plus
    command, value, value_plus = args.command, args.value, args.value_plus

    if args.help or args.about or command == '--about':
        printHelp(args)
        raise SystemExit

    if command == 'init':
        initDir(cur_dir)

    elif command == 'add':
        check_initialized(cur_dir)
        command_add(cur_dir, value, args.info)

    elif command == 'commit':
        check_initialized(cur_dir)
        track_files_is_empty(cur_dir)
        command_commit(cur_dir, value)

    elif command == 'reset':
        check_initialized(cur_dir)
        command_reset(cur_dir, value, args.value_plus)

    elif command == 'delete':
        check_initialized(cur_dir)
        track_files_is_empty(cur_dir)
        command_delete(cur_dir, value)

    elif command == 'log':
        check_initialized(cur_dir)
        command_log(cur_dir)
    else:
        print('Неизвестное значение \'' + command + '\'\n\nДля вывозва справки используйте CVS.py -h')
