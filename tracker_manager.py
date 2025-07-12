#!/usr/bin/env python3
"""
Integrazione Smart Tracker nel Universal Translator
Aggiunge monitoraggio automatico ai progetti esistenti
"""

import os
import subprocess
import time
from pathlib import Path
import threading

class TrackerManager:
    def __init__(self, translations_folder="translations"):
        self.translations_folder = Path(translations_folder)
        self.monitoring_threads = {}
        self.is_monitoring = False
    
    def setup_tracker_for_project(self, project_folder):
        """Installa smart tracker in un progetto esistente"""
        project_path = Path(project_folder)
        
        if not project_path.exists():
            print(f"❌ Progetto non trovato: {project_folder}")
            return False
        
        # Copia smart_tracker.py nel progetto
        tracker_script = project_path / "smart_tracker.py"
        
        # Crea script tracker personalizzato per il progetto
        tracker_content = '''#!/usr/bin/env python3
"""
Smart Tracker per questo progetto
Generato automaticamente dal Universal Translator
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_tracker_system import SmartTracker, monitor_project

def main():
    project_folder = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "monitor":
            monitor_project(project_folder, auto_update_seconds=30)
        elif command == "update":
            tracker = SmartTracker(project_folder)
            tracker.update_all()
            print("✅ Tracker aggiornato")
        elif command == "session-start":
            tracker = SmartTracker(project_folder)
            tracker.start_translation_session()
        elif command == "session-end":
            tracker = SmartTracker(project_folder)
            tracker.end_translation_session()
        elif command == "stats":
            tracker = SmartTracker(project_folder)
            tracker.update_all()
            stats_file = Path(project_folder) / "statistiche_live.md"
            if stats_file.exists():
                with open(stats_file, 'r', encoding='utf-8') as f:
                    print(f.read())
        else:
            print(f"Comando sconosciuto: {command}")
    else:
        # Aggiornamento automatico
        tracker = SmartTracker(project_folder)
        completion = tracker.update_all()
        print(f"📊 Progresso: {completion:.1f}%")

if __name__ == "__main__":
    main()
'''
        
        with open(tracker_script, 'w', encoding='utf-8') as f:
            f.write(tracker_content)
        
        # Crea batch file per Windows
        batch_file = project_path / "tracker.bat"
        batch_content = f'''@echo off
title Smart Tracker - {project_path.name}

:MENU
cls
echo.
echo 📊 SMART TRACKER - {project_path.name}
echo ═══════════════════════════════════════
echo.
echo [1] 🔄 Aggiorna Statistiche
echo [2] 👁️ Monitoraggio Automatico
echo [3] 📝 Inizia Sessione Traduzione
echo [4] ⏹️ Termina Sessione
echo [5] 📈 Visualizza Statistiche
echo [6] 🚪 Esci
echo.
set /p choice="Scegli opzione (1-6): "

if "%choice%"=="1" (
    python smart_tracker.py update
    pause
    goto MENU
)
if "%choice%"=="2" (
    echo 👁️ Avvio monitoraggio automatico...
    echo 🛑 Premi Ctrl+C per fermare
    python smart_tracker.py monitor
    pause
    goto MENU
)
if "%choice%"=="3" (
    python smart_tracker.py session-start
    pause
    goto MENU
)
if "%choice%"=="4" (
    python smart_tracker.py session-end
    pause
    goto MENU
)
if "%choice%"=="5" (
    python smart_tracker.py stats
    pause
    goto MENU
)
if "%choice%"=="6" goto EXIT

goto MENU

:EXIT
echo 👋 Arrivederci!
timeout /t 2 >nul
'''
        
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
        
        print(f"✅ Smart Tracker installato in: {project_folder}")
        print(f"🎯 Usa: {batch_file.name} per interface grafica")
        print(f"⚡ Oppure: python smart_tracker.py [comando]")
        
        return True
    
    def setup_all_projects(self):
        """Installa tracker in tutti i progetti esistenti"""
        if not self.translations_folder.exists():
            print(f"❌ Cartella traduzioni non trovata: {self.translations_folder}")
            return
        
        projects = [d for d in self.translations_folder.iterdir() if d.is_dir()]
        
        if not projects:
            print("❌ Nessun progetto trovato")
            return
        
        print(f"🔍 Trovati {len(projects)} progetti")
        
        for project in projects:
            print(f"⚙️ Setup tracker per: {project.name}")
            self.setup_tracker_for_project(project)
        
        print("✅ Smart Tracker installato in tutti i progetti!")
    
    def monitor_all_projects(self, update_interval=60):
        """Monitora tutti i progetti automaticamente"""
        projects = [d for d in self.translations_folder.iterdir() 
                   if d.is_dir() and (d / "template_traduzione.md").exists()]
        
        if not projects:
            print("❌ Nessun progetto da monitorare")
            return
        
        print(f"👁️ Monitoraggio {len(projects)} progetti ogni {update_interval} secondi")
        self.is_monitoring = True
        
        def monitor_project_thread(project_path):
            """Thread per monitorare singolo progetto"""
            from smart_tracker_system import SmartTracker
            
            tracker = SmartTracker(project_path)
            
            while self.is_monitoring:
                try:
                    completion = tracker.update_all()
                    print(f"📊 {project_path.name}: {completion:.1f}% - {time.strftime('%H:%M:%S')}")
                    
                    if completion >= 100:
                        print(f"🎉 COMPLETATO: {project_path.name}")
                    
                    time.sleep(update_interval)
                    
                except Exception as e:
                    print(f"❌ Errore monitoraggio {project_path.name}: {e}")
                    time.sleep(update_interval)
        
        # Avvia thread per ogni progetto
        for project in projects:
            thread = threading.Thread(
                target=monitor_project_thread, 
                args=(project,),
                daemon=True
            )
            thread.start()
            self.monitoring_threads[project.name] = thread
        
        try:
            while self.is_monitoring:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Monitoraggio fermato")
            self.is_monitoring = False
    
    def generate_global_dashboard(self):
        """Genera dashboard globale di tutti i progetti"""
        projects = [d for d in self.translations_folder.iterdir() 
                   if d.is_dir() and (d / "template_traduzione.md").exists()]
        
        if not projects:
            print("❌ Nessun progetto trovato")
            return
        
        dashboard_file = self.translations_folder / "dashboard_globale.md"
        
        dashboard_content = f"""# 🌟 DASHBOARD GLOBALE TRADUZIONI

*Aggiornato: {time.strftime('%d/%m/%Y alle %H:%M')}*

## 📊 PANORAMICA PROGETTI

| Progetto | Completamento | Capitoli | Caratteri | Stato |
|----------|---------------|----------|-----------|-------|
"""

        total_projects = len(projects)
        completed_projects = 0
        total_completion = 0
        
        for project in projects:
            try:
                from smart_tracker_system import SmartTracker
                tracker = SmartTracker(project)
                tracker.update_all()
                
                stats = tracker.data["statistics"]
                completion = stats["completion_percentage"]
                total_completion += completion
                
                if completion >= 100:
                    completed_projects += 1
                    status_icon = "✅"
                elif completion >= 50:
                    status_icon = "🔄"
                elif completion > 0:
                    status_icon = "🔄"
                else:
                    status_icon = "⏳"
                
                # Barra progresso
                progress_bar = '█' * int(completion // 10) + '░' * (10 - int(completion // 10))
                
                dashboard_content += f"| {project.name[:25]}... | {completion:.1f}% {progress_bar} | {stats['chapters_completed']}/{tracker.data['project_info']['total_chapters']} | {stats['translated_characters']:,}/{stats['total_characters']:,} | {status_icon} |\n"
                
            except Exception as e:
                dashboard_content += f"| {project.name[:25]}... | ❌ Errore | - | - | ❌ |\n"
        
        avg_completion = total_completion / total_projects if total_projects > 0 else 0
        
        dashboard_content += f"""
## 🎯 STATISTICHE GLOBALI

- **Progetti Totali**: {total_projects}
- **Progetti Completati**: {completed_projects}
- **Progetti in Corso**: {total_projects - completed_projects}
- **Completamento Medio**: {avg_completion:.1f}%

## 🏆 TOP PROGRESSI

"""

        # Ordina progetti per completamento
        project_stats = []
        for project in projects:
            try:
                from smart_tracker_system import SmartTracker
                tracker = SmartTracker(project)
                tracker.update_all()
                completion = tracker.data["statistics"]["completion_percentage"]
                project_stats.append((project.name, completion))
            except:
                project_stats.append((project.name, 0))
        
        project_stats.sort(key=lambda x: x[1], reverse=True)
        
        for i, (name, completion) in enumerate(project_stats[:5], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
            dashboard_content += f"{medal} **{name}**: {completion:.1f}%\n"
        
        dashboard_content += f"""
## 📈 AZIONI RAPIDE

- [📊 Monitora Tutti](command:monitor_all)
- [⚙️ Setup Tracker](command:setup_all)
- [🔄 Aggiorna Dashboard](command:refresh_dashboard)

---
*Dashboard generato automaticamente dal Universal Translator*
"""

        with open(dashboard_file, 'w', encoding='utf-8') as f:
            f.write(dashboard_content)
        
        print(f"📊 Dashboard globale salvato: {dashboard_file}")
        return dashboard_file

def main():
    """Interface principale Tracker Manager"""
    import sys
    
    manager = TrackerManager()
    
    print("🎛️ TRACKER MANAGER - Universal Translator")
    print("=" * 45)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup-all":
            manager.setup_all_projects()
        elif command == "monitor-all":
            manager.monitor_all_projects()
        elif command == "dashboard":
            manager.generate_global_dashboard()
        elif command.startswith("setup-"):
            project_name = command[6:]
            project_path = manager.translations_folder / project_name
            manager.setup_tracker_for_project(project_path)
        else:
            print(f"❌ Comando non riconosciuto: {command}")
    else:
        # Menu interattivo
        while True:
            print("\n📋 MENU TRACKER MANAGER")
            print("=" * 25)
            print("[1] ⚙️ Setup Tracker Tutti i Progetti")
            print("[2] 👁️ Monitora Tutti i Progetti")
            print("[3] 📊 Genera Dashboard Globale")
            print("[4] 🔍 Lista Progetti")
            print("[5] 🚪 Esci")
            
            choice = input("\nScegli opzione (1-5): ").strip()
            
            if choice == "1":
                manager.setup_all_projects()
            elif choice == "2":
                print("👁️ Avvio monitoraggio globale...")
                print("🛑 Premi Ctrl+C per fermare")
                manager.monitor_all_projects()
            elif choice == "3":
                dashboard_file = manager.generate_global_dashboard()
                print(f"✅ Dashboard creato: {dashboard_file}")
            elif choice == "4":
                projects = list(manager.translations_folder.glob("*/"))
                if projects:
                    print(f"\n📚 PROGETTI TROVATI ({len(projects)}):")
                    for i, project in enumerate(projects, 1):
                        print(f"  {i}. {project.name}")
                else:
                    print("❌ Nessun progetto trovato")
            elif choice == "5":
                print("👋 Arrivederci!")
                break
            else:
                print("❌ Scelta non valida")

if __name__ == "__main__":
    main()