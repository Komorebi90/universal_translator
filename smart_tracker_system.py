#!/usr/bin/env python3
"""
Smart Tracker System - Monitoraggio Automatico Progresso
Rileva automaticamente traduzioni completate e aggiorna statistiche
"""

import re
import json
import time
from pathlib import Path
from datetime import datetime
import hashlib

class SmartTracker:
    def __init__(self, project_folder):
        self.project_folder = Path(project_folder)
        self.tracker_file = self.project_folder / "smart_tracker.json"
        self.template_file = self.project_folder / "template_traduzione.md"
        self.stats_file = self.project_folder / "statistiche_live.md"
        
        # Carica o inizializza dati tracker
        self.data = self.load_tracker_data()
    
    def load_tracker_data(self):
        """Carica dati tracker esistenti o inizializza"""
        if self.tracker_file.exists():
            with open(self.tracker_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "project_info": {
                    "created": datetime.now().isoformat(),
                    "last_update": datetime.now().isoformat(),
                    "total_chapters": 0,
                    "project_name": self.project_folder.name
                },
                "chapters": {},
                "statistics": {
                    "total_characters": 0,
                    "total_words": 0,
                    "translated_characters": 0,
                    "translated_words": 0,
                    "completion_percentage": 0.0,
                    "estimated_hours_total": 0,
                    "estimated_hours_remaining": 0,
                    "translation_speed_chars_per_minute": 150  # Default
                },
                "sessions": []
            }
    
    def save_tracker_data(self):
        """Salva dati tracker"""
        self.data["project_info"]["last_update"] = datetime.now().isoformat()
        with open(self.tracker_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def scan_template_file(self):
        """Scansiona template per rilevare traduzioni"""
        if not self.template_file.exists():
            return
        
        with open(self.template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern per trovare sezioni capitoli
        chapter_pattern = r'## ([^#\n]+)\n.*?### 📖 TESTO ORIGINALE.*?```\n(.*?)```.*?### 🇮🇹 TRADUZIONE ITALIANA\n(.*?)(?=---|\n##|\Z)'
        
        chapters_found = re.findall(chapter_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for title, original_text, translated_text in chapters_found:
            chapter_id = self.generate_chapter_id(title.strip())
            
            # Analizza stato traduzione
            status = self.analyze_translation_status(original_text, translated_text)
            
            # Aggiorna dati capitolo
            self.update_chapter_data(chapter_id, title.strip(), original_text, translated_text, status)
    
    def generate_chapter_id(self, title):
        """Genera ID unico per capitolo"""
        # Usa hash del titolo per ID consistente
        return hashlib.md5(title.encode()).hexdigest()[:8]
    
    def analyze_translation_status(self, original_text, translated_text):
        """Analizza automaticamente lo stato della traduzione"""
        original_chars = len(original_text.strip())
        translated_chars = len(translated_text.strip())
        
        # Rimuovi placeholder comuni
        placeholders = [
            "*[Inserisci qui la tua traduzione]*",
            "[La tua traduzione]",
            "[TRADUZIONE DA FARE]",
            "[TODO]"
        ]
        
        cleaned_translation = translated_text
        for placeholder in placeholders:
            cleaned_translation = cleaned_translation.replace(placeholder, "")
        
        actual_translated_chars = len(cleaned_translation.strip())
        
        # Determina stato basato su percentuale completamento
        if actual_translated_chars < 50:
            return "⏳ Da fare"
        elif actual_translated_chars < original_chars * 0.3:
            return "🔄 Iniziato"
        elif actual_translated_chars < original_chars * 0.7:
            return "🔄 In corso"
        elif actual_translated_chars < original_chars * 0.95:
            return "🔍 Quasi completo"
        else:
            return "✅ Completato"
    
    def update_chapter_data(self, chapter_id, title, original_text, translated_text, status):
        """Aggiorna dati di un capitolo"""
        original_chars = len(original_text.strip())
        original_words = len(original_text.split())
        
        # Calcola caratteri/parole tradotte effettive
        cleaned_translation = translated_text
        placeholders = [
            "*[Inserisci qui la tua traduzione]*",
            "[La tua traduzione]", 
            "[TRADUZIONE DA FARE]",
            "[TODO]"
        ]
        for placeholder in placeholders:
            cleaned_translation = cleaned_translation.replace(placeholder, "")
        
        translated_chars = len(cleaned_translation.strip())
        translated_words = len(cleaned_translation.split())
        
        completion_percent = min(100, (translated_chars / original_chars * 100)) if original_chars > 0 else 0
        
        self.data["chapters"][chapter_id] = {
            "title": title,
            "original_characters": original_chars,
            "original_words": original_words,
            "translated_characters": translated_chars,
            "translated_words": translated_words,
            "status": status,
            "completion_percentage": round(completion_percent, 1),
            "last_modified": datetime.now().isoformat(),
            "estimated_time_minutes": original_chars // self.data["statistics"]["translation_speed_chars_per_minute"]
        }
    
    def calculate_global_statistics(self):
        """Calcola statistiche globali del progetto"""
        total_original_chars = sum(ch["original_characters"] for ch in self.data["chapters"].values())
        total_original_words = sum(ch["original_words"] for ch in self.data["chapters"].values())
        total_translated_chars = sum(ch["translated_characters"] for ch in self.data["chapters"].values())
        total_translated_words = sum(ch["translated_words"] for ch in self.data["chapters"].values())
        
        completion_percentage = (total_translated_chars / total_original_chars * 100) if total_original_chars > 0 else 0
        
        # Calcola velocità traduzione basata su sessioni recenti
        speed = self.data["statistics"]["translation_speed_chars_per_minute"]
        
        estimated_total_hours = total_original_chars / (speed * 60)
        estimated_remaining_hours = (total_original_chars - total_translated_chars) / (speed * 60)
        
        # Aggiorna statistiche
        self.data["statistics"].update({
            "total_characters": total_original_chars,
            "total_words": total_original_words,
            "translated_characters": total_translated_chars,
            "translated_words": total_translated_words,
            "completion_percentage": round(completion_percentage, 1),
            "estimated_hours_total": round(estimated_total_hours, 1),
            "estimated_hours_remaining": round(estimated_remaining_hours, 1),
            "chapters_completed": len([ch for ch in self.data["chapters"].values() if ch["status"] == "✅ Completato"]),
            "chapters_in_progress": len([ch for ch in self.data["chapters"].values() if "🔄" in ch["status"]]),
            "chapters_todo": len([ch for ch in self.data["chapters"].values() if ch["status"] == "⏳ Da fare"])
        })
        
        self.data["project_info"]["total_chapters"] = len(self.data["chapters"])
    
    def generate_live_report(self):
        """Genera report live in markdown"""
        self.calculate_global_statistics()
        stats = self.data["statistics"]
        project_info = self.data["project_info"]
        
        report = f"""# 📊 STATISTICHE LIVE - {project_info["project_name"]}

## 🎯 PANORAMICA GENERALE

| Metrica | Valore | Progresso |
|---------|--------|-----------|
| **Completamento** | {stats["completion_percentage"]:.1f}% | {'█' * int(stats["completion_percentage"] // 10)}{'░' * (10 - int(stats["completion_percentage"] // 10))} |
| **Caratteri** | {stats["translated_characters"]:,} / {stats["total_characters"]:,} | {stats["completion_percentage"]:.1f}% |
| **Parole** | {stats["translated_words"]:,} / {stats["total_words"]:,} | {(stats["translated_words"]/stats["total_words"]*100) if stats["total_words"] > 0 else 0:.1f}% |
| **Capitoli Completati** | {stats["chapters_completed"]} / {project_info["total_chapters"]} | {(stats["chapters_completed"]/project_info["total_chapters"]*100) if project_info["total_chapters"] > 0 else 0:.1f}% |

## ⏱️ STIME TEMPORALI

| Tempo | Valore |
|--------|--------|
| **Totale Stimato** | {stats["estimated_hours_total"]:.1f} ore |
| **Rimanente** | {stats["estimated_hours_remaining"]:.1f} ore |
| **Velocità Media** | {stats["translation_speed_chars_per_minute"]} caratteri/minuto |

## 📚 DETTAGLIO CAPITOLI

| Capitolo | Stato | Completamento | Caratteri | Tempo Stimato |
|----------|--------|---------------|-----------|---------------|
"""

        for chapter_id, chapter in self.data["chapters"].items():
            progress_bar = '█' * int(chapter["completion_percentage"] // 10) + '░' * (10 - int(chapter["completion_percentage"] // 10))
            report += f"| {chapter['title'][:20]}... | {chapter['status']} | {chapter['completion_percentage']:.1f}% {progress_bar} | {chapter['translated_characters']:,}/{chapter['original_characters']:,} | {chapter['estimated_time_minutes']} min |\n"

        report += f"""
## 📈 DISTRIBUZIONE STATI

- ✅ **Completati**: {stats["chapters_completed"]} capitoli
- 🔄 **In Corso**: {stats["chapters_in_progress"]} capitoli  
- ⏳ **Da Fare**: {stats["chapters_todo"]} capitoli

## 🕒 ULTIMO AGGIORNAMENTO

**{datetime.fromisoformat(project_info["last_update"]).strftime('%d/%m/%Y alle %H:%M')}**

---
*Statistiche generate automaticamente dal Smart Tracker*
"""

        # Salva report
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def start_translation_session(self):
        """Inizia una sessione di traduzione"""
        session = {
            "start_time": datetime.now().isoformat(),
            "start_chars": self.data["statistics"]["translated_characters"],
            "end_time": None,
            "end_chars": None,
            "duration_minutes": None,
            "chars_translated": None,
            "speed_chars_per_minute": None
        }
        
        self.data["sessions"].append(session)
        self.save_tracker_data()
        print(f"📝 Sessione traduzione iniziata alle {datetime.now().strftime('%H:%M')}")
    
    def end_translation_session(self):
        """Termina sessione di traduzione e calcola statistiche"""
        if not self.data["sessions"]:
            return
        
        # Aggiorna dati prima di terminare
        self.scan_template_file()
        self.calculate_global_statistics()
        
        last_session = self.data["sessions"][-1]
        if last_session["end_time"] is None:
            end_time = datetime.now()
            start_time = datetime.fromisoformat(last_session["start_time"])
            
            duration = (end_time - start_time).total_seconds() / 60  # minuti
            chars_translated = self.data["statistics"]["translated_characters"] - last_session["start_chars"]
            speed = chars_translated / duration if duration > 0 else 0
            
            last_session.update({
                "end_time": end_time.isoformat(),
                "end_chars": self.data["statistics"]["translated_characters"],
                "duration_minutes": round(duration, 1),
                "chars_translated": chars_translated,
                "speed_chars_per_minute": round(speed, 1)
            })
            
            # Aggiorna velocità media globale
            if speed > 0:
                speeds = [s["speed_chars_per_minute"] for s in self.data["sessions"] if s.get("speed_chars_per_minute", 0) > 0]
                if speeds:
                    self.data["statistics"]["translation_speed_chars_per_minute"] = round(sum(speeds) / len(speeds), 1)
            
            self.save_tracker_data()
            print(f"⏹️ Sessione terminata: {chars_translated} caratteri in {duration:.1f} minuti ({speed:.1f} char/min)")
    
    def update_all(self):
        """Aggiornamento completo del tracker"""
        print("🔄 Aggiornamento tracker automatico...")
        
        # Scansiona template per cambiamenti
        self.scan_template_file()
        
        # Calcola statistiche globali
        self.calculate_global_statistics()
        
        # Genera report live
        self.generate_live_report()
        
        # Salva tutto
        self.save_tracker_data()
        
        print(f"✅ Tracker aggiornato: {self.data['statistics']['completion_percentage']:.1f}% completato")
        return self.data["statistics"]["completion_percentage"]

def monitor_project(project_folder, auto_update_seconds=30):
    """Monitora progetto e aggiorna automaticamente"""
    import time
    
    tracker = SmartTracker(project_folder)
    print(f"👁️ Monitoraggio automatico progetto: {project_folder}")
    print(f"🔄 Aggiornamento ogni {auto_update_seconds} secondi")
    print("🛑 Premi Ctrl+C per fermare")
    
    try:
        while True:
            completion = tracker.update_all()
            print(f"📊 Progresso: {completion:.1f}% - {time.strftime('%H:%M:%S')}")
            
            if completion >= 100:
                print("🎉 PROGETTO COMPLETATO!")
                break
                
            time.sleep(auto_update_seconds)
            
    except KeyboardInterrupt:
        print("\n⏹️ Monitoraggio fermato dall'utente")
    
    return tracker

def main():
    """Interfaccia principale Smart Tracker"""
    import sys
    
    if len(sys.argv) < 2:
        print("📊 SMART TRACKER - Monitoraggio Automatico")
        print("=" * 40)
        print("Utilizzo:")
        print("  python smart_tracker.py <cartella_progetto>")
        print("  python smart_tracker.py <cartella_progetto> --monitor")
        print("  python smart_tracker.py <cartella_progetto> --session-start")
        print("  python smart_tracker.py <cartella_progetto> --session-end")
        return
    
    project_folder = sys.argv[1]
    
    if not Path(project_folder).exists():
        print(f"❌ Cartella progetto non trovata: {project_folder}")
        return
    
    tracker = SmartTracker(project_folder)
    
    if len(sys.argv) > 2:
        command = sys.argv[2]
        
        if command == "--monitor":
            monitor_project(project_folder)
        elif command == "--session-start":
            tracker.start_translation_session()
        elif command == "--session-end":
            tracker.end_translation_session()
        else:
            print(f"❌ Comando non riconosciuto: {command}")
    else:
        # Aggiornamento singolo
        tracker.update_all()
        print(f"📁 Report salvato in: {tracker.stats_file}")

if __name__ == "__main__":
    main()