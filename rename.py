# FILENAME: rename.py
#!/usr/bin/env python3
"""
Sistema Rinominazione File Compatti
Aggiorna progetti esistenti con nomenclatura compatta
"""

import shutil
from pathlib import Path
from datetime import datetime

class SystemRenamer:
    """Rinomina file sistema esistente con nomi compatti"""
    
    def __init__(self, translations_folder="translations"):
        self.translations_folder = Path(translations_folder)
        
        # Mapping rinominazioni
        self.file_mappings = {
            "template_traduzione.md": "tmpl.md",
            "progress_tracker.md": "prog.md",
            "info_progetto.md": "info.md",
            "smart_tracker.py": "trkr.py",
            "smart_tracker.json": "trkr.json",
            "statistiche_live.md": "stats.md",
            "template_config.json": "cfg.json",
            "tracker.bat": "trkr.bat"
        }
        
        # Pattern backup
        self.backup_patterns = [
            ("template_traduzione_backup_", "tmpl_"),
            ("progress_tracker_backup_", "prog_"),
            ("smart_tracker_backup_", "trkr_")
        ]
    
    def find_projects(self):
        """Trova tutti i progetti esistenti"""
        if not self.translations_folder.exists():
            return []
        
        projects = []
        for project_dir in self.translations_folder.iterdir():
            if project_dir.is_dir():
                # Controlla se ha almeno un file template
                has_template = (
                    (project_dir / "template_traduzione.md").exists() or
                    (project_dir / "tmpl.md").exists()
                )
                if has_template:
                    projects.append(project_dir)
        
        return projects
    
    def analyze_project(self, project_dir):
        """Analizza progetto per rinominazioni necessarie"""
        analysis = {
            'project_name': project_dir.name,
            'project_path': project_dir,
            'files_to_rename': [],
            'backups_to_rename': [],
            'already_renamed': [],
            'total_operations': 0
        }
        
        # Controlla file principali
        for old_name, new_name in self.file_mappings.items():
            old_file = project_dir / old_name
            new_file = project_dir / new_name
            
            if old_file.exists() and not new_file.exists():
                analysis['files_to_rename'].append((old_file, new_file))
            elif new_file.exists():
                analysis['already_renamed'].append(new_name)
        
        # Controlla backup files
        for old_pattern, new_pattern in self.backup_patterns:
            backup_files = list(project_dir.glob(f"{old_pattern}*"))
            for backup_file in backup_files:
                # Estrai timestamp e estensione
                filename = backup_file.name
                suffix = filename[len(old_pattern):]
                
                # Converti formato timestamp se necessario
                new_name = self.convert_backup_name(new_pattern, suffix)
                new_backup = project_dir / new_name
                
                if not new_backup.exists():
                    analysis['backups_to_rename'].append((backup_file, new_backup))
        
        analysis['total_operations'] = (
            len(analysis['files_to_rename']) + 
            len(analysis['backups_to_rename'])
        )
        
        return analysis
    
    def convert_backup_name(self, new_pattern, suffix):
        """Converte nome backup in formato compatto"""
        # Se il suffix è già in formato compatto (MMDD_HHMM.bak)
        if suffix.count('_') == 1 and suffix.endswith('.bak'):
            return new_pattern + suffix
        
        # Se è in formato lungo (YYYYMMDD_HHMMSS.md)
        # Converti a formato compatto
        try:
            if len(suffix) >= 15:  # YYYYMMDD_HHMMSS format
                date_part = suffix[:8]   # YYYYMMDD
                time_part = suffix[9:15] # HHMMSS
                
                # Converti a MMDD_HHMM
                if len(date_part) == 8 and len(time_part) == 6:
                    mm = date_part[4:6]
                    dd = date_part[6:8]
                    hh = time_part[:2]
                    mn = time_part[2:4]
                    
                    return f"{new_pattern}{mm}{dd}_{hh}{mn}.bak"
        except:
            pass
        
        # Fallback: usa timestamp corrente
        timestamp = datetime.now().strftime("%m%d_%H%M")
        return f"{new_pattern}{timestamp}.bak"
    
    def rename_project(self, project_dir, dry_run=True):
        """Rinomina file di un progetto"""
        analysis = self.analyze_project(project_dir)
        
        if analysis['total_operations'] == 0:
            return True, "Nessuna rinominazione necessaria"
        
        results = []
        errors = []
        
        # Rinomina file principali
        for old_file, new_file in analysis['files_to_rename']:
            try:
                if not dry_run:
                    old_file.rename(new_file)
                results.append(f"✅ {old_file.name} → {new_file.name}")
            except Exception as e:
                errors.append(f"❌ {old_file.name}: {e}")
        
        # Rinomina backup
        for old_backup, new_backup in analysis['backups_to_rename']:
            try:
                if not dry_run:
                    old_backup.rename(new_backup)
                results.append(f"📄 {old_backup.name} → {new_backup.name}")
            except Exception as e:
                errors.append(f"❌ {old_backup.name}: {e}")
        
        # Aggiorna riferimenti interni nei file
        if not dry_run:
            self.update_file_references(project_dir)
        
        success = len(errors) == 0
        message = "\n".join(results + errors)
        
        return success, message
    
    def update_file_references(self, project_dir):
        """Aggiorna riferimenti interni nei file rinominati"""
        try:
            # Aggiorna info.md se esiste
            info_file = project_dir / "info.md"
            if info_file.exists():
                with open(info_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Aggiorna riferimenti a file
                content = content.replace("template_traduzione.md", "tmpl.md")
                content = content.replace("progress_tracker.md", "prog.md")
                
                with open(info_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Aggiorna trkr.bat se esiste
            tracker_bat = project_dir / "trkr.bat"
            if tracker_bat.exists():
                with open(tracker_bat, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Aggiorna riferimenti
                content = content.replace("smart_tracker.py", "trkr.py")
                
                with open(tracker_bat, 'w', encoding='utf-8') as f:
                    f.write(content)
        
        except Exception as e:
            print(f"Errore aggiornamento riferimenti: {e}")
    
    def rename_all_projects(self, dry_run=True):
        """Rinomina tutti i progetti"""
        projects = self.find_projects()
        
        if not projects:
            return True, "Nessun progetto trovato"
        
        total_results = []
        total_errors = []
        
        print(f"🔍 Trovati {len(projects)} progetti")
        print(f"{'🔄 SIMULAZIONE' if dry_run else '⚠️ ESECUZIONE REALE'}")
        print("=" * 50)
        
        for project_dir in projects:
            print(f"\n📁 {project_dir.name}")
            
            analysis = self.analyze_project(project_dir)
            
            if analysis['total_operations'] == 0:
                print("  ✅ Già rinominato")
                continue
            
            print(f"  📊 {analysis['total_operations']} operazioni necessarie")
            
            if analysis['already_renamed']:
                print(f"  ✅ Già rinominati: {', '.join(analysis['already_renamed'])}")
            
            success, message = self.rename_project(project_dir, dry_run)
            
            if success:
                total_results.append(f"✅ {project_dir.name}")
                print("  " + message.replace('\n', '\n  '))
            else:
                total_errors.append(f"❌ {project_dir.name}")
                print("  " + message.replace('\n', '\n  '))
        
        print("\n" + "=" * 50)
        print(f"📊 RISULTATI: {len(total_results)} successi, {len(total_errors)} errori")
        
        return len(total_errors) == 0, f"{len(total_results)} progetti rinominati"
    
    def interactive_rename(self):
        """Interface interattiva per rinominazione"""
        print("🔄 SISTEMA RINOMINAZIONE FILE COMPATTI")
        print("=" * 45)
        
        projects = self.find_projects()
        
        if not projects:
            print("❌ Nessun progetto trovato")
            return
        
        print(f"📚 Trovati {len(projects)} progetti")
        print("\n📋 ANALISI PROGETTI:")
        
        total_operations = 0
        for project_dir in projects:
            analysis = self.analyze_project(project_dir)
            status = "✅ OK" if analysis['total_operations'] == 0 else f"🔄 {analysis['total_operations']} ops"
            print(f"  {project_dir.name}: {status}")
            total_operations += analysis['total_operations']
        
        if total_operations == 0:
            print("\n✅ Tutti i progetti sono già aggiornati!")
            return
        
        print(f"\n📊 Totale operazioni necessarie: {total_operations}")
        print("\n📋 OPZIONI:")
        print("[1] 🔍 Simulazione (mostra cosa farebbe)")
        print("[2] ⚠️ Esecuzione reale")
        print("[3] 📁 Rinomina progetto specifico")
        print("[4] 🚪 Esci")
        
        choice = input("\nScegli opzione (1-4): ").strip()
        
        if choice == "1":
            print("\n🔍 SIMULAZIONE:")
            self.rename_all_projects(dry_run=True)
        elif choice == "2":
            confirm = input("\n⚠️ ATTENZIONE: Questa operazione rinominerà file reali. Continuare? (yes/no): ")
            if confirm.lower() in ['yes', 'y', 'si', 's']:
                print("\n⚠️ ESECUZIONE REALE:")
                self.rename_all_projects(dry_run=False)
            else:
                print("❌ Operazione annullata")
        elif choice == "3":
            print("\nProGetti disponibili:")
            for i, project in enumerate(projects, 1):
                analysis = self.analyze_project(project)
                status = "✅ OK" if analysis['total_operations'] == 0 else f"🔄 {analysis['total_operations']} ops"
                print(f"[{i}] {project.name} - {status}")
            
            try:
                project_choice = int(input(f"\nScegli progetto (1-{len(projects)}): ")) - 1
                if 0 <= project_choice < len(projects):
                    project = projects[project_choice]
                    print(f"\n📁 Rinominazione {project.name}...")
                    success, message = self.rename_project(project, dry_run=False)
                    print(message)
                else:
                    print("❌ Scelta non valida")
            except ValueError:
                print("❌ Inserisci un numero valido")
        elif choice == "4":
            print("👋 Arrivederci!")
        else:
            print("❌ Scelta non valida")

def main():
    """Funzione principale"""
    import sys
    
    renamer = SystemRenamer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "analyze":
            projects = renamer.find_projects()
            for project in projects:
                analysis = renamer.analyze_project(project)
                print(f"{project.name}: {analysis['total_operations']} operazioni")
        elif command == "simulate":
            renamer.rename_all_projects(dry_run=True)
        elif command == "execute":
            renamer.rename_all_projects(dry_run=False)
        else:
            print(f"❌ Comando non riconosciuto: {command}")
            print("Comandi disponibili: analyze, simulate, execute")
    else:
        renamer.interactive_rename()

if __name__ == "__main__":
    main()