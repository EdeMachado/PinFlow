"""
Sistema de Licenciamento para PinFlow Pro
Gera, valida e gerencia licenças do software
"""

import hashlib
import json
import os
import platform
from datetime import datetime, timedelta
from pathlib import Path

class LicenseManager:
    """Gerenciador de licenças"""
    
    # Chave secreta para gerar/validar licenças (NUNCA EXPOR EM PRODUÇÃO!)
    # Em produção, usar variável de ambiente ou arquivo separado
    SECRET_KEY = "PINFLOW_PRO_2025_SECRET_KEY_EDE_MACHADO"
    
    LICENSE_FILE = "license.json"
    
    def __init__(self):
        self.license_data = None
        self.load_license()
    
    def get_hardware_id(self):
        """Gera Hardware ID único baseado no sistema"""
        try:
            # Coletar informações do sistema
            machine = platform.machine()
            processor = platform.processor()
            system = platform.system()
            node = platform.node()
            
            # Combinar informações
            hw_string = f"{machine}{processor}{system}{node}"
            
            # Gerar hash MD5
            hw_id = hashlib.md5(hw_string.encode()).hexdigest()
            return hw_id.upper()[:16]  # 16 caracteres
            
        except Exception as e:
            print(f"Erro ao gerar HWID: {e}")
            return "DEFAULT_HWID"
    
    def generate_license_key(self, customer_name="", customer_email="", days_valid=365):
        """
        Gera uma chave de licença
        
        Args:
            customer_name: Nome do cliente
            customer_email: Email do cliente
            days_valid: Dias de validade (padrão: 1 ano)
        
        Returns:
            str: Chave de licença
        """
        # Gerar dados da licença
        issue_date = datetime.now()
        expiry_date = issue_date + timedelta(days=days_valid)
        
        license_data = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "issue_date": issue_date.strftime("%Y-%m-%d"),
            "expiry_date": expiry_date.strftime("%Y-%m-%d"),
            "days_valid": days_valid,
            "version": "3.0"
        }
        
        # Criar string para hash
        license_string = json.dumps(license_data, sort_keys=True) + self.SECRET_KEY
        
        # Gerar hash
        license_hash = hashlib.sha256(license_string.encode()).hexdigest()
        
        # Formatar chave (4 grupos de 4 caracteres)
        license_key = f"{license_hash[:4]}-{license_hash[4:8]}-{license_hash[8:12]}-{license_hash[12:16]}".upper()
        
        # Salvar dados da licença (para validação)
        license_data["license_key"] = license_key
        license_data["hwid"] = None  # Será preenchido na ativação
        
        return license_key, license_data
    
    def validate_license_key(self, license_key):
        """
        Valida uma chave de licença
        
        Args:
            license_key: Chave a validar
        
        Returns:
            tuple: (is_valid, message, license_data)
        """
        try:
            # Normalizar chave (remover espaços e hífens)
            license_key = license_key.replace(" ", "").replace("-", "").upper()
            
            if len(license_key) != 16:
                return False, "Chave inválida: formato incorreto", None
            
            # Verificar se existe arquivo de licenças válidas
            # Em produção, isso viria de um servidor ou banco de dados
            valid_licenses_file = "valid_licenses.json"
            
            if os.path.exists(valid_licenses_file):
                with open(valid_licenses_file, 'r', encoding='utf-8') as f:
                    valid_licenses = json.load(f)
                
                # Procurar chave
                for lic_data in valid_licenses:
                    stored_key = lic_data.get("license_key", "").replace("-", "").upper()
                    if stored_key == license_key:
                        # Verificar validade
                        expiry_date = datetime.strptime(lic_data["expiry_date"], "%Y-%m-%d")
                        if datetime.now() > expiry_date:
                            return False, "Licença expirada", lic_data
                        
                        return True, "Licença válida", lic_data
            
            # Se não encontrou, retornar inválido
            return False, "Chave não encontrada ou inválida", None
            
        except Exception as e:
            return False, f"Erro ao validar: {str(e)}", None
    
    def activate_license(self, license_key):
        """
        Ativa uma licença no sistema atual
        
        Args:
            license_key: Chave de licença
        
        Returns:
            tuple: (success, message)
        """
        # Validar chave
        is_valid, message, license_data = self.validate_license_key(license_key)
        
        if not is_valid:
            return False, message
        
        # Obter HWID atual
        current_hwid = self.get_hardware_id()
        
        # Verificar se já está ativada em outro hardware
        if license_data.get("hwid") and license_data["hwid"] != current_hwid:
            return False, "Licença já ativada em outro computador"
        
        # Ativar licença
        license_data["hwid"] = current_hwid
        license_data["activated_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        license_data["activated"] = True
        
        # Salvar licença local
        self.license_data = license_data
        self.save_license()
        
        return True, "Licença ativada com sucesso!"
    
    def load_license(self):
        """Carrega licença salva localmente"""
        try:
            if os.path.exists(self.LICENSE_FILE):
                with open(self.LICENSE_FILE, 'r', encoding='utf-8') as f:
                    self.license_data = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar licença: {e}")
            self.license_data = None
    
    def save_license(self):
        """Salva licença localmente"""
        try:
            if self.license_data:
                with open(self.LICENSE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(self.license_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar licença: {e}")
    
    def check_license(self):
        """
        Verifica se há licença válida
        
        Returns:
            tuple: (is_valid, message)
        """
        if not self.license_data:
            return False, "Nenhuma licença encontrada"
        
        # Verificar HWID
        current_hwid = self.get_hardware_id()
        stored_hwid = self.license_data.get("hwid")
        
        if stored_hwid and stored_hwid != current_hwid:
            return False, "Licença não é válida para este computador"
        
        # Verificar validade
        expiry_date_str = self.license_data.get("expiry_date")
        if expiry_date_str:
            try:
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
                if datetime.now() > expiry_date:
                    return False, "Licença expirada"
            except:
                pass
        
        return True, "Licença válida"
    
    def get_license_info(self):
        """Retorna informações da licença atual"""
        if not self.license_data:
            return None
        
        return {
            "customer_name": self.license_data.get("customer_name", "N/A"),
            "customer_email": self.license_data.get("customer_email", "N/A"),
            "issue_date": self.license_data.get("issue_date", "N/A"),
            "expiry_date": self.license_data.get("expiry_date", "N/A"),
            "activated_date": self.license_data.get("activated_date", "N/A"),
            "hwid": self.license_data.get("hwid", "N/A"),
            "version": self.license_data.get("version", "3.0")
        }


def generate_license_for_customer(customer_name, customer_email, days=365):
    """
    Função auxiliar para gerar licença para cliente
    
    Uso: generate_license_for_customer("João Silva", "joao@email.com", 365)
    """
    manager = LicenseManager()
    license_key, license_data = manager.generate_license_key(
        customer_name, customer_email, days
    )
    
    # Salvar em arquivo de licenças válidas
    valid_licenses_file = "valid_licenses.json"
    valid_licenses = []
    
    if os.path.exists(valid_licenses_file):
        with open(valid_licenses_file, 'r', encoding='utf-8') as f:
            valid_licenses = json.load(f)
    
    valid_licenses.append(license_data)
    
    with open(valid_licenses_file, 'w', encoding='utf-8') as f:
        json.dump(valid_licenses, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"LICENÇA GERADA COM SUCESSO!")
    print(f"{'='*60}")
    print(f"Cliente: {customer_name}")
    print(f"Email: {customer_email}")
    print(f"Chave: {license_key}")
    print(f"Válida até: {license_data['expiry_date']}")
    print(f"{'='*60}\n")
    
    return license_key, license_data


if __name__ == "__main__":
    # Teste do sistema
    print("=== TESTE DO SISTEMA DE LICENCIAMENTO ===\n")
    
    manager = LicenseManager()
    
    # Gerar HWID
    hwid = manager.get_hardware_id()
    print(f"Hardware ID: {hwid}\n")
    
    # Gerar licença de teste
    print("Gerando licença de teste...")
    license_key, license_data = manager.generate_license_key(
        "Cliente Teste", "teste@email.com", 30
    )
    print(f"Chave gerada: {license_key}\n")
    
    # Validar licença
    print("Validando licença...")
    is_valid, message, data = manager.validate_license_key(license_key)
    print(f"Válida: {is_valid}")
    print(f"Mensagem: {message}\n")

