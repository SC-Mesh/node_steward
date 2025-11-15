import getpass
import os
import subprocess
import syslog

from datetime import datetime

def backup_directory_path():
    return f"/home/{os.getlogin() or 'meshadmin'}/config_backups"

def find_or_create_backup_directory():
    os.makedirs(backup_directory_path(), exist_ok=True)
    return

def config_file_path():
    current_datetime = datetime.now()

    return f"{backup_directory_path()}/backup_{current_datetime.strftime('%Y_%m_%d')}.yml"


if __name__ == "__main__":
    try:
        find_or_create_backup_directory()


        with open(config_file_path(), "w") as backup_file:
            result = subprocess.run(
                ['meshtastic', '--export-config'],
                stdout=backup_file,
                check=True
            )

        syslog.syslog(syslog.LOG_INFO, "Node config was successfully backed up.")
    except subprocess.CalledProcessError as e:
        syslog.syslog(
                syslog.LOG_ERR,
                f"Node config backup failed with exit code {e.returncode}"
        )
        syslog.syslog(
                syslog.LOG_ERR,
                f"Config backup error:: {e.stderr}"
        )

