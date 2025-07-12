#!/usr/bin/env python3
# FILENAME: template_updater.py
"""
Template Updater - Aggiorna progetti esistenti con nuovi template
Converte template vecchi (preview) in template completi (testo full)
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

class TemplateUpdater:
    def __init__(self, translations_folder="translations"):
        self.translations_folder = Path(translations_folder)
    
    def find_existing_projects(self):
        """Trova tutti i progetti esistenti"""
        if not self.translations_folder.exists():
            return []
        
        projects = []
        for project_dir in self.translations_folder.iterdir():
            if project_dir.is_dir() and (project_dir / "template_traduzione.md").exists():
                projects.append(project_dir)
        
        return projects
    
    def backup_existing_template(self, project_folder):
        """Crea backup del template esistente"""
        template_file = project_folder / "template_traduzione.md"
        backup_file = project_folder / f"template_traduzione_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        if template_file.exists():
            shutil.copy2(template_file, backup_file)
            print(f"  📄 Backup creato: {backup_file.name}")
            return backup_file
        return None
    
    def detect_template_type(self, template_file):
        """Rileva se il template ha testo completo o preview"""
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Cerca indicatori di template con preview
        if "[...CONTINUA...]" in content or "[...CONTINUA NEL FILE CAPITOLO...]" in content:
            return "preview"
        elif "SEZIONE" in content and "TESTO ORIGINALE" in content:
            return "sections"
        else:
            return "complete"
    
    def load_original_text(self, project_folder):
        """Carica il testo originale completo dal backup"""
        originale_folder = project_folder / "originale"
        capitoli_folder = project_folder / "capitoli"
        
        chapters = {}
        
        # Prova a caricare dai file capitoli singoli
        if capitoli_folder.exists():
            for capitolo_file in capitoli_folder.glob("*.txt"):
                with open(capitolo_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Estrai titolo e testo
                lines = content.split('\n')
                title = lines[0].replace('# ', '') if lines else capitolo_file.stem
                text = '\n'.join(lines[2:]) if len(lines) > 2 else content
                
                chapter_id = capitolo_file.stem.split('_')[0]  # Es: "Capitolo_01" -> "Capitolo"
                chapters[chapter_id] = {
                    "title": title,
                    "text": text.strip()
                }
        
        return chapters
    
    def regenerate_template(self, project_folder, config=None):
        """Rigenera template con testo completo"""
        try:
            from universal_translator import UniversalNovelTranslator, TemplateConfig
        except ImportError:
            print(f"  ❌ Errore import: assicurati che universal_translator.py sia presente")
            return False
        
        if config is None:
            # Carica config se esiste, altrimenti usa default
            config_file = project_folder / "template_config.json"
            config = TemplateConfig()
            if config_file.exists():
                config.load_from_file(config_file)
        
        # Carica testo originale
        chapters = self.load_original_text(project_folder)
        
        if not chapters:
            print(f"  ❌ Impossibile trovare testo originale per {project_folder.name}")
            return False
        
        # Rigenera template
        translator = UniversalNovelTranslator()
        title = project_folder.name.replace('_PDF', '').replace('_EPUB', '').replace('_', ' ')
        file_type = 'PDF' if '_PDF' in project_folder.name else 'EPUB'
        
        template_path = translator.create_configurable_template(
            project_folder, title, chapters, file_type, config
        )
        
        # Crea file di configurazione se non esiste
        if not (project_folder / "template_config.json").exists():
            translator.create_template_config_file(project_folder)
        
        print(f"  ✅ Template rigenerato: {template_path.name}")
        return True
    
    def update_single_project(self, project_folder, force_update=False):
        """Aggiorna singolo progetto"""
        print(f"\n🔄 Aggiornando: {project_folder.name}")
        
        template_file = project_folder / "template_traduzione.md"
        template_type = self.detect_template_type(template_file)
        
        print(f"  📝 Tipo template rilevato: {template_type}")
        
        if template_type == "complete" and not force_update:
            print(f"  ✅ Template già completo, skip")
            return True
        
        if template_type == "preview" or force_update:
            # Backup del template esistente
            backup = self.backup_existing_template(project_folder)
            
            # Rigenera con testo completo
            success = self.regenerate_template(project_folder)
            
            if success:
                print(f"  🎉 Aggiornamento completato!")
                print(f"  💾 Backup salvato come: {backup.name if backup else 'N/A'}")
                return True
            else:
                print(f"  ❌ Aggiornamento fallito")
                return False
        
        return True
    
    def update_all_projects(self, force_update=False):
        """Aggiorna tutti i progetti esistenti"""
        projects = self.find_existing_projects()
        
        if not projects:
            print("❌ Nessun progetto trovato")
            return
        
        print(f"🔍 Trovati {len(projects)} progetti da controllare")
        
        updated = 0
        skipped = 0
        failed = 0
        
        for project in projects:
            try:
                success = self.update_single_project(project, force_update)
                if success:
                    template_type = self.detect_template_type(project / "template_traduzione.md")
                    if template_type in ["complete", "sections"]:
                        updated += 1
                    else:
                        skipped += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"  ❌ Errore: {e}")
                failed += 1
        
        print(f"\n🎉 RISULTATI AGGIORNAMENTO:")
        print(f"✅ Aggiornati: {updated}")
        print(f"⏭️ Già completi: {skipped}")
        print(f"❌ Falliti: {failed}")
    
    def interactive_update(self):
        """Interface interattiva per aggiornamento"""
        print("🔄 TEMPLATE UPDATER - Aggiorna Template Progetti")
        print("=" * 50)
        
        projects = self.find_existing_projects()
        
        if not projects:
            print("❌ Nessun progetto trovato in translations/")
            return
        
        print(f"📚 Progetti trovati: {len(projects)}")
        print()
        
        for i, project in enumerate(projects, 1):
            template_type = self.detect_template_type(project / "template_traduzione.md")
            status = "✅ OK" if template_type in ["complete", "sections"] else "⚠️ PREVIEW"
            print(f"[{i}] {project.name} - {status}")
        
        print(f"\n📋 OPZIONI:")
        print("[1] 🔄 Aggiorna tutti i progetti (solo quelli con preview)")
        print("[2] 🔄 Aggiorna tutti i progetti (forza, anche quelli completi)")
        print("[3] 🎯 Aggiorna progetto specifico")
        print("[4] 📊 Solo mostra stato progetti")
        print("[5] 🚪 Esci")
        
        choice = input("\nScegli opzione (1-5): ").strip()
        
        if choice == "1":
            self.update_all_projects(force_update=False)
        elif choice == "2":
            self.update_all_projects(force_update=True)
        elif choice == "3":
            print("\nProGetti disponibili:")
            for i, project in enumerate(projects, 1):
                print(f"[{i}] {project.name}")
            
            try:
                project_choice = int(input(f"\nScegli progetto (1-{len(projects)}): ")) - 1
                if 0 <= project_choice < len(projects):
                    self.update_single_project(projects[project_choice], force_update=True)
                else:
                    print("❌ Scelta non valida")
            except ValueError:
                print("❌ Inserisci un numero valido")
        elif choice == "4":
            print(f"\n📊 STATO PROGETTI:")
            for project in projects:
                template_type = self.detect_template_type(project / "template_traduzione.md")
                status_icon = "✅" if template_type in ["complete", "sections"] else "⚠️"
                print(f"{status_icon} {project.name} - {template_type}")
        elif choice == "5":
            print("👋 Arrivederci!")
        else:
            print("❌ Scelta non valida")

def main():
    """Funzione principale"""
    import sys
    
    updater = TemplateUpdater()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "update-all":
            updater.update_all_projects()
        elif command == "force-update-all":
            updater.update_all_projects(force_update=True)
        elif command == "status":
            projects = updater.find_existing_projects()
            for project in projects:
                template_type = updater.detect_template_type(project / "template_traduzione.md")
                print(f"{project.name}: {template_type}")
        else:
            print(f"❌ Comando non riconosciuto: {command}")
            print("Comandi disponibili: update-all, force-update-all, status")
    else:
        updater.interactive_update()

if __name__ == "__main__":
    main()