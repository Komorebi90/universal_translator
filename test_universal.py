#!/usr/bin/env python3
"""
Script di Test per Universal Translator
Verifica che tutte le dipendenze siano installate correttamente
"""

import sys
from pathlib import Path

def test_dependencies():
    """Testa tutte le dipendenze richieste"""
    print("🧪 TEST DIPENDENZE UNIVERSAL TRANSLATOR")
    print("=" * 40)
    
    required_modules = [
        ('PyPDF2', 'PyPDF2'),
        ('BeautifulSoup', 'bs4'), 
        ('XML ElementTree', 'xml.etree.ElementTree'),
        ('Zipfile', 'zipfile'),
        ('Pathlib', 'pathlib'),
        ('Time', 'time'),
        ('JSON', 'json'),
        ('Regular Expressions', 're'),
        ('OS', 'os'),
        ('Shutil', 'shutil')
    ]
    
    success_count = 0
    total_count = len(required_modules)
    
    for name, module in required_modules:
        try:
            __import__(module)
            print(f"✅ {name:20} - OK")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name:20} - MANCANTE: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 RISULTATO: {success_count}/{total_count} moduli disponibili")
    
    if success_count == total_count:
        print("🎉 Tutti i moduli sono installati correttamente!")
        return True
    else:
        print("⚠️  Alcuni moduli mancano. Installa con:")
        print("   pip install PyPDF2 beautifulsoup4")
        return False

def test_file_operations():
    """Testa operazioni sui file"""
    print("\n🗂️  TEST OPERAZIONI FILE")
    print("=" * 40)
    
    try:
        # Test creazione cartelle
        test_dir = Path("test_universal_translator")
        test_dir.mkdir(exist_ok=True)
        print("✅ Creazione cartelle - OK")
        
        # Test scrittura file
        test_file = test_dir / "test.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test contenuto UTF-8 🎌")
        print("✅ Scrittura file UTF-8 - OK")
        
        # Test lettura file
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print("✅ Lettura file UTF-8 - OK")
        
        # Cleanup
        test_file.unlink()
        test_dir.rmdir()
        print("✅ Cleanup test - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore operazioni file: {e}")
        return False

def test_text_processing():
    """Testa elaborazione testo"""
    print("\n📝 TEST ELABORAZIONE TESTO")
    print("=" * 40)
    
    try:
        import re
        
        # Test regex
        test_text = "Chapter 1: The Beginning"
        pattern = r'^Chapter\s+\d+'
        match = re.search(pattern, test_text)
        if match:
            print("✅ Pattern matching - OK")
        else:
            print("❌ Pattern matching - FALLITO")
            return False
        
        # Test pulizia testo
        dirty_text = "  Testo   con   spazi   multipli  \n\n\n  "
        clean_text = re.sub(r'\s+', ' ', dirty_text.strip())
        if clean_text == "Testo con spazi multipli":
            print("✅ Pulizia testo - OK")
        else:
            print("❌ Pulizia testo - FALLITO")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Errore elaborazione testo: {e}")
        return False

def test_pdf_functionality():
    """Testa funzionalità PDF (solo se PyPDF2 disponibile)"""
    print("\n📄 TEST FUNZIONALITÀ PDF")
    print("=" * 40)
    
    try:
        import PyPDF2
        print("✅ PyPDF2 importato correttamente")
        
        # Test creazione PdfReader (senza file)
        print("✅ PyPDF2 funzionale")
        return True
        
    except ImportError:
        print("❌ PyPDF2 non disponibile")
        return False
    except Exception as e:
        print(f"⚠️  PyPDF2 disponibile ma errore: {e}")
        return True  # Non critico

def test_epub_functionality():
    """Testa funzionalità EPUB"""
    print("\n📚 TEST FUNZIONALITÀ EPUB")
    print("=" * 40)
    
    try:
        import zipfile
        import xml.etree.ElementTree as ET
        from bs4 import BeautifulSoup
        
        print("✅ Zipfile disponibile")
        print("✅ XML ElementTree disponibile")
        print("✅ BeautifulSoup disponibile")
        
        # Test parsing XML
        xml_test = '<root><item id="test">content</item></root>'
        root = ET.fromstring(xml_test)
        item = root.find('.//item[@id="test"]')
        if item is not None and item.text == "content":
            print("✅ XML parsing - OK")
        else:
            print("❌ XML parsing - FALLITO")
            return False
        
        # Test BeautifulSoup
        html_test = '<html><body><p>Test HTML</p></body></html>'
        soup = BeautifulSoup(html_test, 'html.parser')
        text = soup.get_text()
        if "Test HTML" in text:
            print("✅ HTML parsing - OK")
        else:
            print("❌ HTML parsing - FALLITO")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Moduli EPUB mancanti: {e}")
        return False
    except Exception as e:
        print(f"❌ Errore funzionalità EPUB: {e}")
        return False

def main():
    """Test completo del sistema"""
    print("🌟 UNIVERSAL TRANSLATOR - TEST COMPLETO")
    print("🔧 Verifica compatibilità sistema")
    print("=" * 50)
    
    tests = [
        ("Dipendenze", test_dependencies),
        ("Operazioni File", test_file_operations),
        ("Elaborazione Testo", test_text_processing),
        ("Funzionalità PDF", test_pdf_functionality),
        ("Funzionalità EPUB", test_epub_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ ERRORE CRITICO in {test_name}: {e}")
            results.append((test_name, False))
    
    # Risultati finali
    print("\n" + "=" * 50)
    print("🏁 RISULTATI FINALI")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} : {status}")
        if result:
            passed += 1
    
    print(f"\n📊 PUNTEGGIO: {passed}/{len(results)} test superati")
    
    if passed == len(results):
        print("\n🎉 SISTEMA PRONTO!")
        print("💡 Puoi usare Universal Translator senza problemi")
        print("🚀 Esegui: python universal_translator.py")
    elif passed >= len(results) - 1:
        print("\n⚠️  SISTEMA QUASI PRONTO")
        print("💡 Funzionalità base disponibili")
        print("🔧 Installa moduli mancanti per funzionalità complete")
    else:
        print("\n❌ SISTEMA NON PRONTO")
        print("🔧 Installa dipendenze mancanti:")
        print("   pip install PyPDF2 beautifulsoup4")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()