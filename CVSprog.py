import os

from binCVS.check_args import parse_args
from binCVS.command_wrapper import command_init_wrapper, command_add_wrapper, command_commit_wrapper, \
    command_reset_wrapper, command_log_wrapped, command_track_wrapper, command_delete_wrapper
from binCVS.exeptions_wrapper import check_initialized_wrapper, track_files_is_empty_wrapper, incorrect_prj_ver_wrapper

if __name__ == "__main__":
    args = parse_args()
    command = args.command

    if command == 'init':
        command_init_wrapper()

    elif command == 'add':
        check_initialized_wrapper()
        command_add_wrapper(args.file_name)

    elif command == 'commit':
        check_initialized_wrapper()
        track_files_is_empty_wrapper()
        command_commit_wrapper(args.comment)

    elif command == 'reset':
        check_initialized_wrapper()

        if len(args.value) == 1:
            file_name = None
            version = args.value[0]
        else:
            file_name = args.value[0]
            version = args.value[1]

        incorrect_prj_ver_wrapper(version)
        command_reset_wrapper(version, file_name)

    elif command == 'delete':
        check_initialized_wrapper()
        track_files_is_empty_wrapper()
        command_delete_wrapper(args.file_name)

    elif command == 'track':
        track_files_is_empty_wrapper()
        command_track_wrapper()

    elif command == 'log':
        check_initialized_wrapper()
        command_log_wrapped()

    elif command == 'zero_args':
        print('Воспользуйтесь справкой CVSprog.py -h')
