@echo off
chcp 65001 >nul
title 🌟 Universal Light Novel Translator

:MENU
cls
echo.
echo ████████████████████████████████████████████████████████
echo ███                                                  ███
echo ███     🌟 UNIVERSAL LIGHT NOVEL TRANSLATOR 🌟       ███  
echo ███          PDF + EPUB Automatico                   ███
echo ███                                                  ███
echo ████████████████████████████████████████████████████████
echo.
echo 📚 MENU PRINCIPALE
echo ═══════════════════
echo.
echo [1] 🚀 Processa Tutti i File (Auto)
echo [2] 📁 Apri Cartella Input
echo [3] 📊 Visualizza Progetti
echo [4] 🛠️ Setup e Dipendenze
echo [5] 📝 Apri Progetto Specifico
echo [6] 🎛️ Smart Tracker (NUOVO!)
echo [7] 📈 Dashboard Globale
echo [8] ❓ Guida e Help
echo [9] 🚪 Esci
echo.
set /p choice="Scegli opzione (1-9): "

if "%choice%"=="1" goto PROCESS
if "%choice%"=="2" goto INPUT_FOLDER
if "%choice%"=="3" goto VIEW_PROJECTS
if "%choice%"=="4" goto SETUP
if "%choice%"=="5" goto OPEN_PROJECT
if "%choice%"=="6" goto SMART_TRACKER
if "%choice%"=="7" goto DASHBOARD
if "%choice%"=="8" goto HELP
if "%choice%"=="9" goto EXIT
goto MENU

:PROCESS
cls
echo 🚀 PROCESSAMENTO AUTOMATICO
echo ══════════════════════════
echo.

if not exist "input_books" (
    echo 📁 Creazione cartella input...
    mkdir input_books
)

echo 🔍 Controllo file nella cartella input_books...
echo.

dir "input_books\*.pdf" >nul 2>&1
set pdf_found=%errorlevel%

dir "input_books\*.epub" >nul 2>&1  
set epub_found=%errorlevel%

if %pdf_found% neq 0 if %epub_found% neq 0 (
    echo ❌ Nessun file PDF o EPUB trovato!
    echo.
    echo 💡 Inserisci file in: input_books\
    echo 📚 Formati supportati: PDF, EPUB
    echo.
    pause
    goto MENU
)

echo ✅ File trovati! Avvio processamento...
echo.
echo 🔄 Processamento in corso...
python universal_translator.py

echo.
echo ✅ Processamento completato!
echo 📁 Controlla cartella 'translations' per i risultati
echo.
pause
goto MENU

:INPUT_FOLDER
cls
echo 📁 GESTIONE CARTELLA INPUT
echo ══════════════════════════
echo.

if not exist "input_books" (
    echo 📁 Creazione cartella input...
    mkdir input_books
)

echo 📂 Apertura cartella input_books...
start "" "input_books"

echo.
echo 💡 ISTRUZIONI:
echo ──────────────
echo 1. Copia i tuoi file PDF/EPUB nella cartella
echo 2. I nomi file saranno usati come titoli progetti
echo 3. Non serve rinominare - funziona con qualsiasi nome
echo 4. Torna al menu e scegli "Processa Tutti i File"
echo.

pause
goto MENU

:VIEW_PROJECTS
cls
echo 📊 PROGETTI ESISTENTI
echo ═══════════════════════
echo.

if not exist "translations" (
    echo ❌ Nessun progetto trovato!
    echo 💡 Esegui prima il processamento (opzione 1)
    echo.
    pause
    goto MENU
)

echo 📁 Progetti nella cartella translations:
echo ─────────────────────────────────────
echo.

set project_count=0
for /d %%i in ("translations\*") do (
    set /a project_count+=1
    echo [!project_count!] %%~ni
)

if %project_count%==0 (
    echo ❌ Nessun progetto trovato
) else (
    echo.
    echo ✅ Trovati %project_count% progetti
    echo.
    echo 📂 Apertura cartella translations...
    start "" "translations"
)

echo.
pause
goto MENU

:OPEN_PROJECT
cls
echo 📝 APRI PROGETTO SPECIFICO
echo ═══════════════════════════
echo.

if not exist "translations" (
    echo ❌ Nessun progetto trovato!
    echo.
    pause
    goto MENU
)

