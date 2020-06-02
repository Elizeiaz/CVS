import argparse
import os

from binCVS.base_work_with_files import read_file



def parse_args():
    parser = argparse.ArgumentParser(description='Локальный контроль версий', usage='CVSprog.py')
    parser.set_defaults(command='zero_args')

    subparsers = parser.add_subparsers()

    parser_init = subparsers.add_parser('init', help='Инициализация CVSprog.py')
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
