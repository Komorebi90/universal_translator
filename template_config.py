# FILENAME: template_config.py
# OPPURE: integrare queste classi in universal_translator.py

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