import os
import shutil
import json

class BackupManager:
    def __init__(self, json_path="backup_list.json"):
        self.json_path = json_path
        self.paths_to_backup = self.load_backup_list()

    def load_backup_list(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_backup_list(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.paths_to_backup, f, indent=2)

    def add_path(self, path):
        if path not in self.paths_to_backup:
            self.paths_to_backup.append(path)
            self.save_backup_list()

    def remove_path(self, index):
        if 0 <= index < len(self.paths_to_backup):
            del self.paths_to_backup[index]
            self.save_backup_list()

    def perform_backup(self, dest_folder, backup_name):
        backup_path = os.path.join(dest_folder, backup_name)
        os.makedirs(backup_path, exist_ok=True)

        for path in self.paths_to_backup:
            if os.path.exists(path):
                try:
                    if os.path.isdir(path):
                        shutil.copytree(path, os.path.join(backup_path, os.path.basename(path)))
                    elif os.path.isfile(path):
                        shutil.copy2(path, backup_path)
                except Exception as e:
                    raise RuntimeError(f"Error al copiar {path}: {e}")
            else:
                raise FileNotFoundError(f"Ruta no válida: {path}")

        return backup_path
