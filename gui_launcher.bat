# FILENAME: gui_launcher.bat
@echo off
chcp 65001 >nul
title 🌟 Universal Light Novel Translator - GUI System

:MAIN_MENU
cls
echo.
echo ████████████████████████████████████████████████████████
echo ███                                                  ███
echo ███     🌟 UNIVERSAL LIGHT NOVEL TRANSLATOR 🌟       ███  
echo ███           Sistema GUI Avanzato                   ███
echo ███                                                  ███
echo ████████████████████████████████████████████████████████
echo.
echo 🎯 NUOVO SISTEMA GUI
echo ═══════════════════════
echo.
echo [1] 🖥️ Avvia GUI Principale (RACCOMANDATO)
echo [2] 📊 GUI Project Manager
echo [3] ✏️ GUI Editor Traduzione
echo [4] 🔄 Rinomina File Sistema (Aggiorna progetti)
echo [5] 🛠️ Sistema Legacy (menu testuale)
echo [6] ⚙️ Setup Dipendenze GUI
echo [7] 🧪 Test Sistema GUI
echo [8] ❓ Guida GUI
echo [9] 🚪 Esci
echo.
set /p choice="Scegli opzione (1-9): "

if "%choice%"=="1" goto GUI_MAIN
if "%choice%"=="2" goto GUI_PROJECTS
if "%choice%"=="3" goto GUI_EDITOR
if "%choice%"=="4" goto RENAME_SYSTEM
if "%choice%"=="5" goto LEGACY_SYSTEM
if "%choice%"=="6" goto SETUP_GUI
if "%choice%"=="7" goto TEST_GUI
if "%choice%"=="8" goto HELP_GUI
if "%choice%"=="9" goto EXIT
goto MAIN_MENU

:GUI_MAIN
cls
echo 🖥️ AVVIO GUI PRINCIPALE
echo ═══════════════════════
echo.
echo 🚀 Avviando sistema GUI completo...
echo.

python main.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ GUI chiusa correttamente
) else (
    echo.
    echo ❌ Errore durante esecuzione GUI
    echo 💡 Controlla che tutti i file GUI siano presenti
    echo 💡 Esegui 'Setup Dipendenze GUI' se necessario
)

echo.
pause
goto MAIN_MENU

:GUI_PROJECTS
cls
echo 📊 PROJECT MANAGER GUI
echo ══════════════════════
echo.
echo 🚀 Avviando Project Manager...
echo.

python pmgui.py

if %ERRORLEVEL% neq 0 (
    echo ❌ Errore avvio Project Manager
    echo 💡 Usa 'GUI Principale' per funzionalità complete
)

echo.
pause
goto MAIN_MENU

:GUI_EDITOR
cls
echo ✏️ EDITOR TRADUZIONE GUI
echo ═══════════════════════
echo.
echo ⚠️ L'editor traduzione deve essere aperto dal Project Manager
echo 💡 Usa invece 'GUI Principale' per accesso completo
echo.
pause
goto MAIN_MENU

:RENAME_SYSTEM
cls
echo 🔄 SISTEMA RINOMINAZIONE FILE
echo ═══════════════════════════════
echo.
echo 📁 Aggiorna progetti esistenti con nomi file compatti
echo 💡 Necessario per compatibilità con sistema GUI
echo.

python rename.py

echo.
pause
goto MAIN_MENU

:LEGACY_SYSTEM
cls
echo 🛠️ SISTEMA LEGACY (Testuale)
echo ═══════════════════════════════
echo.
echo 🔄 Avviando launcher testuale originale...
echo.

call universal_launcher.bat

goto MAIN_MENU

:SETUP_GUI
cls
echo ⚙️ SETUP DIPENDENZE GUI
echo ═══════════════════════
echo.

echo 🔍 Controllo Python...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python installato
    python --version
) else (
    echo ❌ Python NON installato!
    echo.
    echo 📥 Scarica Python da: https://python.org/downloads/
    echo ⚠️  IMPORTANTE: Spunta 'Add Python to PATH'
    echo.
    pause
    goto MAIN_MENU
)

echo.
echo 🔍 Controllo tkinter (GUI)...
python -c "import tkinter; print('✅ tkinter disponibile')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ tkinter NON disponibile
    echo 💡 tkinter dovrebbe essere incluso con Python
    echo 💡 Su Linux: sudo apt-get install python3-tk
) else (
    echo ✅ tkinter disponibile
)

echo.
echo 🔍 Controllo dipendenze backend...

echo Checking PyPDF2...
pip show PyPDF2 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ PyPDF2 installato
) else (
    echo ❌ PyPDF2 mancante - Installazione...
    pip install PyPDF2
)

echo Checking BeautifulSoup4...
pip show beautifulsoup4 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ BeautifulSoup4 installato
) else (
    echo ❌ BeautifulSoup4 mancante - Installazione...
    pip install beautifulsoup4
)

echo.
echo 🔍 Controllo file GUI...
set gui_files_ok=1

if not exist "main.py" (
    echo ❌ main.py mancante
    set gui_files_ok=0
)
if not exist "pmgui.py" (
    echo ❌ pmgui.py mancante
    set gui_files_ok=0
)
if not exist "teditor.py" (
    echo ❌ teditor.py mancante
    set gui_files_ok=0
)
if not exist "styles.py" (
    echo ❌ styles.py mancante
    set gui_files_ok=0
)
if not exist "handler.py" (
    echo ❌ handler.py mancante
    set gui_files_ok=0
)
if not exist "autosave.py" (
    echo ❌ autosave.py mancante
    set gui_files_ok=0
)

