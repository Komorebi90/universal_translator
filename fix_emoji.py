# FILENAME: fix_emoji.py
"""
Script per rimuovere automaticamente emoji da universal_translator.py
"""

import re
from pathlib import Path

def fix_emoji_in_file():
    """Rimuove emoji dal file universal_translator.py"""
    
    file_path = Path("universal_translator.py")
    
    if not file_path.exists():
        print("❌ File universal_translator.py non trovato!")
        return False
    
    # Leggi contenuto file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup originale
    backup_path = Path("universal_translator_backup.py")
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Backup creato: {backup_path}")
    
    # Sostituzioni emoji
    replacements = {
        "🌟": "***",
        "📁": "[FOLDER]", 
        "📚": "[BOOK]",
        "📄": "[FILE]",
        "📝": "[NOTE]",
        "✅": "[OK]",
        "❌": "[ERROR]",
        "🔄": "[PROCESS]",
        "💡": "[TIP]",
        "🚀": "[ROCKET]",
        "📊": "[CHART]",
        "📖": "[READ]",
        "🎯": "[TARGET]",
        "🔍": "[SEARCH]",
        "⚡": "[FAST]",
        "🎉": "[SUCCESS]",
        "🛠️": "[TOOLS]",
        "📈": "[STATS]",
        "🔧": "[CONFIG]",
        "💾": "[SAVE]",
        "\U0001F31F": "***",  # Stella emoji Unicode
        "\U0001F4C1": "[FOLDER]",  # Cartella emoji Unicode
        "\U0001F4DA": "[BOOK]",   # Libro emoji Unicode
    }
    
    # Applica sostituzioni
    modified_content = content
    changes_made = 0
    
    for emoji, replacement in replacements.items():
        if emoji in modified_content:
            count = modified_content.count(emoji)
            modified_content = modified_content.replace(emoji, replacement)
            print(f"🔄 Sostituito '{emoji}' con '{replacement}' ({count} occorrenze)")
            changes_made += count
    
    if changes_made == 0:
        print("ℹ️ Nessuna emoji trovata da sostituire")
        return True
    
    # Salva file modificato
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"✅ File modificato con successo!")
    print(f"📊 Totale sostituzioni: {changes_made}")
    print("🚀 Ora puoi usare 'Processa File' senza errori!")
    
    return True

if __name__ == "__main__":
    print("🔧 FIX EMOJI UNIVERSAL TRANSLATOR")
    print("=" * 40)
    
    success = fix_emoji_in_file()
    
    if success:
        print("\n🎉 FIX COMPLETATO!")
        print("💡 Ora torna al GUI e clicca 'Processa File'")
    else:
        print("\n❌ FIX FALLITO!")
        print("💡 Applica le modifiche manualmente")
    
    input("\nPremi Enter per chiudere...")