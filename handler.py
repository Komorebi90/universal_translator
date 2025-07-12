# FILENAME: handler.py
#!/usr/bin/env python3
"""
Data Handler - Universal Light Novel Translator GUI
Gestisce interfaccia tra GUI e sistema backend
"""

import json
import time
from pathlib import Path
from datetime import datetime

class ProjectDataHandler:
    """Gestisce dati progetti per GUI"""
    
    def __init__(self, translations_folder="translations"):
        self.translations_folder = Path(translations_folder)
        self.translations_folder.mkdir(exist_ok=True)
        
        # Cache dati progetti
        self.projects_cache = {}
        self.last_update = 0
        self.cache_duration = 30  # secondi
    
    def get_all_projects(self, force_refresh=False):
        """Ottieni tutti i progetti con cache"""
        current_time = time.time()
        
        if (force_refresh or 
            current_time - self.last_update > self.cache_duration or
            not self.projects_cache):
            
            self._refresh_projects_cache()
            self.last_update = current_time
        
        return self.projects_cache
    
    def _refresh_projects_cache(self):
        """Aggiorna cache progetti"""
        self.projects_cache = {}
        
        if not self.translations_folder.exists():
            return
        
        for project_dir in self.translations_folder.iterdir():
            if not project_dir.is_dir():
                continue
            
            # Controlla se è un progetto valido
            template_file = project_dir / "tmpl.md"
            if not template_file.exists():
                # Fallback al nome vecchio
                template_file = project_dir / "template_traduzione.md"
                if not template_file.exists():
                    continue
            
            project_data = self._load_project_data(project_dir)
            if project_data:
                self.projects_cache[project_dir.name] = project_data
    
    def _load_project_data(self, project_dir):
        """Carica dati singolo progetto"""
        try:
            project_data = {
                'name': project_dir.name,
                'path': project_dir,
                'status': 'unknown',
                'completion': 0.0,
                'chapters_total': 0,
                'chapters_done': 0,
                'characters_total': 0,
                'characters_done': 0,
                'last_modified': 'N/A',
                'has_tracker': False,
                'template_file': None,
                'info': {}
            }
            
            # Trova file template (nome nuovo o vecchio)
            template_file = project_dir / "tmpl.md"
            if not template_file.exists():
                template_file = project_dir / "template_traduzione.md"
            
            if template_file.exists():
                project_data['template_file'] = template_file
                project_data['last_modified'] = datetime.fromtimestamp(
                    template_file.stat().st_mtime
                ).strftime('%d/%m/%Y %H:%M')
            
            # Carica dati Smart Tracker se disponibile
            tracker_file = project_dir / "trkr.json"
            if not tracker_file.exists():
                tracker_file = project_dir / "smart_tracker.json"
            
            if tracker_file.exists():
                project_data['has_tracker'] = True
                with open(tracker_file, 'r', encoding='utf-8') as f:
                    tracker_data = json.load(f)
                
                stats = tracker_data.get('statistics', {})
                project_data.update({
                    'completion': stats.get('completion_percentage', 0.0),
                    'chapters_total': tracker_data.get('project_info', {}).get('total_chapters', 0),
                    'chapters_done': stats.get('chapters_completed', 0),
                    'characters_total': stats.get('total_characters', 0),
                    'characters_done': stats.get('translated_characters', 0),
                })
                
                # Determina status
                completion = project_data['completion']
                if completion >= 100:
                    project_data['status'] = 'completed'
                elif completion >= 50:
                    project_data['status'] = 'in_progress'
                elif completion > 0:
                    project_data['status'] = 'started'
                else:
                    project_data['status'] = 'not_started'
            else:
                # Stima basica senza tracker
                project_data.update(self._estimate_progress_basic(project_dir))
            
            # Carica info progetto se disponibile
            info_file = project_dir / "info.md"
            if not info_file.exists():
                info_file = project_dir / "info_progetto.md"
            
            if info_file.exists():
                project_data['info'] = self._parse_info_file(info_file)
            
            return project_data
            
        except Exception as e:
            print(f"Errore caricamento progetto {project_dir.name}: {e}")
            return None
    
    def _estimate_progress_basic(self, project_dir):
        """Stima progresso senza tracker"""
        template_file = project_dir / "tmpl.md"
        if not template_file.exists():
            template_file = project_dir / "template_traduzione.md"
        
        if not template_file.exists():
            return {
                'status': 'error',
                'completion': 0.0,
                'chapters_total': 0,
                'chapters_done': 0
            }
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Conta capitoli (sezioni con ##)
            import re
            chapters = re.findall(r'^## ([^#\n]+)', content, re.MULTILINE)
            chapters_total = len(chapters)
            
            # Stima traduzioni (cerca pattern di traduzione vs placeholder)
            placeholders = len(re.findall(r'\[Inserisci qui', content, re.IGNORECASE))
            total_sections = content.count('### 🇮🇹')
            
            if total_sections > 0:
                translated_sections = total_sections - placeholders
                completion = (translated_sections / total_sections) * 100
            else:
                completion = 0
            
            status = 'completed' if completion >= 95 else 'in_progress' if completion > 0 else 'not_started'
            
            return {
                'status': status,
                'completion': completion,
                'chapters_total': chapters_total,
                'chapters_done': int(chapters_total * completion / 100)
            }
            
        except Exception:
            return {
                'status': 'error',
                'completion': 0.0,
                'chapters_total': 0,
                'chapters_done': 0
            }
    
    def _parse_info_file(self, info_file):
        """Estrae informazioni da file info"""
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            info = {}
            
            # Estrai informazioni base con regex
            import re
            
            title_match = re.search(r'Titolo:\*\*\s*(.+)', content)
            if title_match:
                info['title'] = title_match.group(1).strip()
            
            format_match = re.search(r'Formato:\*\*\s*(.+)', content)
            if format_match:
                info['format'] = format_match.group(1).strip()
            
            date_match = re.search(r'Data creazione:\*\*\s*(.+)', content)
            if date_match:
                info['created'] = date_match.group(1).strip()
            
            return info
            
        except Exception:
            return {}
    
    def get_project_chapters(self, project_name):
        """Ottieni lista capitoli di un progetto"""
        project_data = self.projects_cache.get(project_name)
        if not project_data or not project_data['template_file']:
            return []
        
        try:
            with open(project_data['template_file'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            
            # Trova tutti i capitoli
            chapters = []
            chapter_pattern = r'^## ([^#\n]+)\n(.*?)(?=^##|\Z)'
            
            for match in re.finditer(chapter_pattern, content, re.MULTILINE | re.DOTALL):
                title = match.group(1).strip()
                content_text = match.group(2)
                
                # Analizza progresso capitolo
                total_sections = content_text.count('### 🇮🇹')
                placeholders = len(re.findall(r'\[Inserisci qui', content_text, re.IGNORECASE))
                
                if total_sections > 0:
                    progress = ((total_sections - placeholders) / total_sections) * 100
                else:
                    progress = 0
                
                chapters.append({
                    'title': title,
                    'progress': progress,
                    'status': 'completed' if progress >= 95 else 'in_progress' if progress > 0 else 'not_started',
                    'sections_total': total_sections,
                    'sections_done': total_sections - placeholders
                })
            
            return chapters
            
        except Exception as e:
            print(f"Errore caricamento capitoli {project_name}: {e}")
            return []
    
    def get_global_stats(self):
        """Calcola statistiche globali"""
        projects = self.get_all_projects()
        
        if not projects:
            return {
                'total_projects': 0,
                'completed_projects': 0,
                'in_progress_projects': 0,
                'avg_completion': 0.0,
                'total_characters': 0,
                'translated_characters': 0
            }
        
        total_projects = len(projects)
        completed = sum(1 for p in projects.values() if p['status'] == 'completed')
        in_progress = sum(1 for p in projects.values() if p['status'] in ['started', 'in_progress'])
        
        total_completion = sum(p['completion'] for p in projects.values())
        avg_completion = total_completion / total_projects if total_projects > 0 else 0
        
        total_chars = sum(p['characters_total'] for p in projects.values())
        translated_chars = sum(p['characters_done'] for p in projects.values())
        
        return {
            'total_projects': total_projects,
            'completed_projects': completed,
            'in_progress_projects': in_progress,
            'not_started_projects': total_projects - completed - in_progress,
            'avg_completion': avg_completion,
            'total_characters': total_chars,
            'translated_characters': translated_chars
        }
    
    def setup_tracker_for_project(self, project_name):
        """Setup Smart Tracker per progetto"""
        project_data = self.projects_cache.get(project_name)
        if not project_data:
            return False
        
        try:
            # Usa tracker_manager per setup
            from tracker_manager import TrackerManager
            manager = TrackerManager()
            success = manager.setup_tracker_for_project(project_data['path'])
            
            # Aggiorna cache
            if success:
                self._refresh_projects_cache()
            
            return success
            
        except Exception as e:
            print(f"Errore setup tracker {project_name}: {e}")
            return False
    
    def update_tracker_for_project(self, project_name):
        """Aggiorna tracker di un progetto"""
        project_data = self.projects_cache.get(project_name)
        if not project_data or not project_data['has_tracker']:
            return False
        
        try:
            from smart_tracker_system import SmartTracker
            tracker = SmartTracker(project_data['path'])
            completion = tracker.update_all()
            
            # Aggiorna cache per questo progetto
            self._refresh_single_project(project_name)
            
            return completion
            
        except Exception as e:
            print(f"Errore aggiornamento tracker {project_name}: {e}")
            return False
    
    def _refresh_single_project(self, project_name):
        """Aggiorna cache di un singolo progetto"""
        project_data = self.projects_cache.get(project_name)
        if project_data:
            updated_data = self._load_project_data(project_data['path'])
            if updated_data:
                self.projects_cache[project_name] = updated_data