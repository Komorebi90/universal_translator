# FILENAME: advanced_save_diagnostic.py
#!/usr/bin/env python3
"""
Diagnostico Avanzato per Problemi di Salvataggio
Identifica problemi specifici OneDrive, editor, encoding, lock file
"""

import os
import sys
import time
import psutil
import subprocess
import tempfile
from pathlib import Path
import json
import shutil

class AdvancedSaveDiagnostic:
    def __init__(self):
        self.translations_folder = Path("translations")
        self.issues_found = []
        self.solutions = []
        
    def print_header(self, text):
        print(f"\n🔍 {text}")
        print("=" * 50)
    
    def add_issue(self, issue, solution):
        self.issues_found.append(issue)
        self.solutions.append(solution)
        print(f"⚠️  {issue}")
        print(f"💡 Soluzione: {solution}")
    
    def check_onedrive_sync_status(self):
        """Verifica problemi OneDrive"""
        self.print_header("ANALISI ONEDRIVE")
        
        current_path = Path.cwd()
        onedrive_indicators = ["OneDrive", "onedrive"]
        
        is_onedrive = any(indicator in str(current_path) for indicator in onedrive_indicators)
        
        if is_onedrive:
            print("📁 RILEVATO: Cartella su OneDrive")
            
            # Controlla file .tmp o lock di OneDrive
            for project_dir in self.translations_folder.glob("*/"):
                lock_files = list(project_dir.glob("*.tmp")) + list(project_dir.glob("~$*"))
                if lock_files:
                    self.add_issue(
                        f"File temporanei OneDrive in {project_dir.name}: {[f.name for f in lock_files]}",
                        "Chiudi tutti i programmi che usano questi file e aspetta sincronizzazione"
                    )
            
            # Verifica processo OneDrive
            onedrive_running = False
            for proc in psutil.process_iter(['name']):
                if 'onedrive' in proc.info['name'].lower():
                    onedrive_running = True
                    break
            
            if onedrive_running:
                print("✅ OneDrive in esecuzione")
            else:
                self.add_issue(
                    "OneDrive non in esecuzione",
                    "Riavvia OneDrive dal menu Start"
                )
            
            # Test sincronizzazione
            test_file = self.translations_folder / "test_sync.txt"
            try:
                with open(test_file, 'w') as f:
                    f.write(f"Test sync {time.time()}")
                time.sleep(2)
                if test_file.exists():
                    test_file.unlink()
                    print("✅ Sincronizzazione OneDrive funziona")
                else:
                    self.add_issue(
                        "OneDrive non sincronizza correttamente",
                        "Pausa e riprendi sincronizzazione OneDrive"
                    )
            except Exception as e:
                self.add_issue(
                    f"Impossibile creare file test: {e}",
                    "Controlla permessi cartella OneDrive"
                )
        else:
            print("📁 Cartella NON su OneDrive")
    
    def check_file_locks(self):
        """Controlla file bloccati da processi"""
        self.print_header("ANALISI FILE LOCKS")
        
        for project_dir in self.translations_folder.glob("*/"):
            template_file = project_dir / "template_traduzione.md"
            if template_file.exists():
                # Prova apertura esclusiva
                try:
                    with open(template_file, 'r+') as f:
                        pass
                    print(f"✅ {template_file.name} - Non bloccato")
                except PermissionError:
                    # Trova quale processo blocca il file
                    blocking_processes = self.find_process_using_file(template_file)
                    if blocking_processes:
                        self.add_issue(
                            f"File {template_file.name} bloccato da: {', '.join(blocking_processes)}",
                            "Chiudi questi programmi e riprova"
                        )
                    else:
                        self.add_issue(
                            f"File {template_file.name} bloccato (processo sconosciuto)",
                            "Riavvia il computer"
                        )
    
    def find_process_using_file(self, filepath):
        """Trova processi che usano un file specifico"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'open_files']):
                try:
                    if proc.info['open_files']:
                        for file_info in proc.info['open_files']:
                            if Path(file_info.path) == filepath.resolve():
                                processes.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception:
            pass
        return processes
    
    def check_encoding_issues(self):
        """Verifica problemi di encoding"""
        self.print_header("ANALISI ENCODING")
        
        for project_dir in self.translations_folder.glob("*/"):
            template_file = project_dir / "template_traduzione.md"
            if template_file.exists():
                try:
                    # Test lettura con encoding diversi
                    encodings = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252']
                    
                    content = None
                    used_encoding = None
                    
                    for encoding in encodings:
                        try:
                            with open(template_file, 'r', encoding=encoding) as f:
                                content = f.read()
                                used_encoding = encoding
                                break
                        except UnicodeDecodeError:
                            continue
                    
                    if content is None:
                        self.add_issue(
                            f"Impossibile leggere {template_file.name} con encoding standard",
                            "File potrebbe essere corrotto - rigenera template"
                        )
                    elif used_encoding != 'utf-8':
                        self.add_issue(
                            f"{template_file.name} ha encoding {used_encoding} invece di UTF-8",
                            "Converti file in UTF-8"
                        )
                    else:
                        print(f"✅ {template_file.name} - Encoding UTF-8 OK")
                        
                        # Test caratteri problematici
                        problematic_chars = ['\x00', '\ufeff', '\r\r\n']
                        for char in problematic_chars:
                            if char in content:
                                self.add_issue(
                                    f"{template_file.name} contiene caratteri problematici",
                                    "Pulisci file con editor avanzato"
                                )
                                break
                
                except Exception as e:
                    self.add_issue(
                        f"Errore analisi encoding {template_file.name}: {e}",
                        "Rigenera il file template"
                    )
    
    def check_path_length(self):
        """Verifica lunghezza path (problema Windows)"""
        self.print_header("ANALISI LUNGHEZZA PATH")
        
        for project_dir in self.translations_folder.glob("*/"):
            for file_path in project_dir.rglob("*"):
                path_length = len(str(file_path.resolve()))
                if path_length > 260:  # Limite Windows classico
                    self.add_issue(
                        f"Path troppo lungo ({path_length} caratteri): {file_path.name}",
                        "Sposta progetto in cartella con nome più corto"
                    )
                elif path_length > 200:
                    print(f"⚠️  Path lungo ({path_length} caratteri): {file_path.name}")
    
    def check_disk_space_detailed(self):
        """Analisi dettagliata spazio disco"""
        self.print_header("ANALISI SPAZIO DISCO DETTAGLIATA")
        
        # Spazio totale
        total, used, free = shutil.disk_usage(Path.cwd())
        free_gb = free // (1024**3)
        
        print(f"💾 Spazio libero: {free_gb} GB")
        
        if free_gb < 1:
            self.add_issue(
                "Spazio disco quasi esaurito",
                "Libera almeno 1GB di spazio"
            )
        
        # Spazio OneDrive specifico
        current_path = Path.cwd()
        if "OneDrive" in str(current_path):
            # OneDrive ha limiti specifici
            print("📁 Controllo limiti OneDrive...")
            
            # Calcola dimensione progetto
            total_size = 0
            for project_dir in self.translations_folder.glob("*/"):
                for file_path in project_dir.rglob("*"):
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
            
            size_mb = total_size / (1024**2)
            print(f"📊 Dimensione progetti: {size_mb:.1f} MB")
            
            if size_mb > 100:  # OneDrive può avere problemi con file grandi
                self.add_issue(
                    f"Progetti molto grandi ({size_mb:.1f} MB)",
                    "Considera di spostare progetti completati altrove"
                )
    
    def check_antivirus_interference(self):
        """Verifica interferenze antivirus"""
        self.print_header("ANALISI INTERFERENZE ANTIVIRUS")
        
        # Lista antivirus comuni
        common_av = [
            'avgnt.exe', 'avastui.exe', 'mbam.exe', 'msmpeng.exe',
            'norton.exe', 'mcshield.exe', 'kaspersky.exe'
        ]
        
        running_av = []
        for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()
            for av in common_av:
                if av.replace('.exe', '') in proc_name:
                    running_av.append(proc.info['name'])
        
        if running_av:
            print(f"🛡️  Antivirus rilevati: {', '.join(set(running_av))}")
            self.add_issue(
                "Antivirus potrebbe bloccare modifiche ai file",
                "Aggiungi cartella progetti alle esclusioni antivirus"
            )
        else:
            print("✅ Nessun antivirus comune rilevato")
    
    def test_editor_compatibility(self):
        """Test compatibilità con editor comuni"""
        self.print_header("TEST COMPATIBILITÀ EDITOR")
        
        test_file = self.translations_folder / "test_editor.md"
        test_content = """# Test Editor
        
