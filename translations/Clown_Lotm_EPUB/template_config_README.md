# Configurazione Template di Traduzione

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
