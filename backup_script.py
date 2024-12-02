from filestation import FileStation
from config import Config

host = Config.get_hostname()
user = Config.get_user()
password = Config.get_pw()

backup_station = FileStation(host, user, password)

backup_folders = Config.get_local_path()

share_files = FileStation.list_share(backup_station)
items_in_backup_folder = FileStation.list(backup_station, Config.get_folder())

for item in items_in_backup_folder:
    if item.isfolder == 1:
        None




def loop_trough_folder(list, folder_name):
    local_file_list = []
    for item in list:
        if item.isfolder == 1:
            folder_name = "/" + item.filename
            items_in_folder = FileStation.list(backup_station, folder_name)
            loop_trough_folder(items_in_folder,folder_name)
        if item.isfolder == 0:
            None