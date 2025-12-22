"""
Validação de Entrada - PinFlow Pro
Sanitização e validação de dados para segurança
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class InputValidator:
    """Validador de entrada de dados"""
    
    # Limites
    MAX_TITLE_LENGTH = 200
    MAX_NOTES_LENGTH = 10000
    MAX_TAGS = 20
    MAX_TAG_LENGTH = 50
    MAX_PATH_LENGTH = 500
    
    @staticmethod
    def sanitize_json_string(text):
        """
        Sanitiza string para prevenir injection em JSON
        
        Args:
            text: String a sanitizar
        
        Returns:
            str: String sanitizada
        """
        if not isinstance(text, str):
            return str(text) if text else ""
        
        # Remover caracteres de controle (exceto \n, \r, \t)
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Limitar tamanho
        if len(text) > InputValidator.MAX_NOTES_LENGTH:
            text = text[:InputValidator.MAX_NOTES_LENGTH]
        
        return text
    
    @staticmethod
    def validate_title(title):
        """
        Valida título do card
        
        Args:
            title: Título a validar
        
        Returns:
            tuple: (is_valid, message, sanitized_title)
        """
        if not title:
            return False, "Título não pode estar vazio", ""
        
        if not isinstance(title, str):
            title = str(title)
        
        # Sanitizar
        title = InputValidator.sanitize_json_string(title)
        
        # Limitar tamanho
        if len(title) > InputValidator.MAX_TITLE_LENGTH:
            title = title[:InputValidator.MAX_TITLE_LENGTH]
            return True, f"Título truncado para {InputValidator.MAX_TITLE_LENGTH} caracteres", title
        
        return True, "Título válido", title
    
    @staticmethod
    def validate_notes(notes):
        """
        Valida notas do card
        
        Args:
            notes: Notas a validar
        
        Returns:
            tuple: (is_valid, message, sanitized_notes)
        """
        if not notes:
            return True, "Notas vazias (válido)", ""
        
        if not isinstance(notes, str):
            notes = str(notes)
        
        # Sanitizar
        notes = InputValidator.sanitize_json_string(notes)
        
        # Limitar tamanho
        if len(notes) > InputValidator.MAX_NOTES_LENGTH:
            notes = notes[:InputValidator.MAX_NOTES_LENGTH]
            return True, f"Notas truncadas para {InputValidator.MAX_NOTES_LENGTH} caracteres", notes
        
        return True, "Notas válidas", notes
    
    @staticmethod
    def validate_file_path(file_path):
        """
        Valida caminho de arquivo
        
        Args:
            file_path: Caminho a validar
        
        Returns:
            tuple: (is_valid, message, sanitized_path)
        """
        if not file_path:
            return True, "Caminho vazio (válido)", ""
        
        if not isinstance(file_path, str):
            file_path = str(file_path)
        
        # Limitar tamanho
        if len(file_path) > InputValidator.MAX_PATH_LENGTH:
            return False, f"Caminho muito longo (máximo {InputValidator.MAX_PATH_LENGTH} caracteres)", ""
        
        # Verificar caracteres perigosos
        dangerous_chars = ['<', '>', '|', '?', '*', '"']
        for char in dangerous_chars:
            if char in file_path:
                return False, f"Caminho contém caracteres inválidos: {char}", ""
        
        # Verificar se é caminho absoluto válido (Windows)
        try:
            # Normalizar caminho
            path = Path(file_path)
            
            # Verificar se existe (opcional - pode não existir ainda)
            # if not path.exists():
            #     return False, "Arquivo ou pasta não existe", ""
            
            return True, "Caminho válido", str(path.absolute())
        except Exception as e:
            return False, f"Erro ao validar caminho: {str(e)}", ""
    
    @staticmethod
    def validate_tags(tags):
        """
        Valida lista de tags
        
        Args:
            tags: Lista de tags a validar
        
        Returns:
            tuple: (is_valid, message, sanitized_tags)
        """
        if not tags:
            return True, "Tags vazias (válido)", []
        
        if not isinstance(tags, list):
            return False, "Tags deve ser uma lista", []
        
        # Limitar quantidade
        if len(tags) > InputValidator.MAX_TAGS:
            tags = tags[:InputValidator.MAX_TAGS]
        
        sanitized_tags = []
        for tag in tags:
            if not isinstance(tag, str):
                tag = str(tag)
            
            # Remover caracteres especiais
            tag = re.sub(r'[^\w\s-]', '', tag)
            tag = tag.strip()
            
            # Limitar tamanho
            if len(tag) > InputValidator.MAX_TAG_LENGTH:
                tag = tag[:InputValidator.MAX_TAG_LENGTH]
            
            # Adicionar se não vazio e não duplicado
            if tag and tag not in sanitized_tags:
                sanitized_tags.append(tag)
        
        return True, f"{len(sanitized_tags)} tags válidas", sanitized_tags
    
    @staticmethod
    def validate_date(date_str, date_format="%Y-%m-%d"):
        """
        Valida data
        
        Args:
            date_str: String de data a validar
            date_format: Formato esperado
        
        Returns:
            tuple: (is_valid, message, datetime_object)
        """
        if not date_str:
            return True, "Data vazia (válido)", None
        
        if not isinstance(date_str, str):
            date_str = str(date_str)
        
        try:
            date_obj = datetime.strptime(date_str, date_format)
            return True, "Data válida", date_obj
        except ValueError:
            return False, f"Data inválida. Formato esperado: {date_format}", None
    
    @staticmethod
    def validate_time(time_str, time_format="%H:%M"):
        """
        Valida hora
        
        Args:
            time_str: String de hora a validar
            time_format: Formato esperado
        
        Returns:
            tuple: (is_valid, message, time_object)
        """
        if not time_str:
            return True, "Hora vazia (válido)", None
        
        if not isinstance(time_str, str):
            time_str = str(time_str)
        
        try:
            time_obj = datetime.strptime(time_str, time_format).time()
            return True, "Hora válida", time_obj
        except ValueError:
            return False, f"Hora inválida. Formato esperado: {time_format}", None
    
    @staticmethod
    def validate_card_data(card_data):
        """
        Valida dados completos de um card
        
        Args:
            card_data: Dicionário com dados do card
        
        Returns:
            tuple: (is_valid, message, sanitized_data)
        """
        if not isinstance(card_data, dict):
            return False, "Dados do card devem ser um dicionário", {}
        
        sanitized = {}
        
        # Validar título
        is_valid, msg, title = InputValidator.validate_title(card_data.get("titulo", ""))
        if not is_valid:
            return False, msg, {}
        sanitized["titulo"] = title
        
        # Validar notas
        is_valid, msg, notes = InputValidator.validate_notes(card_data.get("notas", ""))
        if not is_valid:
            return False, msg, {}
        sanitized["notas"] = notes
        
        # Validar caminho
        is_valid, msg, path = InputValidator.validate_file_path(card_data.get("caminho", ""))
        if not is_valid:
            return False, msg, {}
        sanitized["caminho"] = path
        
        # Validar tags
        is_valid, msg, tags = InputValidator.validate_tags(card_data.get("tags", []))
        if not is_valid:
            return False, msg, {}
        sanitized["tags"] = tags
        
        # Validar prioridade
        valid_priorities = ["Baixa", "Normal", "Alta", "Urgente"]
        priority = card_data.get("prioridade", "Normal")
        if priority not in valid_priorities:
            priority = "Normal"
        sanitized["prioridade"] = priority
        
        # Copiar outros campos (com sanitização básica)
        for key in ["alerta", "alerta_data", "alerta_hora", "data_criacao", "cor_custom"]:
            if key in card_data:
                value = card_data[key]
                if isinstance(value, str):
                    sanitized[key] = InputValidator.sanitize_json_string(value)
                else:
                    sanitized[key] = value
        
        return True, "Dados do card válidos", sanitized
    
    @staticmethod
    def validate_json_file(file_path):
        """
        Valida arquivo JSON antes de carregar
        
        Args:
            file_path: Caminho do arquivo JSON
        
        Returns:
            tuple: (is_valid, message, data)
        """
        if not os.path.exists(file_path):
            return False, "Arquivo não existe", None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validar estrutura básica
            if not isinstance(data, dict):
                return False, "JSON inválido: raiz deve ser um objeto", None
            
            return True, "JSON válido", data
        except json.JSONDecodeError as e:
            return False, f"Erro ao decodificar JSON: {str(e)}", None
        except Exception as e:
            return False, f"Erro ao ler arquivo: {str(e)}", None

