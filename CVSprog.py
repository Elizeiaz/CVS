import os

from binCVS.functional import command_init, command_add, command_commit, command_reset, \
    command_delete, command_log
from binCVS.exeptions import track_files_is_empty, check_initialized
from binCVS.check_args import parse_args

if __name__ == "__main__":

    args = parse_args()
    command = args.command

    if command == 'init':
        command_init()

    elif command == 'add':
        check_initialized()
        command_add(args.file_name)

    elif command == 'commit':
        check_initialized()
        track_files_is_empty()
        command_commit(value)

    elif command == 'reset':
        check_initialized()
        command_reset(args, value, args.value_plus)

    elif command == 'delete':
        check_initialized()
        track_files_is_empty()
        command_delete(value)

    elif command == 'log':
        check_initialized()
        command_log()
    else:
        print('Неизвестное значение \'' + command + '\'\n\nДля вывозва справки используйте CVS.py -h')
