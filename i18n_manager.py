"""
Sistema de Internacionalização (i18n) - PinFlow Pro
Suporte multilíngue para alcance mundial
"""

import json
import os
import sys
from pathlib import Path

def get_base_path():
    """Retorna o caminho base para arquivos de recursos"""
    # Se executando como .exe (PyInstaller)
    if getattr(sys, 'frozen', False):
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = Path(sys._MEIPASS)
    else:
        # Executando como script Python normal
        base_path = Path(__file__).parent
    return base_path

class I18nManager:
    """Gerenciador de traduções"""
    
    LANGUAGES = {
        "pt_BR": "Português (Brasil)",
        "en_US": "English (US)",
        "es_ES": "Español (España)"
    }
    
    DEFAULT_LANGUAGE = "pt_BR"
    current_language = DEFAULT_LANGUAGE
    translations = {}
    
    @classmethod
    def load_translations(cls, language=None):
        """Carrega traduções para um idioma"""
        if language is None:
            language = cls.current_language
        
        # Tentar carregar do arquivo
        base_path = get_base_path()
        lang_file = base_path / "i18n" / f"{language}.json"
        if lang_file.exists():
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    cls.translations[language] = json.load(f)
                cls.current_language = language
                return True
            except Exception as e:
                print(f"Erro ao carregar tradução {language}: {e}")
        
        # Se não encontrou, usar português como fallback
        if language != cls.DEFAULT_LANGUAGE:
            return cls.load_translations(cls.DEFAULT_LANGUAGE)
        
        return False
    
    @classmethod
    def get_text(cls, key, default=None, **kwargs):
        """Obtém texto traduzido"""
        if cls.current_language not in cls.translations:
            cls.load_translations(cls.current_language)
        
        # Buscar tradução
        text = cls.translations.get(cls.current_language, {}).get(key, default)
        
        # Se não encontrou, usar a chave ou default
        if text is None:
            text = default if default else key
        
        # Substituir variáveis {var}
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass
        
        return text
    
    @classmethod
    def set_language(cls, language):
        """Define o idioma atual"""
        if language in cls.LANGUAGES:
            cls.current_language = language
            cls.load_translations(language)
            return True
        return False
    
    @classmethod
    def get_current_language(cls):
        """Retorna idioma atual"""
        return cls.current_language
    
    @classmethod
    def get_language_name(cls, code):
        """Retorna nome do idioma"""
        return cls.LANGUAGES.get(code, code)

