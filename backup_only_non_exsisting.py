import os
from filestation import FileStation
from config import Config

def sync_to_remote(filestation, local_path, remote_path):
    """
    Synchronize files and directories from local_path to remote_path on QNAP.

    :param filestation: FileStation object (connected to QNAP).
    :param local_path: Path to the local directory to sync.
    :param remote_path: Path to the remote directory on QNAP.
    """
    for root, dirs, files in os.walk(local_path):
        relative_path = os.path.relpath(root, local_path)
        remote_dir = os.path.join(remote_path, relative_path).replace("\\", "/")

        # Ensure the remote directory exists
        if not remote_path_exists(filestation, remote_dir):
            print(f"Creating remote directory: {remote_dir}")
            filestation.create_directory(remote_dir)

        # Process files
        for file in files:
            local_file_path = os.path.join(root, file)
            remote_file_path = os.path.join(remote_dir, file).replace("\\", "/")

            if should_upload(filestation, local_file_path, remote_file_path):
                print(f"Uploading file: {local_file_path} -> {remote_file_path}")
                with open(local_file_path, "rb") as data:
                    filestation.upload(remote_file_path, data)
            else:
                print(f"File is up-to-date, skipping: {remote_file_path}")

def remote_path_exists(filestation, remote_path):
    """
    Check if a remote path exists on QNAP.

    :param filestation: FileStation object.
    :param remote_path: Path to the remote directory.
    :return: True if the remote path exists, False otherwise.
    """
    try:
        filestation.list(remote_path)
        return True
    except Exception:
        return False

def should_upload(filestation, local_file_path, remote_file_path):
    """
    Determine if a file should be uploaded based on timestamps.

    :param filestation: FileStation object.
    :param local_file_path: Path to the local file.
    :param remote_file_path: Path to the remote file.
    :return: True if the file should be uploaded, False otherwise.
    """
    try:
        # Get remote file info
        remote_info = filestation.get_file_info(remote_file_path)

        # Extract remote modification time
        remote_mtime = remote_info.get("modification", None)
        if remote_mtime is None:
            return True  # If no timestamp is available, upload the file

        # Convert to timestamp (if not already in UNIX format)
        remote_mtime = int(remote_mtime)

        # Compare with local file's modification time
        local_mtime = int(os.path.getmtime(local_file_path))
        return local_mtime > remote_mtime  # Upload if local is newer

    except Exception:
        return True  # Upload if the file does not exist on remote

if __name__ == "__main__":
    # QNAP connection details
    qnap_host = Config.get_hostname()
    qnap_user = Config.get_user()
    qnap_password = Config.get_pw()
    qnap_port = "8080"

    # Local and remote paths
    local_path =  Config.get_local_path()
    remote_path = Config.get_remote_path()

    # Connect to QNAP FileStation
    filestation = FileStation(qnap_host, qnap_user, qnap_password, port=qnap_port)

    # Synchronize local files to remote
    for i in range(len(local_path)):   
        sync_to_remote(filestation, local_path[i], remote_path[i])
