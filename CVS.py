import sys
import argparse
import os
import ctypes

from help import *


#
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
def initDir(dir):
    main_folder = dir + '\\.cvs'

    if not os.path.exists(main_folder):
        os.makedirs(main_folder)
        ret = ctypes.windll.kernel32.SetFileAttributesW(main_folder, 0x02)
        os.makedirs(main_folder + '\\prjVer')
        os.makedirs(main_folder + '\\cvsData')
        print('.cvs успешно инициализирован в ' + cur_dir + '\\.cvs')
    else:
        print('.cvs уже инициализирован в ' + cur_dir + '\\.cvs')


# Функция ищет все файлы в dir, которых нет в .cvsignore.txt
def find_all_files(dir):
    files = os.listdir(dir)
    ignore_files = ['.cvs']

    if os.path.exists(dir + '\\.cvsignore.txt'):
        with open(dir + '\\.cvsignore.txt', encoding='utf-8-sig') as ignore:
            ignore_files += ignore.read().splitlines()

    for file in files:
        if os.path.isfile(dir + '\\' + file):
            if file not in ignore_files:
                yield file
        elif file not in ignore_files:
            other_files = find_all_files(dir + '\\' + file)
            for f in other_files:
                if f not in ignore_files:
                    yield file + '\\' + f


def add_track_files(cur_dir, files):
    count = 0
    if isinstance(files, str):
        files = [files, '']
        del files[1]

    if not os.path.exists(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'):
        open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'w+').close()

    with open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'r') as f:
        track_files = f.read().splitlines()

    with open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'a+') as f:
        for file in files:
            if file not in track_files:
                count += 1
                print('    +' + file)
                f.write(file + '\n')

    if count == 0:
        print("Файл(ы) уже отслеживаются")


if __name__ == "__main__":
    cur_dir = os.getcwd()

    args = checkArgs().parse_args()
    command, value = args.command, args.value

    printHelp(args)

    if command == 'init':
        initDir(cur_dir)

    elif command == 'add':
        if not value and not args.info:
            h_add()

        elif not value and args.info:
            print('Отслеживаемые файлы:')
            with open(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt', 'r') as f:
                track_files = f.read().splitlines()
                for file in track_files:
                    print('   ' + file)

        elif value == '.' and not args.info:
            file_list = find_all_files(cur_dir)
            add_track_files(cur_dir, file_list)

        elif not args.info:
            file_list = find_all_files(cur_dir)

            if value in file_list:
                add_track_files(cur_dir, value)
            else:
                print("Не удалось найти файл " + value)