if %gui_files_ok% equ 1 (
    echo ✅ Tutti i file GUI presenti
) else (
    echo ❌ Alcuni file GUI mancanti
    echo 💡 Assicurati di avere tutti i 6 file Python GUI
)

echo.
echo 📁 Creazione cartelle di lavoro...
if not exist "input_books" mkdir input_books
if not exist "translations" mkdir translations
if not exist "gui" mkdir gui >nul 2>&1

echo.
if %gui_files_ok% equ 1 (
    echo ✅ Setup GUI completato!
    echo 🚀 Puoi ora usare il sistema GUI
) else (
    echo ⚠️ Setup parzialmente completato
    echo 💡 Controlla file mancanti prima di usare GUI
)

pause
goto MAIN_MENU

:TEST_GUI
cls
echo 🧪 TEST SISTEMA GUI
echo ═══════════════════
echo.

echo 🔍 Test import moduli GUI...
python -c "
try:
    import tkinter as tk
    print('✅ tkinter OK')
    
    import styles
    print('✅ styles.py OK')
    
    import handler  
    print('✅ handler.py OK')
    
    import autosave
    print('✅ autosave.py OK')
    
    print('🎉 Tutti i moduli GUI funzionanti!')
    
except ImportError as e:
    print(f'❌ Errore import: {e}')
except Exception as e:
    print(f'❌ Errore: {e}')
"

echo.
echo 🔍 Test creazione finestra GUI...
python -c "
import tkinter as tk
try:
    root = tk.Tk()
    root.title('Test GUI')
    root.geometry('300x200')
    
    label = tk.Label(root, text='✅ GUI Test OK!', font=('Calibri', 12))
    label.pack(expand=True)
    
    root.after(2000, root.destroy)  # Chiudi dopo 2 secondi
    root.mainloop()
    
    print('✅ Test finestra GUI completato')
except Exception as e:
    print(f'❌ Errore test GUI: {e}')
"

echo.
pause
goto MAIN_MENU

:HELP_GUI
cls
echo ❓ GUIDA SISTEMA GUI
echo ═══════════════════════
echo.
echo 🎯 SISTEMA GUI COMPLETO:
echo ─────────────────────────
echo.
echo 🖥️ GUI PRINCIPALE:
echo   • Project Manager con tabella progetti
echo   • Auto-refresh ogni 30 secondi
echo   • Integrazione Smart Tracker
echo   • Launcher processamento file
echo.
echo ✏️ EDITOR TRADUZIONE:
echo   • Doppia finestra: originale ^| traduzione
echo   • Navigazione capitoli/sezioni
echo   • Auto-save ogni 30 secondi
echo   • Backup automatici
echo   • Progress tracking live
echo.
echo 🎨 CARATTERISTICHE GUI:
echo   • Font Calibri professionale
echo   • Auto-dimensionamento responsive
echo   • Temi business-oriented
echo   • Status bar informativi
echo   • Context menu click destro
echo.
echo 🔄 WORKFLOW COMPLETO GUI:
echo ─────────────────────────────
echo 1. Avvia 'GUI Principale'
echo 2. Metti file in input_books/
echo 3. Clicca 'Processa File'  
echo 4. Doppio-click progetto per aprire editor
echo 5. Traduci nella finestra destra
echo 6. Auto-save gestisce tutto automaticamente
echo 7. Usa 'Dashboard' per overview globale
echo.
echo 💾 SISTEMA AUTO-SAVE:
echo ─────────────────────────
echo • Auto-save ogni 30 secondi se modifiche
echo • Backup automatico ogni 5 minuti
echo • Recovery da crash automatico
echo • Cronologia ultimi 10 backup
echo • Force-save alla chiusura
echo.
echo 🎛️ TRACKING INTEGRATO:
echo ─────────────────────────────
echo • Progress bar live sui capitoli
echo • Statistiche globali in tempo reale
echo • Setup tracker automatico
echo • Dashboard multi-progetto
echo • Stime tempo personalizzate
echo.
echo 📁 STRUTTURA FILE COMPATTA:
echo ─────────────────────────────────
echo • tmpl.md (template traduzione)
echo • prog.md (progress tracker)
echo • info.md (informazioni progetto)
echo • trkr.py / trkr.json (smart tracker)
echo • stats.md (statistiche live)
echo • backup/ (backup automatici)
echo.
echo 🚨 TROUBLESHOOTING GUI:
echo ─────────────────────────────
echo • "tkinter non trovato" → Reinstalla Python completo
echo • "File GUI mancanti" → Controlla tutti i 6 file .py
echo • "Errore import" → Esegui 'Setup Dipendenze GUI'
echo • "GUI non si apre" → Esegui 'Test Sistema GUI'
echo • "Progetti non appaiono" → Usa 'Rinomina File Sistema'
echo.
echo 💡 VANTAGGI GUI vs TESTUALE:
echo ─────────────────────────────────
echo ✅ Workflow fluido senza cambio file
echo ✅ Controllo visivo completo progresso  
echo ✅ Auto-save e backup intelligenti
echo ✅ Navigazione intuitiva capitoli
echo ✅ Produttività traduzione +200%%
echo ✅ Tracking automatico integrato
echo ✅ Interface moderna e professionale
echo.
pause
goto MAIN_MENU

:EXIT
cls
echo.
echo 👋 Grazie per aver usato Universal Light Novel Translator!
echo.
echo 🖥️ Sistema GUI Features:
echo    ✏️ Editor doppia finestra professionale
echo    📊 Project Manager con tracking live
echo    💾 Auto-save e backup intelligenti
echo    🎨 Interface moderna business-style
echo    🔄 Integrazione completa Smart Tracker
echo.
echo 🎌 Buona traduzione e buona lettura!
echo.
timeout /t 3 >nul
exit