echo 📋 Progetti disponibili:
echo ────────────────────────
echo.

set count=0
for /d %%i in ("translations\*") do (
    set /a count+=1
    echo [!count!] %%~ni
    set "project_!count!=%%i"
)

if %count%==0 (
    echo ❌ Nessun progetto trovato
    pause
    goto MENU
)

echo.
set /p project_choice="Scegli progetto (1-%count%): "

if defined project_%project_choice% (
    set "selected_project=!project_%project_choice%!"
    echo.
    echo 📂 Apertura progetto: !selected_project!
    
    if exist "!selected_project!\template_traduzione.md" (
        start "" "!selected_project!\template_traduzione.md"
    )
    
    if exist "!selected_project!\progress_tracker.md" (
        start "" "!selected_project!\progress_tracker.md"  
    )
    
    echo ✅ File aperti!
) else (
    echo ❌ Scelta non valida
)

echo.
pause
goto MENU

:SETUP
cls
echo 🛠️ SETUP E DIPENDENZE
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
    goto MENU
)

echo.
echo 🔍 Controllo dipendenze...

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

echo Checking requests...
pip show requests >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Requests installato
) else (
    echo ℹ️  Requests non necessario per funzionalità base
)

echo.
echo 📁 Creazione cartelle di lavoro...
if not exist "input_books" mkdir input_books
if not exist "translations" mkdir translations

echo.
echo ✅ Setup completato!
echo 💡 Ora puoi usare tutte le funzioni del translator

pause
goto MENU

:SMART_TRACKER
cls
echo 🎛️ SMART TRACKER MANAGEMENT
echo ══════════════════════════
echo.

if not exist "translations" (
    echo ❌ Nessun progetto trovato!
    echo 💡 Esegui prima il processamento (opzione 1)
    echo.
    pause
    goto MENU
)

echo 📊 OPZIONI SMART TRACKER:
echo ─────────────────────────
echo.
echo [1] ⚙️ Setup Tracker (Tutti i Progetti)
echo [2] 👁️ Monitora Tutti i Progetti  
echo [3] 📋 Lista Progetti con Tracker
echo [4] 🔄 Aggiorna Tutti i Tracker
echo [5] 🔙 Torna al Menu Principale
echo.
set /p tracker_choice="Scegli opzione (1-5): "

if "%tracker_choice%"=="1" (
    echo ⚙️ Setup Smart Tracker in tutti i progetti...
    if exist "tracker_manager.py" (
        python tracker_manager.py setup-all
    ) else (
        echo ❌ tracker_manager.py non trovato!
        echo 💡 Assicurati di avere tutti i file del sistema
    )
    pause
    goto SMART_TRACKER
)

if "%tracker_choice%"=="2" (
    echo 👁️ Avvio monitoraggio globale...
    echo 🛑 Premi Ctrl+C per fermare
    if exist "tracker_manager.py" (
        python tracker_manager.py monitor-all
    ) else (
        echo ❌ tracker_manager.py non trovato!
    )
    pause
    goto SMART_TRACKER
)

if "%tracker_choice%"=="3" (
    echo 📋 PROGETTI CON SMART TRACKER:
    echo ─────────────────────────────
    echo.
    for /d %%i in ("translations\*") do (
        if exist "%%i\smart_tracker.py" (
            echo ✅ %%~ni - Tracker attivo
        ) else (
            echo ⏳ %%~ni - Tracker non installato
        )
    )
    echo.
    pause
    goto SMART_TRACKER
)

if "%tracker_choice%"=="4" (
    echo 🔄 Aggiornamento tracker in corso...
    for /d %%i in ("translations\*") do (
        if exist "%%i\smart_tracker.py" (
            echo Aggiornando %%~ni...
            cd "%%i"
            python smart_tracker.py update
            cd ..\..
        )
    )
    echo ✅ Tutti i tracker aggiornati!
    pause
    goto SMART_TRACKER
)

if "%tracker_choice%"=="5" goto MENU

goto SMART_TRACKER

:DASHBOARD
cls
echo 📈 DASHBOARD GLOBALE
echo ═══════════════════════
echo.

if not exist "translations" (
    echo ❌ Nessuna traduzione trovata!
    echo.
    pause
    goto MENU
)

echo 📊 Generazione dashboard globale...

