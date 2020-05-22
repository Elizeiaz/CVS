import os
from work_with_files import find_last_ver, return_track_files


class CVS:
    cur_dir = os.getcwd()
    last_project_version = find_last_ver()
    track_files = return_track_files(cur_dir)


my_cvs = CVS
