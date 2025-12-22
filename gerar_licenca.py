"""
Script para gerar licenças para clientes
Uso: python gerar_licenca.py "Nome Cliente" "email@cliente.com" 365
"""

import sys
from license_manager import generate_license_for_customer

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python gerar_licenca.py \"Nome Cliente\" \"email@cliente.com\" [dias]")
        print("\nExemplo:")
        print('  python gerar_licenca.py "João Silva" "joao@email.com" 365')
        sys.exit(1)
    
    customer_name = sys.argv[1]
    customer_email = sys.argv[2]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 365
    
    generate_license_for_customer(customer_name, customer_email, days)

