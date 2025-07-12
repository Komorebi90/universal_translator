# FILENAME: teditor.py
#!/usr/bin/env python3
"""
Translation Editor GUI - Universal Light Novel Translator
Editor a doppia finestra per traduzione (originale | traduzione)
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import re
from pathlib import Path

from styles import GUIStyles
from handler import ProjectDataHandler
from autosave import AutoSaveManager, RecoveryManager

class TranslationEditorGUI:
    """GUI Editor traduzione a doppia finestra"""
    
    def __init__(self, project_name, parent=None):
        self.parent = parent
        self.project_name = project_name
        self.root = tk.Toplevel(parent.root if parent else None) if parent else tk.Tk()
        self.styles = GUIStyles()
        self.handler = ProjectDataHandler()
        
        print(f"🎯 Inizializzando editor per progetto: {project_name}")
        
        # Configurazione finestra
        self.styles.configure_window(self.root, f"Editor Traduzione - {project_name}")
        self.root.geometry("1400x800")
        
        # Dati progetto
        self.project_data = None
        self.template_content = ""
        self.chapters = []
        self.current_chapter = 0
        self.is_modified = False
        
        # Componenti auto-save
        self.auto_save_manager = None
        self.recovery_manager = None
        
        # Setup in ordine
        print("🔄 Caricando progetto...")
        self.load_project()
        
        print("🔄 Configurando UI...")
        self.setup_ui()
        
        print("🔄 Configurando auto-save...")
        self.setup_auto_save()
        
        print("🔄 Controllando recovery...")
        self.check_recovery()
        
        print("🔄 Caricando capitolo corrente...")
        self.load_current_chapter()
        
        print("✅ Editor inizializzato!")
        
        # Debug info
        print(f"📊 Template content: {len(self.template_content)} caratteri")
        print(f"📚 Capitoli trovati: {len(self.chapters)}")
        if self.chapters:
            print(f"📖 Primo capitolo: {self.chapters[0]['title'][:50]}...")
    
    def load_project(self):
        """Carica dati progetto"""
        projects = self.handler.get_all_projects()
        self.project_data = projects.get(self.project_name)
        
        if not self.project_data:
            messagebox.showerror("Errore", f"Progetto {self.project_name} non trovato")
            self.root.destroy()
            return
        
        # Carica template content
        template_file = self.project_data['template_file']
        if template_file and template_file.exists():
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    self.template_content = f.read()
                print(f"✅ Template caricato: {len(self.template_content)} caratteri")
            except Exception as e:
                print(f"❌ Errore lettura template: {e}")
                messagebox.showerror("Errore", f"Impossibile leggere template: {e}")
                return
        else:
            print(f"❌ Template file non trovato: {template_file}")
            messagebox.showerror("Errore", f"File template non trovato: {template_file}")
            return
        
        # Estrai capitoli
        self.extract_chapters()
        
        if not self.chapters:
            print("❌ Nessun capitolo estratto, provo metodo alternativo")
            self.extract_chapters_fallback()
    
    def extract_chapters(self):
        """Estrae capitoli dal template"""
        print("🔍 Estraendo capitoli dal template...")
        
        # Pattern più flessibile per trovare capitoli
        patterns = [
            # Pattern principale: ## TITOLO
            r'^## ([^#\n]+)\n(.*?)(?=^##|\Z)',
            # Pattern alternativo: # TITOLO  
            r'^# ([^#\n]+)\n(.*?)(?=^#|\Z)',
            # Pattern backup: qualsiasi header con contenuto
            r'^(#{1,3}) ([^#\n]+)\n(.*?)(?=^#{1,3}|\Z)'
        ]
        
        chapters = []
        
        for i, pattern in enumerate(patterns):
            print(f"Tentativo pattern {i+1}...")
            matches = list(re.finditer(pattern, self.template_content, re.MULTILINE | re.DOTALL))
            
            if matches:
                print(f"✅ Trovati {len(matches)} capitoli con pattern {i+1}")
                
                for j, match in enumerate(matches):
                    if len(match.groups()) == 2:
                        title, content = match.groups()
                    else:
                        # Pattern con 3 gruppi (include #)
                        _, title, content = match.groups()
                    
                    title = title.strip()
                    content = content.strip()
                    
                    # Salta capitoli troppo corti (probabilmente header)
                    if len(content) < 100:
                        continue
                    
                    # Estrai sezioni originale e traduzione
                    sections = self.parse_chapter_sections(content)
                    
                    # Se non trova sezioni, crea una sezione unica
                    if not sections:
                        sections = [{
                            'original_header': 'Testo Completo',
                            'original_text': content[:2000] + "..." if len(content) > 2000 else content,
                            'translation_header': 'Traduzione Completa',
                            'translation_text': '*[Inserisci qui la tua traduzione]*',
                            'is_placeholder': True
                        }]
                    
                    chapters.append({
                        'title': title,
                        'content': content,
                        'sections': sections,
                        'start_pos': match.start(),
                        'end_pos': match.end()
                    })
                
                if chapters:
                    break  # Se trova capitoli, ferma i tentativi
        
        self.chapters = chapters
        print(f"📚 Capitoli estratti: {len(self.chapters)}")
        
        if self.chapters:
            for i, ch in enumerate(self.chapters):
                print(f"  {i+1}. {ch['title'][:50]}... ({len(ch['sections'])} sezioni)")
    
    def extract_chapters_fallback(self):
        """Metodo fallback se estrazione normale fallisce"""
        print("🆘 Usando metodo fallback...")
        
        # Dividi per paragrafi e crea capitoli artificiali
        paragraphs = [p.strip() for p in self.template_content.split('\n\n') if p.strip()]
        
        if not paragraphs:
            print("❌ Nessun paragrafo trovato")
            return
        
        # Raggruppa paragrafi in "capitoli" di ~2000 caratteri
        current_text = ""
        chapter_num = 1
        chapters = []
        
        for paragraph in paragraphs:
            if len(current_text) + len(paragraph) > 2000 and current_text:
                # Crea capitolo
                sections = [{
                    'original_header': 'Testo Completo',
                    'original_text': current_text,
                    'translation_header': 'Traduzione Completa', 
                    'translation_text': '*[Inserisci qui la tua traduzione]*',
                    'is_placeholder': True
                }]
                
                chapters.append({
                    'title': f"Sezione {chapter_num}",
                    'content': current_text,
                    'sections': sections,
                    'start_pos': 0,
                    'end_pos': len(current_text)
                })
                
                chapter_num += 1
                current_text = paragraph
            else:
                current_text += "\n\n" + paragraph if current_text else paragraph
        
        # Ultimo capitolo
        if current_text:
            sections = [{
                'original_header': 'Testo Completo',
                'original_text': current_text,
                'translation_header': 'Traduzione Completa',
                'translation_text': '*[Inserisci qui la tua traduzione]*', 
                'is_placeholder': True
            }]
            
            chapters.append({
                'title': f"Sezione {chapter_num}",
                'content': current_text,
                'sections': sections,
                'start_pos': 0,
                'end_pos': len(current_text)
            })
        
        self.chapters = chapters
        print(f"🔄 Capitoli fallback creati: {len(self.chapters)}")
    
    def parse_chapter_sections(self, chapter_content):
        """Estrae sezioni originale e traduzione da un capitolo"""
        sections = []
        
        # Pattern per sezioni
        section_pattern = r'### 📖 (.*?TESTO ORIGINALE.*?)\n```\n(.*?)\n```\n\n### 🇮🇹 (.*?TRADUZIONE.*?)\n(.*?)(?=---|\n###|\Z)'
        
        for match in re.finditer(section_pattern, chapter_content, re.DOTALL):
            original_header = match.group(1).strip()
            original_text = match.group(2).strip()
            translation_header = match.group(3).strip()
            translation_text = match.group(4).strip()
            
            sections.append({
                'original_header': original_header,
                'original_text': original_text,
                'translation_header': translation_header,
                'translation_text': translation_text,
                'is_placeholder': '[Inserisci qui' in translation_text.lower()
            })
        
        return sections
    
    def setup_ui(self):
        """Setup interface utente"""
        # Main container
        main_frame = self.styles.create_frame(self.root, 'main')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Header con navigation
        self.create_header(main_frame)
        
        # Pannello principale doppio
        self.create_split_panel(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Crea header con navigazione"""
        header_frame = self.styles.create_frame(parent, 'secondary')
        header_frame.pack(fill='x', pady=(0, 5))
        
        # Info progetto
        info_frame = self.styles.create_frame(header_frame, 'secondary')
        info_frame.pack(side='left', fill='x', expand=True)
        
        project_label = self.styles.create_label(
            info_frame,
            f"[BOOK] {self.project_name}",
            'header'
        )
        project_label.pack(side='left')
        
        # Navigation controls
        nav_frame = self.styles.create_frame(header_frame, 'secondary')
        nav_frame.pack(side='right')
        
        # Chapter selector
        self.styles.create_label(nav_frame, "Capitolo:", 'normal').pack(side='left', padx=(0, 5))
        
        self.chapter_var = tk.StringVar()
        chapter_combo = ttk.Combobox(
            nav_frame,
            textvariable=self.chapter_var,
            values=[f"{i+1}. {ch['title']}" for i, ch in enumerate(self.chapters)],
            state='readonly',
            width=30
        )
        chapter_combo.pack(side='left', padx=(0, 10))
        chapter_combo.bind('<<ComboboxSelected>>', self.on_chapter_change)
        self.chapter_combo = chapter_combo
        
        # Navigation buttons
        nav_buttons = [
            ("< Precedente", self.prev_chapter, 'normal'),
            ("> Successivo", self.next_chapter, 'normal'),
            ("[SAVE] Salva", self.manual_save, 'primary'),
            ("[OK] Completa", self.mark_complete, 'success'),
            ("[UPDATE] Aggiorna Tracker", self.update_tracker, 'normal')
        ]
        
        for text, command, style in nav_buttons:
            btn = self.styles.create_button(nav_frame, text, command, style)
            btn.pack(side='left', padx=(5, 0))
    
    def create_split_panel(self, parent):
        """Crea pannello doppio originale|traduzione"""
        # Paned window per split resizable
        paned = ttk.PanedWindow(parent, orient='horizontal')
        paned.pack(fill='both', expand=True, pady=(5, 0))
        
        # Frame sinistro - Originale
        left_frame = self.styles.create_frame(paned, 'main')
        paned.add(left_frame, weight=1)
        
        # Header originale
        orig_header = self.styles.create_frame(left_frame, 'secondary')
        orig_header.pack(fill='x', pady=(0, 5))
        
        self.styles.create_label(
            orig_header,
            "[READ] TESTO ORIGINALE",
            'header'
        ).pack(side='left')
        
        # Sezione navigation originale
        self.orig_section_var = tk.StringVar()
        self.orig_section_combo = ttk.Combobox(
            orig_header,
            textvariable=self.orig_section_var,
            state='readonly',
            width=15
        )
        self.orig_section_combo.pack(side='right')
        self.orig_section_combo.bind('<<ComboboxSelected>>', self.on_section_change)
        
        # Text widget originale (solo lettura)
        self.original_text = self.styles.create_text(left_frame, state='disabled')
        self.original_text.pack(fill='both', expand=True)
        
        # Frame destro - Traduzione
        right_frame = self.styles.create_frame(paned, 'main')
        paned.add(right_frame, weight=1)
        
        # Header traduzione
        trans_header = self.styles.create_frame(right_frame, 'secondary')
        trans_header.pack(fill='x', pady=(0, 5))
        
        self.styles.create_label(
            trans_header,
            "[IT] TRADUZIONE ITALIANA",
            'header'
        ).pack(side='left')
        
        # Progress indicator
        self.progress_label = self.styles.create_label(
            trans_header,
            "0%",
            'small'
        )
        self.progress_label.pack(side='right')
        
        # Text widget traduzione (editabile)
        self.translation_text = self.styles.create_text(right_frame, state='normal')
        self.translation_text.pack(fill='both', expand=True)
        self.translation_text.bind('<KeyRelease>', self.on_text_change)
        self.translation_text.bind('<Button-1>', self.on_text_change)
        
        # Sincronizza scrolling DOPO aver creato i widget
        self.sync_scrollbars()
        
        self.paned = paned
    
    def sync_scrollbars(self):
        """Sincronizza scrolling tra i due pannelli"""
        def sync_original_to_translation(*args):
            """Sincronizza scroll da originale a traduzione"""
            if len(args) >= 2:
                # args[0] è la posizione top, args[1] è bottom
                self.translation_text.yview_moveto(float(args[0]))
        
        def sync_translation_to_original(*args):
            """Sincronizza scroll da traduzione a originale"""
            if len(args) >= 2:
                # args[0] è la posizione top, args[1] è bottom  
                self.original_text.yview_moveto(float(args[0]))
        
        # Configura scrollbars separate per evitare ricorsioni
        v_scroll_orig = ttk.Scrollbar(self.original_text.master, orient='vertical')
        v_scroll_trans = ttk.Scrollbar(self.translation_text.master, orient='vertical')
        
        # Configura scroll originale
        self.original_text.configure(yscrollcommand=lambda *args: [
            v_scroll_orig.set(*args),
            sync_original_to_translation(*args)
        ])
        v_scroll_orig.configure(command=self.original_text.yview)
        
        # Configura scroll traduzione
        self.translation_text.configure(yscrollcommand=lambda *args: [
            v_scroll_trans.set(*args), 
            sync_translation_to_original(*args)
        ])
        v_scroll_trans.configure(command=self.translation_text.yview)
        
        # Pack scrollbars
        v_scroll_orig.pack(side='right', fill='y')
        v_scroll_trans.pack(side='right', fill='y')
    
    def create_status_bar(self, parent):
        """Crea status bar"""
        status_frame = self.styles.create_frame(parent, 'secondary')
        status_frame.pack(fill='x', pady=(5, 0))
        
        # Status principale
        self.status_label = self.styles.create_label(
            status_frame,
            "Pronto",
            'small'
        )
        self.status_label.pack(side='left')
        
        # Indicatori auto-save
        self.auto_save_label = self.styles.create_label(
            status_frame,
            "[SAVE] Auto-save: ON",
            'small'
        )
        self.auto_save_label.pack(side='right', padx=(10, 0))
        
        # Progress bar capitolo
        self.chapter_progress = self.styles.create_progress_bar(status_frame, 200)
        self.chapter_progress.pack(side='right', padx=(10, 0))
    
    def setup_auto_save(self):
        """Setup auto-save manager"""
        if self.project_data and self.project_data['template_file']:
            self.auto_save_manager = AutoSaveManager(
                self.project_data['path'],
                self.project_data['template_file']
            )
            
            self.recovery_manager = RecoveryManager(self.project_data['path'])
            
            # Avvia monitoring
            self.auto_save_manager.start_monitoring(self.get_current_content)
    
    def check_recovery(self):
        """Controlla se esistono dati di recovery"""
        if self.recovery_manager and self.recovery_manager.has_recovery_data():
            recovery_data = self.recovery_manager.load_recovery_data()
            
            if recovery_data:
                response = messagebox.askyesno(
                    "Ripristino",
                    "Trovati dati di ripristino da una sessione precedente.\n"
                    "Vuoi ripristinare il lavoro non salvato?"
                )
                
                if response:
                    self.template_content = recovery_data['content']
                    self.extract_chapters()
                    
                    # Ripristina posizione cursore se disponibile
                    if recovery_data.get('cursor_position'):
                        # TODO: Implementare ripristino posizione cursore
                        pass
    
    def load_current_chapter(self):
        """Carica capitolo corrente nell'editor"""
        if not self.chapters:
            print("❌ Nessun capitolo disponibile")
            messagebox.showwarning("Attenzione", "Nessun capitolo trovato nel progetto")
            return
        
        chapter = self.chapters[self.current_chapter]
        print(f"📖 Caricando capitolo: {chapter['title']}")
        
        # Aggiorna combo
        self.chapter_var.set(f"{self.current_chapter + 1}. {chapter['title']}")
        
        # Aggiorna sezioni combo
        sections = chapter['sections']
        if sections:
            section_values = [f"Sezione {i+1}" for i in range(len(sections))]
            self.orig_section_combo['values'] = section_values
            self.orig_section_combo.set("Sezione 1")
            print(f"📝 Sezioni disponibili: {len(sections)}")
        else:
            print("⚠️ Nessuna sezione trovata")
            self.orig_section_combo['values'] = ["Nessuna sezione"]
            self.orig_section_combo.set("Nessuna sezione")
        
        # Carica prima sezione
        if sections:
            self.load_section(0)
        else:
            # Fallback: mostra tutto il contenuto
            self.show_full_chapter_content(chapter)
        
        # Aggiorna progress
        self.update_chapter_progress()
    
    def show_full_chapter_content(self, chapter):
        """Mostra contenuto completo del capitolo se le sezioni non sono disponibili"""
        print("🔄 Mostrando contenuto completo del capitolo")
        
        # Carica testo originale completo
        self.original_text.config(state='normal')
        self.original_text.delete('1.0', 'end')
        self.original_text.insert('1.0', chapter['content'])
        self.original_text.config(state='disabled')
        
        # Carica traduzione vuota
        self.translation_text.delete('1.0', 'end')
        placeholder = "*[Inserisci qui la tua traduzione per tutto il capitolo]*"
        self.translation_text.insert('1.0', placeholder)
        
        # Evidenzia placeholder
        self.translation_text.tag_add('placeholder', '1.0', 'end')
        self.translation_text.tag_config('placeholder', foreground='#6c757d', font=(self.styles.font_family, 10, 'italic'))
    
    def load_section(self, section_index):
        """Carica sezione specifica"""
        if not self.chapters or section_index >= len(self.chapters[self.current_chapter]['sections']):
            print(f"❌ Sezione {section_index} non valida")
            return
        
        section = self.chapters[self.current_chapter]['sections'][section_index]
        print(f"📄 Caricando sezione {section_index + 1}")
        
        # Carica testo originale
        self.original_text.config(state='normal')
        self.original_text.delete('1.0', 'end')
        
        original_text = section.get('original_text', '')
        if not original_text:
            original_text = "Testo originale non disponibile"
        
        self.original_text.insert('1.0', original_text)
        self.original_text.config(state='disabled')
        
        # Carica traduzione
        self.translation_text.delete('1.0', 'end')
        translation = section.get('translation_text', '*[Inserisci qui la tua traduzione]*')
        
        # Evidenzia placeholder
        if section.get('is_placeholder', True):
            self.translation_text.insert('1.0', translation)
            self.translation_text.tag_add('placeholder', '1.0', 'end')
            self.translation_text.tag_config('placeholder', foreground='#6c757d', font=(self.styles.font_family, 10, 'italic'))
        else:
            self.translation_text.insert('1.0', translation)
        
        print(f"✅ Sezione caricata: {len(original_text)} caratteri originali")
    
    def on_chapter_change(self, event=None):
        """Gestisce cambio capitolo"""
        selection = self.chapter_combo.get()
        if selection:
            chapter_num = int(selection.split('.')[0]) - 1
            if 0 <= chapter_num < len(self.chapters):
                self.current_chapter = chapter_num
                self.load_current_chapter()
    
    def on_section_change(self, event=None):
        """Gestisce cambio sezione"""
        selection = self.orig_section_combo.get()
        if selection:
            section_num = int(selection.split()[-1]) - 1
            self.load_section(section_num)
    
    def on_text_change(self, event=None):
        """Gestisce modifiche al testo"""
        self.is_modified = True
        self.update_chapter_progress()
        
        # Salva stato recovery
        if self.recovery_manager:
            self.recovery_manager.save_recovery_state(
                self.get_current_content(),
                self.translation_text.index(tk.INSERT)
            )
    
    def get_current_content(self):
        """Ottieni contenuto corrente completo"""
        # Aggiorna la sezione corrente nel template
        current_section_index = self.orig_section_combo.current()
        if current_section_index >= 0 and self.chapters:
            current_translation = self.translation_text.get('1.0', 'end-1c')
            
            # Aggiorna la sezione nel chapters
            chapter = self.chapters[self.current_chapter]
            if current_section_index < len(chapter['sections']):
                chapter['sections'][current_section_index]['translation_text'] = current_translation
                chapter['sections'][current_section_index]['is_placeholder'] = '[Inserisci qui' in current_translation.lower()
        
        # Ricostruisci template completo
        return self.rebuild_template()
    
    def rebuild_template(self):
        """Ricostruisce template completo dalle modifiche"""
        # TODO: Implementare ricostruzione completa template
        # Per ora ritorna il contenuto originale
        return self.template_content
    
    def update_chapter_progress(self):
        """Aggiorna progress bar capitolo"""
        if not self.chapters:
            return
        
        chapter = self.chapters[self.current_chapter]
        sections = chapter['sections']
        
        if sections:
            completed_sections = sum(1 for s in sections if not s['is_placeholder'])
            progress = (completed_sections / len(sections)) * 100
            
            self.chapter_progress['value'] = progress
            self.progress_label.config(text=f"{progress:.1f}%")
    
    def prev_chapter(self):
        """Capitolo precedente"""
        if self.current_chapter > 0:
            self.current_chapter -= 1
            self.load_current_chapter()
    
    def next_chapter(self):
        """Capitolo successivo"""
        if self.current_chapter < len(self.chapters) - 1:
            self.current_chapter += 1
            self.load_current_chapter()
    
    def manual_save(self):
        """Salvataggio manuale"""
        if self.auto_save_manager:
            content = self.get_current_content()
            success = self.auto_save_manager.manual_save(content)
            
            if success:
                self.is_modified = False
                self.status_label.config(text="💾 Salvato")
                messagebox.showinfo("Salvato", "Progetto salvato con successo!")
            else:
                messagebox.showerror("Errore", "Errore durante il salvataggio")
    
    def mark_complete(self):
        """Marca capitolo come completato"""
        response = messagebox.askyesno(
            "Completa Capitolo",
            f"Marcare il capitolo '{self.chapters[self.current_chapter]['title']}' come completato?"
        )
        
        if response:
            # Salva e aggiorna tracker
            self.manual_save()
            self.update_tracker()
    
    def update_tracker(self):
        """Aggiorna tracker progetto"""
        if self.handler:
            completion = self.handler.update_tracker_for_project(self.project_name)
            if completion is not False:
                self.status_label.config(text=f"📊 Tracker aggiornato - {completion:.1f}%")
    
    def run(self):
        """Avvia editor"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        if not self.parent:
            self.root.mainloop()
        else:
            self.root.grab_set()  # Modal se ha parent
    
    def on_closing(self):
        """Gestisce chiusura editor"""
        if self.is_modified:
            response = messagebox.askyesnocancel(
                "Salva modifiche",
                "Ci sono modifiche non salvate. Vuoi salvare prima di chiudere?"
            )
            
            if response is None:  # Cancel
                return
            elif response:  # Yes - save
                content = self.get_current_content()
                if self.auto_save_manager:
                    self.auto_save_manager.force_save_and_backup(content)
        
        # Pulisci recovery data
        if self.recovery_manager:
            self.recovery_manager.clear_recovery_data()
        
        # Ferma auto-save
        if self.auto_save_manager:
            self.auto_save_manager.stop_monitoring()
        
        # Chiudi finestra
        if self.parent:
            self.root.grab_release()
        
        self.root.destroy()

if __name__ == "__main__":
    # Test standalone
    editor = TranslationEditorGUI("Test_Project")
    editor.run()