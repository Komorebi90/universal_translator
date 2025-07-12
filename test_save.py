# FILENAME: test_save.py
"""
Script per diagnosticare problemi di salvataggio
"""

import os
import time
from pathlib import Path

def test_save_permissions():
    """Test permessi di salvataggio"""
    print("🔍 DIAGNOSTICA ERRORI SALVATAGGIO")
    print("=" * 40)
    
    # Test cartella translations
    translations_dir = Path("translations")
    
    if not translations_dir.exists():
        print("❌ Cartella 'translations' non esiste")
        return
    
    print(f"✅ Cartella translations: {translations_dir.absolute()}")
    
    # Lista progetti
    projects = [d for d in translations_dir.iterdir() if d.is_dir()]
    print(f"📚 Progetti trovati: {len(projects)}")
    
    for project in projects:
        print(f"\n📁 Progetto: {project.name}")
        
        # Trova file template
        template_files = [
            project / "tmpl.md",
            project / "template_traduzione.md"
        ]
        
        template_file = None
        for tf in template_files:
            if tf.exists():
                template_file = tf
                break
        
        if not template_file:
            print("  ❌ File template non trovato")
            continue
        
        print(f"  📄 Template: {template_file.name}")
        
        # Test permessi
        permissions = {
            "readable": os.access(template_file, os.R_OK),
            "writable": os.access(template_file, os.W_OK), 
            "executable": os.access(template_file, os.X_OK)
        }
        
        print(f"  🔐 Permessi: R:{permissions['readable']} W:{permissions['writable']} X:{permissions['executable']}")
        
        if not permissions['writable']:
            print("  ❌ FILE NON SCRIVIBILE!")
            
            # Prova a cambiare permessi
            try:
                os.chmod(template_file, 0o666)
                print("  🔧 Tentativo fix permessi...")
                if os.access(template_file, os.W_OK):
                    print("  ✅ Permessi corretti!")
                else:
                    print("  ❌ Fix permessi fallito")
            except Exception as e:
                print(f"  ❌ Errore cambio permessi: {e}")
        
        # Test scrittura
        try:
            # Leggi contenuto originale
            with open(template_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            # Aggiungi timestamp di test
            test_content = original_content + f"\n<!-- Test save {time.time()} -->"
            
            # Prova a scrivere
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(test_content)
                f.flush()
                os.fsync(f.fileno())
            
            print("  ✅ Test scrittura OK")
            
            # Ripristina contenuto originale
            with open(template_file, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
        except PermissionError as e:
            print(f"  ❌ Errore permessi scrittura: {e}")
        except OSError as e:
            print(f"  ❌ Errore OS scrittura: {e}")
        except Exception as e:
            print(f"  ❌ Errore generico scrittura: {e}")
        
        # Test spazio disco (Windows-compatible)
        try:
            import shutil
            free_space = shutil.disk_usage(str(template_file.parent)).free
            print(f"  💾 Spazio libero: {free_space // (1024*1024)} MB")
            if free_space < 10 * 1024 * 1024:  # Meno di 10MB
                print("  ⚠️ Spazio disco basso!")
        except Exception as e:
            print(f"  💾 Spazio disco: non controllabile - {e}")

def fix_common_issues():
    """Fix automatico problemi comuni"""
    print("\n🔧 FIX AUTOMATICO PROBLEMI COMUNI")
    print("=" * 40)
    
    translations_dir = Path("translations")
    
    for project in translations_dir.iterdir():
        if not project.is_dir():
            continue
        
        print(f"\n🔧 Fix progetto: {project.name}")
        
        # Fix permessi cartella
        try:
            os.chmod(project, 0o755)
            print("  ✅ Permessi cartella corretti")
        except:
            print("  ❌ Fix permessi cartella fallito")
        
        # Fix permessi file
        for file_path in project.rglob("*.md"):
            try:
                os.chmod(file_path, 0o666)
                print(f"  ✅ Permessi file {file_path.name} corretti")
            except:
                print(f"  ❌ Fix permessi {file_path.name} fallito")
        
        # Crea cartella backup se mancante
        backup_dir = project / "backup"
        backup_dir.mkdir(exist_ok=True)
        print(f"  ✅ Cartella backup: {backup_dir}")

if __name__ == "__main__":
    test_save_permissions()
    
    print("\n" + "=" * 40)
    fix_choice = input("Vuoi provare il fix automatico? (y/n): ")
    
    if fix_choice.lower() in ['y', 'yes', 's', 'si']:
        fix_common_issues()
        print("\n✅ Fix completato! Riprova il salvataggio nell'editor.")
    
    input("\nPremi Enter per chiudere...")