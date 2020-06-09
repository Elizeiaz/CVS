import os

from bin_cvs.command_wrapper import command_init_wrapper, command_add_wrapper, command_commit_wrapper, \
    command_reset_wrapper, command_log_wrapped, command_track_wrapper, command_delete_wrapper, zero_args_wrapper
from bin_cvs.classes import my_cvs
from bin_cvs.errors import IncorrectCVSVersionError, CVSNotInitializedError, TrackFilesIsEmptyError


class CommandHandler:
    def __init__(self, command, **args):
        self.__command = command
        self.__args = args

    @property
    def command_dict(self):
        command_handler = {'init': self.com_init,
                           'add': self.com_add,
                           'commit': self.com_commit,
                           'reset': self.com_reset,
                           'log': self.com_log,
                           'track': self.com_track,
                           'delete': self.com_delete,
                           'zero_args': self.com_zero_args}
        return command_handler

    def handler(self):
        self.command_dict[self.__command](**self.__args)

    def com_init(self):
        command_init_wrapper()

    def com_add(self, file_name):
        try:
            if not os.path.exists(my_cvs.path.way_to_cvs):
                raise CVSNotInitializedError('Initialize .cvs')

            command_add_wrapper(file_name)

        except CVSNotInitializedError as e:
            print(e)
            exit(1)

    def com_commit(self, comment):
        try:
            if not os.path.exists(my_cvs.path.way_to_cvs):
                raise CVSNotInitializedError('Initialize .cvs')
            if not my_cvs.track_files:
                raise TrackFilesIsEmptyError('Track files is empty')

            command_commit_wrapper(comment)

        except CVSNotInitializedError as e:
            print(e)
            exit(1)
        except TrackFilesIsEmptyError as e:
            print(e)
            exit(1)

    def com_reset(self, value):
        try:
            if value[0] and len(value) == 1:
                version = value[0]
                file_name = None
            else:
                version = value[1]
                file_name = value[0]
        except IndexError:
            print('Введите аргументы')
            exit(1)

        try:
            if not os.path.exists(os.path.join(my_cvs.path.way_to_prj_ver, version)):
                raise IncorrectCVSVersionError('Incorrect project version')
            if not os.path.exists(my_cvs.path.way_to_cvs):
                raise CVSNotInitializedError('Initialize .cvs')

            command_reset_wrapper(version, file_name)

        except CVSNotInitializedError as e:
            print(e)
            exit(1)
        except IncorrectCVSVersionError as e:
            print(e)
            exit(1)

    def com_track(self):
        try:
            if not os.path.exists(my_cvs.path.way_to_cvs):
                raise CVSNotInitializedError('Initialize .cvs')
            if not my_cvs.track_files:
                raise TrackFilesIsEmptyError('Track files is empty')

            command_track_wrapper()

        except CVSNotInitializedError as e:
            print(e)
            exit(1)
        except TrackFilesIsEmptyError as e:
            print(e)
            exit(1)

    def com_log(self):
        try:
            if not os.path.exists(my_cvs.path.way_to_cvs):
                raise CVSNotInitializedError('Initialize .cvs')
            command_log_wrapped()
        except CVSNotInitializedError as e:
            print(e)
            exit(1)

    def com_delete(self, file_name):
        try:
            if not os.path.exists(my_cvs.path.way_to_cvs):
                raise CVSNotInitializedError('Initialize .cvs')
            if not my_cvs.track_files:
                raise TrackFilesIsEmptyError('Track files is empty')

            command_delete_wrapper(file_name)

        except CVSNotInitializedError as e:
            print(e)
            exit(1)
        except TrackFilesIsEmptyError as e:
            print(e)
            exit(1)

    def com_zero_args(self):
        zero_args_wrapper()
