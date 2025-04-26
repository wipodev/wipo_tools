import json
import shutil
import os

class SettingsManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        # Estructura de datos en memoria
        self.data = {
            "backup_name": "Backup",
            "paths": []
        }
        self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                # Si falla al leer, regenerar archivo
                self._save_config()
        else:
            # Si no existe, crear con valores por defecto
            self._save_config()

    def _save_config(self):
        os.makedirs(os.path.dirname(self.config_path) or '.', exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # --- Propiedades para backup_name ---
    @property
    def backup_name(self) -> str:
        return self.data.get("backup_name", "")

    @backup_name.setter
    def backup_name(self, value: str):
        self.data["backup_name"] = value
        self._save_config()

    # --- Métodos para paths ---
    def get_paths(self) -> list[str]:
        return list(self.data.get("paths", []))

    def add_path(self, path: str):
        if path not in self.data["paths"]:
            self.data["paths"].append(path)
            self._save_config()

    def remove_path(self, path: str):
        if path in self.data["paths"]:
            self.data["paths"].remove(path)
            self._save_config()

    def clear_paths(self):
        self.data["paths"] = []
        self._save_config()

    # --- Importar / Exportar configuración ---
    def import_config(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        # Validar estructura mínima
        if not isinstance(loaded, dict) or "paths" not in loaded or "backup_name" not in loaded:
            raise ValueError("Archivo de configuración inválido")
        self.data = loaded
        self._save_config()

    def export_config(self, filepath: str):
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    # --- Lógica de backup ---
    def perform_backup(self, dest_folder: str = None, backup_name: str = None) -> str:
        # Determinar carpeta de destino y nombre de backup
        dest = dest_folder or os.getcwd()
        name = backup_name or self.backup_name or "backup"

        backup_path = os.path.join(dest, name)
        os.makedirs(backup_path, exist_ok=True)

        for path in self.data.get("paths", []):
            if not os.path.exists(path):
                raise FileNotFoundError(f"Ruta no válida: {path}")
            try:
                if os.path.isdir(path):
                    shutil.copytree(path, os.path.join(backup_path, os.path.basename(path)))
                else:
                    shutil.copy2(path, backup_path)
            except Exception as e:
                raise RuntimeError(f"Error al copiar {path}: {e}")

        return backup_path
