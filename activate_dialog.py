"""
Dialog de Ativação de Licença - PinFlow Pro
Interface para o usuário ativar o software
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QMessageBox, QTextEdit,
                               QGroupBox, QFormLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from license_manager import LicenseManager

# Sistema de Internacionalização
try:
    from i18n_manager import I18nManager
    I18N_ENABLED = True
except ImportError:
    I18N_ENABLED = False
    class I18nManager:
        @staticmethod
        def get_text(key, default=None, **kwargs):
            return default if default else key

def _(key, default=None, **kwargs):
    """Função helper para obter texto traduzido"""
    if I18N_ENABLED:
        return I18nManager.get_text(key, default, **kwargs)
    return default if default else key

class ActivateDialog(QDialog):
    """Dialog para ativar licença"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.license_manager = LicenseManager()
        self.setup_ui()
        self.load_license_info()
    
    def setup_ui(self):
        """Configura interface"""
        self.setWindowTitle(_("license_activation_title", "🔐 Ativação - PinFlow Pro"))
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Título
        title = QLabel(_("license_activation_header", "🔐 Ativação de Licença"))
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a5f; padding: 10px;")
        layout.addWidget(title)
        
        # Informações
        info_label = QLabel(
            _("license_activation_info", "Digite sua chave de licença para ativar o PinFlow Pro.\nA chave foi enviada para seu email após a compra.")
        )
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(info_label)
        
        # Formulário
        form_group = QGroupBox(_("license_key_group", "Chave de Licença"))
        form_layout = QFormLayout()
        
        # Campo de chave
        self.license_input = QLineEdit()
        self.license_input.setPlaceholderText(_("license_key_placeholder", "XXXX-XXXX-XXXX-XXXX"))
        self.license_input.setMaxLength(19)  # 16 caracteres + 3 hífens
        self.license_input.textChanged.connect(self.format_license_key)
        form_layout.addRow(_("license_key_label", "Chave:"), self.license_input)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Informações da licença atual (se houver)
        self.license_info_group = QGroupBox(_("license_info", "Informações da Licença"))
        self.license_info_layout = QVBoxLayout()
        self.license_info_text = QTextEdit()
        self.license_info_text.setReadOnly(True)
        self.license_info_text.setMaximumHeight(150)
        self.license_info_layout.addWidget(self.license_info_text)
        self.license_info_group.setLayout(self.license_info_layout)
        self.license_info_group.setVisible(False)
        layout.addWidget(self.license_info_group)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        self.activate_btn = QPushButton(_("activate_button", "✅ Ativar"))
        self.activate_btn.clicked.connect(self.activate_license)
        self.activate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #8b9dc3);
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #152d4a, stop:1 #7a8bb0);
            }
        """)
        
        self.cancel_btn = QPushButton(_("cancel_button", "❌ Cancelar"))
        self.cancel_btn.clicked.connect(self.reject)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.activate_btn)
        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def format_license_key(self, text):
        """Formata chave de licença (adiciona hífens)"""
        # Remover hífens existentes
        text = text.replace("-", "").replace(" ", "").upper()
        
        # Adicionar hífens a cada 4 caracteres
        formatted = ""
        for i, char in enumerate(text):
            if i > 0 and i % 4 == 0:
                formatted += "-"
            formatted += char
        
        # Atualizar campo (evitar loop infinito)
        if formatted != self.license_input.text():
            self.license_input.blockSignals(True)
            self.license_input.setText(formatted)
            self.license_input.blockSignals(False)
    
    def load_license_info(self):
        """Carrega informações da licença atual"""
        info = self.license_manager.get_license_info()
        
        if info:
            info_text = f"""
<b>{_('customer_name', 'Cliente')}:</b> {info['customer_name']}<br>
<b>{_('customer_email', 'Email')}:</b> {info['customer_email']}<br>
<b>{_('issue_date', 'Emitida em')}:</b> {info['issue_date']}<br>
<b>{_('expiry_date', 'Válida até')}:</b> {info['expiry_date']}<br>
<b>{_('activated_date', 'Ativada em')}:</b> {info['activated_date']}<br>
<b>{_('hardware_id', 'Hardware ID')}:</b> {info['hwid']}
            """
            self.license_info_text.setHtml(info_text)
            self.license_info_group.setVisible(True)
        else:
            self.license_info_group.setVisible(False)
    
    def activate_license(self):
        """Ativa a licença"""
        license_key = self.license_input.text().strip()
        
        if not license_key:
            QMessageBox.warning(self, _("warning", "Aviso"), _("license_key_empty", "Por favor, digite sua chave de licença."))
            return
        
        # Remover hífens e espaços
        license_key = license_key.replace("-", "").replace(" ", "").upper()
        
        # Ativar
        success, message = self.license_manager.activate_license(license_key)
        
        if success:
            QMessageBox.information(
                self, 
                _("success", "Sucesso!"), 
                f"{message}\n\n{_('license_activation_success', 'O PinFlow Pro foi ativado com sucesso!')}"
            )
            self.load_license_info()
            self.accept()
        else:
            QMessageBox.critical(
                self, 
                _("error", "Erro"), 
                _("license_activation_failed", "Não foi possível ativar a licença:\n\n{message}\n\nVerifique se a chave está correta ou entre em contato com o suporte.").format(message=message)
            )

