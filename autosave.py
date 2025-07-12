# FILENAME: autosave.py
#!/usr/bin/env python3
"""
Auto Save Manager - Universal Light Novel Translator GUI
Gestisce salvataggio automatico e cronologia modifiche
"""

import os
import time
import json
import hashlib
import threading
from pathlib import Path
from datetime import datetime

class AutoSaveManager:
    """Gestisce auto-save e backup intelligenti"""
    
    def __init__(self, project_path, template_file):
        self.project_path = Path(project_path)
        self.template_file = Path(template_file)
        self.backup_folder = self.project_path / "backup"
        self.backup_folder.mkdir(exist_ok=True)
        
        # Configurazione
        self.auto_save_interval = 30  # secondi
        self.backup_interval = 300    # 5 minuti
        self.max_backups = 10         # massimo backup da tenere
        
        # Stato
        self.last_content = ""
        self.last_save_time = 0
        self.last_backup_time = 0
        self.is_monitoring = False
        self.has_changes = False
        
        # Thread monitoring
        self.monitor_thread = None
        
        # Carica stato iniziale
        self.load_initial_state()
    
    def load_initial_state(self):
        """Carica stato iniziale del file"""
        if self.template_file.exists():
            with open(self.template_file, 'r', encoding='utf-8') as f:
                self.last_content = f.read()
            self.last_save_time = time.time()
    
    def start_monitoring(self, content_callback=None):
        """Avvia monitoraggio auto-save"""
        self.is_monitoring = True
        self.content_callback = content_callback
        
        def monitor_loop():
            while self.is_monitoring:
                try:
                    current_time = time.time()
                    
                    # Ottieni contenuto corrente
                    if self.content_callback:
                        current_content = self.content_callback()
                    else:
                        continue
                    
                    # Controlla se ci sono modifiche
                    if current_content != self.last_content:
                        self.has_changes = True
                        
                        # Auto-save se è passato abbastanza tempo
                        if current_time - self.last_save_time >= self.auto_save_interval:
                            self.auto_save(current_content)
                        
                        # Backup periodico
                        if current_time - self.last_backup_time >= self.backup_interval:
                            self.create_backup(current_content)
                    
                    time.sleep(5)  # Controlla ogni 5 secondi
                    
                except Exception as e:
                    print(f"Errore auto-save monitoring: {e}")
                    time.sleep(10)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Ferma monitoraggio"""
        self.is_monitoring = False
    
    def auto_save(self, content):
        """Salvataggio automatico"""
        try:
            # Salva solo se ci sono realmente modifiche
            if content != self.last_content:
                with open(self.template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.last_content = content
                self.last_save_time = time.time()
                self.has_changes = False
                
                return True
        except Exception as e:
            print(f"Errore auto-save: {e}")
            return False
    
    def manual_save(self, content):
        """Salvataggio manuale esplicito"""
        success = self.auto_save(content)
        if success:
            # Crea backup anche per save manuali importanti
            self.create_backup(content, prefix="manual")
        return success
    
    def create_backup(self, content, prefix="auto"):
        """Crea backup con timestamp"""
        try:
            # Nome file backup compatto
            timestamp = datetime.now().strftime("%m%d_%H%M")
            backup_name = f"tmpl_{prefix}_{timestamp}.bak"
            backup_path = self.backup_folder / backup_name
            
            # Salva backup
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.last_backup_time = time.time()
            
            # Pulisci vecchi backup
            self.cleanup_old_backups()
            
            return backup_path
            
        except Exception as e:
            print(f"Errore creazione backup: {e}")
            return None
    
    def cleanup_old_backups(self):
        """Rimuovi backup vecchi per risparmiare spazio"""
        try:
            # Lista tutti i backup
            backups = list(self.backup_folder.glob("tmpl_*.bak"))
            
            # Ordina per data di modifica (più recenti prima)
            backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Rimuovi backup in eccesso
            for backup in backups[self.max_backups:]:
                backup.unlink()
                
        except Exception as e:
            print(f"Errore cleanup backup: {e}")
    
    def get_backup_list(self):
        """Ottieni lista backup disponibili"""
        try:
            backups = []
            for backup_file in self.backup_folder.glob("tmpl_*.bak"):
                stat = backup_file.stat()
                backups.append({
                    'file': backup_file,
                    'name': backup_file.name,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'type': 'manual' if 'manual' in backup_file.name else 'auto'
                })
            
            # Ordina per data (più recenti prima)
            backups.sort(key=lambda x: x['modified'], reverse=True)
            return backups
            
        except Exception as e:
            print(f"Errore lettura backup: {e}")
            return []
    
    def restore_backup(self, backup_file):
        """Ripristina da backup"""
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                return False
            
            # Crea backup del contenuto corrente prima di ripristinare
            if self.template_file.exists():
                with open(self.template_file, 'r', encoding='utf-8') as f:
                    current_content = f.read()
                self.create_backup(current_content, prefix="before_restore")
            
            # Ripristina backup
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            
            with open(self.template_file, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            
            self.last_content = backup_content
            self.last_save_time = time.time()
            
            return True
            
        except Exception as e:
            print(f"Errore ripristino backup: {e}")
            return False
    
    def get_change_summary(self, content):
        """Ottieni riassunto modifiche rispetto all'ultimo save"""
        if not self.last_content:
            return {
                'char_diff': len(content),
                'translation_progress': 0,
                'has_significant_changes': True,
                'is_new_file': True
            }
        
        # Calcola differenze di base
        old_lines = self.last_content.split('\n')
        new_lines = content.split('\n')
        
        old_chars = len(self.last_content)
        new_chars = len(content)
        char_diff = new_chars - old_chars
        
        # Stima traduzioni aggiunte/rimosse
        old_placeholders = self.last_content.count('[Inserisci qui')
        new_placeholders = content.count('[Inserisci qui')
        translation_diff = old_placeholders - new_placeholders
        
        summary = {
            'char_diff': char_diff,
            'translation_progress': translation_diff,
            'has_significant_changes': abs(char_diff) > 100 or translation_diff != 0
        }
        
        return summary
    
    def get_save_status(self):
        """Ottieni stato corrente salvataggio"""
        return {
            'has_unsaved_changes': self.has_changes,
            'last_save_time': self.last_save_time,
            'last_backup_time': self.last_backup_time,
            'backup_count': len(list(self.backup_folder.glob("tmpl_*.bak"))),
            'is_monitoring': self.is_monitoring
        }
    
    def force_save_and_backup(self, content):
        """Forza salvataggio e backup (per chiusura app)"""
        try:
            # Salva sempre
            with open(self.template_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Crea backup se ci sono modifiche significative
            summary = self.get_change_summary(content)
            if summary.get('has_significant_changes', False):
                self.create_backup(content, prefix="exit")
            
            self.last_content = content
            self.has_changes = False
            
            return True
            
        except Exception as e:
            print(f"Errore force save: {e}")
            return False

class RecoveryManager:
    """Gestisce recovery da crash"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.recovery_file = self.project_path / "recovery.tmp"
    
    def save_recovery_state(self, content, cursor_position=None):
        """Salva stato per recovery"""
        try:
            recovery_data = {
                'content': content,
                'timestamp': time.time(),
                'cursor_position': cursor_position
            }
            
            with open(self.recovery_file, 'w', encoding='utf-8') as f:
                json.dump(recovery_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Errore save recovery: {e}")
    
    def has_recovery_data(self):
        """Controlla se esistono dati di recovery"""
        return self.recovery_file.exists()
    
    def load_recovery_data(self):
        """Carica dati di recovery"""
        try:
            if not self.recovery_file.exists():
                return None
            
            with open(self.recovery_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Controlla se i dati sono recenti (meno di 1 ora)
            if time.time() - data['timestamp'] < 3600:
                return data
            else:
                self.clear_recovery_data()
                return None
                
        except Exception as e:
            print(f"Errore load recovery: {e}")
            return None
    
    def clear_recovery_data(self):
        """Pulisci dati recovery"""
        try:
            if self.recovery_file.exists():
                self.recovery_file.unlink()
        except Exception as e:
            print(f"Errore clear recovery: {e}")