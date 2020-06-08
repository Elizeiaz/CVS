import os
from binCVS.work_with_files import find_last_ver
from binCVS.base_work_with_files import read_file
from binCVS.work_with_files import add_deleted_files


# Класс наполняющий path для CVS_prog.py
class WorkingRep:
    def __init__(self, cur_dir, last_project_version):
        self.__cur_dir = cur_dir
        self.__last_project_version = last_project_version

    @property
    def last_project_version(self):
        return self.__last_project_version

    @property
    def cur_dir(self):
        return self.__cur_dir

    @property
    def way_to_cvs(self):
        return os.path.join(self.cur_dir, '.cvs')

    @property
    def way_to_prj_ver(self):
        return os.path.join(self.way_to_cvs, 'prjVer')

    @property
    def way_to_added_file(self):
        return os.path.join(self.way_to_prj_ver, '.addedFiles')

    @property
    def way_to_last_prj_ver(self):
        return os.path.join(self.way_to_prj_ver, str(self.last_project_version))

    @property
    def way_to_cvs_data(self):
        return os.path.join(self.way_to_cvs, 'cvsData')

    @property
    def way_to_track_file(self):
        return os.path.join(self.way_to_cvs_data, 'trackFiles.txt')

    @property
    def way_to_cvs_ignore(self):
        return os.path.join(self.cur_dir, '.cvsignore.txt')


class CVS:
    cur_dir = os.getcwd()
    last_project_version = find_last_ver(cur_dir)
    path = WorkingRep(cur_dir, last_project_version)
    track_files = read_file(path.way_to_track_file)
    added_files = read_file(path.way_to_added_file)


@add_deleted_files
def make_class_cvs():
    pass


my_cvs = CVS
