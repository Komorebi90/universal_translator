# FILENAME: main.py
#!/usr/bin/env python3
"""
GUI Launcher - Universal Light Novel Translator
Entry point principale per sistema GUI
"""

import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

def check_dependencies():
    """Controlla dipendenze GUI"""
    missing = []
    
    try:
        import tkinter as tk
    except ImportError:
        missing.append("tkinter")
    
    # Controlla file sistema esistenti
    required_files = [
        "universal_translator.py",
        "smart_tracker_system.py", 
        "tracker_manager.py"
    ]
    
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    return missing

def show_error(title, message):
    """Mostra errore graceful"""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(title, message)
        root.destroy()
    except:
        print(f"ERRORE: {title}\n{message}")

def main():
    """Entry point principale"""
    print("🚀 Universal Light Novel Translator - GUI System")
    
    # Controlla dipendenze
    missing = check_dependencies()
    if missing:
        error_msg = f"File/moduli mancanti:\n" + "\n".join(f"- {item}" for item in missing)
        show_error("Dipendenze Mancanti", error_msg)
        return 1
    
    # Crea cartelle necessarie
    Path("translations").mkdir(exist_ok=True)
    Path("input_books").mkdir(exist_ok=True)
    Path("gui").mkdir(exist_ok=True)
    
    try:
        # Avvia GUI principale
        from pmgui import ProjectManagerGUI
        
        app = ProjectManagerGUI()
        app.run()
        
    except ImportError as e:
        show_error("Errore Sistema", f"Impossibile avviare GUI:\n{e}")
        return 1
    except Exception as e:
        show_error("Errore Critico", f"Errore inaspettato:\n{e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())