import sys
import argparse
import os
import ctypes

from help import *


def checkArgs():
    parse_Args = argparse.ArgumentParser(add_help=False, conflict_handler='resolve')
    parse_Args.add_argument('command', nargs='?', default='--about')
    parse_Args.add_argument('value', nargs='?')
    parse_Args.add_argument('-h', '--help', action="store_true")
    parse_Args.add_argument('-a', '--about', action="store_true")

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


def find_all_files(dir):
    files = os.listdir(dir)

    for file in files:
        if os.path.isfile(dir + '\\' + file):
            yield file
        else:
            other_files = find_all_files(dir + '\\' + file)
            for f in other_files:
                yield f


if __name__ == "__main__":
    cur_dir = os.getcwd()
    cur_files = os.listdir()
    track_files = []

    args = checkArgs().parse_args()
    command = args.command

    printHelp(args)

    if command == 'init':
        initDir(cur_dir)

    elif command == 'add':
        test = find_all_files(cur_dir)
        for i in test:
            print(i)
    