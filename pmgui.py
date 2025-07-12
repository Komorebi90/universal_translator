# FILENAME: pmgui.py
#!/usr/bin/env python3
"""
Project Manager GUI - Universal Light Novel Translator
Finestra principale gestione progetti (sostituto .bat)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import subprocess
import os
from pathlib import Path

from styles import GUIStyles
from handler import ProjectDataHandler

class ProjectManagerGUI:
    """GUI principale gestione progetti"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.styles = GUIStyles()
        self.handler = ProjectDataHandler()
        
        # Configurazione finestra
        self.styles.configure_window(self.root, "Universal Light Novel Translator - Project Manager")
        
        # Variabili
        self.projects_data = {}
        self.selected_project = None
        self.auto_refresh = True
        self.refresh_thread = None
        
        # Setup UI
        self.setup_ui()
        self.refresh_projects()
        self.start_auto_refresh()
    
    def setup_ui(self):
        """Setup interface utente"""
        # Main container
        main_frame = self.styles.create_frame(self.root, 'main')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Toolbar
        self.create_toolbar(main_frame)
        
        # Content area (tabella progetti + stats)
        content_frame = self.styles.create_frame(main_frame, 'main')
        content_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Projects table
        self.create_projects_table(content_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Crea header applicazione"""
        header_frame = self.styles.create_frame(parent, 'main')
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Titolo
        title_label = self.styles.create_label(
            header_frame, 
            "🌟 Universal Light Novel Translator", 
            'title'
        )
        title_label.pack(side='left')
        
        # Statistiche globali
        self.stats_frame = self.styles.create_frame(header_frame, 'main')
        self.stats_frame.pack(side='right')
        
        self.stats_label = self.styles.create_label(
            self.stats_frame, 
            "Caricamento...", 
            'normal'
        )
        self.stats_label.pack()
    
    def create_toolbar(self, parent):
        """Crea toolbar con pulsanti azioni"""
        toolbar_frame = self.styles.create_frame(parent, 'secondary')
        toolbar_frame.pack(fill='x', pady=(0, 10))
        
        # Pulsanti principali
        buttons = [
            ("🚀 Processa File", self.process_files, 'primary'),
            ("📁 Cartella Input", self.open_input_folder, 'normal'),
            ("✏️ Apri Editor", self.open_editor, 'success'),
            ("🎛️ Setup Tracker", self.setup_tracker, 'normal'),
            ("📊 Dashboard", self.show_dashboard, 'normal'),
            ("🔄 Aggiorna", self.refresh_projects, 'normal')
        ]
        
        for text, command, style in buttons:
            btn = self.styles.create_button(toolbar_frame, text, command, style)
            btn.pack(side='left', padx=(0, 5))
        
        # Pulsanti utility a destra
        self.styles.create_separator(toolbar_frame, 'vertical').pack(side='right', fill='y', padx=10)
        
        auto_refresh_btn = self.styles.create_button(
            toolbar_frame, 
            "⏸️ Pausa Auto", 
            self.toggle_auto_refresh, 
            'warning'
        )
        auto_refresh_btn.pack(side='right', padx=(5, 0))
        self.auto_refresh_btn = auto_refresh_btn
    
    def create_projects_table(self, parent):
        """Crea tabella progetti"""
        # Frame contenitore con scrollbar
        table_frame = self.styles.create_frame(parent, 'main')
        table_frame.pack(fill='both', expand=True)
        
        # Colonne tabella
        columns = ('status', 'completion', 'chapters', 'characters', 'modified', 'tracker')
        
        self.tree = self.styles.create_treeview(table_frame, columns)
        
        # Configurazione colonne
        self.tree.heading('#0', text='Progetto', anchor='w')
        self.tree.heading('status', text='Stato', anchor='center')
        self.tree.heading('completion', text='Progresso', anchor='center')
        self.tree.heading('chapters', text='Capitoli', anchor='center')
        self.tree.heading('characters', text='Caratteri', anchor='center')
        self.tree.heading('modified', text='Modificato', anchor='center')
        self.tree.heading('tracker', text='Tracker', anchor='center')
        
        # Larghezze colonne
        self.tree.column('#0', width=250, minwidth=200)
        self.tree.column('status', width=100, minwidth=80)
        self.tree.column('completion', width=150, minwidth=120)
        self.tree.column('chapters', width=80, minwidth=60)
        self.tree.column('characters', width=120, minwidth=100)
        self.tree.column('modified', width=130, minwidth=110)
        self.tree.column('tracker', width=80, minwidth=60)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack tree e scrollbars
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind eventi
        self.tree.bind('<Double-1>', self.on_project_double_click)
        self.tree.bind('<Button-3>', self.on_project_right_click)
        self.tree.bind('<<TreeviewSelect>>', self.on_project_select)
    
    def create_status_bar(self, parent):
        """Crea status bar"""
        status_frame = self.styles.create_frame(parent, 'secondary')
        status_frame.pack(fill='x', pady=(10, 0))
        
        self.status_label = self.styles.create_label(
            status_frame, 
            "Pronto", 
            'small'
        )
        self.status_label.pack(side='left')
        
        # Progress bar per operazioni lunghe
        self.progress_bar = self.styles.create_progress_bar(status_frame, 200)
        self.progress_bar.pack(side='right', padx=(10, 0))
        self.progress_bar.pack_forget()  # Nascosto di default
    
    def refresh_projects(self):
        """Aggiorna lista progetti"""
        self.set_status("Aggiornamento progetti...")
        
        # Carica dati
        self.projects_data = self.handler.get_all_projects(force_refresh=True)
        
        # Pulisci tabella
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Popola tabella
        for project_name, data in self.projects_data.items():
            self.insert_project_row(project_name, data)
        
        # Aggiorna statistiche globali
        self.update_global_stats()
        
        self.set_status(f"Aggiornato - {len(self.projects_data)} progetti")
    
    def insert_project_row(self, project_name, data):
        """Inserisce riga progetto nella tabella"""
        # Icone stato
        status_icons = {
            'completed': '✅',
            'in_progress': '🔄',
            'started': '🔄',
            'not_started': '⏳',
            'error': '❌',
            'unknown': '❓'
        }
        
        # Progress bar testuale
        completion = data['completion']
        progress_chars = int(completion / 10)
        progress_bar = '█' * progress_chars + '░' * (10 - progress_chars)
        progress_text = f"{completion:.1f}% {progress_bar}"
        
        # Formattazione dati
        status_text = f"{status_icons.get(data['status'], '❓')} {data['status'].replace('_', ' ').title()}"
        chapters_text = f"{data['chapters_done']}/{data['chapters_total']}"
        chars_text = f"{data['characters_done']:,}/{data['characters_total']:,}" if data['characters_total'] > 0 else "N/A"
        tracker_text = "✅" if data['has_tracker'] else "❌"
        
        # Inserisci riga
        self.tree.insert(
            '',
            'end',
            text=project_name,
            values=(
                status_text,
                progress_text,
                chapters_text,
                chars_text,
                data['last_modified'],
                tracker_text
            ),
            tags=(data['status'],)
        )
        
        # Tag colori per stati
        self.tree.tag_configure('completed', foreground='#28a745')
        self.tree.tag_configure('in_progress', foreground='#2c5aa0')
        self.tree.tag_configure('started', foreground='#ffc107')
        self.tree.tag_configure('not_started', foreground='#6c757d')
        self.tree.tag_configure('error', foreground='#dc3545')
    
    def update_global_stats(self):
        """Aggiorna statistiche globali"""
        stats = self.handler.get_global_stats()
        
        stats_text = (
            f"📚 {stats['total_projects']} progetti | "
            f"✅ {stats['completed_projects']} completati | "
            f"🔄 {stats['in_progress_projects']} in corso | "
            f"📊 {stats['avg_completion']:.1f}% medio"
        )
        
        self.stats_label.config(text=stats_text)
    
    def on_project_select(self, event):
        """Gestisce selezione progetto"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            self.selected_project = self.tree.item(item, 'text')
    
    def on_project_double_click(self, event):
        """Gestisce doppio click su progetto"""
        if self.selected_project:
            self.open_editor()
    
    def on_project_right_click(self, event):
        """Gestisce click destro su progetto"""
        # Context menu
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="✏️ Apri Editor", command=self.open_editor)
        context_menu.add_command(label="📂 Apri Cartella", command=self.open_project_folder)
        context_menu.add_separator()
        context_menu.add_command(label="🎛️ Setup Tracker", command=self.setup_tracker)
        context_menu.add_command(label="🔄 Aggiorna Tracker", command=self.update_tracker)
        context_menu.add_separator()
        context_menu.add_command(label="📊 Statistiche", command=self.show_project_stats)
        
        context_menu.post(event.x_root, event.y_root)
    
    def process_files(self):
        """Processa nuovi file"""
        self.set_status("Processamento file...")
        self.show_progress()
        
        def process_thread():
            try:
                # Esegui universal_translator
                result = subprocess.run(
                    ['python', 'universal_translator.py'],
                    capture_output=True,
                    text=True
                )
                
                self.root.after(0, self.hide_progress)
                
                if result.returncode == 0:
                    self.root.after(0, lambda: self.set_status("Processamento completato"))
                    self.root.after(0, self.refresh_projects)
                    messagebox.showinfo("Successo", "File processati con successo!")
                else:
                    error_msg = result.stderr or "Errore sconosciuto"
                    self.root.after(0, lambda: self.set_status("Errore processamento"))
                    messagebox.showerror("Errore", f"Errore processamento:\n{error_msg}")
                    
            except Exception as e:
                self.root.after(0, self.hide_progress)
                self.root.after(0, lambda: self.set_status("Errore processamento"))
                messagebox.showerror("Errore", f"Errore durante processamento:\n{e}")
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def open_input_folder(self):
        """Apri cartella input"""
        input_folder = Path("input_books")
        input_folder.mkdir(exist_ok=True)
        
        try:
            os.startfile(str(input_folder))
        except:
            # Fallback per sistemi non Windows
            subprocess.run(['explorer', str(input_folder)], shell=True)
    
    def open_editor(self):
        """Apri editor traduzione"""
        if not self.selected_project:
            messagebox.showwarning("Attenzione", "Seleziona un progetto prima")
            return
        
        try:
            from teditor import TranslationEditorGUI
            editor = TranslationEditorGUI(self.selected_project, parent=self)
            editor.run()
        except ImportError:
            messagebox.showerror("Errore", "Editor traduzione non disponibile")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore apertura editor:\n{e}")
    
    def open_project_folder(self):
        """Apri cartella progetto"""
        if not self.selected_project:
            return
        
        project_data = self.projects_data.get(self.selected_project)
        if project_data:
            try:
                os.startfile(str(project_data['path']))
            except:
                subprocess.run(['explorer', str(project_data['path'])], shell=True)
    
    def setup_tracker(self):
        """Setup tracker per progetto selezionato"""
        if not self.selected_project:
            messagebox.showwarning("Attenzione", "Seleziona un progetto prima")
            return
        
        self.set_status(f"Setup tracker per {self.selected_project}...")
        
        def setup_thread():
            success = self.handler.setup_tracker_for_project(self.selected_project)
            
            if success:
                self.root.after(0, lambda: self.set_status("Tracker installato"))
                self.root.after(0, self.refresh_projects)
                messagebox.showinfo("Successo", "Smart Tracker installato con successo!")
            else:
                self.root.after(0, lambda: self.set_status("Errore setup tracker"))
                messagebox.showerror("Errore", "Errore durante setup tracker")
        
        threading.Thread(target=setup_thread, daemon=True).start()
    
    def update_tracker(self):
        """Aggiorna tracker progetto selezionato"""
        if not self.selected_project:
            return
        
        completion = self.handler.update_tracker_for_project(self.selected_project)
        if completion is not False:
            self.refresh_projects()
            self.set_status(f"Tracker aggiornato - {completion:.1f}%")
    
    def show_dashboard(self):
        """Mostra dashboard globale"""
        try:
            from tracker_manager import TrackerManager
            manager = TrackerManager()
            dashboard_file = manager.generate_global_dashboard()
            
            if dashboard_file and dashboard_file.exists():
                os.startfile(str(dashboard_file))
            else:
                messagebox.showerror("Errore", "Impossibile generare dashboard")
                
        except Exception as e:
            messagebox.showerror("Errore", f"Errore dashboard:\n{e}")
    
    def show_project_stats(self):
        """Mostra statistiche progetto"""
        if not self.selected_project:
            return
        
        project_data = self.projects_data.get(self.selected_project)
        if project_data:
            chapters = self.handler.get_project_chapters(self.selected_project)
            
            stats_window = tk.Toplevel(self.root)
            self.styles.configure_window(stats_window, f"Statistiche - {self.selected_project}")
            stats_window.geometry("600x400")
            
            # TODO: Implementare finestra statistiche dettagliate
            self.styles.create_label(stats_window, f"Statistiche {self.selected_project}", 'title').pack(pady=20)
    
    def toggle_auto_refresh(self):
        """Toggle auto refresh"""
        self.auto_refresh = not self.auto_refresh
        
        if self.auto_refresh:
            self.auto_refresh_btn.config(text="⏸️ Pausa Auto")
            self.start_auto_refresh()
        else:
            self.auto_refresh_btn.config(text="▶️ Avvia Auto")
    
    def start_auto_refresh(self):
        """Avvia auto refresh"""
        def auto_refresh_thread():
            import time
            while self.auto_refresh:
                time.sleep(30)  # Aggiorna ogni 30 secondi
                if self.auto_refresh:
                    self.root.after(0, self.refresh_projects)
        
        if self.auto_refresh and (not self.refresh_thread or not self.refresh_thread.is_alive()):
            self.refresh_thread = threading.Thread(target=auto_refresh_thread, daemon=True)
            self.refresh_thread.start()
    
    def set_status(self, text):
        """Imposta testo status bar"""
        self.status_label.config(text=text)
    
    def show_progress(self):
        """Mostra progress bar"""
        self.progress_bar.pack(side='right', padx=(10, 0))
        self.progress_bar.start()
    
    def hide_progress(self):
        """Nascondi progress bar"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
    
    def run(self):
        """Avvia GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Gestisce chiusura applicazione"""
        self.auto_refresh = False
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    app = ProjectManagerGUI()
    app.run()