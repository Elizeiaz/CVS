import argparse
import os

from functional import *
from help import *

if __name__ == "__main__":
    cur_dir = os.getcwd()
    if os.path.exists(cur_dir + '\\.cvs\\cvsData\\trackFiles.txt'):
        add_deleted_files(cur_dir)

    args = checkArgs().parse_args()
    command, value, value_plus = args.command, args.value, args.value_plus

    if args.help or args.about or command == '--about':
        printHelp(args, command)
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
