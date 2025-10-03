#!/usr/bin/env python3
"""
Translation management script for Flask-Notes
Extracts, updates and compiles translation files using pybabel
"""

import os
import sys
import subprocess
from pathlib import Path

# Configuration
LANGUAGES = ['de', 'en']
BABEL_CFG = 'babel.cfg'
POT_FILE = 'messages.pot'
TRANSLATIONS_DIR = 'translations'

def run_command(command, description):
    """Execute a command and show the result"""
    print(f"\n[INFO] {description}")
    print(f"Command: {command}")

    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"Success: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Command failed: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def extract_messages():
    """Extract all translatable strings from source code"""
    command = f"pybabel extract -F {BABEL_CFG} -k translate -k translate_lazy -o {POT_FILE} ."
    return run_command(command, "Extracting translatable strings from source code")

def init_language(lang):
    """Initialize a new language"""
    command = f"pybabel init -i {POT_FILE} -d {TRANSLATIONS_DIR} -l {lang}"
    return run_command(command, f"Initializing {lang.upper()} translations")

def update_language(lang):
    """Update an existing language and remove obsolete strings"""
    command = f"pybabel update -i {POT_FILE} -d {TRANSLATIONS_DIR} -l {lang} --ignore-obsolete"
    return run_command(command, f"Updating {lang.upper()} translations and removing obsolete strings")

def compile_language(lang):
    """Compile a language to .mo files"""
    command = f"pybabel compile -d {TRANSLATIONS_DIR} -l {lang}"
    return run_command(command, f"Compiling {lang.upper()} translations")

def cleanup_obsolete_strings(lang):
    """Remove obsolete strings from .po files"""
    po_file = Path(TRANSLATIONS_DIR) / lang / "LC_MESSAGES" / "messages.po"
    
    if not po_file.exists():
        return False
        
    print(f"\n[INFO] Cleaning up obsolete strings in {lang.upper()}")
    
    try:
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove obsolete entries (marked with #~ )
        lines = content.split('\n')
        cleaned_lines = []
        skip_obsolete = False
        
        for line in lines:
            if line.startswith('#~ '):
                skip_obsolete = True
                continue
            elif skip_obsolete and (line.startswith('msgid') or line.startswith('msgstr') or line.startswith('"')):
                if not line.strip():
                    skip_obsolete = False
                continue
            else:
                skip_obsolete = False
                cleaned_lines.append(line)
        
        # Write cleaned content back
        cleaned_content = '\n'.join(cleaned_lines)
        
        with open(po_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
            
        print(f"[SUCCESS] Obsolete strings removed from {lang.upper()}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to clean up obsolete strings: {e}")
        return False

def language_exists(lang):
    """Check if a language file already exists"""
    po_file = Path(TRANSLATIONS_DIR) / lang / "LC_MESSAGES" / "messages.po"
    return po_file.exists()

def main():
    """Main function to handle translation workflow"""
    print("Flask-Notes Translation Manager")
    print("=" * 40)

    # Check if we are in the correct directory
    if not os.path.exists(BABEL_CFG):
        print(f"[ERROR] {BABEL_CFG} not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)

    # Step 1: Extract translatable strings
    if not extract_messages():
        print("[ERROR] Failed to extract strings!")
        sys.exit(1)

    # Step 2: Update or initialize each language
    for lang in LANGUAGES:
        print(f"\n[INFO] Processing language: {lang.upper()}")

        if language_exists(lang):
            # Language exists - update it
            if not update_language(lang):
                print(f"[ERROR] Failed to update {lang}!")
                continue
        else:
            # New language - initialize it
            if not init_language(lang):
                print(f"[ERROR] Failed to initialize {lang}!")
                continue

        # Clean up obsolete strings
        cleanup_obsolete_strings(lang)

        # Compile translations
        if not compile_language(lang):
            print(f"[ERROR] Failed to compile {lang}!")

    print("\n[SUCCESS] Translation update completed!")
    print("\nNext steps:")
    print("1. Edit .po files in translations/*/LC_MESSAGES/")
    print("2. Add your translations for empty msgstr entries")
    print("3. Run this script again to compile changes")
    print("4. Restart Flask server for changes to take effect")

    # Show status summary
    print("\nTranslation status:")
    for lang in LANGUAGES:
        po_file = Path(TRANSLATIONS_DIR) / lang / "LC_MESSAGES" / "messages.po"
        mo_file = Path(TRANSLATIONS_DIR) / lang / "LC_MESSAGES" / "messages.mo"

        po_status = "OK" if po_file.exists() else "MISSING"
        mo_status = "OK" if mo_file.exists() else "MISSING"

        print(f"  {lang.upper()}: .po [{po_status}] | .mo [{mo_status}]")

if __name__ == "__main__":
    main()