## Sezione Test
        
Questo è un test per verificare la compatibilità dell'editor.

```
Testo in code block
Con caratteri speciali: àèìòù
E emoji: 🎌📚✅
```

### Fine Test
"""
        
        try:
            # Test scrittura
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
            
            # Test lettura
            with open(test_file, 'r', encoding='utf-8') as f:
                read_content = f.read()
            
            if read_content == test_content:
                print("✅ Test editor base: OK")
            else:
                self.add_issue(
                    "Contenuto modificato durante salvataggio",
                    "Usa un editor che supporta UTF-8 (VSCode, Notepad++)"
                )
            
            # Cleanup
            test_file.unlink()
            
        except Exception as e:
            self.add_issue(
                f"Errore test editor: {e}",
                "Problemi di base con scrittura file"
            )
    
    def suggest_editor_alternatives(self):
        """Suggerisce editor alternativi"""
        self.print_header("RACCOMANDAZIONI EDITOR")
        
        editors = [
            ("Visual Studio Code", "Gratuito, ottimo per markdown"),
            ("Notepad++", "Leggero, supporto UTF-8 eccellente"),
            ("Sublime Text", "Veloce, buono per file grandi"),
            ("Typora", "Specializzato per markdown")
        ]
        
        print("📝 EDITOR RACCOMANDATI:")
        for name, desc in editors:
            print(f"   • {name}: {desc}")
        
        print("\n💡 CONFIGURAZIONE EDITOR:")
        print("   • Encoding: UTF-8 without BOM")
        print("   • Line endings: LF o CRLF")
        print("   • Salvataggio automatico: OFF")
        print("   • Backup automatico: OFF")
    
    def create_emergency_backup(self):
        """Crea backup di emergenza"""
        self.print_header("BACKUP DI EMERGENZA")
        
        backup_folder = Path("emergency_backup")
        backup_folder.mkdir(exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        
        for project_dir in self.translations_folder.glob("*/"):
            template_file = project_dir / "template_traduzione.md"
            if template_file.exists():
                backup_file = backup_folder / f"{project_dir.name}_template_{timestamp}.md"
                try:
                    shutil.copy2(template_file, backup_file)
                    print(f"✅ Backup: {backup_file.name}")
                except Exception as e:
                    print(f"❌ Errore backup {project_dir.name}: {e}")
        
        print(f"💾 Backup salvati in: {backup_folder.absolute()}")
    
    def run_all_diagnostics(self):
        """Esegue tutti i test diagnostici"""
        print("🔍 DIAGNOSTICO AVANZATO PROBLEMI SALVATAGGIO")
        print("=" * 55)
        
        self.check_onedrive_sync_status()
        self.check_file_locks()
        self.check_encoding_issues()
        self.check_path_length()
        self.check_disk_space_detailed()
        self.check_antivirus_interference()
        self.test_editor_compatibility()
        
        # Riepilogo
        self.print_header("RIEPILOGO PROBLEMI")
        
        if self.issues_found:
            print(f"❌ Trovati {len(self.issues_found)} problemi:")
            for i, (issue, solution) in enumerate(zip(self.issues_found, self.solutions), 1):
                print(f"\n{i}. PROBLEMA: {issue}")
                print(f"   SOLUZIONE: {solution}")
        else:
            print("✅ Nessun problema critico rilevato!")
            print("\n💡 Se il problema persiste:")
            print("   • Prova un editor diverso")
            print("   • Sposta progetto fuori da OneDrive temporaneamente")
            print("   • Controlla log Windows Event Viewer")
        
        self.suggest_editor_alternatives()
        
        # Offri backup
        if input("\nCreare backup di emergenza? (y/n): ").lower() == 'y':
            self.create_emergency_backup()

def main():
    diagnostic = AdvancedSaveDiagnostic()
    diagnostic.run_all_diagnostics()
    
    print("\n" + "=" * 55)
    print("Premi Enter per chiudere...")
    input()

if __name__ == "__main__":
    main()