# 🌟 Universal Light Novel Translator

Sistema automatico per l'estrazione, organizzazione e gestione delle traduzioni di light novel da file PDF ed EPUB.

## 📋 Indice

- [Panoramica](#-panoramica)
- [Caratteristiche](#-caratteristiche)
- [Installazione](#-installazione)
- [Utilizzo Rapido](#-utilizzo-rapido)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Smart Tracker](#-smart-tracker)
- [Funzionalità Avanzate](#-funzionalità-avanzate)
- [Troubleshooting](#-troubleshooting)
- [Note Legali](#-note-legali)

## 🎯 Panoramica

**Universal Light Novel Translator** è un sistema completo che automatizza il processo di traduzione di light novel, gestendo automaticamente:

- **Estrazione intelligente** del testo da PDF ed EPUB
- **Organizzazione automatica** in progetti strutturati
- **Monitoraggio del progresso** con statistiche in tempo reale
- **Gestione multiprogetto** con dashboard globale
- **Interface user-friendly** per Windows

### Prima e Dopo

**❌ Prima (Manuale):**
```
File.pdf → Copia-incolla testo → Documento Word → Traduci tutto insieme → Confusione
```

**✅ Ora (Automatico):**
```
File.pdf → Progetto organizzato → Capitoli separati → Tracker progresso → Traduzione fluida
```

## ✨ Caratteristiche

### 🔄 Processamento Automatico
- **Multi-formato**: Supporta PDF ed EPUB nativamente
- **Rilevamento intelligente**: Estrae automaticamente capitoli e struttura
- **Cleanup automatico**: Rimuove header, footer e formattazione indesiderata
- **Titoli automatici**: Usa il nome del file come titolo del progetto

### 📊 Smart Tracker Integrato
- **Monitoraggio automatico**: Rileva progresso traduzione in tempo reale
- **Statistiche live**: Caratteri tradotti, velocità personale, tempo rimanente
- **Sessioni di lavoro**: Traccia tempo e produttività
- **Dashboard globale**: Overview di tutti i progetti contemporaneamente

### 🏗️ Organizzazione Professionale
- **Progetti separati**: Ogni libro diventa un progetto completo
- **Template pronti**: File già strutturati per iniziare subito
- **Backup automatico**: Testi originali sempre preservati
- **Struttura standardizzata**: Layout consistente e professionale

### 🖥️ Interface User-Friendly
- **Launcher Windows**: Menu grafico con tutte le funzioni
- **Setup automatico**: Controlla e installa dipendenze
- **Gestione progetti**: Apre, visualizza e gestisce tutto con un click

## 🛠️ Installazione

### Requisiti di Sistema
- **Windows 10/11** (il launcher è ottimizzato per Windows)
- **Python 3.7+** ([Download qui](https://python.org/downloads/))
- **Connessione internet** (per installazione dipendenze)

### Setup Automatico (Raccomandato)

1. **Scarica tutti i file** del progetto in una cartella
2. **Double-click** su `universal_launcher.bat`
3. **Scegli** `[4] 🛠️ Setup e Dipendenze`
4. **Attendi** l'installazione automatica
5. **Pronto!** Il sistema è configurato

### Setup Manuale (Alternativo)

```bash
# 1. Installa dipendenze Python
pip install PyPDF2 beautifulsoup4

# 2. Verifica installazione
python test_universal.py

# 3. Testa il sistema
python universal_translator.py
```

## 🚀 Utilizzo Rapido

### Traduzione in 5 Passi

1. **📥 Inserisci file**
   ```
   Metti i tuoi PDF/EPUB in: input_books/
   ```

2. **⚡ Processa automaticamente**
   ```
   Launcher → [1] Processa Tutti i File
   ```

3. **📊 Attiva tracking**
   ```
   Launcher → [6] Smart Tracker → Setup Tracker
   ```

4. **✍️ Inizia traduzione**
   ```
   Apri: translations/TuoLibro_PDF/template_traduzione.md
   ```

5. **📈 Monitora progresso**
   ```
   Launcher → [7] Dashboard Globale
   ```

### Workflow Tipico

```mermaid
graph LR
    A[File PDF/EPUB] --> B[input_books/]
    B --> C[Launcher: Processa]
    C --> D[Progetto Creato]
    D --> E[Template Traduzione]
    E --> F[Smart Tracker]
    F --> G[Dashboard Globale]
```

## 📁 Struttura del Progetto

### Layout Generale
```
universal_translator/
├── 📁 input_books/              # ← Metti qui i tuoi file
├── 📁 translations/             # ← Progetti creati automaticamente
├── 🐍 universal_translator.py   # ← Motore principale
├── 🐍 smart_tracker_system.py   # ← Sistema tracking
├── 🐍 tracker_manager.py        # ← Gestione globale
├── 🖥️ universal_launcher.bat    # ← Interface Windows
├── 🧪 test_universal.py         # ← Test sistema
└── 📚 README.md                 # ← Questa guida
```

### Progetto Singolo Creato
```
translations/Mushoku_Tensei_Vol1_PDF/
├── 📝 template_traduzione.md     # ← FILE PRINCIPALE PER TRADURRE
├── 📊 progress_tracker.md        # ← Tracker progresso manuale
├── ℹ️ info_progetto.md           # ← Informazioni e metadata
├── 📁 originale/                 # ← Testo estratto originale
├── 📁 capitoli/                  # ← Capitoli separati
├── 📁 traduzione/                # ← Risultato finale
├── 🎛️ smart_tracker.py          # ← Tracker automatico progetto
├── 🖥️ tracker.bat               # ← Interface tracker Windows
├── 📊 smart_tracker.json        # ← Database progresso (auto)
└── 📈 statistiche_live.md       # ← Report live (auto-generato)
```

## 🎛️ Smart Tracker

### Cos'è il Smart Tracker?

Il **Smart Tracker** è un sistema di monitoraggio automatico che:

- **Rileva automaticamente** quanto hai tradotto
- **Calcola statistiche** precise su progresso e velocità
- **Genera report** grafici in tempo reale
- **Stima tempi** rimanenti basati sulla tua velocità personale

### Come Funziona

```python
# Il tracker scansiona template_traduzione.md ogni 30 secondi
# Riconosce automaticamente:

❌ Placeholder: "[Inserisci qui la tua traduzione]"
✅ Testo tradotto: "Era una notte buia e tempestosa..."

# E aggiorna automaticamente:
⏳ Da fare → 🔄 In corso → ✅ Completato
```

### Modalità di Tracking

#### 1. **Aggiornamento Singolo**
```bash
python smart_tracker.py update
```
Aggiorna una volta e mostra statistiche.

#### 2. **Monitoraggio Continuo**
```bash
python smart_tracker.py monitor
```
Aggiorna automaticamente ogni 30 secondi.

#### 3. **Sessioni di Lavoro**
```bash
# Inizia sessione
python smart_tracker.py session-start

# [traduci normalmente...]

# Termina sessione  
python smart_tracker.py session-end
```
Traccia tempo di lavoro e calcola velocità personale.

#### 4. **Dashboard Globale**
```bash
python tracker_manager.py dashboard
```
Overview di tutti i progetti insieme.

### Esempio Output Tracker

```markdown
# 📊 STATISTICHE LIVE - Mushoku Tensei Vol 1

## 🎯 PANORAMICA GENERALE
| Metrica | Valore | Progresso |
|---------|--------|-----------|
| Completamento | 67.3% | ██████▓░░░ |
| Caratteri | 45,230 / 67,200 | 67.3% |
| Velocità Media | 156 char/min | Tua velocità |
| Tempo Rimanente | 2.4 ore | Stima personalizzata |

## 📚 DETTAGLIO CAPITOLI
| Capitolo | Stato | Completamento |
|----------|--------|---------------|
| L'Hikikomori | ✅ Completato | 100% ██████████ |
| Il Passato | ✅ Completato | 100% ██████████ |
| La Transizione | 🔄 In corso | 45% ████▓░░░░░ |
| Nuova Vita | ⏳ Da fare | 0% ░░░░░░░░░░ |
```

## 📝 Template di Traduzione Migliorati

### 🎯 Problema Risolto: Testo Completo nel Template

**❌ Problema precedente:**
- Template mostrava solo preview (1500 caratteri)
- Necessario aprire file capitoli separati
- Workflow inefficiente con più file aperti

**✅ Soluzione attuale:**
- **Testo originale completo** direttamente nel template
- **Divisione automatica** in sezioni per capitoli lunghi
- **Workflow fluido** - un solo file da gestire

### 📖 Esempio Nuovo Template

```markdown
## CAPITOLO 1 - L'HIKIKOMORI

### 📖 SEZIONE 1/3 - TESTO ORIGINALE
```
[Tutto il testo inglese della sezione qui - circa 4000 caratteri]
```

### 🇮🇹 SEZIONE 1/3 - TRADUZIONE ITALIANA
*[Inserisci qui la traduzione di questa sezione]*

### 📝 NOTE SEZIONE 1
*Note del traduttore, difficoltà, scelte linguistiche*

**📊 Stats Sezione 1:** 3,847 caratteri • 682 parole • ~26 min

---

### 📖 SEZIONE 2/3 - TESTO ORIGINALE
```
[Continua con la sezione successiva...]
```
```

### 🔧 Configurazione Personalizzabile

Ogni progetto include `template_config.json` per personalizzare:

```json
{
  "include_full_text": true,           // ← Testo completo nel template
  "auto_split_long_chapters": true,    // ← Dividi capitoli lunghi
  "split_threshold": 8000,             // ← Caratteri sopra cui dividere
  "target_section_size": 4000,         // ← Dimensione ideale sezione
  "include_notes_section": true,       // ← Sezioni note traduttore
  "include_stats": true                // ← Statistiche dettagliate
}
```

### 🎛️ Tipi di Template

#### Template Sezioni (Capitoli Lunghi >8000 caratteri)
- **Divisione automatica** in sezioni da ~4000 caratteri
- **Traduzione progressiva** sezione per sezione
- **Note separate** per ogni sezione
- **Statistiche dettagliate** per tracking micro-progresso

#### Template Integrale (Capitoli Normali)
- **Tutto il testo** in un blocco unico
- **Traduzione completa** in una volta
- **Note globali** per tutto il capitolo
- **Statistiche totali** del capitolo

## 🔧 Funzionalità Avanzate

### Launcher Windows Completo

Il `universal_launcher.bat` fornisce un menu completo:

```
🌟 UNIVERSAL LIGHT NOVEL TRANSLATOR
═══════════════════════════════════

[1] 🚀 Processa Tutti i File (Auto)    # ← Elabora tutto input_books/
[2] 📁 Apri Cartella Input              # ← Apre input_books/
[3] 📊 Visualizza Progetti              # ← Apre translations/
[4] 🛠️ Setup e Dipendenze              # ← Installa tutto automaticamente
[5] 📝 Apri Progetto Specifico          # ← Scegli e apri progetto
[6] 🎛️ Smart Tracker                   # ← Gestione tracking avanzato
[7] 📈 Dashboard Globale                # ← Overview tutti progetti
[8] ❓ Guida e Help                     # ← Documentazione integrata
[9] 🚪 Esci
```

### Gestione Multi-Progetto

```bash
# Setup tracker per tutti i progetti esistenti
python tracker_manager.py setup-all

# Monitora tutti i progetti contemporaneamente
python tracker_manager.py monitor-all

# Genera dashboard globale
python tracker_manager.py dashboard
```

### Personalizzazione

Il sistema è facilmente estendibile:

- **Glossari personalizzati**: Modifica `base_glossary` in `universal_translator.py`
- **Pattern capitoli**: Personalizza `chapter_patterns` per riconoscimento specifico
- **Template custom**: Modifica `create_translation_template()` per layout personalizzati
- **Statistiche avanzate**: Estendi `calculate_global_statistics()` per metriche custom

## 🐛 Troubleshooting

### Problemi Comuni

#### ❌ "Python non riconosciuto"
**Soluzione:**
1. Installa Python da [python.org](https://python.org/downloads/)
2. **IMPORTANTE**: Spunta "Add Python to PATH" durante installazione
3. Riavvia prompt dei comandi

#### ❌ "PyPDF2 non trovato"
**Soluzione:**
```bash
pip install PyPDF2 beautifulsoup4
```

#### ❌ "Nessun file trovato"
**Soluzione:**
1. Verifica che i file siano in `input_books/`
2. Controlla estensioni supportate: `.pdf`, `.epub`
3. Assicurati che i file non siano corrotti

#### ❌ "Tracker non aggiorna automaticamente"
**Soluzione:**
1. Salva `template_traduzione.md` dopo le modifiche
2. Verifica che `smart_tracker.py` sia presente nella cartella progetto
3. Riesegui setup tracker: `python tracker_manager.py setup-all`

#### ❌ "Estrazione PDF incompleta"
**Possibili cause:**
- PDF con testo come immagini (richiede OCR)
- PDF protetti da password
- PDF con encoding non standard

**Soluzioni:**
- Usa PDF text-based (no scansioni)
- Rimuovi password se presente
- Prova con EPUB dello stesso libro

#### ❌ "EPUB non si apre"
**Possibili cause:**
- EPUB corrotto o non standard
- Protezioni DRM

**Soluzioni:**
- Verifica integrità file EPUB
- Rimuovi DRM se necessario (legalmente)
- Prova con PDF dello stesso libro

### Log e Debug

```bash
# Test completo sistema
python test_universal.py

# Debug singolo file
python universal_translator.py --debug

# Verifica struttura EPUB
python -c "import zipfile; print(zipfile.ZipFile('file.epub').namelist())"
```

### Performance e Ottimizzazione

- **File grandi**: Il sistema gestisce automaticamente file fino a 500+ pagine
- **Memoria**: Usa circa 100MB RAM per libro medio
- **Velocità**: ~1-2 minuti per processamento completo libro standard
- **Storage**: Ogni progetto occupa ~5-10MB (include backup completi)

## ⚖️ Note Legali

### Uso Responsabile

Questo software è progettato per:

✅ **Traduzione personale** di opere possedute legalmente
✅ **Studio e comprensione** di testi in lingua straniera  
✅ **Backup e organizzazione** del proprio materiale
✅ **Progetti educativi** e di ricerca

### Limitazioni Importanti

❌ **Non distribuire** traduzioni di opere protette da copyright
❌ **Non utilizzare** per scopi commerciali senza autorizzazione
❌ **Rispettare** i diritti degli autori e degli editori

### Raccomandazioni

- **Acquista sempre** le opere originali per supportare gli autori
- **Verifica copyright** prima di tradurre opere recenti
- **Usa** principalmente per opere di dominio pubblico quando possibile
- **Considera** di contattare editori per traduzioni ufficiali

### Disclaimer

Gli sviluppatori di questo software:
- Non incoraggiano violazioni di copyright
- Non sono responsabili dell'uso improprio del software
- Raccomandano sempre il rispetto dei diritti d'autore
- Suggeriscono di consultare un legale per usi specifici

## 🆘 Supporto e Community

### Ottenere Aiuto

1. **Leggi questo README** - Copre la maggior parte dei casi
2. **Esegui test_universal.py** - Diagnostica problemi automaticamente
3. **Controlla troubleshooting** - Soluzioni ai problemi comuni
4. **Documenta il problema** - Con screenshot e messaggi di errore

### Contribuire

Il progetto è in sviluppo attivo! Contributi benvenuti:

- **Bug reports** con dettagli e screenshot
- **Miglioramenti** al codice e alla documentazione
- **Traduzioni** di questa guida in altre lingue
- **Test** su diversi formati di file

### Roadmap Futura

- 🔄 **Integrazione API** automatiche (DeepL, Google Translate)
- 📱 **Interface web** per uso multi-piattaforma
- 🎨 **Temi personalizzabili** per template
- 🌐 **Supporto lingue** multiple (non solo EN→IT)
- 📊 **Analytics avanzate** e reporting
- 🔗 **Cloud sync** per backup automatici

---

## 🎉 Conclusione

**Universal Light Novel Translator** trasforma la traduzione di light novel da un processo laborioso e disorganizzato in un workflow professionale e automatizzato.

### Vantaggi Chiave

✨ **Risparmio tempo**: Da ore di setup a minuti di configurazione
✨ **Organizzazione perfetta**: Progetti strutturati e professionali
✨ **Monitoraggio automatico**: Sempre sapere a che punto sei
✨ **Scalabilità**: Gestisci decine di progetti contemporaneamente
✨ **Facilità d'uso**: Interface intuitive per ogni livello

### Per Iniziare Subito

1. **Download** tutti i file del progetto
2. **Double-click** `universal_launcher.bat`
3. **Setup** automatico (opzione 4)
4. **Metti** i tuoi file in `input_books/`
5. **Processa** tutto (opzione 1)
6. **Inizia** a tradurre! 🎌

**Buona traduzione e buona lettura!** 📚✨

---

*README creato per Universal Light Novel Translator v2.0*  
*Ultima revisione: 2025*