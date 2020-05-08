import sys
import argparse

from help import *


def checkArgs():
    parseArgs = argparse.ArgumentParser(add_help=False, conflict_handler='resolve')
    parseArgs.add_argument('command', nargs='?', default='about')
    parseArgs.add_argument('value', nargs='?')

    return parseArgs


if __name__ == "__main__":
    args = checkArgs().parse_args()
    command = args.command
    print(args)

    if command == 'about' or command == 'a':
        print('Локальный контроль версий v1.0\n')
        print('Для вызова справки введите команду:\n   CVS.py help \n   или \n   CVS.py h')
    elif command == 'help' or command == 'h':
        h_help()
