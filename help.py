def h_help():
    print('Локальный контроль версий v1.0\n')
    print('...')


def h_about():
    print('Локальный контроль версий v1.0\n')
    print('Для вызова справки введите команду:\n   CVS.py --help \n   или \n   CVS.py -h')


def h_add():
    print('Вы ввели CVS.py add без значения!\n')
    print('Справка:')
    print('Для отслеживания всех файлов вы можете использовать CVS.py add .')
    print('Для отслеживания отдельных файлов используйте CVS.py add имя_файла')
    print('*Если файл находится в папке используйте CVS.py add путь\\имя_файла')
    print('**Путь считается от того каталога, где был инифиализирован .cvs')