# FILENAME: styles.py
#!/usr/bin/env python3
"""
GUI Styles - Universal Light Novel Translator
Gestione stili e temi per interfacce GUI
"""

import tkinter as tk
from tkinter import ttk
from tkinter import WORD, NORMAL, DISABLED, CHAR, NONE
from typing import Optional, Callable, Any, Union, List, Tuple, Sequence

class GUIStyles:
    """Gestione stili GUI professionali"""
    
    def __init__(self):
        # Font base - Calibri come preferenza utente
        self.font_family = "Calibri"
        self.font_fallback = ["Segoe UI", "Arial", "Helvetica"]
        
        # Dimensioni font
        self.font_normal = (self.font_family, 10)
        self.font_large = (self.font_family, 12)
        self.font_small = (self.font_family, 9)
        self.font_title = (self.font_family, 14, "bold")
        self.font_header = (self.font_family, 11, "bold")
        
        # Colori - Schema professionale supply chain
        self.colors = {
            # Primari
            'bg_main': '#f8f9fa',           # Grigio chiaro principale
            'bg_secondary': '#e9ecef',       # Grigio secondario
            'bg_accent': '#2c5aa0',         # Blu navy (professionale)
            'bg_success': '#28a745',        # Verde successo
            'bg_warning': '#ffc107',        # Giallo attenzione
            'bg_danger': '#dc3545',         # Rosso errore
            
            # Testi
            'text_primary': '#212529',       # Nero principale
            'text_secondary': '#6c757d',     # Grigio testo
            'text_light': '#ffffff',        # Bianco
            'text_accent': '#2c5aa0',       # Blu navy testo
            
            # Bordi e separatori
            'border': '#dee2e6',            # Bordo standard
            'border_focus': '#2c5aa0',      # Bordo focus
            'separator': '#ced4da',         # Separatore
            
            # Stati
            'hover': '#e7f1ff',             # Hover azzurro
            'selected': '#cce7ff',          # Selezione azzurra
            'disabled': '#f8f9fa'           # Disabilitato
        }
        
        # Dimensioni
        self.padding = {
            'small': 5,
            'normal': 10, 
            'large': 15,
            'xl': 20
        }
        
        self.sizes = {
            'button_height': 32,
            'entry_height': 28,
            'min_width': 1200,
            'min_height': 700,
            'sidebar_width': 250
        }
    
    def configure_window(self, window: Union[tk.Tk, tk.Toplevel], title: str = "Universal Translator") -> None:
        """Configura finestra principale"""
        window.title(title)
        window.configure(bg=self.colors['bg_main'])
        
        # Dimensioni responsive
        window.minsize(self.sizes['min_width'], self.sizes['min_height'])
        
        # Centra finestra
        self.center_window(window, self.sizes['min_width'], self.sizes['min_height'])
        
        # Icona (se disponibile)
        try:
            window.iconbitmap('icon.ico')
        except:
            pass
    
    def center_window(self, window: Union[tk.Tk, tk.Toplevel], width: int, height: int) -> None:
        """Centra finestra sullo schermo"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_frame(self, parent: Union[tk.Widget, tk.Tk, tk.Toplevel], style: str = 'main') -> tk.Frame:
        """Crea frame con stile"""
        bg_color = self.colors.get(f'bg_{style}', self.colors['bg_main'])
        
        frame = tk.Frame(
            parent,
            bg=bg_color,
            relief='flat',
            bd=0
        )
        return frame
    
    def create_label(self, parent: Union[tk.Widget, tk.Tk, tk.Toplevel], text: str, style: str = 'normal') -> tk.Label:
        """Crea label con stile"""
        fonts = {
            'title': self.font_title,
            'header': self.font_header,
            'normal': self.font_normal,
            'small': self.font_small
        }
        
        colors = {
            'title': self.colors['text_accent'],
            'header': self.colors['text_primary'],
            'normal': self.colors['text_primary'],
            'small': self.colors['text_secondary']
        }
        
        label = tk.Label(
            parent,
            text=text,
            font=fonts.get(style, self.font_normal),
            fg=colors.get(style, self.colors['text_primary']),
            bg=parent.cget('bg'),
            anchor='w'
        )
        return label
    
    def create_button(self, parent: Union[tk.Widget, tk.Tk, tk.Toplevel], text: str, command: Optional[Callable[[], Any]] = None, style: str = 'normal') -> tk.Button:
        """Crea pulsante con stile"""
        styles = {
            'normal': {
                'bg': self.colors['bg_secondary'],
                'fg': self.colors['text_primary'],
                'activebackground': self.colors['hover'],
                'activeforeground': self.colors['text_primary']
            },
            'primary': {
                'bg': self.colors['bg_accent'],
                'fg': self.colors['text_light'],
                'activebackground': '#1e3d72',
                'activeforeground': self.colors['text_light']
            },
            'success': {
                'bg': self.colors['bg_success'],
                'fg': self.colors['text_light'],
                'activebackground': '#1e7e34',
                'activeforeground': self.colors['text_light']
            },
            'warning': {
                'bg': self.colors['bg_warning'],
                'fg': self.colors['text_primary'],
                'activebackground': '#d39e00',
                'activeforeground': self.colors['text_primary']
            }
        }
        
        btn_style = styles.get(style, styles['normal'])
        
        # Gestisci command None per evitare errori tipo
        button_args = {
            'text': text,
            'font': self.font_normal,
            'height': 1,
            'relief': 'solid',
            'bd': 1,
            'cursor': 'hand2',
            **btn_style
        }
        
        # Aggiungi command solo se non è None
        if command is not None:
            button_args['command'] = command
        
        button = tk.Button(parent, **button_args)
        
        # Bind hover effects
        def on_enter(e):
            button.configure(bg=btn_style['activebackground'])
        
        def on_leave(e):
            button.configure(bg=btn_style['bg'])
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return button
    
    def create_entry(self, parent: Union[tk.Widget, tk.Tk, tk.Toplevel], width: Optional[int] = None) -> tk.Entry:
        """Crea entry con stile"""
        entry = tk.Entry(
            parent,
            font=self.font_normal,
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.colors['border_focus'],
            highlightbackground=self.colors['border']
        )
        
        if width:
            entry.configure(width=width)
        
        return entry
    
    def create_text(self, parent: Union[tk.Widget, tk.Tk, tk.Toplevel], wrap: str = 'word', state: str = 'normal') -> tk.Text:
        """Crea widget text con stile"""
        # Converti stringhe in costanti tkinter
        if wrap == 'word':
            wrap_mode = WORD
        elif wrap == 'char':
            wrap_mode = CHAR
        elif wrap == 'none':
            wrap_mode = NONE
        else:
            wrap_mode = WORD  # Default sicuro
            
        if state == 'normal':
            text_state = NORMAL
        elif state == 'disabled':
            text_state = DISABLED
        else:
            text_state = NORMAL  # Default sicuro
        
        text_widget = tk.Text(
            parent,
            font=self.font_normal,
            wrap=wrap_mode,
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.colors['border_focus'],
            highlightbackground=self.colors['border'],
            bg='white',
            fg=self.colors['text_primary'],
            selectbackground=self.colors['selected'],
            insertbackground=self.colors['text_primary'],
            state=text_state
        )
        return text_widget
    
    def create_treeview(self, parent: Union[tk.Widget, tk.Tk, tk.Toplevel], columns: Sequence[str]) -> ttk.Treeview:
        """Crea treeview (tabella) con stile"""
        style = ttk.Style()
        
        # Configura stile treeview
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground=self.colors['text_primary'],
            fieldbackground="white",
            font=self.font_normal
        )
        
        style.configure(
            "Custom.Treeview.Heading",
            background=self.colors['bg_secondary'],
            foreground=self.colors['text_primary'],
            font=self.font_header,
            relief='solid',
            borderwidth=1
        )
        
        # Converti Sequence in list per compatibilità tkinter
        columns_list = list(columns)
        
        tree = ttk.Treeview(
            parent,
            columns=columns_list,
            style="Custom.Treeview",
            show='tree headings'
        )
        
        return tree
    
    def create_progress_bar(self, parent: Union[tk.Widget, tk.Tk, tk.Toplevel], length: int = 200) -> ttk.Progressbar:
        """Crea progress bar con stile"""
        style = ttk.Style()
        
        style.configure(
            "Custom.Horizontal.TProgressbar",
            background=self.colors['bg_accent'],
            troughcolor=self.colors['bg_secondary'],
            borderwidth=1,
            lightcolor=self.colors['bg_accent'],
            darkcolor=self.colors['bg_accent']
        )
        
        progress = ttk.Progressbar(
            parent,
            length=length,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        
        return progress
    
    def create_separator(self, parent: Union[tk.Widget, tk.Tk, tk.Toplevel], orient: str = 'horizontal') -> ttk.Separator:
        """Crea separatore con stile"""
        style = ttk.Style()
        
        style.configure(
            "Custom.TSeparator",
            background=self.colors['separator']
        )
        
        # Assicurati che orient sia il tipo corretto
        orientation = 'horizontal' if orient == 'horizontal' else 'vertical'
        
        separator = ttk.Separator(
            parent,
            orient=orientation,
            style="Custom.TSeparator"
        )
        
        return separator