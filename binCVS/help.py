﻿def h_help():
    print('Локальный контроль версий v1.0\n')
    print('Комманды:\n'
          ' CVS.py init\n'
          '   Инициализация всех необходимых для работы директорий\n\n'
          ' CVS.py add название_файла"\n'
          '   Добавляет файлы в отслеживаемые.\n'
          '   Вы можете ввести название_файла в качестве\n'
          '   передаваемого аргумента или, если файл находится\n'
          '   в поддиректории, то путь\название_файла\n'
          '   Если Вы хотите добавить сразу все файлы используйте\n'
          '   CVS.py add .\n'
          '   Учтите, добавятся все файлы, кроме тех,\n'
          '   которые Вы указали в .cvsignore.txt\n'
          '   *Если вы хотите, чтобы файлы не отслеживались,\n'
          '    cоздайте в основной директории файл .cvsignore.txt\n'
          '    и внесите название файлов через enter\n'
          '   **Учтите, что путь считается от папки, где проинициализирован .cvs\n\n'
          ' CVS.py delete "название_файла"\n'   
          '   Позволяет удалить файл из отслеживаемых.\n'
          '   В качестве аргумента передаётся название файла.\n\n'
          ' CVS.py commit \"текст_комментария\"\n'
          '   Сохраняет версию текущего проекта.\n'
          '   Вы можете оставить комментарий, передав аргумент\n'
          '   в \"кавычках\" \n\n'
          ' CVS.py reset номер_версии позволяет изменить версию проекта\n'
          '   в качестве аргумента передаётся номер версии проекта\n'
          '   Также вы можете вернуть только один файл к другой версии\n'
          '   CVS.py reset имя_файла номер_версии')
    print(' Инстуркция:\n'
          '    Первым делом Вам необходимо инициализировать .cvs в той\n'
          '   директории, где находится Ваш проект. Сделать это можно\n'
          '   командой CVS.py init\n\n'
          '    Далее Вам надо выбрать те файлы, которые вы хотите \"отслеживать\",\n'
          '   то есть те, которые программа будет вносить в контроль версий проекта.\n'
          '   Сделать это можно CVS.py add название_файла,\n'
          '   либо же внести все файлы командой CVS.py add .\n'
          '    Коммандой CVS.py add -i Вы можете просмотреть отслеживаемые файлы\n'
          '   Удалить файл из отслеживаемых вам поможет команда CVS.py delete имя_файла\n\n'
          '    Чтобы случайно не внести \"нежелательные\" файлы используйте .cvsignore.txt\n'
          '   Для этого создайте файл \'.cvsignore.txt\' в своей основной директории.\n'
          '   и через enter укажите названия файлов, если файл находится в поддиректории\n'
          '   укажите путь от начальной директории до файла, т.е. путь\\имя_файла\n'
          '   *Учтите, путь начинается от той директории, где был инифиализирован .cvs\n\n'
          '    Подготовка окончена!\n'
          '   Теперь вы можете \'сохранить\' проект командой CVS.py commit \"ваш_комментарий\"\n'
          '   *Можно обойтись без комментария\n'
          '   Просмотреть текущие версии проекта Вам поможет CVS.py log\n'
          '   команда выведет номер версии и дату, в случае наличия - комментарий\n\n'
          '   Сменить версию проекта Вы можете при помощи CVS.py reset версия_проекта')



def h_about():
    print('Локальный контроль версий v1.0\n')
    print('Для вызова справки введите команду:\n CVS.py --help \nили \n CVS.py -h\n')
    print(' Данная программа позволяет делать сохранения вашего проекта.\n'
          ' После добавления новой версии проекта'
          ' командой commit,\n вы в любой момент сможете вернутся к ней.\n'
          ' Не забудьте перед этим сохранить текущую версию!')


def h_add():
    print('Вы ввели CVS.py add без значения!\n')
    print('Справка:')
    print('Для отслеживания всех файлов вы можете использовать CVS.py add .')
    print('Для отслеживания отдельных файлов используйте CVS.py add имя_файла')
    print('*Если файл находится в папке используйте CVS.py add путь\\имя_файла')
    print('**Путь считается от того каталога, где был инифиализирован .cvs')