if exist "tracker_manager.py" (
    python tracker_manager.py dashboard
    
    if exist "translations\dashboard_globale.md" (
        echo ✅ Dashboard generato con successo!
        echo 📂 Apertura dashboard...
        start "" "translations\dashboard_globale.md"
    ) else (
        echo ❌ Errore nella generazione dashboard
    )
) else (
    echo ❌ tracker_manager.py non trovato!
    echo 💡 Assicurati di avere tutti i file del sistema
)

echo.
pause
goto MENU

:HELP
cls
echo ❓ GUIDA UNIVERSAL TRANSLATOR + SMART TRACKER
echo ═══════════════════════════════════════════════
echo.
echo 🎯 WORKFLOW COMPLETO CON SMART TRACKER:
echo ──────────────────────────────────────────
echo.
echo 1️⃣ [Prima volta] Setup e Dipendenze
echo 2️⃣ Metti file PDF/EPUB in input_books/
echo 3️⃣ Processa Tutti i File (crea progetti)
echo 4️⃣ Setup Smart Tracker (installa monitoraggio)
echo 5️⃣ Apri progetto e inizia traduzione
echo 6️⃣ Monitora progresso automaticamente!
echo.
echo 📊 SMART TRACKER FEATURES:
echo ──────────────────────────────
echo ✅ Rileva automaticamente progresso traduzione
echo ✅ Calcola statistiche live (caratteri, parole, tempo)
echo ✅ Genera report grafici con barre progresso
echo ✅ Monitora sessioni di traduzione
echo ✅ Dashboard globale per tutti i progetti
echo ✅ Stime tempo e velocità personalizzate
echo.
echo 🎛️ MONITORAGGIO AUTOMATICO:
echo ──────────────────────────────
echo • Aggiornamento ogni 30 secondi per progetto
echo • Dashboard globale ogni 60 secondi
echo • Statistiche live in tempo reale
echo • Backup automatico di tutti i progressi
echo.
echo 🚀 COMANDI TRACKER PER PROGETTO:
echo ──────────────────────────────────────
echo • tracker.bat - Interface grafica
echo • python smart_tracker.py update - Aggiorna una volta
echo • python smart_tracker.py monitor - Monitor continuo
echo • python smart_tracker.py session-start - Inizia sessione
echo • python smart_tracker.py session-end - Termina sessione
echo.
echo 📈 WORKFLOW SESSIONE TRADUZIONE:
echo ──────────────────────────────────────
echo 1. Vai nella cartella del progetto
echo 2. python smart_tracker.py session-start
echo 3. Traduci nel template_traduzione.md
echo 4. Tracker aggiorna automaticamente ogni 30 sec
echo 5. python smart_tracker.py session-end
echo 6. Vedi statistiche velocità personali!
echo.
echo 🎨 NUOVE CARATTERISTICHE:
echo ──────────────────────────────
echo ✅ Tracking automatico progresso
echo ✅ Statistiche personalizzate  
echo ✅ Dashboard multi-progetto
echo ✅ Sessioni di traduzione monitorate
echo ✅ Stime tempo accurate
echo ✅ Backup automatico completo
echo ✅ Interface grafiche integrate
echo.
echo 🆘 PROBLEMI COMUNI + TRACKER:
echo ─────────────────────────────────
echo • "tracker_manager.py non trovato" → Scarica file aggiornati
echo • "Smart Tracker non funziona" → Esegui Setup prima
echo • "Statistiche non aggiornate" → Salva template_traduzione.md
echo • "Dashboard vuoto" → Installa tracker nei progetti
echo.
echo 💡 SUGGERIMENTI PRO:
echo ──────────────────────
echo • Usa sessioni per tracciare velocità reale
echo • Controlla dashboard globale per priorità
echo • Monitora automatico durante traduzione
echo • Backup regolari cartella translations
echo.
pause
goto MENU

:EXIT
cls
echo.
echo 👋 Grazie per aver usato Universal Light Novel Translator!
echo.
echo 📚 Sistema Features:
echo    🔄 Processamento automatico PDF + EPUB
echo    📁 Progetti organizzati automaticamente  
echo    🎯 Template pronti per traduzione
echo    📊 Tracking progresso integrato
echo.
echo 🎌 Buona traduzione e buona lettura!
echo.
timeout /t 3 >nul
exit