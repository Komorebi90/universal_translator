#!/usr/bin/env python3
# FILENAME: universal_translator.py
"""
Universal Light Novel Translator
Gestisce automaticamente PDF ed EPUB da una cartella
Crea progetti organizzati per ogni libro
"""

import PyPDF2
import zipfile
import xml.etree.ElementTree as ET
import time
import json
import re
import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

class TemplateConfig:
    """Configurazione per personalizzare i template di traduzione"""
    
    def __init__(self):
        # Opzioni di layout
        self.include_full_text = True          # Include tutto il testo originale
        self.auto_split_long_chapters = True   # Dividi capitoli lunghi in sezioni
        self.split_threshold = 8000            # Caratteri sopra cui dividere
        self.target_section_size = 4000        # Dimensione target per sezione
        self.max_section_size = 6000           # Dimensione massima per sezione
        
        # Opzioni di contenuto
        self.include_stats = True              # Include statistiche dettagliate
        self.include_progress_tracking = True  # Include tracker progresso manuale
        self.include_notes_section = True      # Include sezione note traduttore
        self.include_glossary_hints = True     # Include suggerimenti glossario
        
        # Opzioni di formattazione
        self.use_section_dividers = True       # Usa separatori tra sezioni
        self.highlight_important_passages = True  # Evidenzia passaggi importanti
        self.include_page_references = True    # Include riferimenti pagine PDF
        
    def load_from_file(self, config_file):
        """Carica configurazione da file JSON"""
        if Path(config_file).exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                for key, value in config_data.items():
                    if hasattr(self, key):
                        setattr(self, key, value)
    
    def save_to_file(self, config_file):
        """Salva configurazione in file JSON"""
        config_data = {
            attr: getattr(self, attr) 
            for attr in dir(self) 
            if not attr.startswith('_') and not callable(getattr(self, attr))
        }
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)

