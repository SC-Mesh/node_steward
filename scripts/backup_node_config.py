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

def prune_config_backups(keep_last_n=7):
    backup_dir = backup_directory_path()
    backups = sorted(
        [
            f for f in os.listdir(backup_dir)
            if os.path.isfile(os.path.join(backup_dir, f))
        ],
        key=lambda x: os.path.getmtime(os.path.join(backup_dir, x))
    )

    for backup in backups[:-keep_last_n]:
        os.remove(os.path.join(backup_dir, backup))


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

        prune_config_backups(keep_last_n=7)
    except subprocess.CalledProcessError as e:
        syslog.syslog(
                syslog.LOG_ERR,
                f"Node config backup failed with exit code {e.returncode}"
        )
        syslog.syslog(
                syslog.LOG_ERR,
                f"Config backup error:: {e.stderr}"
        )
