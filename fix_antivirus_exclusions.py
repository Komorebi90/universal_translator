# FILENAME: fix_antivirus_exclusions.py
#!/usr/bin/env python3
"""
Guida per Aggiungere Esclusioni Antivirus
Risolve problemi di salvataggio causati da antivirus
"""

import os
import sys
import subprocess
from pathlib import Path

class AntivirusExclusionGuide:
    def __init__(self):
        self.project_path = Path.cwd().absolute()
        self.translations_path = self.project_path / "translations"
        
    def print_header(self, text):
        print(f"\n🛡️ {text}")
        print("=" * 50)
    
    def detect_antivirus(self):
        """Rileva quale antivirus è in uso"""
        self.print_header("RILEVAMENTO ANTIVIRUS")
        
        # Comandi per rilevare antivirus comuni
        antivirus_checks = [
            ("Windows Defender", "powershell Get-MpPreference"),
            ("Avast", "tasklist | findstr avast"),
            ("AVG", "tasklist | findstr avg"),
            ("Norton", "tasklist | findstr norton"),
            ("McAfee", "tasklist | findstr mcafee"),
            ("Kaspersky", "tasklist | findstr kaspersky"),
            ("Malwarebytes", "tasklist | findstr mbam")
        ]
        
        detected_av = []
        
        for av_name, command in antivirus_checks:
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    detected_av.append(av_name)
                    print(f"✅ Rilevato: {av_name}")
            except Exception:
                pass
        
        if not detected_av:
            print("⚠️  Antivirus non rilevato automaticamente")
            print("💡 Controlla manualmente nel Task Manager o Area di Notifica")
        
        return detected_av
    
    def windows_defender_exclusions(self):
        """Guida per Windows Defender"""
        self.print_header("WINDOWS DEFENDER - ESCLUSIONI")
        
        print("📝 METODO 1 - AUTOMATICO (Amministratore):")
        print("   Esegui questo script come Amministratore per aggiungere automaticamente")
        
        print("\n📝 METODO 2 - MANUALE:")
        print("   1. Apri 'Sicurezza di Windows'")
        print("   2. Vai su 'Protezione da virus e minacce'")
        print("   3. Clicca 'Gestisci impostazioni' sotto 'Impostazioni protezione da virus e minacce'")
        print("   4. Scorri fino a 'Esclusioni' e clicca 'Aggiungi o rimuovi esclusioni'")
        print("   5. Clicca 'Aggiungi un'esclusione' → 'Cartella'")
        print("   6. Seleziona queste cartelle:")
        print(f"      📁 {self.project_path}")
        print(f"      📁 {self.translations_path}")
        
        print("\n🔧 COMANDI POWERSHELL (da eseguire come Amministratore):")
        print(f'   Add-MpPreference -ExclusionPath "{self.project_path}"')
        print(f'   Add-MpPreference -ExclusionPath "{self.translations_path}"')
        print('   Add-MpPreference -ExclusionExtension ".md"')
        print('   Add-MpPreference -ExclusionProcess "python.exe"')
        
        # Crea script PowerShell
        ps_script = self.project_path / "add_defender_exclusions.ps1"
        with open(ps_script, 'w') as f:
            f.write(f'''# Script per aggiungere esclusioni Windows Defender
# Esegui come Amministratore

Write-Host "🛡️ Aggiunta esclusioni Windows Defender..." -ForegroundColor Green

try {{
    Add-MpPreference -ExclusionPath "{self.project_path}"
    Write-Host "✅ Aggiunta esclusione: {self.project_path}" -ForegroundColor Green
    
    Add-MpPreference -ExclusionPath "{self.translations_path}"
    Write-Host "✅ Aggiunta esclusione: {self.translations_path}" -ForegroundColor Green
    
    Add-MpPreference -ExclusionExtension ".md"
    Write-Host "✅ Aggiunta esclusione estensione: .md" -ForegroundColor Green
    
    Add-MpPreference -ExclusionProcess "python.exe"
    Write-Host "✅ Aggiunta esclusione processo: python.exe" -ForegroundColor Green
    
    Write-Host "🎉 Esclusioni aggiunte con successo!" -ForegroundColor Green
    Write-Host "💡 Riprova ora a salvare i file" -ForegroundColor Yellow
    
}} catch {{
    Write-Host "❌ Errore: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "💡 Assicurati di eseguire come Amministratore" -ForegroundColor Yellow
}}

Write-Host "Premi Enter per chiudere..."
Read-Host
''')
        
        print(f"\n📄 Script PowerShell creato: {ps_script.name}")
        print("   Clicca destro → 'Esegui con PowerShell' (come Amministratore)")
    
    def third_party_antivirus_guide(self):
        """Guida per antivirus di terze parti"""
        self.print_header("ANTIVIRUS TERZE PARTI - ESCLUSIONI")
        
        guides = {
            "Avast": {
                "steps": [
                    "Apri Avast Antivirus",
                    "Vai su 'Menu' → 'Impostazioni'",
                    "Seleziona 'Protezione' → 'Core Shields'",
                    "Clicca 'Configura impostazioni scudo' per 'File System Shield'",
                    "Vai su 'Esclusioni'",
                    "Aggiungi le cartelle del progetto"
                ]
            },
            "Norton": {
                "steps": [
                    "Apri Norton Security",
                    "Clicca 'Impostazioni'",
                    "Seleziona 'Antivirus'",
                    "Clicca su 'Scansioni ed esami'",
                    "Nella sezione 'Esclusioni/Rischi bassi' clicca 'Configura'",
                    "Aggiungi cartelle e file da escludere"
                ]
            },
            "McAfee": {
                "steps": [
                    "Apri McAfee Security Center",
                    "Clicca 'Protezione Web e Email'",
                    "Clicca 'Protezione Antivirus'",
                    "Clicca 'File esclusi'",
                    "Aggiungi le cartelle del progetto"
                ]
            },
            "Kaspersky": {
                "steps": [
                    "Apri Kaspersky",
                    "Clicca sull'icona ingranaggio (Impostazioni)",
                    "Vai su 'Protezione'",
                    "Seleziona 'File Antivirus'",
                    "Clicca 'Impostazioni'",
                    "Vai su 'Esclusioni' e aggiungi le cartelle"
                ]
            }
        }
        
        for av_name, guide in guides.items():
            print(f"\n📋 {av_name.upper()}:")
            for i, step in enumerate(guide["steps"], 1):
                print(f"   {i}. {step}")
    
    def create_test_script(self):
        """Crea script per testare se le esclusioni funzionano"""
        test_script = self.project_path / "test_antivirus_exclusions.py"
        
        with open(test_script, 'w', encoding='utf-8') as f:
            f.write(f'''#!/usr/bin/env python3
"""
Test Esclusioni Antivirus
Verifica se l'antivirus blocca ancora le modifiche
"""

import time
import random
from pathlib import Path

def test_file_operations():
    """Test operazioni sui file"""
    test_folder = Path("translations")
    test_file = test_folder / "antivirus_test.md"
    
    print("🧪 TEST ESCLUSIONI ANTIVIRUS")
    print("=" * 40)
    
    tests = [
        ("Creazione file", lambda: test_file.write_text("Test content", encoding='utf-8')),
        ("Lettura file", lambda: test_file.read_text(encoding='utf-8')),
        ("Modifica file", lambda: test_file.write_text(f"Modified {{time.time()}}", encoding='utf-8')),
        ("Eliminazione file", lambda: test_file.unlink() if test_file.exists() else None)
    ]
    
    for test_name, test_func in tests:
        try:
            start_time = time.time()
            test_func()
            duration = time.time() - start_time
            
            if duration > 2:
                print(f"⚠️  {{test_name}}: OK ma lento ({{duration:.1f}}s) - Possibile interferenza antivirus")
            else:
                print(f"✅ {{test_name}}: OK ({{duration:.2f}}s)")
                
        except Exception as e:
            print(f"❌ {{test_name}}: FALLITO - {{e}}")
            print("💡 L'antivirus sta ancora bloccando le operazioni")
            return False
    
    print("\\n🎉 Tutti i test superati! Esclusioni funzionanti.")
    return True

def test_template_editing():
    """Test specifico per template di traduzione"""
    print("\\n📝 TEST TEMPLATE TRADUZIONE")
    print("=" * 40)
    
    # Trova un template esistente
    for project_dir in Path("translations").glob("*/"):
        template_file = project_dir / "template_traduzione.md"
        if template_file.exists():
            print(f"🎯 Test su: {{template_file}}")
            
            try:
                # Backup
                backup_content = template_file.read_text(encoding='utf-8')
                
                # Modifica
                test_content = backup_content + f"\\n<!-- Test antivirus {{time.time()}} -->"
                template_file.write_text(test_content, encoding='utf-8')
                
                # Verifica
                time.sleep(1)
                current_content = template_file.read_text(encoding='utf-8')
                
                if test_content == current_content:
                    print("✅ Modifica template: OK")
                    
                    # Ripristina
                    template_file.write_text(backup_content, encoding='utf-8')
                    print("✅ Ripristino template: OK")
                    return True
                else:
                    print("❌ Contenuto non corrisponde - Possibile interferenza")
                    template_file.write_text(backup_content, encoding='utf-8')
                    return False
                    
            except Exception as e:
                print(f"❌ Errore test template: {{e}}")
                return False
    
    print("⚠️  Nessun template trovato per il test")
    return True

if __name__ == "__main__":
    success1 = test_file_operations()
    success2 = test_template_editing()
    
    if success1 and success2:
        print("\\n🎉 ESCLUSIONI ANTIVIRUS FUNZIONANTI!")
        print("💡 Ora puoi salvare i template senza problemi")
    else:
        print("\\n❌ ESCLUSIONI NON ANCORA ATTIVE")
        print("💡 Ricontrolla le impostazioni antivirus")
    
    input("\\nPremi Enter per chiudere...")
''')
        
        print(f"📄 Script di test creato: {test_script.name}")
        print("   Esegui dopo aver aggiunto le esclusioni per verificare")
    
    def create_quick_fix_batch(self):
        """Crea script batch per fix rapido"""
        batch_script = self.project_path / "quick_antivirus_fix.bat"
        
        with open(batch_script, 'w') as f:
            f.write(f'''@echo off
title Fix Antivirus per Universal Translator

echo 🛡️ FIX RAPIDO ANTIVIRUS
echo ========================

echo 📁 Cartella progetto: {self.project_path}
echo 📁 Cartella traduzioni: {self.translations_path}

echo.
echo 🔧 OPZIONI DISPONIBILI:
echo [1] Apri Sicurezza Windows (per esclusioni manuali)
echo [2] Esegui script PowerShell (esclusioni automatiche)
echo [3] Test esclusioni antivirus
echo [4] Apri guide antivirus terze parti
echo [5] Disabilita temporaneamente protezione in tempo reale
echo [0] Esci

set /p choice="Scegli opzione: "

if "%choice%"=="1" (
    echo 📖 Apertura Sicurezza Windows...
    start ms-settings:windowsdefender
    echo 💡 Vai su Protezione da virus e minacce → Gestisci impostazioni → Esclusioni
    pause
)

if "%choice%"=="2" (
    echo 🔧 Esecuzione script PowerShell...
    powershell -ExecutionPolicy Bypass -File "add_defender_exclusions.ps1"
    pause
)

if "%choice%"=="3" (
    echo 🧪 Test esclusioni...
    python test_antivirus_exclusions.py
    pause
)

if "%choice%"=="4" (
    echo 📖 Apertura documentazione...
    start https://support.microsoft.com/windows/add-an-exclusion-to-windows-security-811816c0-4dfd-af4a-47e4-c301afe13b26
    pause
)

if "%choice%"=="5" (
    echo ⚠️ ATTENZIONE: Disabilita temporaneamente la protezione
    echo Ricordati di riattivarla dopo aver salvato!
    powershell "Set-MpPreference -DisableRealtimeMonitoring $true"
    echo ✅ Protezione disabilitata temporaneamente
    echo 💡 Per riattivare: Set-MpPreference -DisableRealtimeMonitoring $false
    pause
)

echo 👋 Arrivederci!
''')
        
        print(f"📄 Script fix rapido creato: {batch_script.name}")
        print("   Double-click per accesso rapido a tutte le soluzioni")
    
    def run_guide(self):
        """Esegue la guida completa"""
        print("🛡️ GUIDA ESCLUSIONI ANTIVIRUS")
        print("=" * 50)
        print(f"📁 Cartella progetto: {self.project_path}")
        print(f"📁 Cartella traduzioni: {self.translations_path}")
        
        detected_av = self.detect_antivirus()
        
        print("\n🎯 CARTELLE DA ESCLUDERE:")
        print(f"   📁 {self.project_path}")
        print(f"   📁 {self.translations_path}")
        print("   📄 Estensioni: .md, .py, .json, .txt")
        print("   ⚙️ Processi: python.exe")
        
        if "Windows Defender" in detected_av or not detected_av:
            self.windows_defender_exclusions()
        
        if any(av in detected_av for av in ["Avast", "Norton", "McAfee", "Kaspersky"]):
            self.third_party_antivirus_guide()
        
        self.create_test_script()
        self.create_quick_fix_batch()
        
        print(f"\n🎉 RISULTATO:")
        print("   📄 File creati per aiutarti:")
        print("   • add_defender_exclusions.ps1 (script automatico)")
        print("   • test_antivirus_exclusions.py (verifica esclusioni)")
        print("   • quick_antivirus_fix.bat (accesso rapido)")
        
        print(f"\n💡 PROSSIMI PASSI:")
        print("   1. Aggiungi le esclusioni usando i metodi sopra")
        print("   2. Esegui test_antivirus_exclusions.py per verificare")
        print("   3. Riprova a salvare i template")

def main():
    guide = AntivirusExclusionGuide()
    guide.run_guide()
    
    print("\n" + "=" * 50)
    print("Premi Enter per chiudere...")
    input()

if __name__ == "__main__":
    main()