class UniversalNovelTranslator:
    def __init__(self, input_folder="input_books", output_folder="translations"):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        
        # Crea cartelle se non esistono
        self.input_folder.mkdir(exist_ok=True)
        self.output_folder.mkdir(exist_ok=True)
        
        # Estensioni supportate
        self.supported_extensions = ['.pdf', '.epub']
        
        # Glossario termini base (espandibile)
        self.base_glossary = {
            "magic": "magia",
            "sword": "spada", 
            "adventurer": "avventuriero",
            "monster": "mostro",
            "labyrinth": "labirinto",
            "guild": "gilda",
            "knight": "cavaliere",
            "demon": "demone",
            "dragon": "drago",
            "princess": "principessa"
        }

    def scan_input_folder(self):
        """Scansiona cartella input per file supportati"""
        print(f"🔍 Scansione cartella: {self.input_folder}")
        
        found_files = []
        
        for file_path in self.input_folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                found_files.append(file_path)
                print(f"  📚 Trovato: {file_path.name}")
        
        if not found_files:
            print("❌ Nessun file PDF/EPUB trovato nella cartella input!")
            print(f"💡 Inserisci file in: {self.input_folder.absolute()}")
            
        return found_files

    def extract_title_from_filename(self, file_path):
        """Estrae titolo pulito dal nome file"""
        filename = file_path.stem  # Nome senza estensione
        
        # Pulizia del nome
        title = filename.replace('_', ' ').replace('-', ' ')
        title = re.sub(r'\s+', ' ', title)  # Normalizza spazi
        title = re.sub(r'[Vv]ol\.?\s*\d+', '', title)  # Rimuovi "Vol 1", "Volume 1", etc
        title = re.sub(r'[Cc]hapter\s*\d+', '', title)  # Rimuovi "Chapter 1", etc
        title = title.strip()
        
        # Capitalizza parole principali
        words = title.split()
        title = ' '.join(word.capitalize() for word in words)
        
        return title

    def create_project_folder(self, title, file_type):
        """Crea cartella progetto organizzata"""
        # Nome cartella sicuro
        safe_name = re.sub(r'[<>:"/\\|?*]', '', title)
        safe_name = safe_name.replace(' ', '_')
        
        project_folder = self.output_folder / f"{safe_name}_{file_type.upper()}"
        project_folder.mkdir(exist_ok=True)
        
        # Sottocartelle
        (project_folder / "originale").mkdir(exist_ok=True)
        (project_folder / "capitoli").mkdir(exist_ok=True)
        (project_folder / "traduzione").mkdir(exist_ok=True)
        
        return project_folder

    def extract_pdf_text(self, pdf_path):
        """Estrae testo da PDF"""
        print(f"📖 Estraendo testo da PDF: {pdf_path.name}")
        
        text_pages = {}
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    if text.strip():  # Solo pagine con contenuto
                        cleaned_text = self.clean_text(text)
                        text_pages[page_num + 1] = cleaned_text
                        
        except Exception as e:
            print(f"❌ Errore estrazione PDF: {e}")
            return None
            
        print(f"✅ Estratte {len(text_pages)} pagine con contenuto")
        return text_pages

    def extract_epub_text(self, epub_path):
        """Estrae testo da EPUB"""
        print(f"📖 Estraendo testo da EPUB: {epub_path.name}")
        
        chapters = {}
        
        try:
            with zipfile.ZipFile(epub_path, 'r') as epub:
                # Trova file spine (ordine capitoli)
                container = epub.read('META-INF/container.xml')
                container_root = ET.fromstring(container)
                
                # Trova OPF file
                rootfile_element = container_root.find('.//{urn:oasis:names:tc:opendocument:xmlns:container}rootfile')
                if rootfile_element is None:
                    print("❌ Impossibile trovare rootfile nel container.xml")
                    return None
                    
                opf_path = rootfile_element.get('full-path')
                if opf_path is None:
                    print("❌ Impossibile trovare full-path nel rootfile")
                    return None
                    
                opf_content = epub.read(opf_path)
                opf_root = ET.fromstring(opf_content)
                
                # Namespace handling
                namespaces = {'opf': 'http://www.idpf.org/2007/opf'}
                
                # Trova spine order
                spine_items = opf_root.findall('.//opf:spine/opf:itemref', namespaces)
                
                chapter_num = 1
                for item in spine_items:
                    item_id = item.get('idref')
                    if item_id is None:
                        continue
                    
                    # Trova file corrispondente
                    manifest_item = opf_root.find(f'.//opf:manifest/opf:item[@id="{item_id}"]', namespaces)
                    if manifest_item is not None:
                        href = manifest_item.get('href')
                        if href is None:
                            continue
                        
                        # Costruisci path completo
                        opf_dir = str(Path(opf_path).parent)
                        if opf_dir == '.':
                            file_path = href
                        else:
                            file_path = f"{opf_dir}/{href}"
                        
                        try:
                            content = epub.read(file_path).decode('utf-8')
                            
                            # Estrai testo da HTML
                            soup = BeautifulSoup(content, 'html.parser')
                            text = soup.get_text()
                            
                            if text.strip() and len(text.strip()) > 100:  # Solo capitoli sostanziali
                                cleaned_text = self.clean_text(text)
                                chapters[f"Capitolo_{chapter_num:02d}"] = {
                                    "title": f"Capitolo {chapter_num}",
                                    "text": cleaned_text
                                }
                                chapter_num += 1
                                
                        except Exception as e:
                            print(f"⚠️ Errore lettura {file_path}: {e}")
                            continue
                            
        except Exception as e:
            print(f"❌ Errore estrazione EPUB: {e}")
            return None
            
        print(f"✅ Estratti {len(chapters)} capitoli")
        return chapters if chapters else None

    def clean_text(self, text):
        """Pulisce testo estratto"""
        # Rimuovi header/footer comuni
        text = re.sub(r'\d+\s*\|\s*P\s*a\s*g\s*e', '', text)
        text = re.sub(r'Page\s*\|\s*\d+', '', text)
        
        # Normalizza spazi e newlines
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        return text.strip()

    def auto_detect_chapters_pdf(self, text_pages):
        """Rileva automaticamente capitoli in PDF"""
        chapters = {}
        current_chapter = 1
        chapter_text = ""
        
        # Pattern per rilevare inizi capitolo
        chapter_patterns = [
            r'^Chapter\s+\d+',
            r'^CHAPTER\s+\d+', 
            r'^\d+\.\s+[A-Z]',
            r'^[A-Z\s]{10,}$'  # Titoli in maiuscolo
        ]
        
        pages_per_chapter = max(10, len(text_pages) // 15)  # Stima capitoli
        
        current_pages = 0
        for page_num, text in text_pages.items():
            chapter_text += text + "\n\n"
            current_pages += 1
            
            # Controlla se è inizio nuovo capitolo
            is_chapter_break = False
            for pattern in chapter_patterns:
                if re.search(pattern, text[:200], re.MULTILINE):
                    is_chapter_break = True
                    break
            
            # Forza break ogni X pagine o se rilevato pattern
            if current_pages >= pages_per_chapter or is_chapter_break:
                if chapter_text.strip():
                    chapters[f"Capitolo_{current_chapter:02d}"] = {
                        "title": f"Capitolo {current_chapter}",
                        "text": chapter_text.strip(),
                        "pages": f"{page_num - current_pages + 1}-{page_num}"
                    }
                    current_chapter += 1
                    chapter_text = ""
                    current_pages = 0
        
        # Ultimo capitolo
        if chapter_text.strip():
            chapters[f"Capitolo_{current_chapter:02d}"] = {
                "title": f"Capitolo {current_chapter}",
                "text": chapter_text.strip(),
                "pages": f"{list(text_pages.keys())[-1]}"
            }
        
        return chapters

    def create_configurable_template(self, project_folder, title, chapters, file_type, config=None):
        """Crea template con configurazione personalizzabile"""
        
        if config is None:
            config = TemplateConfig()
        
        template_path = project_folder / "template_traduzione.md"
        
        with open(template_path, 'w', encoding='utf-8') as f:
            # Header del progetto
            f.write(f"# {title.upper()}\n")
            f.write(f"## Traduzione Personale - {file_type.upper()}\n\n")
            f.write("*Progetto di traduzione per uso personale*\n\n")
            
            if config.include_progress_tracking:
                f.write("## 📊 PROGRESSO GLOBALE\n")
                f.write("- [ ] Lettura completa\n")
                f.write("- [ ] Prima bozza traduzione\n") 
                f.write("- [ ] Revisione e correzioni\n")
                f.write("- [ ] Controllo finale\n\n")
            
            if config.include_glossary_hints:
                f.write("## 📝 NOTE DEL TRADUTTORE\n")
                f.write("*Usa questa sezione per glossario personale, note sui personaggi, terminologia ricorrente, ecc.*\n\n")
            
            f.write("---\n\n")
            
            for chapter_id, chapter_data in chapters.items():
                f.write(f"## {chapter_data['title'].upper()}\n")
                
                if config.include_page_references and 'pages' in chapter_data:
                    f.write(f"*Pagine: {chapter_data['pages']}*\n\n")
                
                chapter_text = chapter_data['text']
                char_count = len(chapter_text)
                
                # Decisione se dividere in sezioni
                should_split = (config.auto_split_long_chapters and 
                              char_count > config.split_threshold)
                
                if should_split:
                    sections = self.smart_split_chapter(chapter_text, config)
                    total_sections = len(sections)
                    
                    f.write(f"*Capitolo diviso in {total_sections} sezioni per facilità di traduzione*\n\n")
                    
                    for i, section in enumerate(sections, 1):
                        if config.use_section_dividers:
                            f.write(f"### 📖 SEZIONE {i}/{total_sections} - TESTO ORIGINALE\n")
                        else:
                            f.write(f"### 📖 TESTO ORIGINALE - PARTE {i}\n")
                        
                        f.write("```\n")
                        f.write(section)
                        f.write("\n```\n\n")
                        
                        f.write(f"### 🇮🇹 TRADUZIONE ITALIANA - SEZIONE {i}\n")
                        f.write("*[Inserisci qui la traduzione di questa sezione]*\n\n")
                        
                        if config.include_notes_section:
                            f.write(f"### 📝 NOTE SEZIONE {i}\n")
                            f.write("*Note del traduttore, difficoltà, scelte linguistiche, ecc.*\n\n")
                        
                        if config.include_stats:
                            section_chars = len(section)
                            section_words = len(section.split())
                            estimated_time = section_chars // 150
                            
                            f.write(f"**📊 Stats Sezione {i}:** {section_chars:,} caratteri • {section_words:,} parole • ~{estimated_time} min\n\n")
                        
                        if config.use_section_dividers:
                            f.write("---\n\n")
                else:
                    # Capitolo intero
                    f.write("### 📖 TESTO ORIGINALE COMPLETO\n")
                    f.write("```\n")
                    if config.include_full_text:
                        f.write(chapter_text)
                    else:
                        # Fallback al preview se configurato per non includere tutto
                        preview_text = chapter_text[:1500]
                        f.write(preview_text)
                        if len(chapter_text) > 1500:
                            f.write("\n\n[...CONTINUA NEL FILE CAPITOLO...]\n")
                    f.write("\n```\n\n")
                    
                    f.write("### 🇮🇹 TRADUZIONE ITALIANA COMPLETA\n")
                    f.write("*[Inserisci qui la tua traduzione completa]*\n\n")
                    
                    if config.include_notes_section:
                        f.write("### 📝 NOTE CAPITOLO\n")
                        f.write("*Note del traduttore per questo capitolo*\n\n")
                
                # Statistiche finali capitolo
                if config.include_stats:
                    word_count = len(chapter_text.split())
                    estimated_time = char_count // 150
                    
                    f.write("### 📊 STATISTICHE CAPITOLO\n")
                    f.write(f"- **Caratteri totali:** {char_count:,}\n")
                    f.write(f"- **Parole totali:** {word_count:,}\n")
                    f.write(f"- **Tempo stimato:** {estimated_time} minuti\n")
                    f.write(f"- **Difficoltà stimata:** {'🔴 Alta' if char_count > 10000 else '🟡 Media' if char_count > 5000 else '🟢 Bassa'}\n\n")
                
                if config.use_section_dividers:
                    f.write("=" * 60 + "\n\n")
        
        return template_path

    def smart_split_chapter(self, text, config):
        """Divisione intelligente capitoli con configurazione"""
        target_size = config.target_section_size
        max_size = config.max_section_size
        
        # Prova a dividere per paragrafi prima
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        sections = []
        current_section = ""
        
        for paragraph in paragraphs:
            potential_section = current_section + ("\n\n" if current_section else "") + paragraph
            
            if len(potential_section) > target_size and current_section:
                sections.append(current_section)
                current_section = paragraph
            else:
                current_section = potential_section
        
        if current_section:
            sections.append(current_section)
        
        # Controlla sezioni troppo lunghe
        final_sections = []
        for section in sections:
            if len(section) > max_size:
                # Dividi su frasi
                sentences = section.split('. ')
                current_subsection = ""
                
                for sentence in sentences:
                    potential = current_subsection + (". " if current_subsection else "") + sentence
                    if len(potential) > target_size and current_subsection:
                        final_sections.append(current_subsection + ".")
                        current_subsection = sentence
                    else:
                        current_subsection = potential
                
                if current_subsection:
                    if not current_subsection.endswith('.'):
                        current_subsection += "."
                    final_sections.append(current_subsection)
            else:
                final_sections.append(section)
        
        return final_sections

    def create_template_config_file(self, project_folder):
        """Crea file di configurazione template per il progetto"""
        config = TemplateConfig()
        config_file = project_folder / "template_config.json"
        config.save_to_file(config_file)
        
        # Crea anche file di spiegazione
        readme_config = project_folder / "template_config_README.md"
        with open(readme_config, 'w', encoding='utf-8') as f:
            f.write("""# Configurazione Template di Traduzione

## Come Personalizzare

Modifica `template_config.json` per personalizzare il template:

### Opzioni Layout
- `include_full_text`: Include tutto il testo originale (raccomandato: true)
- `auto_split_long_chapters`: Dividi capitoli lunghi automaticamente
- `split_threshold`: Caratteri sopra cui dividere (default: 8000)
- `target_section_size`: Dimensione ideale sezione (default: 4000)

### Opzioni Contenuto  
- `include_stats`: Include statistiche dettagliate
- `include_notes_section`: Include sezioni per note traduttore
- `include_glossary_hints`: Include suggerimenti glossario

### Opzioni Formattazione
- `use_section_dividers`: Usa separatori visivi
- `include_page_references`: Include riferimenti pagine PDF

## Rigenerare Template

Dopo aver modificato la configurazione:
```bash
python universal_translator.py --regenerate-template
```
""")
        
        return config_file

    def create_translation_template(self, project_folder, title, chapters, file_type):
        """Crea template traduzione migliorato con testo completo"""
        # Usa sempre la versione configurabile con impostazioni di default
        config = TemplateConfig()
        return self.create_configurable_template(project_folder, title, chapters, file_type, config)

    def save_individual_chapters(self, project_folder, chapters):
        """Salva capitoli singoli"""
        chapters_folder = project_folder / "capitoli"
        
        for chapter_id, chapter_data in chapters.items():
            filename = f"{chapter_id}_{chapter_data['title'].replace(' ', '_')}.txt"
            filepath = chapters_folder / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {chapter_data['title']}\n\n")
                if 'pages' in chapter_data:
                    f.write(f"Pagine: {chapter_data['pages']}\n\n")
                f.write(chapter_data['text'])

    def create_project_info(self, project_folder, title, file_type, original_file):
        """Crea file info progetto"""
        info_path = project_folder / "info_progetto.md"
        
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write(f"# Progetto Traduzione: {title}\n\n")
            f.write(f"## Informazioni\n")
            f.write(f"- **Titolo:** {title}\n")
            f.write(f"- **Formato:** {file_type.upper()}\n")
            f.write(f"- **File originale:** {original_file.name}\n")
            f.write(f"- **Data creazione:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## Struttura Progetto\n")
            f.write(f"```\n")
            f.write(f"{project_folder.name}/\n")
            f.write(f"├── template_traduzione.md    # File principale\n")
            f.write(f"├── info_progetto.md          # Questo file\n")
            f.write(f"├── progress_tracker.md       # Tracker progresso\n")
            f.write(f"├── originale/                # Testi estratti\n")
            f.write(f"├── capitoli/                 # Capitoli singoli\n")
            f.write(f"└── traduzione/               # Risultato finale\n")
            f.write(f"```\n\n")
            
            f.write(f"## Come Iniziare\n")
            f.write(f"1. Apri `template_traduzione.md`\n")
            f.write(f"2. Traduci sezione per sezione\n")
            f.write(f"3. Aggiorna `progress_tracker.md`\n")
            f.write(f"4. Salva versione finale in `traduzione/`\n")

    def create_progress_tracker(self, project_folder, chapters):
        """Crea tracker progresso"""
        tracker_path = project_folder / "progress_tracker.md"
        
        with open(tracker_path, 'w', encoding='utf-8') as f:
            f.write("# 📊 TRACKER PROGRESSO TRADUZIONE\n\n")
            
            total_chars = sum(len(ch['text']) for ch in chapters.values())
            total_words = sum(len(ch['text'].split()) for ch in chapters.values())
            
            f.write(f"## 📈 Statistiche Globali\n")
            f.write(f"- **Capitoli totali:** {len(chapters)}\n")
            f.write(f"- **Caratteri totali:** {total_chars:,}\n") 
            f.write(f"- **Parole totali:** {total_words:,}\n")
            f.write(f"- **Tempo stimato:** {total_chars // 150} minuti\n\n")
            
            f.write("## 📋 Progresso Capitoli\n\n")
            f.write("| Capitolo | Titolo | Caratteri | Stato | Note |\n")
            f.write("|----------|--------|-----------|-------|------|\n")
            
            for chapter_id, chapter_data in chapters.items():
                char_count = len(chapter_data['text'])
                f.write(f"| {chapter_id} | {chapter_data['title']} | {char_count:,} | ⏳ Da fare | |\n")
            
            f.write("\n## 🎯 Legenda Stati\n")
            f.write("- ⏳ Da fare\n")
            f.write("- 🔄 In corso\n")
            f.write("- ✅ Completato\n")
            f.write("- 🔍 In revisione\n")

    def process_single_file(self, file_path):
        """Processa singolo file (PDF o EPUB)"""
        print(f"\n🎯 Processando: {file_path.name}")
        
        # Estrai titolo e determina tipo
        title = self.extract_title_from_filename(file_path)
        file_type = file_path.suffix[1:].lower()  # pdf o epub
        
        print(f"📚 Titolo rilevato: {title}")
        print(f"📄 Formato: {file_type.upper()}")
        
        # Crea cartella progetto
        project_folder = self.create_project_folder(title, file_type)
        print(f"📁 Progetto creato: {project_folder.name}")
        
        # Inizializza chapters come None
        chapters = None
        
        # Estrai contenuto in base al formato
        if file_type == 'pdf':
            content = self.extract_pdf_text(file_path)
            if content:
                chapters = self.auto_detect_chapters_pdf(content)
        
        elif file_type == 'epub':
            chapters = self.extract_epub_text(file_path)
            
        else:
            print(f"❌ Formato non supportato: {file_type}")
            return False
        
        if not chapters:
            print(f"❌ Impossibile estrarre contenuto da {file_path.name}")
            return False
        
        print(f"✅ Rilevati {len(chapters)} capitoli")
        
        # Crea tutti i file del progetto
        template_path = self.create_translation_template(project_folder, title, chapters, file_type)
        self.save_individual_chapters(project_folder, chapters)
        self.create_project_info(project_folder, title, file_type, file_path)
        self.create_progress_tracker(project_folder, chapters)
        self.create_template_config_file(project_folder)  # Crea file configurazione
        
        # Salva testo originale
        original_path = project_folder / "originale" / f"{title.replace(' ', '_')}_originale.txt"
        with open(original_path, 'w', encoding='utf-8') as f:
            for chapter_id, chapter_data in chapters.items():
                f.write(f"# {chapter_data['title']}\n\n")
                f.write(chapter_data['text'])
                f.write("\n\n" + "="*50 + "\n\n")
        
        print(f"✅ Progetto completato: {project_folder.name}")
        print(f"📝 Template principale: template_traduzione.md")
        
        return True

    def process_all_files(self):
        """Processa tutti i file nella cartella input"""
        print("🚀 UNIVERSAL LIGHT NOVEL TRANSLATOR")
        print("=" * 50)
        
        # Scansiona file
        files = self.scan_input_folder()
        
        if not files:
            return
        
        print(f"\n📚 Trovati {len(files)} file da processare")
        
        successful = 0
        failed = 0
        
        for file_path in files:
            try:
                if self.process_single_file(file_path):
                    successful += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"❌ Errore processando {file_path.name}: {e}")
                failed += 1
        
        print(f"\n🎉 RISULTATI FINALI:")
        print(f"✅ Successi: {successful}")
        print(f"❌ Fallimenti: {failed}")
        print(f"📁 Progetti creati in: {self.output_folder.absolute()}")
        
        if successful > 0:
            print(f"\n💡 Apri le cartelle progetti e inizia con template_traduzione.md!")

def main():
    """Funzione principale"""
    print("🌟 UNIVERSAL LIGHT NOVEL TRANSLATOR")
    print("Gestisce automaticamente PDF ed EPUB")
    print("=" * 50)
    
    # Crea cartelle di default se non esistono
    input_folder = Path("input_books")
    input_folder.mkdir(exist_ok=True)
    
    print(f"📁 Cartella input: {input_folder.absolute()}")
    print("💡 Inserisci file PDF/EPUB nella cartella 'input_books'")
    
    if not any(input_folder.iterdir()):
        print("\n❌ Cartella input vuota!")
        print("📥 Aggiungi file PDF o EPUB e riprova")
        return
    
    # Avvia processamento
    translator = UniversalNovelTranslator()
    translator.process_all_files()

if __name__ == "__main__":
    main()