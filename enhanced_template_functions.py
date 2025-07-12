# FILENAME: enhanced_template_functions.py
# OPPURE: integrare queste funzioni in universal_translator.py

def create_enhanced_translation_template(self, project_folder, title, chapters, file_type):
    """Crea template traduzione con testo completo e sezioni gestibili"""
    template_path = project_folder / "template_traduzione.md"
    
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title.upper()}\n")
        f.write(f"## Traduzione Personale - {file_type.upper()}\n\n")
        f.write("*Progetto di traduzione per uso personale*\n\n")
        f.write("---\n\n")
        
        for chapter_id, chapter_data in chapters.items():
            f.write(f"## {chapter_data['title'].upper()}\n")
            
            if 'pages' in chapter_data:
                f.write(f"*Pagine: {chapter_data['pages']}*\n\n")
            
            chapter_text = chapter_data['text']
            char_count = len(chapter_text)
            
            # Se il capitolo è molto lungo (>8000 caratteri), dividilo in sezioni
            if char_count > 8000:
                f.write(f"*Capitolo lungo diviso in {self.calculate_sections(char_count)} sezioni per facilità di traduzione*\n\n")
                
                sections = self.split_chapter_into_sections(chapter_text)
                
                for i, section in enumerate(sections, 1):
                    f.write(f"### 📖 SEZIONE {i} - TESTO ORIGINALE\n")
                    f.write("```\n")
                    f.write(section)
                    f.write("\n```\n\n")
                    
                    f.write(f"### 🇮🇹 SEZIONE {i} - TRADUZIONE ITALIANA\n")
                    f.write("*[Inserisci qui la traduzione di questa sezione]*\n\n")
                    
                    # Statistiche sezione
                    section_chars = len(section)
                    section_words = len(section.split())
                    estimated_time = section_chars // 150
                    
                    f.write(f"**Sezione {i} Stats:** {section_chars:,} caratteri, {section_words:,} parole, ~{estimated_time} min\n\n")
                    f.write("---\n\n")
            else:
                # Capitolo normale - tutto insieme
                f.write("### 📖 TESTO ORIGINALE COMPLETO\n")
                f.write("```\n")
                f.write(chapter_text)
                f.write("\n```\n\n")
                
                f.write("### 🇮🇹 TRADUZIONE ITALIANA COMPLETA\n")
                f.write("*[Inserisci qui la tua traduzione completa]*\n\n")
            
            # Stats totali capitolo
            word_count = len(chapter_text.split())
            estimated_time = char_count // 150
            
            f.write("### 📊 STATISTICHE CAPITOLO TOTALI\n")
            f.write(f"- **Caratteri:** {char_count:,}\n")
            f.write(f"- **Parole:** {word_count:,}\n")
            f.write(f"- **Tempo stimato:** {estimated_time} minuti\n\n")
            
            f.write("=" * 60 + "\n\n")
    
    return template_path

def calculate_sections(self, char_count):
    """Calcola numero ottimale di sezioni"""
    target_section_size = 4000  # ~4000 caratteri per sezione
    return max(2, (char_count // target_section_size) + 1)

def split_chapter_into_sections(self, text):
    """Divide intelligentemente un capitolo in sezioni"""
    target_size = 4000
    sections = []
    
    # Dividi per paragrafi prima
    paragraphs = text.split('\n\n')
    
    current_section = ""
    
    for paragraph in paragraphs:
        # Se aggiungendo questo paragrafo supero la dimensione target
        if len(current_section) + len(paragraph) > target_size and current_section:
            sections.append(current_section.strip())
            current_section = paragraph
        else:
            if current_section:
                current_section += "\n\n" + paragraph
            else:
                current_section = paragraph
    
    # Aggiungi l'ultima sezione
    if current_section:
        sections.append(current_section.strip())
    
    # Se le sezioni sono ancora troppo lunghe, forza la divisione
    final_sections = []
    for section in sections:
        if len(section) > target_size * 1.5:  # Se ancora troppo lunga
            # Dividi forzatamente ogni target_size caratteri su spazi
            while len(section) > target_size:
                split_point = section.rfind(' ', 0, target_size)
                if split_point == -1:  # Nessuno spazio trovato
                    split_point = target_size
                final_sections.append(section[:split_point].strip())
                section = section[split_point:].strip()
            if section:  # Aggiungi il resto
                final_sections.append(section)
        else:
            final_sections.append(section)
    
    return final_sections

# Aggiorna anche il metodo principale per usare la nuova funzione
def create_translation_template(self, project_folder, title, chapters, file_type):
    """Crea template traduzione migliorato"""
    return self.create_enhanced_translation_template(project_folder, title, chapters, file_type)