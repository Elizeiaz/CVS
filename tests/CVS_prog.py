import argparse

from bin_cvs.command_wrapper import command_init_wrapper, command_add_wrapper, command_commit_wrapper, \
    command_reset_wrapper, command_log_wrapped, command_track_wrapper, command_delete_wrapper, zero_args_wrapper
from bin_cvs.command_handler import CommandHandler


def parse_args():
    parser = argparse.ArgumentParser(description='Локальный контроль версий', usage='CVS_prog.py')
    parser.set_defaults(command='zero_args')

    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init', help='Инициализация CVS_prog.py')
    parser_init.set_defaults(command='init')

    parser_add = subparsers.add_parser('add', help='Добавление файлов для отслеживания')
    parser_add.add_argument('file_name', help='Инфонрамация для add', type=str, default=None)
    parser_add.set_defaults(command='add')

    parser_delete = subparsers.add_parser('delete', help='Удаление файла из отслеживаемых')
    parser_delete.add_argument('file_name', help='Информация для delete', type=str)
    parser_delete.set_defaults(command='delete')

    parser_track = subparsers.add_parser('track', help='Вывод отслеживаемых файлов')
    parser_track.set_defaults(command='track')

    parser_commit = subparsers.add_parser('commit', help='Сохранение проекта')
    parser_commit.add_argument('comment', help='Комментарий к сохранению', type=str)
    parser_commit.set_defaults(command='commit')

    parser_log = subparsers.add_parser('log', help='Вывод информации о версиях проекта')
    parser_log.set_defaults(command='log')

    parser_reset = subparsers.add_parser('reset', help='Смена версии проекта')
    parser_reset.add_argument('value', help='Версия', type=str, nargs='*')
    parser_reset.set_defaults(command='reset')

    return parser.parse_args()


if __name__ == "__main__":
    command_handler = {'init': command_init_wrapper,
                       'add': command_add_wrapper,
                       'commit': command_commit_wrapper,
                       'reset': command_reset_wrapper,
                       'log': command_log_wrapped,
                       'track': command_track_wrapper,
                       'delete': command_delete_wrapper,
                       'zero_args': zero_args_wrapper}

    args = parse_args()
    cli_args = dict(args.__dict__)
    command = cli_args.pop('command')

    mini_handler = CommandHandler(command, **cli_args)
    mini_handler.handler()
    # command_handler[command](**cli_args)
