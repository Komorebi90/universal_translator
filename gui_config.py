# FILENAME: gui_config.py
#!/usr/bin/env python3
"""
GUI Configuration Manager
Gestisce configurazioni persistenti per sistema GUI
"""

import json
from pathlib import Path

class GUIConfig:
    """Gestisce configurazione GUI persistente"""
    
    def __init__(self, config_file="gui_config.json"):
        self.config_file = Path(config_file)
        self.defaults = {
            # Finestra principale
            "main_window": {
                "width": 1200,
                "height": 700,
                "pos_x": None,  # None = auto-center
                "pos_y": None,
                "maximized": False
            },
            
            # Editor traduzione
            "editor": {
                "width": 1400,
                "height": 800,
                "split_position": 0.5,  # 50% split
                "font_size": 10,
                "sync_scroll": True,
                "auto_save_interval": 30,  # secondi
                "backup_interval": 300,    # 5 minuti
                "max_backups": 10
            },
            
            # Project Manager
            "project_manager": {
                "auto_refresh": True,
                "refresh_interval": 30,  # secondi
                "show_completed": True,
                "sort_column": "modified",
                "sort_direction": "desc",
                "column_widths": {
                    "project": 250,
                    "status": 100,
                    "completion": 150,
                    "chapters": 80,
                    "characters": 120,
                    "modified": 130,
                    "tracker": 80
                }
            },
            
            # Appearance
            "appearance": {
                "theme": "professional",  # professional, dark, light
                "font_family": "Calibri",
                "color_scheme": "blue_navy",  # blue_navy, green, purple
                "show_tooltips": True,
                "animations": True
            },
            
            # Behavior
            "behavior": {
                "confirm_exit": True,
                "auto_backup_on_exit": True,
                "restore_session": True,
                "check_updates": True,
                "minimize_to_tray": False
            },
            
            # Advanced
            "advanced": {
                "debug_mode": False,
                "log_level": "info",  # debug, info, warning, error
                "performance_mode": False,
                "experimental_features": False
            }
        }
        
        self.config = self.load_config()
    
    def load_config(self):
        """Carica configurazione da file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                
                # Merge con defaults (mantieni defaults per chiavi mancanti)
                merged_config = self._deep_merge(self.defaults.copy(), saved_config)
                return merged_config
                
            except Exception as e:
                print(f"Errore caricamento config: {e}")
                return self.defaults.copy()
        else:
            # Prima volta - crea file con defaults
            self.save_config(self.defaults)
            return self.defaults.copy()
    
    def _deep_merge(self, base, override):
        """Merge profondo di dizionari"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
    
    def save_config(self, config=None):
        """Salva configurazione su file"""
        config_to_save = config or self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore salvataggio config: {e}")
            return False
    
    def get(self, path, default=None):
        """Ottieni valore configurazione con path (es: 'editor.font_size')"""
        keys = path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, path, value):
        """Imposta valore configurazione con path"""
        keys = path.split('.')
        config = self.config
        
        # Naviga fino al penultimo livello
        for key in keys[:-1]:
            if key not in config or not isinstance(config[key], dict):
                config[key] = {}
            config = config[key]
        
        # Imposta valore finale
        config[keys[-1]] = value
        
        # Salva automaticamente
        self.save_config()
    
    def get_window_geometry(self, window_type="main"):
        """Ottieni geometria finestra"""
        window_config = self.get(f"{window_type}_window", {})
        
        # Assicurati che window_config sia un dict
        if not isinstance(window_config, dict):
            window_config = {}
        
        width = window_config.get("width", 1200)
        height = window_config.get("height", 700)
        pos_x = window_config.get("pos_x")
        pos_y = window_config.get("pos_y")
        maximized = window_config.get("maximized", False)
        
        return {
            "width": width,
            "height": height,
            "pos_x": pos_x,
            "pos_y": pos_y,
            "maximized": maximized
        }
    
    def save_window_geometry(self, window_type, width, height, x=None, y=None, maximized=False):
        """Salva geometria finestra"""
        self.set(f"{window_type}_window.width", width)
        self.set(f"{window_type}_window.height", height)
        
        if x is not None:
            self.set(f"{window_type}_window.pos_x", x)
        if y is not None:
            self.set(f"{window_type}_window.pos_y", y)
        
        self.set(f"{window_type}_window.maximized", maximized)
    
    def get_column_widths(self):
        """Ottieni larghezze colonne project manager"""
        widths = self.get("project_manager.column_widths", {})
        # Assicurati che sia un dict
        if not isinstance(widths, dict):
            widths = {}
        return widths
    
    def save_column_widths(self, widths):
        """Salva larghezze colonne"""
        for column, width in widths.items():
            self.set(f"project_manager.column_widths.{column}", width)
    
    def get_editor_settings(self):
        """Ottieni impostazioni editor"""
        return {
            "split_position": self.get("editor.split_position", 0.5),
            "font_size": self.get("editor.font_size", 10),
            "sync_scroll": self.get("editor.sync_scroll", True),
            "auto_save_interval": self.get("editor.auto_save_interval", 30),
            "backup_interval": self.get("editor.backup_interval", 300),
            "max_backups": self.get("editor.max_backups", 10)
        }
    
    def get_appearance_settings(self):
        """Ottieni impostazioni aspetto"""
        return {
            "theme": self.get("appearance.theme", "professional"),
            "font_family": self.get("appearance.font_family", "Calibri"),
            "color_scheme": self.get("appearance.color_scheme", "blue_navy"),
            "show_tooltips": self.get("appearance.show_tooltips", True),
            "animations": self.get("appearance.animations", True)
        }
    
    def reset_to_defaults(self):
        """Reset configurazione ai defaults"""
        self.config = self.defaults.copy()
        self.save_config()
    
    def export_config(self, export_file):
        """Esporta configurazione"""
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore esportazione: {e}")
            return False
    
    def import_config(self, import_file):
        """Importa configurazione"""
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
            
            # Merge con configurazione corrente
            self.config = self._deep_merge(self.defaults.copy(), imported_config)
            self.save_config()
            return True
            
        except Exception as e:
            print(f"Errore importazione: {e}")
            return False

class ThemeManager:
    """Gestisce temi GUI"""
    
    def __init__(self):
        self.themes = {
            "professional": {
                "colors": {
                    'bg_main': '#f8f9fa',
                    'bg_secondary': '#e9ecef',
                    'bg_accent': '#2c5aa0',
                    'text_primary': '#212529',
                    'text_secondary': '#6c757d'
                }
            },
            "dark": {
                "colors": {
                    'bg_main': '#2b2b2b',
                    'bg_secondary': '#3c3c3c',
                    'bg_accent': '#4a9eff',
                    'text_primary': '#ffffff',
                    'text_secondary': '#cccccc'
                }
            },
            "light": {
                "colors": {
                    'bg_main': '#ffffff',
                    'bg_secondary': '#f5f5f5',
                    'bg_accent': '#007bff',
                    'text_primary': '#000000',
                    'text_secondary': '#666666'
                }
            }
        }
    
    def get_theme(self, theme_name):
        """Ottieni tema"""
        return self.themes.get(theme_name, self.themes["professional"])
    
    def apply_theme_to_styles(self, styles_instance, theme_name):
        """Applica tema a istanza GUIStyles"""
        theme = self.get_theme(theme_name)
        if theme and 'colors' in theme:
            styles_instance.colors.update(theme['colors'])

# Istanza globale configurazione
gui_config = GUIConfig()

def get_config():
    """Ottieni istanza configurazione globale"""
    return gui_config