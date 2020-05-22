import os

from functional import check_args, print_help, command_init, command_add, command_commit, command_reset, \
    command_delete, command_log

from exeptions import track_files_is_empty, check_initialized
from work_with_files import add_deleted_files

if __name__ == "__main__":

    if os.path.exists(os.getcwd() + '\\.cvs\\cvsData\\trackFiles.txt'):
        add_deleted_files(os.getcwd())

    args = check_args().parse_args()
    command, value, value_plus = args.command, args.value, args.value_plus

    if args.help or args.about or command == '--about':
        print_help(args, command)
        raise SystemExit

    if command == 'init':
        command_init()

    elif command == 'add':
        check_initialized()
        command_add(value, args.info)

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
