import os
from binCVS.work_with_files import find_last_ver, return_track_files, add_deleted_files

if os.path.exists(os.path.join(os.getcwd(), '.cvs', 'cvsData', 'trackFiles.txt')):
    add_deleted_files(os.getcwd())


class CVS:
    cur_dir = os.getcwd()
    last_project_version = find_last_ver(cur_dir)
    track_files = return_track_files(cur_dir)
    way_to_cvs = os.path.join(cur_dir, '.cvs')
    way_to_prj_ver = os.path.join(cur_dir, '.cvs', 'prjVer')
    way_to_cvs_data = os.path.join(cur_dir, '.cvs', 'cvsData')
    way_to_track_file = os.path.join(cur_dir, '.cvs', 'cvsData', 'trackFiles.txt')
    way_to_added_file = os.path.join(cur_dir, '.cvs', 'prjVer', '.addedFiles')
    way_to_last_prj_ver = os.path.join(cur_dir, '.cvs', 'prjVer', str(last_project_version))
    way_to_cvs_ignore = os.path.join(cur_dir, '.cvsignore.txt')


my_cvs = CVS