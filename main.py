import sys
import json
import os
import csv
from datetime import datetime, timedelta
from pathlib import Path

# Validação de entrada
try:
    from validators import InputValidator
    VALIDATION_ENABLED = True
except ImportError:
    print("⚠️ Validação de entrada não disponível")
    VALIDATION_ENABLED = False

# Notificações Windows - DESABILITADAS (problemas com antivírus)
NOTIFICATIONS_AVAILABLE = False
NOTIFICATION_METHOD = None
print("⚠️ Notificações do Windows desabilitadas (apenas card pisca)")

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                               QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame,
                               QDialog, QLineEdit, QTextEdit, QComboBox, QSlider,
                               QSystemTrayIcon, QMenu, QDialogButtonBox, QMessageBox,
                               QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
                               QDateEdit, QTimeEdit, QGroupBox, QTabWidget)
from PySide6.QtCore import Qt, QMimeData, QPoint, QSize, Signal, QDate, QTime, QTimer
from PySide6.QtGui import QDrag, QPalette, QColor, QFont, QIcon, QKeySequence, QShortcut, QAction, QTextCharFormat
import PySide6

# Sistema de Licenciamento
try:
    from license_manager import LicenseManager
    from activate_dialog import ActivateDialog
    LICENSE_ENABLED = True
except ImportError:
    print("⚠️ Sistema de licenciamento não disponível")
    LICENSE_ENABLED = False

# Sistema de Internacionalização (i18n)
try:
    from i18n_manager import I18nManager
    I18N_ENABLED = True
    # Carregar idioma salvo ou usar padrão
    try:
        if os.path.exists("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
                lang = settings.get("language", "pt_BR")
                I18nManager.set_language(lang)
    except:
        pass
except ImportError:
    print("⚠️ Sistema de internacionalização não disponível")
    I18N_ENABLED = False
    # Fallback: criar função dummy
    class I18nManager:
        @staticmethod
        def get_text(key, default=None, **kwargs):
            return default if default else key
        @staticmethod
        def set_language(lang):
            return True
        @staticmethod
        def get_current_language():
            return "pt_BR"
        @staticmethod
        def get_language_name(code):
            return code
        LANGUAGES = {"pt_BR": "Português (Brasil)"}

# Importar para personalizar cor da barra de título no Windows
try:
    import ctypes
    from ctypes import wintypes
    DWMWA_CAPTION_COLOR = 35
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
except:
    pass  # Se não for Windows, ignora

DATA_FILE = "kanban.json"
ARCHIVE_FILE = "kanban_arquivo.json"

# Cores disponíveis para cards individuais (IGUAL POST-IT)
CARD_COLORS = {
    # Linha 1
    "Vermelho": "#ff4444",
    "Laranja Escuro": "#ff8800", 
    "Verde Lima": "#88cc00",
    "Verde": "#00aa66",
    "Ciano": "#00bcd4",
    "Azul": "#2196f3",
    "Roxo": "#9c27b0",
    "Cinza": "#757575",
    # Linha 2
    "Magenta": "#e91e63",
    "Amarelo Ouro": "#ffc107",
    "Amarelo": "#ffeb3b",
    "Verde Claro": "#8bc34a",
    "Ciano Claro": "#00e5ff",
    "Azul Claro": "#03a9f4",
    "Marrom": "#795548",
    "Cinza Claro": "#9e9e9e",
    # Linha 3
    "Rosa": "#f48fb1",
    "Pêssego": "#ffcc80",
    "Creme": "#fff9c4",
    "Verde Pastel": "#c5e1a5",
    "Azul Gelo": "#b3e5fc",
    "Azul Pastel": "#90caf9",
    "Lavanda": "#ce93d8",
    "Branco": "#ffffff"
}

# Prioridades com cores automáticas dos post-its
PRIORITIES = {
    "Baixa": {
        "color": "#4caf50", 
        "icon": "🔽",
        "postit_color": "#b4ff87"  # Verde claro
    },
    "Normal": {
        "color": "#2196F3", 
        "icon": "⚪",
        "postit_color": "#fff740"  # Amarelo padrão
    },
    "Alta": {
        "color": "#ff9800", 
        "icon": "🔶",
        "postit_color": "#ffb347"  # Laranja
    },
    "Urgente": {
        "color": "#f44336", 
        "icon": "🔴",
        "postit_color": "#ff87c3"  # Rosa/Vermelho
    }
}


class ArchivedDialog(QDialog):
    """Dialog para visualizar cards arquivados"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.archived_cards = []
        self.filtered_cards = []
        self.setup_ui()
        self.load_archived()
        
    def setup_ui(self):
        """Configura interface do dialog"""
        self.setWindowTitle("📂 Cards Arquivados")
        self.setModal(True)
        self.setMinimumSize(1000, 600)
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("📂 Histórico de Cards Arquivados")
        header.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("padding: 15px; background-color: #607d8b; color: white; border-radius: 5px;")
        layout.addWidget(header)
        
        # Estatísticas
        self.stats_group = QGroupBox("📊 Estatísticas")
        stats_layout = QHBoxLayout()
        
        self.total_label = QLabel("Total: 0")
        self.week_label = QLabel("Esta semana: 0")
        self.month_label = QLabel("Este mês: 0")
        
        for label in [self.total_label, self.week_label, self.month_label]:
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            label.setStyleSheet("padding: 10px; background-color: #e0e0e0; border-radius: 5px;")
            stats_layout.addWidget(label)
            
        self.stats_group.setLayout(stats_layout)
        layout.addWidget(self.stats_group)
        
        # Filtros
        filters_group = QGroupBox("🔍 Filtros")
        filters_layout = QHBoxLayout()
        
        # Busca por texto
        filters_layout.addWidget(QLabel("Buscar:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Digite para buscar...")
        self.search_input.textChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.search_input)
        
        # Filtro por data
        filters_layout.addWidget(QLabel("De:"))
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.dateChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.date_from)
        
        filters_layout.addWidget(QLabel("Até:"))
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.dateChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.date_to)
        
        # Filtro por prioridade
        filters_layout.addWidget(QLabel("Prioridade:"))
        self.priority_filter = QComboBox()
        self.priority_filter.addItem("Todas")
        for priority in PRIORITIES.keys():
            icon = PRIORITIES[priority]["icon"]
            self.priority_filter.addItem(f"{icon} {priority}")
        self.priority_filter.currentTextChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.priority_filter)
        
        filters_group.setLayout(filters_layout)
        layout.addWidget(filters_group)
        
        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Título", "Prioridade", "Tags", "Data Criação", "Data Arquivo", "Ações"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
            }
            QTableWidget::item:alternate {
                background-color: #f5f5f5;
            }
        """)
        layout.addWidget(self.table)
        
        # Botões inferiores
        buttons_layout = QHBoxLayout()
        
        export_btn = QPushButton("📤 Exportar CSV")
        export_btn.clicked.connect(self.export_csv)
        
        clear_btn = QPushButton("🗑️ Limpar Arquivo")
        clear_btn.clicked.connect(self.clear_archive)
        
        close_btn = QPushButton("✖ Fechar")
        close_btn.clicked.connect(self.accept)
        
        btn_style = """
            QPushButton {
                padding: 10px;
                font-weight: bold;
                border-radius: 5px;
                min-width: 120px;
            }
        """
        
        export_btn.setStyleSheet(btn_style + "QPushButton { background-color: #2196F3; color: white; }")
        clear_btn.setStyleSheet(btn_style + "QPushButton { background-color: #f44336; color: white; }")
        close_btn.setStyleSheet(btn_style + "QPushButton { background-color: #9e9e9e; color: white; }")
        
        buttons_layout.addWidget(export_btn)
        buttons_layout.addWidget(clear_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        
    def load_archived(self):
        """Carrega cards arquivados"""
        if os.path.exists(ARCHIVE_FILE):
            try:
                with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
                    self.archived_cards = json.load(f)
            except:
                self.archived_cards = []
        else:
            self.archived_cards = []
            
        self.filtered_cards = self.archived_cards.copy()
        self.update_stats()
        self.populate_table()
        
    def update_stats(self):
        """Atualiza estatísticas"""
        total = len(self.archived_cards)
        
        # Esta semana
        week_ago = datetime.now() - timedelta(days=7)
        week_count = sum(1 for card in self.archived_cards 
                        if datetime.strptime(card.get("data_arquivamento", "01/01/2000 00:00"), "%d/%m/%Y %H:%M") >= week_ago)
        
        # Este mês
        month_ago = datetime.now() - timedelta(days=30)
        month_count = sum(1 for card in self.archived_cards 
                         if datetime.strptime(card.get("data_arquivamento", "01/01/2000 00:00"), "%d/%m/%Y %H:%M") >= month_ago)
        
        self.total_label.setText(f"Total: {total}")
        self.week_label.setText(f"Esta semana: {week_count}")
        self.month_label.setText(f"Este mês: {month_count}")
        
    def apply_filters(self):
        """Aplica filtros"""
        search_text = self.search_input.text().lower()
        priority_filter = self.priority_filter.currentText()
        date_from = self.date_from.date().toPython()
        date_to = self.date_to.date().toPython()
        
        self.filtered_cards = []
        
        for card in self.archived_cards:
            # Filtro de busca
            if search_text:
                match = (search_text in card.get("titulo", "").lower() or
                        search_text in card.get("caminho", "").lower() or
                        search_text in card.get("notas", "").lower() or
                        any(search_text in tag.lower() for tag in card.get("tags", [])))
                if not match:
                    continue
            
            # Filtro de prioridade
            if priority_filter != "Todas":
                priority = priority_filter.split(" ", 1)[1]
                if card.get("prioridade", "Normal") != priority:
                    continue
            
            # Filtro de data
            try:
                card_date = datetime.strptime(card.get("data_arquivamento", "01/01/2000 00:00"), "%d/%m/%Y %H:%M").date()
                if not (date_from <= card_date <= date_to):
                    continue
            except:
                pass
            
            self.filtered_cards.append(card)
        
        self.populate_table()
        
    def populate_table(self):
        """Popula tabela com cards filtrados"""
        self.table.setRowCount(len(self.filtered_cards))
        
        for row, card in enumerate(self.filtered_cards):
            # Título
            title_item = QTableWidgetItem(card.get("titulo", ""))
            self.table.setItem(row, 0, title_item)
            
            # Prioridade
            priority = card.get("prioridade", "Normal")
            icon = PRIORITIES[priority]["icon"]
            priority_item = QTableWidgetItem(f"{icon} {priority}")
            priority_item.setBackground(QColor(PRIORITIES[priority]["postit_color"]))
            self.table.setItem(row, 1, priority_item)
            
            # Tags
            tags = ", ".join(card.get("tags", []))
            self.table.setItem(row, 2, QTableWidgetItem(tags))
            
            # Data criação
            self.table.setItem(row, 3, QTableWidgetItem(card.get("data_criacao", "")))
            
            # Data arquivamento
            self.table.setItem(row, 4, QTableWidgetItem(card.get("data_arquivamento", "")))
            
            # Botões de ação
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            restore_btn = QPushButton("↩️")
            restore_btn.setToolTip("Restaurar")
            restore_btn.setMaximumWidth(40)
            restore_btn.clicked.connect(lambda checked, r=row: self.restore_card(r))
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setToolTip("Deletar permanentemente")
            delete_btn.setMaximumWidth(40)
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_card(r))
            
            actions_layout.addWidget(restore_btn)
            actions_layout.addWidget(delete_btn)
            actions_widget.setLayout(actions_layout)
            
            self.table.setCellWidget(row, 5, actions_widget)
            
    def restore_card(self, row):
        """Restaura card arquivado"""
        if row >= len(self.filtered_cards):
            return
            
        card = self.filtered_cards[row]
        
        reply = QMessageBox.question(self, "Restaurar", 
                                     f"Restaurar '{card.get('titulo', '')}' para 'Concluído'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Remover do arquivo
            self.archived_cards.remove(card)
            self.save_archive()
            
            # Adicionar de volta na coluna Concluído
            if self.parent_window:
                # Remove data de arquivamento
                if "data_arquivamento" in card:
                    del card["data_arquivamento"]
                self.parent_window.col_completed.add_card(card)
                self.parent_window.save_data()
            
            # Atualizar dialog
            self.load_archived()
            QMessageBox.information(self, "Sucesso", "Card restaurado!")
            
    def delete_card(self, row):
        """Deleta card permanentemente"""
        if row >= len(self.filtered_cards):
            return
            
        card = self.filtered_cards[row]
        
        reply = QMessageBox.warning(self, "Atenção", 
                                    f"Deletar permanentemente '{card.get('titulo', '')}'?\n\nEsta ação não pode ser desfeita!",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.archived_cards.remove(card)
            self.save_archive()
            self.load_archived()
            QMessageBox.information(self, "Deletado", "Card removido permanentemente!")
            
    def export_csv(self):
        """Exporta para CSV"""
        if not self.filtered_cards:
            QMessageBox.information(self, "Info", "Nenhum card para exportar!")
            return
            
        filename, _ = QFileDialog.getSaveFileName(self, "Exportar CSV", "kanban_arquivados.csv", "CSV Files (*.csv)")
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Título", "Caminho", "Prioridade", "Tags", "Notas", "Data Criação", "Data Arquivamento"])
                    
                    for card in self.filtered_cards:
                        writer.writerow([
                            card.get("titulo", ""),
                            card.get("caminho", ""),
                            card.get("prioridade", ""),
                            ", ".join(card.get("tags", [])),
                            card.get("notas", ""),
                            card.get("data_criacao", ""),
                            card.get("data_arquivamento", "")
                        ])
                
                QMessageBox.information(self, "Sucesso", f"Exportado {len(self.filtered_cards)} cards para:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao exportar: {e}")
                
    def clear_archive(self):
        """Limpa todo o arquivo"""
        if not self.archived_cards:
            QMessageBox.information(self, "Info", "Arquivo já está vazio!")
            return
            
        reply = QMessageBox.warning(self, "ATENÇÃO", 
                                    f"Deletar TODOS os {len(self.archived_cards)} cards arquivados?\n\n⚠️ ESTA AÇÃO NÃO PODE SER DESFEITA!",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.archived_cards = []
            self.save_archive()
            self.load_archived()
            QMessageBox.information(self, "Limpo", "Todos os cards arquivados foram removidos!")
            
    def save_archive(self):
        """Salva arquivo"""
        with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.archived_cards, f, indent=2, ensure_ascii=False)


class CardDialog(QDialog):
    """Dialog para criar/editar cards"""
    
    def __init__(self, parent=None, card_data=None):
        super().__init__(parent)
        self.card_data = card_data
        self.setup_ui()
        
        if card_data:
            self.load_data(card_data)
            
    def setup_ui(self):
        """Configura interface do dialog"""
        self.setWindowTitle("✏️ Editar Card" if self.card_data else "➕ Novo Card")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout()
        
        # Título
        layout.addWidget(QLabel("📝 Título:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Digite o título do card...")
        layout.addWidget(self.title_input)
        
        # Caminho (opcional para criação manual)
        layout.addWidget(QLabel("📂 Caminho (opcional):"))
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Deixe vazio ou cole um caminho de arquivo/pasta...")
        layout.addWidget(self.path_input)
        
        # Notas com formatação
        notes_group = QGroupBox("📋 Notas")
        notes_layout = QVBoxLayout()
        
        # Barra de ferramentas de formatação para notas
        notes_toolbar = QHBoxLayout()
        
        self.notes_bold_btn = QPushButton("B")
        self.notes_bold_btn.setCheckable(True)
        self.notes_bold_btn.setMaximumWidth(35)
        self.notes_bold_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.notes_bold_btn.setToolTip("Negrito nas notas")
        self.notes_bold_btn.clicked.connect(self.apply_notes_bold)
        
        self.notes_italic_btn = QPushButton("I")
        self.notes_italic_btn.setCheckable(True)
        self.notes_italic_btn.setMaximumWidth(35)
        notes_italic_font = QFont("Arial", 11)
        notes_italic_font.setItalic(True)
        self.notes_italic_btn.setFont(notes_italic_font)
        self.notes_italic_btn.setToolTip("Itálico nas notas")
        self.notes_italic_btn.clicked.connect(self.apply_notes_italic)
        
        self.notes_underline_btn = QPushButton("U")
        self.notes_underline_btn.setCheckable(True)
        self.notes_underline_btn.setMaximumWidth(35)
        notes_underline_font = QFont("Arial", 11)
        notes_underline_font.setUnderline(True)
        self.notes_underline_btn.setFont(notes_underline_font)
        self.notes_underline_btn.setToolTip("Sublinhado nas notas")
        self.notes_underline_btn.clicked.connect(self.apply_notes_underline)
        
        format_btn_style = """
            QPushButton {
                padding: 5px;
                border: 2px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton:checked {
                background-color: #2196F3;
                color: white;
                border-color: #2196F3;
            }
            QPushButton:hover {
                border-color: #2196F3;
            }
        """
        
        self.notes_bold_btn.setStyleSheet(format_btn_style)
        self.notes_italic_btn.setStyleSheet(format_btn_style)
        self.notes_underline_btn.setStyleSheet(format_btn_style)
        
        notes_toolbar.addWidget(self.notes_bold_btn)
        notes_toolbar.addWidget(self.notes_italic_btn)
        notes_toolbar.addWidget(self.notes_underline_btn)
        notes_toolbar.addStretch()
        
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Adicione observações, links, detalhes...")
        self.notes_input.setMaximumHeight(100)
        
        notes_layout.addLayout(notes_toolbar)
        notes_layout.addWidget(self.notes_input)
        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)
        
        # === DATAS DO PROJETO (GANTT) ===
        gantt_group = QGroupBox("📊 Cronograma (Gantt)")
        gantt_layout = QHBoxLayout()
        
        # Data Início
        start_layout = QVBoxLayout()
        start_layout.addWidget(QLabel("📅 Data Início:"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setDisplayFormat("dd/MM/yyyy")
        self.start_date.setStyleSheet("""
            QDateEdit {
                color: #000000;
                background-color: white;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QDateEdit::drop-down {
                border: none;
            }
        """)
        start_layout.addWidget(self.start_date)
        
        # Data Fim
        end_layout = QVBoxLayout()
        end_layout.addWidget(QLabel("🏁 Data Fim:"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate().addDays(7))  # +7 dias por padrão
        self.end_date.setDisplayFormat("dd/MM/yyyy")
        self.end_date.setStyleSheet("""
            QDateEdit {
                color: #000000;
                background-color: white;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QDateEdit::drop-down {
                border: none;
            }
        """)
        end_layout.addWidget(self.end_date)
        
        gantt_layout.addLayout(start_layout)
        gantt_layout.addLayout(end_layout)
        gantt_layout.addStretch()
        
        gantt_group.setLayout(gantt_layout)
        layout.addWidget(gantt_group)
        
        # Alerta/Lembrete COM DATA E HORA
        alert_group = QGroupBox("⏰ Alerta/Lembrete (opcional)")
        alert_layout = QVBoxLayout()
        
        # Mensagem do alerta
        alert_layout.addWidget(QLabel("📝 Mensagem:"))
        self.alert_input = QLineEdit()
        self.alert_input.setPlaceholderText("Ex: Entregar relatório, Reunião importante...")
        alert_layout.addWidget(self.alert_input)
        
        # Data e Hora do alerta
        datetime_layout = QHBoxLayout()
        
        # Data
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("📅 Data:"))
        self.alert_date = QDateEdit()
        self.alert_date.setCalendarPopup(True)
        self.alert_date.setDate(QDate.currentDate())
        self.alert_date.setDisplayFormat("dd/MM/yyyy")
        self.alert_date.setStyleSheet("""
            QDateEdit {
                color: #000000;
                background-color: white;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QDateEdit::drop-down {
                border: none;
            }
        """)
        date_layout.addWidget(self.alert_date)
        
        # Hora
        time_layout = QVBoxLayout()
        time_layout.addWidget(QLabel("🕐 Hora:"))
        self.alert_time = QTimeEdit()
        self.alert_time.setDisplayFormat("HH:mm")
        self.alert_time.setTime(QTime.currentTime())
        self.alert_time.setStyleSheet("""
            QTimeEdit {
                color: #000000;
                background-color: white;
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QTimeEdit::drop-down {
                border: none;
            }
        """)
        time_layout.addWidget(self.alert_time)
        
        datetime_layout.addLayout(date_layout)
        datetime_layout.addLayout(time_layout)
        datetime_layout.addStretch()
        
        alert_layout.addLayout(datetime_layout)
        alert_group.setLayout(alert_layout)
        layout.addWidget(alert_group)
        
        # Prioridade (define cor automaticamente)
        layout.addWidget(QLabel("⚡ Prioridade (define a cor do post-it):"))
        self.priority_combo = QComboBox()
        for priority in PRIORITIES.keys():
            icon = PRIORITIES[priority]["icon"]
            self.priority_combo.addItem(f"{icon} {priority}")
        self.priority_combo.setCurrentText("⚪ Normal")
        layout.addWidget(self.priority_combo)
        
        # Tags
        layout.addWidget(QLabel("🏷️ Tags (separe por vírgula):"))
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Ex: urgente, trabalho, pessoal")
        layout.addWidget(self.tags_input)
        
        # === FORMATAÇÃO DE TEXTO ===
        format_group = QGroupBox("✏️ Formatação do Texto")
        format_layout = QHBoxLayout()
        
        # Negrito
        self.bold_checkbox = QPushButton("B")
        self.bold_checkbox.setCheckable(True)
        self.bold_checkbox.setMaximumWidth(40)
        self.bold_checkbox.setFont(QFont("Arial", 12, QFont.Bold))
        self.bold_checkbox.setToolTip("Negrito")
        self.bold_checkbox.setStyleSheet("""
            QPushButton {
                padding: 5px;
                border: 2px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton:checked {
                background-color: #2196F3;
                color: white;
                border-color: #2196F3;
            }
            QPushButton:hover {
                border-color: #2196F3;
            }
        """)
        
        # Itálico
        self.italic_checkbox = QPushButton("I")
        self.italic_checkbox.setCheckable(True)
        self.italic_checkbox.setMaximumWidth(40)
        italic_font = QFont("Arial", 12)
        italic_font.setItalic(True)
        self.italic_checkbox.setFont(italic_font)
        self.italic_checkbox.setToolTip("Itálico")
        self.italic_checkbox.setStyleSheet("""
            QPushButton {
                padding: 5px;
                border: 2px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton:checked {
                background-color: #2196F3;
                color: white;
                border-color: #2196F3;
            }
            QPushButton:hover {
                border-color: #2196F3;
            }
        """)
        
        # Sublinhado
        self.underline_checkbox = QPushButton("U")
        self.underline_checkbox.setCheckable(True)
        self.underline_checkbox.setMaximumWidth(40)
        underline_font = QFont("Arial", 12)
        underline_font.setUnderline(True)
        self.underline_checkbox.setFont(underline_font)
        self.underline_checkbox.setToolTip("Sublinhado")
        self.underline_checkbox.setStyleSheet("""
            QPushButton {
                padding: 5px;
                border: 2px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QPushButton:checked {
                background-color: #2196F3;
                color: white;
                border-color: #2196F3;
            }
            QPushButton:hover {
                border-color: #2196F3;
            }
        """)
        
        # Tamanho da fonte
        format_layout.addWidget(self.bold_checkbox)
        format_layout.addWidget(self.italic_checkbox)
        format_layout.addWidget(self.underline_checkbox)
        format_layout.addSpacing(20)
        
        format_layout.addWidget(QLabel("Tamanho:"))
        self.fontsize_combo = QComboBox()
        self.fontsize_combo.addItems(["8", "9", "10", "11", "12", "14", "16", "18", "20", "24"])
        self.fontsize_combo.setCurrentText("10")
        self.fontsize_combo.setMaximumWidth(60)
        format_layout.addWidget(self.fontsize_combo)
        
        format_layout.addStretch()
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def apply_notes_bold(self):
        """Aplica negrito no texto selecionado das notas"""
        cursor = self.notes_input.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontWeight(QFont.Bold if not fmt.fontWeight() == QFont.Bold else QFont.Normal)
            cursor.mergeCharFormat(fmt)
            self.notes_input.setTextCursor(cursor)
    
    def apply_notes_italic(self):
        """Aplica itálico no texto selecionado das notas"""
        cursor = self.notes_input.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontItalic(not fmt.fontItalic())
            cursor.mergeCharFormat(fmt)
            self.notes_input.setTextCursor(cursor)
    
    def apply_notes_underline(self):
        """Aplica sublinhado no texto selecionado das notas"""
        cursor = self.notes_input.textCursor()
        if cursor.hasSelection():
            fmt = cursor.charFormat()
            fmt.setFontUnderline(not fmt.fontUnderline())
            cursor.mergeCharFormat(fmt)
            self.notes_input.setTextCursor(cursor)
        
    def load_data(self, data):
        """Carrega dados existentes"""
        self.title_input.setText(data.get("titulo", ""))
        self.path_input.setText(data.get("caminho", ""))
        
        # Notas com HTML se existir formatação
        notes_html = data.get("notas_html", "")
        if notes_html:
            self.notes_input.setHtml(notes_html)
        else:
            self.notes_input.setPlainText(data.get("notas", ""))
        
        # Datas do projeto (Gantt)
        start_date_str = data.get("data_inicio", "")
        if start_date_str:
            try:
                date_parts = start_date_str.split("/")
                self.start_date.setDate(QDate(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])))
            except:
                self.start_date.setDate(QDate.currentDate())
        
        end_date_str = data.get("data_fim", "")
        if end_date_str:
            try:
                date_parts = end_date_str.split("/")
                self.end_date.setDate(QDate(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])))
            except:
                self.end_date.setDate(QDate.currentDate().addDays(7))
        
        # Alerta com data e hora
        self.alert_input.setText(data.get("alerta", ""))
        alert_date = data.get("alerta_data", "")
        if alert_date:
            try:
                date_parts = alert_date.split("/")
                self.alert_date.setDate(QDate(int(date_parts[2]), int(date_parts[1]), int(date_parts[0])))
            except:
                self.alert_date.setDate(QDate.currentDate())
        
        alert_time = data.get("alerta_hora", "")
        if alert_time:
            try:
                time_parts = alert_time.split(":")
                self.alert_time.setTime(QTime(int(time_parts[0]), int(time_parts[1])))
            except:
                self.alert_time.setTime(QTime.currentTime())
        
        priority = data.get("prioridade", "Normal")
        icon = PRIORITIES[priority]["icon"]
        self.priority_combo.setCurrentText(f"{icon} {priority}")
        
        tags = data.get("tags", [])
        self.tags_input.setText(", ".join(tags))
        
        # Formatação do título
        self.bold_checkbox.setChecked(data.get("fonte_negrito", False))
        self.italic_checkbox.setChecked(data.get("fonte_italico", False))
        self.underline_checkbox.setChecked(data.get("fonte_sublinhado", False))
        self.fontsize_combo.setCurrentText(str(data.get("fonte_tamanho", 10)))
        
    def get_data(self):
        """Retorna dados do formulário"""
        priority_text = self.priority_combo.currentText().split(" ", 1)[1]
        tags_text = self.tags_input.text().strip()
        tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
        
        # Cor automática baseada na prioridade
        postit_color = PRIORITIES[priority_text]["postit_color"]
        
        # Data e hora do alerta
        alert_date_str = self.alert_date.date().toString("dd/MM/yyyy") if self.alert_input.text().strip() else ""
        alert_time_str = self.alert_time.time().toString("HH:mm") if self.alert_input.text().strip() else ""
        
        # Datas do projeto (Gantt)
        start_date_str = self.start_date.date().toString("dd/MM/yyyy")
        end_date_str = self.end_date.date().toString("dd/MM/yyyy")
        
        return {
            "titulo": self.title_input.text().strip(),
            "caminho": self.path_input.text().strip(),
            "notas": self.notes_input.toPlainText().strip(),
            "notas_html": self.notes_input.toHtml(),  # Salvar HTML formatado
            "alerta": self.alert_input.text().strip(),
            "alerta_data": alert_date_str,
            "alerta_hora": alert_time_str,
            "alerta_lido": False,  # Novo campo para controlar se foi lido
            "prioridade": priority_text,
            "cor": postit_color,
            "tags": tags,
            "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
            # Datas do cronograma (Gantt)
            "data_inicio": start_date_str,
            "data_fim": end_date_str,
            # Formatação do título
            "fonte_negrito": self.bold_checkbox.isChecked(),
            "fonte_italico": self.italic_checkbox.isChecked(),
            "fonte_sublinhado": self.underline_checkbox.isChecked(),
            "fonte_tamanho": int(self.fontsize_combo.currentText())
        }


def get_event_pos(event):
    """Obtém posição do evento de forma compatível (PySide6 antigo/novo)"""
    if hasattr(event, 'position'):
        return event.position().toPoint()
    return event.pos()

class PostItCard(QFrame):
    """Cartão estilo post-it que pode ser arrastado"""
    
    def __init__(self, data, parent_column):
        super().__init__()
        self.data = data
        self.titulo = data.get("titulo", "Sem título")
        self.caminho = data.get("caminho", "")
        self.notas = data.get("notas", "")
        self.alerta = data.get("alerta", "")
        self.prioridade = data.get("prioridade", "Normal")
        # Cor pode ser custom ou baseada na prioridade
        self.cor_custom = data.get("cor_custom", None)
        self.cor = self.cor_custom if self.cor_custom else data.get("cor", PRIORITIES[self.prioridade]["postit_color"])
        self.tags = data.get("tags", [])
        self.data_criacao = data.get("data_criacao", datetime.now().strftime("%d/%m/%Y %H:%M"))
        # Formatação de texto
        self.fonte_tamanho = data.get("fonte_tamanho", 10)
        self.fonte_negrito = data.get("fonte_negrito", False)
        self.fonte_italico = data.get("fonte_italico", False)
        self.fonte_sublinhado = data.get("fonte_sublinhado", False)
        self.card_size = data.get("card_size", "medio")  # pequeno, medio, grande
        self.parent_column = parent_column
        self.drag_start_position = None
        self.resize_start = None
        self.resizing = False
        self.resize_edge = None  # None, 'right', 'bottom', 'corner'
        
        # Sistema de alertas
        self.alerta_data = data.get("alerta_data", "")
        self.alerta_hora = data.get("alerta_hora", "")
        self.alerta_ativo = False
        self.blink_state = False
        
        # Timer para verificar alertas (a cada 30 segundos)
        self.alert_timer = QTimer(self)
        self.alert_timer.timeout.connect(self.check_alert)
        self.alert_timer.start(30000)  # 30 segundos
        
        # Timer para piscar (quando alerta ativo)
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.toggle_blink)
        
        self.setup_ui()
        self.check_alert()  # Verificar imediatamente
        
    def setup_ui(self):
        """Configura visual do post-it"""
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setLineWidth(0)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Header com Prioridade + Título + Engrenagem (CANTO SUPERIOR DIREITO)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(5)
        
        # Prioridade
        priority_icon = PRIORITIES[self.prioridade]["icon"]
        priority_label = QLabel(priority_icon)
        priority_label.setFont(QFont("Segoe UI", 12))
        
        # Título
        self.title_label = QLabel(self.titulo)
        self.title_label.setWordWrap(True)
        self.apply_text_formatting(self.title_label)
        
        # Engrenagem (menu de opções) - CANTO SUPERIOR DIREITO
        self.gear_btn = QPushButton("⚙")
        self.gear_btn.setMaximumSize(QSize(20, 20))
        self.gear_btn.setToolTip("Opções do Card")
        self.gear_btn.setCursor(Qt.PointingHandCursor)
        # Garantir que o botão receba eventos de mouse
        self.gear_btn.setAttribute(Qt.WA_NoMouseReplay, False)
        self.gear_btn.setFocusPolicy(Qt.NoFocus)  # Não roubar foco
        self.gear_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
                font-weight: bold;
                color: rgba(0, 0, 0, 0.6);
            }
            QPushButton:hover {
                color: rgba(0, 0, 0, 0.9);
                transform: scale(1.2);
            }
        """)
        self.gear_btn.clicked.connect(self.show_menu)
        
        header_layout.addWidget(priority_label)
        header_layout.addWidget(self.title_label, stretch=1)
        header_layout.addWidget(self.gear_btn)
        
        # Tags - MAIS VISÍVEIS
        if self.tags:
            tags_layout = QHBoxLayout()
            tags_layout.setSpacing(5)
            for tag in self.tags[:3]:  # Máximo 3 tags visíveis
                tag_label = QLabel(f"#{tag}")
                tag_label.setStyleSheet("""
                    background-color: rgba(0, 0, 0, 0.7);
                    color: white;
                    padding: 4px 10px;
                    border-radius: 10px;
                    font-size: 10px;
                    font-weight: bold;
                """)
                tags_layout.addWidget(tag_label)
            tags_layout.addStretch()
            
        # Caminho (se existir) - CLICÁVEL
        if self.caminho:
            path_label = QLabel(self.caminho)
            path_label.setWordWrap(True)
            path_label.setFont(QFont("Segoe UI", 8))
            path_label.setStyleSheet("""
                color: #0066cc; 
                text-decoration: underline;
                cursor: pointer;
            """)
            path_label.setCursor(Qt.PointingHandCursor)
            path_label.mousePressEvent = lambda event: self.open_folder()
            path_label.setToolTip("Clique para abrir a pasta")
            
            # Ícone de pasta ao lado
            folder_icon = QLabel("📁")
            folder_icon.setFont(QFont("Segoe UI", 10))
            
            path_layout = QHBoxLayout()
            path_layout.addWidget(folder_icon)
            path_layout.addWidget(path_label, stretch=1)
            path_layout.setSpacing(5)
        
        # Notas (preview) - COM TOOLTIP COMPLETO
        if self.notas:
            notes_preview = self.notas[:50] + "..." if len(self.notas) > 50 else self.notas
            self.notes_label = QLabel(f"💭 {notes_preview}")
            self.notes_label.setWordWrap(True)
            self.notes_label.setFont(QFont("Segoe UI", 8))
            self.notes_label.setStyleSheet("color: #555; font-style: italic;")
            
            # TOOLTIP com nota completa (preview ao passar o mouse)
            self.notes_label.setToolTip(f"📝 NOTA COMPLETA:\n\n{self.notas}")
        
        # Alerta (se existir) - DESTACADO
        if self.alerta:
            alert_label = QLabel(f"⚠️ {self.alerta}")
            alert_label.setWordWrap(True)
            alert_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
            alert_label.setStyleSheet("""
                color: #d32f2f; 
                background-color: rgba(255, 235, 59, 0.3);
                padding: 5px;
                border-radius: 3px;
                border-left: 3px solid #d32f2f;
            """)
        
        # RODAPÉ com Data
        footer_layout = QHBoxLayout()
        footer_layout.setSpacing(5)
        
        # Data
        date_label = QLabel(f"🕐 {self.data_criacao}")
        date_label.setFont(QFont("Segoe UI", 7))
        date_label.setStyleSheet("color: #999;")
        
        footer_layout.addWidget(date_label, stretch=1)
        
        # Montar layout
        layout.addLayout(header_layout)
        if self.tags:
            layout.addLayout(tags_layout)
        if self.alerta:
            layout.addWidget(alert_label)
        if self.caminho:
            layout.addLayout(path_layout)
        if self.notas:
            layout.addWidget(self.notes_label)
        layout.addLayout(footer_layout)  # Rodapé com data
        
        self.setLayout(layout)
        
        # Aplicar tamanho do card
        self.apply_card_size()
        
        # Aplicar estilo baseado no tema
        self.update_card_style()
        
        self.setCursor(Qt.OpenHandCursor)
        
        # Habilitar mouse tracking para resize
        self.setMouseTracking(True)
        
        # TOOLTIP NO CARD INTEIRO mostrando nota completa
        if self.notas:
            tooltip_text = f"📝 NOTA COMPLETA:\n\n{self.notas}"
            self.setToolTip(tooltip_text)
        
        # Navegação por teclado
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_KeyboardFocusChange, True)
    
    def update_card_style(self):
        """Atualiza estilo do card baseado no tema"""
        border_color = PRIORITIES[self.prioridade]["color"]
        
        # Verificar se está em modo escuro
        if hasattr(self.parent_column, 'window') and hasattr(self.parent_column.window, 'dark_mode') and self.parent_column.window.dark_mode:
            # MODO ESCURO - Cards com fundo mais escuro mas mantendo cores
            # Escurecer a cor do card mantendo o tom
            dark_cor = self.darken_color(self.cor, 0.3)  # 30% mais escuro
            
            self.setStyleSheet(f"""
                PostItCard {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 {dark_cor}, stop:1 {self.darken_color(self.cor, 0.5)});
                    border-left: 5px solid {border_color};
                    border-right: 1px solid #1a1a1a;
                    border-top: 1px solid #1a1a1a;
                    border-bottom: 1px solid #1a1a1a;
                    border-radius: 5px;
                    min-height: 80px;
                    color: #e0e0e0;
                }}
                PostItCard:hover {{
                    filter: brightness(1.2);
                    border-left: 5px solid {border_color};
                    border-right: 2px solid #2d2d2d;
                    border-top: 2px solid #2d2d2d;
                    border-bottom: 2px solid #2d2d2d;
                }}
                QLabel {{
                    color: #e0e0e0;
                    background-color: transparent;
                }}
            """)
        else:
            # MODO CLARO - Visual original vibrante
            self.setStyleSheet(f"""
                PostItCard {{
                    background-color: {self.cor};
                    border-left: 5px solid {border_color};
                    border-right: 1px solid #e6d000;
                    border-top: 1px solid #e6d000;
                    border-bottom: 1px solid #e6d000;
                    border-radius: 5px;
                    min-height: 80px;
                }}
                PostItCard:hover {{
                    background-color: {self.cor};
                    filter: brightness(1.1);
                    border-left: 5px solid {border_color};
                    border-right: 2px solid #ccaa00;
                    border-top: 2px solid #ccaa00;
                    border-bottom: 2px solid #ccaa00;
                }}
            """)
    
    def darken_color(self, hex_color, factor=0.3):
        """Escurece uma cor hex por um fator (0.0 a 1.0)"""
        # Remove o # se existir
        hex_color = hex_color.lstrip('#')
        
        # Converte para RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        # Escurece
        r = int(r * (1 - factor))
        g = int(g * (1 - factor))
        b = int(b * (1 - factor))
        
        # Converte de volta para hex
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def get_resize_edge(self, pos):
        """Detecta se está na borda para resize"""
        margin = 10  # Margem para detectar borda
        rect = self.rect()
        
        on_right = abs(pos.x() - rect.right()) < margin
        on_bottom = abs(pos.y() - rect.bottom()) < margin
        
        if on_right and on_bottom:
            return 'corner'
        elif on_right:
            return 'right'
        elif on_bottom:
            return 'bottom'
        return None
    
    def update_cursor_for_resize(self, edge):
        """Atualiza cursor baseado na borda"""
        if edge == 'corner':
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge == 'right':
            self.setCursor(Qt.SizeHorCursor)
        elif edge == 'bottom':
            self.setCursor(Qt.SizeVerCursor)
        else:
            if not self.resizing:
                self.setCursor(Qt.OpenHandCursor)
    
    def apply_text_formatting(self, label):
        """Aplica formatação de texto ao label"""
        font = QFont("Segoe UI", self.fonte_tamanho)
        font.setBold(self.fonte_negrito or True)  # Título sempre em negrito
        font.setItalic(self.fonte_italico)
        font.setUnderline(self.fonte_sublinhado)
        label.setFont(font)
    
    def check_alert(self):
        """Verifica se o alerta deve ser ativado"""
        if not self.alerta or not self.alerta_data or not self.alerta_hora:
            return
        
        # Se já foi lido, não fazer nada
        if self.data.get("alerta_lido", False):
            return
        
        try:
            # Montar datetime do alerta
            data_parts = self.alerta_data.split("/")
            hora_parts = self.alerta_hora.split(":")
            
            alert_datetime = datetime(
                int(data_parts[2]),  # ano
                int(data_parts[1]),  # mês
                int(data_parts[0]),  # dia
                int(hora_parts[0]),  # hora
                int(hora_parts[1]) if len(hora_parts) > 1 else 0  # minuto
            )
            
            now = datetime.now()
            
            # Se passou do horário do alerta E ainda não foi notificado
            if now >= alert_datetime and not self.alerta_ativo:
                self.alerta_ativo = True
                self.blink_timer.start(500)  # Piscar a cada 500ms
                print(f"⏰ ALERTA ATIVADO: {self.titulo}")
                print(f"   Data/Hora alerta: {self.alerta_data} {self.alerta_hora}")
                print(f"   Data/Hora atual: {now.strftime('%d/%m/%Y %H:%M')}")
                
                # 🔔 ENVIAR NOTIFICAÇÃO DO WINDOWS
                print(f"   Tentando enviar notificação...")
                print(f"   NOTIFICATIONS_AVAILABLE = {NOTIFICATIONS_AVAILABLE}")
                print(f"   NOTIFICATION_METHOD = {NOTIFICATION_METHOD}")
                self.send_windows_notification()
            
        except Exception as e:
            print(f"❌ Erro ao verificar alerta: {e}")
            import traceback
            traceback.print_exc()
    
    def send_windows_notification(self):
        """Envia notificação nativa do Windows em thread separada"""
        import threading
        
        def _send_notification():
            global NOTIFICATIONS_AVAILABLE, NOTIFICATION_METHOD
            
            print(f"\n🔔 === INICIANDO ENVIO DE NOTIFICAÇÃO ===")
            print(f"   Card: {self.titulo}")
            print(f"   NOTIFICATION_METHOD: {NOTIFICATION_METHOD}")
            
            if not NOTIFICATIONS_AVAILABLE:
                print("❌ Notificações não disponíveis")
                return
            
            try:
                # Preparar mensagem
                titulo_notif = f"⏰ {self.titulo}"
                mensagem_notif = self.alerta
                
                # Adicionar data/hora
                if self.alerta_data and self.alerta_hora:
                    mensagem_notif += f"\n📅 {self.alerta_data} às {self.alerta_hora}"
                
                # Adicionar notas (primeiras 100 caracteres)
                if self.notas:
                    notas_preview = self.notas[:100]
                    if len(self.notas) > 100:
                        notas_preview += "..."
                    mensagem_notif += f"\n\n📋 {notas_preview}"
                
                # Enviar notificação baseado no método disponível
                if NOTIFICATION_METHOD == "win11toast":
                    print(f"   Usando win11toast (thread separada)...")
                    from win11toast import toast as win11_toast
                    
                    win11_toast(
                        titulo_notif,
                        mensagem_notif,
                        audio={'silent': 'false'},
                        duration='long'
                    )
                    print(f"✅ NOTIFICAÇÃO ENVIADA (win11toast)")
                    
                elif NOTIFICATION_METHOD == "winotify":
                    print(f"   Usando winotify...")
                    from winotify import Notification, audio
                    
                    toast = Notification(
                        app_id="PinFlow Pro",
                        title=titulo_notif,
                        msg=mensagem_notif,
                        duration="long"
                    )
                    toast.set_audio(audio.LoopingAlarm, loop=False)
                    toast.show()
                    print(f"✅ NOTIFICAÇÃO ENVIADA (winotify)")
                    
                elif NOTIFICATION_METHOD == "plyer":
                    print(f"   Usando plyer...")
                    from plyer import notification
                    notification.notify(
                        title=titulo_notif,
                        message=mensagem_notif,
                        app_name="PinFlow Pro",
                        timeout=10,
                        toast=True
                    )
                    print(f"✅ NOTIFICAÇÃO ENVIADA (plyer)")
                
                print(f"🔔 === FIM DO ENVIO ===\n")
                
            except Exception as e:
                print(f"❌ ERRO AO ENVIAR NOTIFICAÇÃO: {e}")
                import traceback
                traceback.print_exc()
        
        # Executar em thread separada para NÃO BLOQUEAR o piscar
        thread = threading.Thread(target=_send_notification, daemon=True)
        thread.start()
        print(f"🚀 Thread de notificação iniciada (não vai bloquear o piscar!)")
    
    def toggle_blink(self):
        """Alterna estado de piscar"""
        self.blink_state = not self.blink_state
        
        if self.blink_state:
            # Estado "aceso" - destaque vermelho
            self.setStyleSheet(f"""
                PostItCard {{
                    background-color: #ff4444 !important;
                    border: 5px solid #ff0000 !important;
                    border-radius: 5px;
                    animation: blink 1s infinite;
                }}
            """)
        else:
            # Estado "apagado" - cor normal
            self.update_card_style()
    
    def mark_alert_as_read(self):
        """Marca alerta como lido e para de piscar"""
        # Parar timers
        self.blink_timer.stop()
        self.alert_timer.stop()
        
        # Desativar alerta
        self.alerta_ativo = False
        self.blink_state = False
        
        # Limpar dados do alerta
        self.alerta = ""
        self.alerta_data = ""
        self.alerta_hora = ""
        self.data["alerta"] = ""
        self.data["alerta_data"] = ""
        self.data["alerta_hora"] = ""
        
        # Voltar ao estilo normal
        self.update_card_style()
        
        # Salvar
        self.parent_column.window.save_data()
        
        QMessageBox.information(self, "Alerta Lido", "Alerta marcado como lido!\n\nO card parou de piscar e o alerta foi removido.")
    
    def apply_card_size(self):
        """Aplica tamanho do card (padrão ou personalizado)"""
        # Verificar se há tamanho personalizado salvo
        if "custom_width" in self.data and "custom_height" in self.data:
            # Usar tamanho personalizado
            card_width = self.data["custom_width"]
            card_height = self.data["custom_height"]
        else:
            # TAMANHO PADRÃO: Baseado no card "cejan" em Concluídos
            card_width = 250  # Largura padrão
            card_height = 120  # Altura padrão
        
        # Definir tamanho fixo
        self.setFixedSize(card_width, card_height)
    
    def show_menu(self):
        """Mostra menu de opções ao clicar na engrenagem (COMPLETO IGUAL POST-IT)"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
                font-size: 12px;
            }
            QMenu::item {
                padding: 10px 40px 10px 20px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
            }
            QMenu::separator {
                height: 1px;
                background-color: #e0e0e0;
                margin: 5px 0px;
            }
        """)
        
        # === SEÇÃO 1: ABRIR ARQUIVOS ===
        if self.caminho and os.path.exists(self.caminho):
            open_action = QAction("📂 Abrir Arquivo/Pasta", self)
            open_action.triggered.connect(lambda: os.startfile(self.caminho))
            menu.addAction(open_action)
            
            open_folder_action = QAction("📁 Abrir Pasta Contendo", self)
            open_folder_action.triggered.connect(self.open_folder)
            menu.addAction(open_folder_action)
            menu.addSeparator()
        
        # === ALERTA ATIVO - MARCAR COMO LIDO ===
        if self.alerta_ativo:
            mark_read_action = QAction("✓ Marcar como Lido (Parar de Piscar)", self)
            mark_read_action.triggered.connect(self.mark_alert_as_read)
            menu.addAction(mark_read_action)
            menu.addSeparator()
        
        # === SEÇÃO 2: APARÊNCIA ===
        color_action = QAction("🎨 Cor", self)
        color_action.triggered.connect(self.show_color_menu)
        menu.addAction(color_action)
        
        size_action = QAction("📐 Tamanho", self)
        size_action.triggered.connect(self.show_size_menu)
        menu.addAction(size_action)
        
        menu.addSeparator()
        
        # === SEÇÃO 3: EDIÇÃO ===
        edit_action = QAction("✏️ Editar", self)
        edit_action.triggered.connect(self.edit_card)
        menu.addAction(edit_action)
        
        duplicate_action = QAction("📋 Duplicar\tAlt+D", self)
        duplicate_action.triggered.connect(self.duplicate_card)
        menu.addAction(duplicate_action)
        
        menu.addSeparator()
        
        # === SEÇÃO 3.5: NOTA (Copiar/Imprimir) ===
        if self.notas:
            copy_notes_action = QAction("📋 Copiar Nota", self)
            copy_notes_action.triggered.connect(self.copy_notes)
            menu.addAction(copy_notes_action)
            
            print_notes_action = QAction("🖨️ Imprimir Nota", self)
            print_notes_action.triggered.connect(self.print_notes)
            menu.addAction(print_notes_action)
            
            menu.addSeparator()
        
        # === SEÇÃO 4: AÇÕES ===
        archive_action = QAction("📦 Arquivar", self)
        archive_action.triggered.connect(self.archive_card)
        menu.addAction(archive_action)
        
        remove_action = QAction("🗑️ Eliminar Nota\tAlt+Del", self)
        remove_action.triggered.connect(self.remove_self)
        menu.addAction(remove_action)
        
        # Mostrar menu
        menu.exec(self.gear_btn.mapToGlobal(self.gear_btn.rect().bottomLeft()))
    
    def show_color_menu(self):
        """Mostra paleta de cores COMPLETA (igual Post-it)"""
        # Criar dialog customizado com grid de cores
        dialog = QDialog(self)
        dialog.setWindowTitle("Escolha uma cor")
        dialog.setModal(True)
        dialog.setFixedSize(380, 200)
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Grid de cores
        grid = QHBoxLayout()
        grid.setSpacing(5)
        
        # Criar botões de cores em grid 8x3
        colors_list = list(CARD_COLORS.items())
        for i in range(0, 24, 8):  # 3 linhas de 8 cores
            col_layout = QVBoxLayout()
            col_layout.setSpacing(5)
            for j in range(8):
                if i + j < len(colors_list):
                    color_name, color_hex = colors_list[i + j]
                    btn = QPushButton()
                    btn.setFixedSize(40, 40)
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {color_hex};
                            border: 2px solid #ddd;
                            border-radius: 5px;
                        }}
                        QPushButton:hover {{
                            border: 3px solid #333;
                        }}
                    """)
                    btn.setCursor(Qt.PointingHandCursor)
                    btn.setToolTip(color_name)
                    btn.clicked.connect(lambda checked, c=color_hex, n=color_name: self.apply_color(c, n, dialog))
                    col_layout.addWidget(btn)
            grid.addLayout(col_layout)
        
        layout.addLayout(grid)
        
        # Botão para cor automática
        reset_btn = QPushButton("🔄 Cor Automática (Por Prioridade)")
        reset_btn.clicked.connect(lambda: self.reset_color_and_close(dialog))
        reset_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        layout.addWidget(reset_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def apply_color(self, color, color_name, dialog):
        """Aplica cor e fecha dialog"""
        self.set_custom_color(color, color_name)
        dialog.accept()
    
    def reset_color_and_close(self, dialog):
        """Reseta cor e fecha dialog"""
        self.reset_color()
        dialog.accept()
    
    def show_size_menu(self):
        """Menu de tamanho do card"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Tamanho do Card")
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        # Opções de tamanho
        pequeno_radio = QRadioButton("Pequeno (200px)")
        medio_radio = QRadioButton("Médio (250px)")
        grande_radio = QRadioButton("Grande (320px)")
        
        # Marcar atual
        if self.card_size == "pequeno":
            pequeno_radio.setChecked(True)
        elif self.card_size == "medio":
            medio_radio.setChecked(True)
        elif self.card_size == "grande":
            grande_radio.setChecked(True)
        else:
            medio_radio.setChecked(True)
        
        layout.addWidget(pequeno_radio)
        layout.addWidget(medio_radio)
        layout.addWidget(grande_radio)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            if pequeno_radio.isChecked():
                self.set_card_size("pequeno")
            elif medio_radio.isChecked():
                self.set_card_size("medio")
            elif grande_radio.isChecked():
                self.set_card_size("grande")
    
    def set_card_size(self, size):
        """Define tamanho do card (remove custom size)"""
        self.card_size = size
        self.data["card_size"] = size
        
        # Remover tamanho customizado
        if "custom_width" in self.data:
            del self.data["custom_width"]
        if "custom_height" in self.data:
            del self.data["custom_height"]
        
        # Aplicar tamanho predefinido
        sizes = {
            "pequeno": (180, 200),
            "medio": (230, 250),
            "grande": (300, 320)
        }
        
        min_width, max_width = sizes.get(size, (230, 250))
        
        # Resetar para tamanho não-fixo
        self.setMinimumSize(min_width, 100)
        self.setMaximumSize(max_width, 800)
        
        # Forçar atualização visual
        self.updateGeometry()
        self.parent_column.cards_container.updateGeometry()
        
        self.parent_column.window.save_data()
        QMessageBox.information(self, "Tamanho Alterado", f"Card alterado para: {size.title()}\n\nDica: Você também pode arrastar a borda/canto do card para redimensionar livremente!")
    
    def toggle_bold(self):
        """Toggle negrito"""
        self.fonte_negrito = not self.fonte_negrito
        self.data["fonte_negrito"] = self.fonte_negrito
        self.apply_text_formatting(self.title_label)
        self.parent_column.window.save_data()
    
    def toggle_italic(self):
        """Toggle itálico"""
        self.fonte_italico = not self.fonte_italico
        self.data["fonte_italico"] = self.fonte_italico
        self.apply_text_formatting(self.title_label)
        self.parent_column.window.save_data()
    
    def toggle_underline(self):
        """Toggle sublinhado"""
        self.fonte_sublinhado = not self.fonte_sublinhado
        self.data["fonte_sublinhado"] = self.fonte_sublinhado
        self.apply_text_formatting(self.title_label)
        self.parent_column.window.save_data()
    
    def change_font_size(self):
        """Muda tamanho da fonte"""
        from PySide6.QtWidgets import QInputDialog
        
        sizes = ["8", "9", "10", "11", "12", "14", "16", "18", "20", "24"]
        current = str(self.fonte_tamanho)
        
        size, ok = QInputDialog.getItem(
            self,
            "Tamanho da Fonte",
            "Escolha o tamanho:",
            sizes,
            sizes.index(current) if current in sizes else 2,
            False
        )
        
        if ok:
            self.fonte_tamanho = int(size)
            self.data["fonte_tamanho"] = self.fonte_tamanho
            self.apply_text_formatting(self.title_label)
            self.parent_column.window.save_data()
    
    def change_color(self):
        """DEPRECATED - usar show_color_menu"""
        self.show_color_menu()
    
    def set_custom_color(self, color, color_name):
        """Define cor customizada"""
        self.cor_custom = color
        self.cor = color
        self.data["cor_custom"] = color
        self.setStyleSheet(f"""
            PostItCard {{
                background-color: {self.cor};
                border-left: 5px solid {PRIORITIES[self.prioridade]["color"]};
                border-right: 1px solid #e6d000;
                border-top: 1px solid #e6d000;
                border-bottom: 1px solid #e6d000;
                border-radius: 5px;
                min-height: 80px;
                max-width: 250px;
            }}
            PostItCard:hover {{
                background-color: {self.cor};
                filter: brightness(1.1);
            }}
        """)
        self.parent_column.window.save_data()
    
    def reset_color(self):
        """Volta à cor automática por prioridade"""
        self.cor_custom = None
        self.cor = PRIORITIES[self.prioridade]["postit_color"]
        self.data["cor_custom"] = None
        self.setStyleSheet(f"""
            PostItCard {{
                background-color: {self.cor};
                border-left: 5px solid {PRIORITIES[self.prioridade]["color"]};
                border-right: 1px solid #e6d000;
                border-top: 1px solid #e6d000;
                border-bottom: 1px solid #e6d000;
                border-radius: 5px;
                min-height: 80px;
                max-width: 250px;
            }}
            PostItCard:hover {{
                background-color: {self.cor};
                filter: brightness(1.1);
            }}
        """)
        self.parent_column.window.save_data()
    
    def duplicate_card(self):
        """Duplica o card"""
        new_data = self.data.copy()
        new_data["titulo"] = f"{self.titulo} (Cópia)"
        new_data["data_criacao"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.parent_column.add_card(new_data)
        self.parent_column.window.save_data()
        QMessageBox.information(self, "Duplicado", "Card duplicado com sucesso!")
        
    def edit_card(self):
        """Abre dialog para editar"""
        dialog = CardDialog(self, self.data)
        if dialog.exec() == QDialog.Accepted:
            new_data = dialog.get_data()
            
            # Validar dados (se validação habilitada)
            if VALIDATION_ENABLED:
                is_valid, message, sanitized_data = InputValidator.validate_card_data(new_data)
                if not is_valid:
                    QMessageBox.warning(self, "Dados Inválidos", f"Não foi possível salvar:\n{message}")
                    return
                new_data = sanitized_data
            
            # Preservar data de criação original
            new_data["data_criacao"] = self.data_criacao
            
            # Preservar cor customizada se existir
            if "cor_custom" in self.data:
                new_data["cor_custom"] = self.data["cor_custom"]
            
            # Atualizar data
            self.data = new_data
            
            # Pegar índice do card na coluna
            card_index = self.parent_column.cards.index(self)
            
            # Remover card antigo
            self.parent_column.cards_layout.removeWidget(self)
            self.parent_column.cards.remove(self)
            
            # Criar novo card com dados atualizados
            new_card = PostItCard(new_data, self.parent_column)
            self.parent_column.cards.insert(card_index, new_card)
            self.parent_column.cards_layout.insertWidget(card_index, new_card)
            
            # Deletar card antigo
            self.deleteLater()
            
            # Salvar
            self.parent_column.window.save_data()
        
    def mousePressEvent(self, event):
        """Inicia drag, resize ou abre card"""
        if event.button() == Qt.LeftButton:
            pos = get_event_pos(event)
            # Verificar se clicou na engrenagem
            gear_btn_rect = self.gear_btn.geometry()
            
            # Não iniciar drag se clicou na engrenagem
            if gear_btn_rect.contains(pos):
                # Passar o evento para o botão processar
                event.ignore()
                # Enviar evento diretamente para o botão
                self.gear_btn.mousePressEvent(event)
                return
            
            # Verificar se clicou na borda para resize
            edge = self.get_resize_edge(pos)
            if edge:
                self.resizing = True
                self.resize_edge = edge
                self.resize_start = pos
                self.update_cursor_for_resize(edge)
                return
            
            # Se não for drag nem resize, marcar posição inicial para possível drag
            self.drag_start_position = pos
            self.setCursor(Qt.ClosedHandCursor)
            
    def mouseMoveEvent(self, event):
        """Executa drag OU resize"""
        pos = get_event_pos(event)
        # Se está redimensionando
        if self.resizing and self.resize_start:
            delta = pos - self.resize_start
            new_size = self.size()
            
            if self.resize_edge in ['right', 'corner']:
                new_width = max(180, min(500, self.width() + delta.x()))
                new_size.setWidth(new_width)
            
            if self.resize_edge in ['bottom', 'corner']:
                new_height = max(100, min(800, self.height() + delta.y()))
                new_size.setHeight(new_height)
            
            self.setFixedSize(new_size)
            self.resize_start = pos
            
            # Salvar novo tamanho personalizado
            self.data["custom_width"] = new_size.width()
            self.data["custom_height"] = new_size.height()
            # Remover card_size padrão quando usar tamanho custom
            if "card_size" in self.data:
                del self.data["card_size"]
            
            # Salvar imediatamente
            self.parent_column.window.save_data()
            return
        
        # Se não está redimensionando, verifica se pode começar a arrastar
        if not (event.buttons() & Qt.LeftButton):
            # Apenas atualizando cursor
            edge = self.get_resize_edge(pos)
            self.update_cursor_for_resize(edge)
            return
            
        if not self.drag_start_position:
            return
            
        if (pos - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
            
        # Criar drag
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(json.dumps(self.data))
        drag.setMimeData(mime_data)
        
        drag.exec(Qt.MoveAction)
        self.setCursor(Qt.OpenHandCursor)
        
    def mouseReleaseEvent(self, event):
        """Finaliza drag, resize ou abre card"""
        if event.button() == Qt.LeftButton:
            # Se estava redimensionando, finalizar
            if self.resizing:
                self.resizing = False
                self.resize_start = None
                self.resize_edge = None
                self.parent_column.window.save_data()
                self.setCursor(Qt.OpenHandCursor)
                return
            
            # Se moveu pouco, foi um clique simples - ABRIR CARD
            if self.drag_start_position:
                pos = get_event_pos(event)
                distance = (pos - self.drag_start_position).manhattanLength()
                if distance < 10:  # Clique simples (moveu menos de 10 pixels)
                    self.edit_card()
                    self.drag_start_position = None
                    self.setCursor(Qt.OpenHandCursor)
                    return
            
            # Finalizar drag
            self.drag_start_position = None
            self.setCursor(Qt.OpenHandCursor)
        
    def open_folder(self):
        """Abre a pasta onde o arquivo está localizado"""
        if not self.caminho or not os.path.exists(self.caminho):
            QMessageBox.warning(self, "Aviso", "Caminho não existe!")
            return
        
        # Se é pasta, abre ela
        if os.path.isdir(self.caminho):
            os.startfile(self.caminho)
        # Se é arquivo, abre a pasta pai e seleciona o arquivo
        else:
            folder = os.path.dirname(self.caminho)
            # Abre o Explorer e seleciona o arquivo
            os.system(f'explorer /select,"{self.caminho}"')
            
    def archive_card(self):
        """Arquiva este card"""
        reply = QMessageBox.question(self, "Arquivar", 
                                     f"Arquivar '{self.titulo}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Adicionar data de arquivamento
            archive_data = self.data.copy()
            archive_data["data_arquivamento"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Carregar arquivo existente
            archived_cards = []
            if os.path.exists(ARCHIVE_FILE):
                try:
                    with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
                        archived_cards = json.load(f)
                except:
                    archived_cards = []
            
            # Adicionar novo card
            archived_cards.append(archive_data)
            
            # Salvar
            with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
                json.dump(archived_cards, f, indent=2, ensure_ascii=False)
            
            # Remover da coluna
            self.parent_column.remove_card(self)
            
            QMessageBox.information(self, "Arquivado", f"'{self.titulo}' foi arquivado!")
    
    def keyPressEvent(self, event):
        """Navegação por teclado no card"""
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            # Enter - Editar card
            self.edit_card()
            event.accept()
        elif event.key() == Qt.Key_Delete or (event.key() == Qt.Key_Backspace and event.modifiers() == Qt.ControlModifier):
            # Delete ou Ctrl+Backspace - Remover card
            self.remove_self()
            event.accept()
        elif event.key() == Qt.Key_Up:
            # Seta para cima - Card anterior
            self.navigate_card(-1)
            event.accept()
        elif event.key() == Qt.Key_Down:
            # Seta para baixo - Próximo card
            self.navigate_card(1)
            event.accept()
        elif event.key() == Qt.Key_Left:
            # Seta esquerda - Coluna anterior
            self.navigate_column(-1)
            event.accept()
        elif event.key() == Qt.Key_Right:
            # Seta direita - Próxima coluna
            self.navigate_column(1)
            event.accept()
        elif event.key() == Qt.Key_Space:
            # Espaço - Mostrar menu
            self.show_menu()
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def navigate_card(self, direction):
        """Navega para card anterior/próximo na mesma coluna"""
        try:
            current_index = self.parent_column.cards.index(self)
            new_index = current_index + direction
            
            if 0 <= new_index < len(self.parent_column.cards):
                next_card = self.parent_column.cards[new_index]
                next_card.setFocus()
        except (ValueError, IndexError):
            pass
    
    def navigate_column(self, direction):
        """Navega para coluna anterior/próxima"""
        try:
            current_col_index = self.parent_column.window.columns.index(self.parent_column)
            new_col_index = current_col_index + direction
            
            if 0 <= new_col_index < len(self.parent_column.window.columns):
                next_column = self.parent_column.window.columns[new_col_index]
                if next_column.cards:
                    # Focar no primeiro card da próxima coluna
                    next_column.cards[0].setFocus()
                else:
                    # Se não houver cards, focar na coluna
                    next_column.setFocus()
        except (ValueError, IndexError):
            pass
    
    def focusInEvent(self, event):
        """Quando card recebe foco"""
        super().focusInEvent(event)
        # Adicionar borda de foco visual
        current_style = self.styleSheet()
        if ":focus" not in current_style:
            focus_style = """
                PostItCard:focus {
                    border: 3px solid #2196F3 !important;
                    background-color: rgba(33, 150, 243, 0.15) !important;
                    outline: 2px solid rgba(33, 150, 243, 0.4) !important;
                }
            """
            self.setStyleSheet(current_style + focus_style)
    
    def focusOutEvent(self, event):
        """Quando card perde foco"""
        super().focusOutEvent(event)
            
    def remove_self(self):
        """Remove este cartão"""
        reply = QMessageBox.question(self, "Confirmar", 
                                     f"Remover card '{self.titulo}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.parent_column.remove_card(self)


class KanbanColumn(QFrame):
    """Coluna do Kanban que aceita drops"""
    
    def __init__(self, titulo, cor, window, column_id=None):
        super().__init__()
        self.titulo = titulo
        self.cor = cor
        self.window = window
        self.column_id = column_id if column_id else titulo.lower().replace(" ", "_")
        self.cards = []
        self.drag_start_position = None  # Para arrastar coluna
        
        self.setup_ui()
        self.setAcceptDrops(True)
    
    def setup_ui(self):
        """Configura visual da coluna"""
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Header da coluna - Carregar cor salva ou usar padrão
        header_container = QWidget()
        # Carregar cor salva (se houver)
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    if "column_header_color" in settings:
                        column_header_color = settings["column_header_color"]
                        color = QColor(column_header_color)
                        r, g, b = color.red(), color.green(), color.blue()
                        header_container.setStyleSheet(f"""
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 rgb({r}, {g}, {b}), 
                                stop:1 rgb({min(255, r+30)}, {min(255, g+30)}, {min(255, b+30)}));
                            border-radius: 8px;
                            padding: 8px;
                        """)
                    else:
                        header_container.setStyleSheet("""
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #1e3a5f, stop:1 #2a5080);
                            border-radius: 8px;
                            padding: 8px;
                        """)
            else:
                header_container.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #1e3a5f, stop:1 #2a5080);
                    border-radius: 8px;
                    padding: 8px;
                """)
        except:
            header_container.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #2a5080);
                border-radius: 8px;
                padding: 8px;
            """)
        header_container.setCursor(Qt.OpenHandCursor)  # Cursor de mão para arrastar
        
        # GUARDAR REFERÊNCIA para poder atualizar depois
        self.header_container = header_container
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_container.setLayout(header_layout)
        
        # Título da coluna (editável) - BRANCO sobre azul marinho
        self.title_label = QLabel(self.titulo)
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.title_label.setStyleSheet("color: white; padding: 5px;")
        self.title_label.setCursor(Qt.IBeamCursor)
        self.title_label.setToolTip("Duplo clique para editar nome")
        self.title_label.mouseDoubleClickEvent = lambda event: self.edit_title()
        
        # Menu de opções da coluna
        self.column_menu_btn = QPushButton("⋮")
        self.column_menu_btn.setMaximumSize(QSize(25, 25))
        self.column_menu_btn.setCursor(Qt.PointingHandCursor)
        self.column_menu_btn.setToolTip("Opções da coluna")
        self.column_menu_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 12px;
            }
        """)
        self.column_menu_btn.clicked.connect(self.show_column_menu)
        
        # Contador
        self.counter_label = QLabel("0")
        self.counter_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.counter_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.3);
            color: white;
            padding: 3px 8px;
            border-radius: 10px;
        """)
        
        # Botão adicionar
        add_btn = QPushButton("➕")
        add_btn.setMaximumSize(QSize(30, 30))
        add_btn.setToolTip("Adicionar novo card")
        add_btn.clicked.connect(self.add_card_manual)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.3);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.5);
            }
        """)
        
        header_layout.addWidget(self.title_label, stretch=1)
        header_layout.addWidget(self.counter_label)
        header_layout.addWidget(add_btn)
        header_layout.addWidget(self.column_menu_btn)
        
        # Salvar referência ao header para drag
        self.header_widget = header_container
        
        # Área de scroll para os cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container dos cards
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # CENTRALIZADO
        self.cards_layout.setSpacing(10)
        self.cards_container.setLayout(self.cards_layout)
        
        scroll.setWidget(self.cards_container)
        
        layout.addWidget(header_container)  # Header colorido
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        
        # Estilo da coluna
        self.update_column_style()
        
        self.setMinimumWidth(240)
        self.setMaximumWidth(400)  # Limite máximo para coluna
    
    def update_column_style(self):
        """Atualiza estilo da coluna baseado no tema"""
        # Carregar cor salva dos headers das colunas (apenas para modo claro)
        column_header_color_saved = None
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    if "column_header_color" in settings:
                        column_header_color_saved = settings["column_header_color"]
        except:
            pass
        
        if hasattr(self.window, 'dark_mode') and self.window.dark_mode:
            # MODO ESCURO - TUDO PRETO (cores fixas, não aplica cores personalizadas)
            self.setStyleSheet(f"""
                KanbanColumn {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1a1a1a, stop:1 #2d2d2d);
                    border: 2px solid #3d3d3d;
                    border-radius: 10px;
                }}
            """)
            # Header das colunas também preto no modo escuro (cores fixas)
            if hasattr(self, 'header_container'):
                self.header_container.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #1a1a1a, stop:1 #2d2d2d);
                    border-radius: 8px;
                    padding: 8px;
                """)
        else:
            # MODO CLARO - Cinza claro original (pode usar cores personalizadas)
            self.setStyleSheet(f"""
                KanbanColumn {{
                    background-color: #f5f5f5;
                    border: 2px dashed #ccc;
                    border-radius: 10px;
                }}
            """)
            # Aplicar cor salva no header se houver (apenas modo claro)
            if column_header_color_saved and hasattr(self, 'header_container'):
                color = QColor(column_header_color_saved)
                r, g, b = color.red(), color.green(), color.blue()
                self.header_container.setStyleSheet(f"""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb({r}, {g}, {b}), 
                        stop:1 rgb({min(255, r+30)}, {min(255, g+30)}, {min(255, b+30)}));
                    border-radius: 8px;
                    padding: 8px;
                """)
            elif hasattr(self, 'header_container'):
                # Se não houver cor salva, usar padrão azul marinho
                self.header_container.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #1e3a5f, stop:1 #2a5080);
                    border-radius: 8px;
                    padding: 8px;
                """)
    
    def edit_title(self):
        """Edita o título da coluna"""
        from PySide6.QtWidgets import QInputDialog
        
        new_title, ok = QInputDialog.getText(
            self,
            "Editar Nome da Coluna",
            "Novo nome:",
            QLineEdit.Normal,
            self.titulo
        )
        
        if ok and new_title.strip():
            self.titulo = new_title.strip()
            self.title_label.setText(self.titulo)
            self.window.save_data()
    
    def show_column_menu(self):
        """Menu de opções da coluna"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
            }
            QMenu::item {
                padding: 8px 30px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
            }
        """)
        
        # Editar nome
        edit_action = QAction("✏️ Editar Nome", self)
        edit_action.triggered.connect(self.edit_title)
        menu.addAction(edit_action)
        
        # Mudar cor
        color_action = QAction("🎨 Mudar Cor", self)
        color_action.triggered.connect(self.change_column_color)
        menu.addAction(color_action)
        
        menu.addSeparator()
        
        # Remover coluna
        remove_action = QAction("🗑️ Remover Coluna", self)
        remove_action.triggered.connect(self.remove_column)
        menu.addAction(remove_action)
        
        menu.exec(self.column_menu_btn.mapToGlobal(self.column_menu_btn.rect().bottomLeft()))
    
    def change_column_color(self):
        """Muda cor da coluna com paleta"""
        # Criar dialog com paleta de cores
        dialog = QDialog(self)
        dialog.setWindowTitle("🎨 Escolha uma cor para a coluna")
        dialog.setModal(True)
        dialog.setFixedSize(450, 150)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Grid de cores para colunas
        colors_layout = QHBoxLayout()
        colors_layout.setSpacing(8)
        
        column_colors = [
            ("#2196F3", "Azul"),
            ("#ff9800", "Laranja"),
            ("#9c27b0", "Roxo"),
            ("#00bcd4", "Ciano"),
            ("#4caf50", "Verde"),
            ("#f44336", "Vermelho"),
            ("#607d8b", "Cinza"),
            ("#e91e63", "Rosa"),
            ("#795548", "Marrom"),
            ("#ffc107", "Amarelo Ouro"),
            ("#00e676", "Verde Neon"),
            ("#1e88e5", "Azul Escuro")
        ]
        
        selected_color = {"value": self.cor}
        
        for color_hex, color_name in column_colors:
            btn = QPushButton()
            btn.setFixedSize(50, 50)
            is_current = (color_hex == self.cor)
            border_style = "4px solid #000" if is_current else "2px solid #ddd"
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_hex};
                    border: {border_style};
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    border: 4px solid #333;
                }}
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setToolTip(color_name)
            btn.clicked.connect(lambda checked, c=color_hex: self.apply_column_color(c, dialog))
            colors_layout.addWidget(btn)
        
        layout.addWidget(QLabel("Selecione uma cor:"))
        layout.addLayout(colors_layout)
        
        # Botão cancelar
        cancel_btn = QPushButton("✖ Cancelar")
        cancel_btn.clicked.connect(dialog.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 8px;
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        layout.addWidget(cancel_btn)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def apply_column_color(self, color_hex, dialog):
        """Aplica cor à coluna e fecha dialog"""
        self.cor = color_hex
        self.title_label.setStyleSheet(f"color: {self.cor}; padding: 5px;")
        self.counter_label.setStyleSheet(f"""
            background-color: {self.cor};
            color: white;
            padding: 3px 8px;
            border-radius: 10px;
        """)
        # Atualizar estilo do botão adicionar também
        for i in range(self.layout().itemAt(0).layout().count()):
            item = self.layout().itemAt(0).layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QPushButton):
                widget = item.widget()
                if widget.text() == "➕":
                    widget.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {self.cor};
                            color: white;
                            border: none;
                            border-radius: 15px;
                            font-weight: bold;
                        }}
                        QPushButton:hover {{
                            background-color: {self.cor};
                            filter: brightness(1.2);
                        }}
                    """)
        self.window.save_data()
        QMessageBox.information(self, "✅ Cor Alterada", f"Cor da coluna '{self.titulo}' alterada com sucesso!")
        dialog.accept()
    
    def remove_column(self):
        """Remove a coluna"""
        if len(self.cards) > 0:
            reply = QMessageBox.question(
                self,
                "Remover Coluna",
                f"A coluna '{self.titulo}' tem {len(self.cards)} card(s).\n\nRemover mesmo assim?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        reply = QMessageBox.question(
            self,
            "Confirmar",
            f"Remover coluna '{self.titulo}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.window.remove_column(self)
        
    def add_card_manual(self):
        """Adiciona card manualmente via dialog"""
        dialog = CardDialog(self)
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            if data["titulo"]:
                self.add_card(data)
                self.window.save_data()
                
    def update_counter(self):
        """Atualiza contador de cards"""
        self.counter_label.setText(str(len(self.cards)))
        
    def dragEnterEvent(self, event):
        """Aceita drag de arquivos do Windows e cards internos"""
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            event.acceptProposedAction()
            self.setStyleSheet(f"""
                KanbanColumn {{
                    background-color: #e8f5e9;
                    border: 3px dashed {self.cor};
                    border-radius: 10px;
                }}
            """)
            
    def dragLeaveEvent(self, event):
        """Remove highlight"""
        self.setStyleSheet(f"""
            KanbanColumn {{
                background-color: #f5f5f5;
                border: 2px dashed #ccc;
                border-radius: 10px;
            }}
        """)
        
    def dropEvent(self, event):
        """Processa drop de arquivos/pastas ou cards"""
        # Remove highlight
        self.dragLeaveEvent(event)
        
        # Drop de arquivos/pastas do Windows
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                caminho = url.toLocalFile()
                nome = os.path.basename(caminho)
                
                # Verifica se é arquivo ou pasta
                if os.path.isdir(caminho):
                    titulo = f"📁 {nome}"
                else:
                    titulo = f"📄 {nome}"
                    
                data = {
                    "titulo": titulo,
                    "caminho": caminho,
                    "notas": "",
                    "prioridade": "Normal",
                    "cor": PRIORITIES["Normal"]["postit_color"],
                    "tags": [],
                    "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M")
                }
                
                self.add_card(data)
            
            event.acceptProposedAction()
            self.window.save_data()
            
        # Drop de card interno (mover entre colunas OU reordenar na mesma coluna)
        elif event.mimeData().hasText():
            try:
                data = json.loads(event.mimeData().text())
                
                # Pegar card de origem
                source_widget = event.source()
                if isinstance(source_widget, PostItCard):
                    source_column = source_widget.parent_column
                    
                    # Calcular posição de drop dentro da coluna
                    pos = get_event_pos(event)
                    drop_y = pos.y()
                    target_index = 0
                    
                    # Encontrar posição baseada em onde foi dropado
                    for i, card in enumerate(self.cards):
                        card_top = card.y()
                        card_bottom = card.y() + card.height()
                        if drop_y < card_bottom:
                            target_index = i
                            break
                    else:
                        target_index = len(self.cards)  # Adicionar no final
                    
                    # Se for a mesma coluna - reordenar
                    if source_column == self:
                        old_index = self.cards.index(source_widget)
                        
                        # Ajustar índice se estiver movendo para baixo
                        if target_index > old_index:
                            target_index -= 1
                        
                        if old_index != target_index:
                            # Remover e inserir na nova posição
                            self.cards.pop(old_index)
                            self.cards.insert(target_index, source_widget)
                            
                            # Reorganizar layout
                            self.cards_layout.removeWidget(source_widget)
                            self.cards_layout.insertWidget(target_index, source_widget)
                            
                            self.window.save_data()
                    else:
                        # Mover entre colunas diferentes
                        source_column.remove_card(source_widget, save=False)
                        
                        # Criar novo card na posição específica
                        new_card = PostItCard(data, self)
                        self.cards.insert(target_index, new_card)
                        self.cards_layout.insertWidget(target_index, new_card)
                        self.update_counter()
                        
                        self.window.save_data()
                    
                    event.acceptProposedAction()
            except:
                pass
    
    def mousePressEvent(self, event):
        """Inicia arrastar coluna"""
        if event.button() == Qt.LeftButton:
            # Só arrastar se clicar no header
            pos = get_event_pos(event)
            if self.header_widget.geometry().contains(pos):
                self.drag_start_position = pos
                self.header_widget.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Arrasta coluna"""
        if event.buttons() & Qt.LeftButton and self.drag_start_position:
            pos = get_event_pos(event)
            # Verifica se moveu o suficiente para iniciar drag
            if (pos - self.drag_start_position).manhattanLength() < 20:
                return
            
            # Criar drag
            drag = QDrag(self)
            mime_data = QMimeData()
            
            # Passar index da coluna
            column_index = self.window.columns.index(self)
            mime_data.setText(f"COLUMN:{column_index}")
            drag.setMimeData(mime_data)
            
            # Executar drag
            drag.exec(Qt.MoveAction)
            self.header_widget.setCursor(Qt.OpenHandCursor)
    
    def mouseReleaseEvent(self, event):
        """Finaliza arrastar coluna"""
        self.drag_start_position = None
        self.header_widget.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
                
    def add_card(self, data):
        """Adiciona um novo card"""
        card = PostItCard(data, self)
        self.cards_layout.addWidget(card)
        self.cards.append(card)
        self.update_counter()
        
    def remove_card(self, card, save=True):
        """Remove um card"""
        if card in self.cards:
            self.cards.remove(card)
            card.deleteLater()
            self.update_counter()
            if save:
                self.window.save_data()
                
    def get_cards_data(self):
        """Retorna dados dos cards"""
        return [card.data for card in self.cards]
        
    def load_cards_data(self, cards_data):
        """Carrega cards dos dados"""
        for card_data in cards_data:
            self.add_card(card_data)
            
    def filter_cards(self, search_text):
        """Filtra cards baseado em texto de busca"""
        search_text = search_text.lower()
        for card in self.cards:
            match = (search_text in card.titulo.lower() or 
                    search_text in card.caminho.lower() or
                    search_text in card.notas.lower() or
                    any(search_text in tag.lower() for tag in card.tags))
            card.setVisible(match)


class DashboardDialog(QDialog):
    """Dialog para visualizar Dashboard de Estatísticas"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.setup_ui()
        self.load_statistics()
        
    def setup_ui(self):
        """Configura interface do Dashboard"""
        self.setWindowTitle("📈 Dashboard - Estatísticas e Produtividade")
        self.setModal(False)
        self.setMinimumSize(900, 650)
        
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel("📈 DASHBOARD DE PRODUTIVIDADE")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1e3a5f, stop:1 #c0c0c0);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        layout.addWidget(header_label)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        stats_widget = QWidget()
        stats_layout = QVBoxLayout()
        
        # Container para as estatísticas
        self.stats_container = QVBoxLayout()
        stats_layout.addLayout(self.stats_container)
        
        stats_widget.setLayout(stats_layout)
        scroll.setWidget(stats_widget)
        layout.addWidget(scroll)
        
        # Botões
        buttons_layout = QHBoxLayout()
        
        export_btn = QPushButton("📊 Exportar para CSV")
        export_btn.clicked.connect(self.export_to_csv)
        export_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #8b9dc3);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #152d4a, stop:1 #7a8bb0);
            }
        """)
        
        refresh_btn = QPushButton("🔄 Atualizar")
        refresh_btn.clicked.connect(self.load_statistics)
        refresh_btn.setStyleSheet(export_btn.styleSheet())
        
        close_btn = QPushButton("✖ Fechar")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet(export_btn.styleSheet())
        
        buttons_layout.addWidget(export_btn)
        buttons_layout.addWidget(refresh_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        
    def load_statistics(self):
        """Carrega e exibe estatísticas"""
        # Limpar container
        while self.stats_container.count():
            child = self.stats_container.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Coletar dados
        total_cards = 0
        cards_by_column = {}
        cards_by_priority = {"Baixa": 0, "Normal": 0, "Alta": 0, "Urgente": 0}
        cards_with_alert = 0
        cards_with_files = 0
        total_tags = []
        
        for column in self.parent_window.columns:
            column_name = column.titulo
            count = column.cards_layout.count()
            cards_by_column[column_name] = count
            total_cards += count
            
            for i in range(count):
                card_widget = column.cards_layout.itemAt(i).widget()
                if isinstance(card_widget, PostItCard):
                    data = card_widget.data
                    
                    # Prioridade
                    priority = data.get("prioridade", "Normal")
                    if priority in cards_by_priority:
                        cards_by_priority[priority] += 1
                    
                    # Alertas
                    if data.get("alerta"):
                        cards_with_alert += 1
                    
                    # Arquivos
                    if data.get("caminho"):
                        cards_with_files += 1
                    
                    # Tags
                    tags = data.get("tags", [])
                    total_tags.extend(tags)
        
        # Cards arquivados
        archived_count = 0
        if os.path.exists(ARCHIVE_FILE):
            try:
                with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
                    archived_data = json.load(f)
                    archived_count = len(archived_data)
            except:
                pass
        
        # === RESUMO GERAL ===
        summary_card = self.create_stat_card(
            "📊 RESUMO GERAL",
            [
                ("📝 Total de Cards Ativos", total_cards),
                ("📦 Cards Arquivados", archived_count),
                ("🎯 Cards com Alertas", cards_with_alert),
                ("📎 Cards com Arquivos", cards_with_files),
                ("🏷️ Tags Únicas", len(set(total_tags)))
            ],
            "#2196f3"
        )
        self.stats_container.addWidget(summary_card)
        
        # === CARDS POR COLUNA ===
        column_items = [(name, count) for name, count in cards_by_column.items()]
        column_card = self.create_stat_card(
            "📋 CARDS POR COLUNA",
            column_items,
            "#4caf50"
        )
        self.stats_container.addWidget(column_card)
        
        # === CARDS POR PRIORIDADE ===
        priority_items = [(f"{PRIORITIES[p]['icon']} {p}", count) for p, count in cards_by_priority.items() if count > 0]
        priority_card = self.create_stat_card(
            "⚡ CARDS POR PRIORIDADE",
            priority_items,
            "#ff9800"
        )
        self.stats_container.addWidget(priority_card)
        
        # === TOP TAGS ===
        if total_tags:
            from collections import Counter
            tag_counter = Counter(total_tags)
            top_tags = tag_counter.most_common(10)
            tags_card = self.create_stat_card(
                "🏷️ TOP 10 TAGS MAIS USADAS",
                top_tags,
                "#9c27b0"
            )
            self.stats_container.addWidget(tags_card)
        
        self.stats_container.addStretch()
        
    def create_stat_card(self, title, items, color):
        """Cria um card de estatística"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box | QFrame.Raised)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 3px solid {color};
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {color}; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Items
        for item_name, item_value in items:
            item_layout = QHBoxLayout()
            
            name_label = QLabel(item_name)
            name_label.setStyleSheet("font-size: 12px; color: #333;")
            
            value_label = QLabel(str(item_value))
            value_label.setFont(QFont("Arial", 12, QFont.Bold))
            value_label.setStyleSheet(f"color: {color};")
            value_label.setAlignment(Qt.AlignRight)
            
            # Barra de progresso visual (se for numérico)
            if isinstance(item_value, int) and item_value > 0:
                # Calcular porcentagem (baseado no maior valor)
                max_value = max([v for _, v in items if isinstance(v, int)], default=1)
                percent = (item_value / max_value) * 100 if max_value > 0 else 0
                
                bar = QFrame()
                bar.setFixedHeight(8)
                bar.setStyleSheet(f"""
                    QFrame {{
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 {color}, stop:{percent/100} {color}, 
                            stop:{percent/100} #e0e0e0, stop:1 #e0e0e0);
                        border-radius: 4px;
                    }}
                """)
                
                item_layout.addWidget(name_label, 3)
                item_layout.addWidget(bar, 4)
                item_layout.addWidget(value_label, 1)
            else:
                item_layout.addWidget(name_label)
                item_layout.addStretch()
                item_layout.addWidget(value_label)
            
            layout.addLayout(item_layout)
        
        card.setLayout(layout)
        return card
        
    def export_to_csv(self):
        """Exporta estatísticas para CSV"""
        try:
            # Escolher local para salvar
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar Estatísticas",
                f"dashboard_kanban_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV Files (*.csv)"
            )
            
            if not file_path:
                return
            
            # Coletar dados
            rows = [["Métrica", "Valor"]]
            
            # Estatísticas gerais
            total_cards = sum(col.cards_layout.count() for col in self.parent_window.columns)
            rows.append(["Total de Cards Ativos", total_cards])
            
            # Por coluna
            for column in self.parent_window.columns:
                rows.append([f"Cards em {column.titulo}", column.cards_layout.count()])
            
            # Salvar CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            
            QMessageBox.information(
                self,
                "✅ Sucesso!",
                f"Estatísticas exportadas para:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Erro",
                f"Erro ao exportar:\n{str(e)}"
            )


class GanttDialog(QDialog):
    """Dialog para visualizar Gantt Chart"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.cards_data = []
        self.setup_ui()
        self.load_cards()
        
    def setup_ui(self):
        """Configura interface do Gantt"""
        self.setWindowTitle("📊 Visão Gantt - Cronograma Visual")
        self.setModal(False)
        self.setMinimumSize(1200, 700)
        
        layout = QVBoxLayout()
        
        # Header
        header_label = QLabel("📊 CRONOGRAMA DO PROJETO (GANTT CHART)")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #1e3a5f, stop:1 #c0c0c0);
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        layout.addWidget(header_label)
        
        # Filtros
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("🔍 Filtrar por coluna:"))
        
        self.column_filter = QComboBox()
        self.column_filter.addItem("🌐 Todas as Colunas")
        self.column_filter.currentTextChanged.connect(self.filter_cards)
        filter_layout.addWidget(self.column_filter)
        
        filter_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Atualizar")
        refresh_btn.clicked.connect(self.load_cards)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
        # Scroll area para o Gantt
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        self.gantt_widget = QWidget()
        self.gantt_layout = QVBoxLayout()
        self.gantt_widget.setLayout(self.gantt_layout)
        
        scroll.setWidget(self.gantt_widget)
        layout.addWidget(scroll)
        
        # Legenda
        legend_layout = QHBoxLayout()
        legend_layout.addWidget(QLabel("📊 Legenda:"))
        
        on_time_label = QLabel("▓ No prazo")
        on_time_label.setStyleSheet("color: #4caf50; font-weight: bold;")
        legend_layout.addWidget(on_time_label)
        
        late_label = QLabel("▓ Atrasado")
        late_label.setStyleSheet("color: #f44336; font-weight: bold;")
        legend_layout.addWidget(late_label)
        
        today_label = QLabel("│ Hoje")
        today_label.setStyleSheet("color: #2196f3; font-weight: bold;")
        legend_layout.addWidget(today_label)
        
        legend_layout.addStretch()
        layout.addLayout(legend_layout)
        
        # Botão fechar
        close_btn = QPushButton("✖ Fechar")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #c0c0c0);
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2a5080, stop:1 #d0d0d0);
            }
        """)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
    def load_cards(self):
        """Carrega todos os cards de todas as colunas"""
        self.cards_data = []
        self.column_filter.clear()
        self.column_filter.addItem("🌐 Todas as Colunas")
        
        # Coletar cards de todas as colunas
        for column in self.parent_window.columns:
            column_name = column.titulo
            self.column_filter.addItem(column_name)
            
            for i in range(column.cards_layout.count()):
                card_widget = column.cards_layout.itemAt(i).widget()
                if isinstance(card_widget, PostItCard):
                    card_data = card_widget.data.copy()
                    card_data["coluna"] = column_name
                    self.cards_data.append(card_data)
        
        self.render_gantt()
        
    def filter_cards(self):
        """Filtra cards por coluna"""
        self.render_gantt()
        
    def render_gantt(self):
        """Renderiza o Gantt Chart"""
        # Limpar layout
        while self.gantt_layout.count():
            child = self.gantt_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Filtrar cards
        filter_text = self.column_filter.currentText()
        filtered_cards = self.cards_data
        
        if filter_text != "🌐 Todas as Colunas":
            filtered_cards = [c for c in self.cards_data if c.get("coluna") == filter_text]
        
        # Ordenar por data início (cards sem data vão pro final)
        def sort_key(card):
            date = self.parse_date(card.get("data_inicio", ""))
            if date is None:
                return QDate(9999, 12, 31)  # Data muito futura para ir pro final
            return date
        
        filtered_cards = sorted(filtered_cards, key=sort_key)
        
        if not filtered_cards:
            no_data_label = QLabel("📭 Nenhum card encontrado neste filtro")
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet("color: #999; font-size: 14px; padding: 50px;")
            self.gantt_layout.addWidget(no_data_label)
            return
        
        # Calcular range de datas (apenas cards com datas válidas)
        all_dates = []
        cards_with_dates = []
        
        for card in filtered_cards:
            start = self.parse_date(card.get("data_inicio", ""))
            end = self.parse_date(card.get("data_fim", ""))
            
            # Só adicionar cards que têm pelo menos data de início
            if start:
                cards_with_dates.append(card)
                all_dates.append(start)
                if end:
                    all_dates.append(end)
        
        if not all_dates:
            no_data_label = QLabel("""
                <div style='text-align: center; padding: 50px;'>
                    <h2 style='color: #ff9800;'>⚠️ Nenhum card com datas definidas</h2>
                    <p style='color: #666; font-size: 14px;'>
                        Para visualizar o Gantt Chart, você precisa:<br><br>
                        1. Criar ou editar um card<br>
                        2. Preencher os campos:<br>
                        &nbsp;&nbsp;&nbsp;<b>📅 Data Início</b><br>
                        &nbsp;&nbsp;&nbsp;<b>🏁 Data Fim</b><br>
                        3. Voltar aqui para ver o cronograma!
                    </p>
                </div>
            """)
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setTextFormat(Qt.RichText)
            self.gantt_layout.addWidget(no_data_label)
            return
        
        # Usar apenas cards com datas
        filtered_cards = cards_with_dates
        
        min_date = min(all_dates)
        max_date = max(all_dates)
        
        # Adicionar margem
        min_date = min_date.addDays(-3)
        max_date = max_date.addDays(3)
        
        total_days = min_date.daysTo(max_date)
        
        # Header com datas
        header_widget = QWidget()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(200, 0, 20, 0)
        
        # Gerar marcadores de data (a cada 7 dias)
        current_date = min_date
        while current_date <= max_date:
            date_label = QLabel(current_date.toString("dd/MM"))
            date_label.setStyleSheet("font-size: 10px; color: #666; font-weight: bold;")
            date_label.setMinimumWidth(100)
            date_label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(date_label)
            current_date = current_date.addDays(7)
        
        header_widget.setLayout(header_layout)
        self.gantt_layout.addWidget(header_widget)
        
        # Linha de hoje
        today = QDate.currentDate()
        
        # Renderizar cada card
        for card in filtered_cards:
            card_widget = self.create_gantt_row(card, min_date, max_date, total_days, today)
            self.gantt_layout.addWidget(card_widget)
        
        self.gantt_layout.addStretch()
        
    def create_gantt_row(self, card, min_date, max_date, total_days, today):
        """Cria uma linha do Gantt para um card"""
        row_widget = QWidget()
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(10, 5, 10, 5)
        row_layout.setSpacing(0)
        
        # Título do card (fixo à esquerda)
        title_label = QLabel(card.get("titulo", "Sem título"))
        title_label.setMinimumWidth(180)
        title_label.setMaximumWidth(180)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("""
            font-weight: bold;
            font-size: 11px;
            padding: 5px;
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            border-radius: 4px;
        """)
        row_layout.addWidget(title_label)
        
        # Timeline container
        timeline_container = QWidget()
        timeline_layout = QHBoxLayout()
        timeline_layout.setContentsMargins(0, 0, 0, 0)
        timeline_layout.setSpacing(0)
        
        # Parse dates
        start_date = self.parse_date(card.get("data_inicio", ""))
        end_date = self.parse_date(card.get("data_fim", ""))
        
        if not start_date or not end_date:
            # Sem datas válidas
            no_date_label = QLabel("⚠ Sem datas")
            no_date_label.setStyleSheet("color: #999; font-style: italic; padding: 5px;")
            timeline_layout.addWidget(no_date_label)
        else:
            # Calcular posições
            days_from_start = min_date.daysTo(start_date)
            card_duration = start_date.daysTo(end_date) + 1
            
            # Espaço antes da barra
            if days_from_start > 0:
                spacer_before = QWidget()
                spacer_before.setFixedWidth(int((days_from_start / total_days) * 800))
                timeline_layout.addWidget(spacer_before)
            
            # Barra do card
            bar_width = int((card_duration / total_days) * 800)
            bar_widget = QWidget()
            bar_widget.setFixedWidth(max(bar_width, 20))  # Mínimo 20px
            bar_widget.setFixedHeight(30)
            
            # Cor da barra (verde se no prazo, vermelho se atrasado)
            is_late = end_date < today
            bar_color = "#f44336" if is_late else card.get("cor", "#4caf50")
            
            bar_widget.setStyleSheet(f"""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {bar_color}, stop:1 {self.darken_color(bar_color)});
                border: 2px solid {self.darken_color(bar_color)};
                border-radius: 6px;
            """)
            
            # Tooltip com informações
            tooltip = f"""
            📋 {card.get('titulo', '')}
            📅 Início: {card.get('data_inicio', '')}
            🏁 Fim: {card.get('data_fim', '')}
            📂 Coluna: {card.get('coluna', '')}
            ⚡ Prioridade: {card.get('prioridade', 'Normal')}
            """
            bar_widget.setToolTip(tooltip.strip())
            
            timeline_layout.addWidget(bar_widget)
            
            # Linha do "hoje"
            if min_date <= today <= max_date:
                days_to_today = min_date.daysTo(today)
                # Será desenhado depois
        
        timeline_layout.addStretch()
        timeline_container.setLayout(timeline_layout)
        row_layout.addWidget(timeline_container)
        
        row_widget.setLayout(row_layout)
        row_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border-bottom: 1px solid #e0e0e0;
            }
            QWidget:hover {
                background-color: #f9f9f9;
            }
        """)
        
        return row_widget
        
    def parse_date(self, date_str):
        """Converte string dd/mm/yyyy para QDate"""
        if not date_str:
            return None
        try:
            parts = date_str.split("/")
            return QDate(int(parts[2]), int(parts[1]), int(parts[0]))
        except:
            return None
            
    def darken_color(self, color):
        """Escurece uma cor hex em 30%"""
        color = color.lstrip('#')
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        r = int(r * 0.7)
        g = int(g * 0.7)
        b = int(b * 0.7)
        return f'#{r:02x}{g:02x}{b:02x}'


class KanbanWindow(QMainWindow):
    """Janela principal do Kanban"""
    
    def __init__(self):
        super().__init__()
        self.dark_mode = False  # Começa no modo claro
        
        # Sistema de licenciamento
        self.license_manager = None
        if LICENSE_ENABLED:
            self.license_manager = LicenseManager()
            if not self.check_license():
                return  # Sair se não houver licença válida
        
        self.setup_ui()
        self.setup_shortcuts()
        self.setup_tray()
        self.load_data()
    
    def check_license(self):
        """Verifica licença no startup"""
        if not LICENSE_ENABLED or not self.license_manager:
            return True  # Se licenciamento desabilitado, permitir uso
        
        is_valid, message = self.license_manager.check_license()
        
        if not is_valid:
            # Mostrar dialog de ativação
            dialog = ActivateDialog(self)
            if dialog.exec() == QDialog.Accepted:
                # Licença ativada, continuar
                return True
            else:
                # Usuário cancelou, sair
                QMessageBox.warning(
                    self,
                    "Licença Necessária",
                    "O PinFlow Pro requer uma licença válida para funcionar.\n\n"
                    "Por favor, ative sua licença para continuar."
                )
                return False
        
        return True
    
    def set_titlebar_color(self):
        """Personaliza cor da barra de título do Windows para azul marinho"""
        try:
            # Azul marinho: #1e3a5f = RGB(30, 58, 95)
            # Windows usa formato BGR (inverso)
            hwnd = int(self.winId())
            blue = 95   # Componente azul
            green = 58  # Componente verde
            red = 30    # Componente vermelho
            
            # BGR em formato DWORD (0x00BBGGRR)
            color = blue << 16 | green << 8 | red
            
            # Aplicar cor à barra de título
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 
                DWMWA_CAPTION_COLOR,
                ctypes.byref(ctypes.c_int(color)),
                ctypes.sizeof(ctypes.c_int)
            )
        except:
            pass  # Se falhar (não Windows ou sem permissão), continua normalmente
        
    def setup_ui(self):
        """Configura interface"""
        self.setWindowTitle("📌 PinFlow Pro")
        self.setGeometry(100, 100, 1500, 750)
        
        # Always on top
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # Personalizar cor da barra de título do Windows (azul marinho)
        self.set_titlebar_color()
        
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        # Header com logo
        header_layout = QHBoxLayout()
        
        # Logo + Título no canto esquerdo - SEMPRE PinFlow Pro
        title_label = QLabel("📌➜ Pin<span style='color: #00C853; font-weight: bold;'>Flow</span> <span style='color: #888888; font-size: 14px;'>Pro</span>")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_label.setTextFormat(Qt.RichText)
        title_label.setStyleSheet("color: #1e3a5f; padding: 10px;")  # Azul marinho escuro
        
        # Guardar referência para não mudar cor quando header mudar
        self.title_label = title_label
        
        # Nome do cliente no lado direito (se houver licença)
        customer_name_label = None
        if LICENSE_ENABLED and self.license_manager:
            license_info = self.license_manager.get_license_info()
            if license_info:
                customer_name = license_info.get('customer_name', None)
                if customer_name:
                    customer_name_text = f"<span style='color: #1e3a5f; font-weight: bold;'>{customer_name}</span>"
                    customer_name_label = QLabel(customer_name_text)
                    customer_name_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
                    customer_name_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    customer_name_label.setTextFormat(Qt.RichText)
                    customer_name_label.setStyleSheet("color: #1e3a5f; padding: 10px; cursor: pointer;")  # Cursor pointer para indicar clicável
                    customer_name_label.setCursor(Qt.PointingHandCursor)
                    customer_name_label.mousePressEvent = lambda e: self.show_config_dialog()  # Clicável para abrir configurações
        
        # Logo e tema no canto superior direito (lado a lado)
        logo_theme_layout = QHBoxLayout()
        logo_theme_layout.setSpacing(10)
        logo_theme_layout.setAlignment(Qt.AlignCenter)
        
        # Toggle tema (Sol/Lua) - À ESQUERDA
        self.theme_toggle = QPushButton("☀️")
        self.theme_toggle.setCheckable(True)
        self.theme_toggle.setChecked(False)
        self.theme_toggle.clicked.connect(self.toggle_theme)
        self.theme_toggle.setFixedSize(QSize(50, 50))
        self.theme_toggle.setCursor(Qt.PointingHandCursor)
        self.theme_toggle.setToolTip("Alternar tema (Claro/Escuro)")
        self.theme_toggle.setStyleSheet("""
            QPushButton {
                background-color: rgba(30, 58, 95, 0.15);
                border: 2px solid rgba(30, 58, 95, 0.6);
                border-radius: 25px;
                font-size: 24px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(30, 58, 95, 0.25);
                border: 3px solid #1e3a5f;
                transform: scale(1.1);
            }
            QPushButton:checked {
                background-color: rgba(30, 58, 95, 0.3);
                border: 2px solid rgba(30, 58, 95, 0.8);
            }
        """)
        
        # Logo - À DIREITA
        logo_label = QLabel("📌\nKANBAN\nPRO")
        logo_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            color: #1e3a5f;
            background-color: rgba(30, 58, 95, 0.1);
            border: 2px solid #1e3a5f;
            border-radius: 10px;
            padding: 10px;
            min-width: 80px;
            max-width: 80px;
            min-height: 80px;
            max-height: 80px;
        """)
        
        logo_theme_layout.addWidget(self.theme_toggle)
        logo_theme_layout.addWidget(logo_label)
        
        # Botão Configuração do Sistema
        self.config_btn = QPushButton("⚙️ Configuração")
        self.config_btn.setCursor(Qt.PointingHandCursor)
        self.config_btn.setToolTip("Configurações do Sistema")
        self.config_btn.setFocusPolicy(Qt.StrongFocus)  # Permitir foco
        self.config_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #8b9dc3);
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #152d4a, stop:1 #7a8bb0);
            }
        """)
        self.config_btn.clicked.connect(self.show_config_dialog)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.config_btn)
        header_layout.addLayout(logo_theme_layout)
        
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        self.header_widget = header_widget  # Guardar referência para modo escuro
        
        # Carregar cor do header salva (se houver)
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    if "header_color" in settings:
                        header_color = settings["header_color"]
                        # Converter hex para RGB
                        color = QColor(header_color)
                        r, g, b = color.red(), color.green(), color.blue()
                        header_widget.setStyleSheet(f"""
                            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 rgb({r}, {g}, {b}), 
                                stop:1 rgb({min(255, r+50)}, {min(255, g+50)}, {min(255, b+50)}));
                            border-radius: 8px;
                            padding: 10px;
                        """)
                    else:
                        header_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a5f, stop:1 #8b9dc3); border-radius: 8px; padding: 10px;")
            else:
                header_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a5f, stop:1 #8b9dc3); border-radius: 8px; padding: 10px;")
        except:
            header_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a5f, stop:1 #8b9dc3); border-radius: 8px; padding: 10px;")
        
        # Barra de ferramentas
        toolbar_layout = QHBoxLayout()
        
        # Busca
        search_label = QLabel("🔍")
        search_label.setFont(QFont("Segoe UI", 12))
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar cards...")
        self.search_input.textChanged.connect(self.filter_cards)
        self.search_input.setMaximumWidth(300)
        
        # Estilo padrão para botões da toolbar - Gradiente azul marinho → prata
        btn_style = """
            QPushButton {
                padding: 8px 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #8b9dc3);
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #152d4a, stop:1 #7a8bb0);
            }
        """
        
        # Botão Nova Coluna
        new_column_btn = QPushButton("➕ Nova Coluna")
        new_column_btn.clicked.connect(self.add_new_column)
        new_column_btn.setCursor(Qt.PointingHandCursor)
        new_column_btn.setStyleSheet(btn_style)
        
        # Botão Gantt Chart
        gantt_btn = QPushButton("📊 Gantt")
        gantt_btn.clicked.connect(self.show_gantt)
        gantt_btn.setCursor(Qt.PointingHandCursor)
        gantt_btn.setStyleSheet(btn_style)
        gantt_btn.setToolTip("Ver cronograma visual do projeto")
        
        # Botão Dashboard
        dashboard_btn = QPushButton("📈 Dashboard")
        dashboard_btn.clicked.connect(self.show_dashboard)
        dashboard_btn.setCursor(Qt.PointingHandCursor)
        dashboard_btn.setStyleSheet(btn_style)
        dashboard_btn.setToolTip("Ver estatísticas e produtividade")
        
        # Botão Backup
        backup_btn = QPushButton("💾 Backup")
        backup_btn.clicked.connect(self.create_backup)
        backup_btn.setCursor(Qt.PointingHandCursor)
        backup_btn.setStyleSheet(btn_style)
        backup_btn.setToolTip("Criar backup dos dados")
        
        # GUARDAR REFERÊNCIAS DOS BOTÕES PARA ATUALIZAR CORES DEPOIS
        self.toolbar_buttons = [new_column_btn, gantt_btn, dashboard_btn, backup_btn]
        
        # Transparência
        transparency_label = QLabel("💎 Transparência:")
        
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setMinimum(30)
        self.transparency_slider.setMaximum(100)
        self.transparency_slider.setValue(100)
        self.transparency_slider.setMaximumWidth(150)
        self.transparency_slider.valueChanged.connect(self.change_transparency)
        
        self.transparency_value_label = QLabel("100%")
        self.transparency_value_label.setMinimumWidth(40)
        
        toolbar_layout.addWidget(search_label)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(new_column_btn)
        toolbar_layout.addWidget(gantt_btn)
        toolbar_layout.addWidget(dashboard_btn)
        toolbar_layout.addWidget(backup_btn)
        
        # Botão Licença (se habilitado)
        if LICENSE_ENABLED and self.license_manager:
            license_btn = QPushButton("🔐 Licença")
            license_btn.clicked.connect(self.show_activate_dialog)
            license_btn.setCursor(Qt.PointingHandCursor)
            license_btn.setStyleSheet(btn_style)
            license_btn.setToolTip("Ativar ou verificar licença")
            toolbar_layout.addWidget(license_btn)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(transparency_label)
        toolbar_layout.addWidget(self.transparency_slider)
        toolbar_layout.addWidget(self.transparency_value_label)
        
        # Área de colunas com scroll horizontal
        self.columns_scroll = QScrollArea()
        self.columns_scroll.setWidgetResizable(True)
        self.columns_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.columns_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.columns_container = QWidget()
        self.columns_container.setAcceptDrops(True)
        self.columns_layout = QHBoxLayout()
        self.columns_layout.setSpacing(15)
        self.columns_layout.setAlignment(Qt.AlignLeft)
        
        # Colunas iniciais
        self.columns = []
        self.add_initial_columns()
        
        self.columns_container.setLayout(self.columns_layout)
        
        # Sobrescrever dragEnterEvent e dropEvent do container para reordenar colunas
        def columns_drag_enter(event):
            if event.mimeData().hasText() and event.mimeData().text().startswith("COLUMN:"):
                event.acceptProposedAction()
        
        def columns_drop(event):
            if event.mimeData().hasText() and event.mimeData().text().startswith("COLUMN:"):
                try:
                    # Pegar index da coluna arrastada
                    old_index = int(event.mimeData().text().split(":")[1])
                    
                    # Calcular novo index baseado na posição do drop
                    pos = get_event_pos(event)
                    drop_x = pos.x()
                    new_index = 0
                    accumulated_width = 0
                    
                    for i, col in enumerate(self.columns):
                        accumulated_width += col.width() + self.columns_layout.spacing()
                        if drop_x < accumulated_width:
                            new_index = i
                            break
                    else:
                        new_index = len(self.columns)
                    
                    # Reordenar
                    if old_index != new_index:
                        self.reorder_columns(old_index, new_index)
                    
                    event.acceptProposedAction()
                except:
                    pass
        
        self.columns_container.dragEnterEvent = columns_drag_enter
        self.columns_container.dropEvent = columns_drop
        
        self.columns_scroll.setWidget(self.columns_container)
        
        # Barra de botões inferior
        buttons_layout = QHBoxLayout()
        
        # Always on top toggle
        self.toggle_btn = QPushButton("📌 Always On Top: ON")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(True)
        self.toggle_btn.clicked.connect(self.toggle_always_on_top)
        
        # Limpar concluídos
        clear_completed_btn = QPushButton("🗑️ Limpar Concluídos")
        clear_completed_btn.clicked.connect(self.clear_completed)
        
        # Ver arquivados
        view_archived_btn = QPushButton("📂 Ver Arquivados")
        view_archived_btn.clicked.connect(self.view_archived)
        
        # Atalhos
        shortcuts_btn = QPushButton("⌨️ Atalhos")
        shortcuts_btn.clicked.connect(self.show_shortcuts)
        
        # Estilo unificado: Gradiente azul marinho → prata
        button_style = """
            QPushButton {
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #a0a0a0);
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #152d4a, stop:1 #8a8a8a);
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2a4f7f, stop:1 #b0b0b0);
            }
        """
        
        self.toggle_btn.setStyleSheet(button_style)
        clear_completed_btn.setStyleSheet(button_style)
        view_archived_btn.setStyleSheet(button_style)
        shortcuts_btn.setStyleSheet(button_style)
        
        # GUARDAR REFERÊNCIAS DOS BOTÕES INFERIORES PARA ATUALIZAR CORES DEPOIS
        self.bottom_buttons = [self.toggle_btn, clear_completed_btn, view_archived_btn, shortcuts_btn]
        
        buttons_layout.addWidget(self.toggle_btn)
        buttons_layout.addWidget(clear_completed_btn)
        buttons_layout.addWidget(view_archived_btn)
        buttons_layout.addWidget(shortcuts_btn)
        
        # Copyright
        copyright_label = QLabel("© 2025 - Criado por Ede Machado")
        copyright_label.setFont(QFont("Segoe UI", 8))
        copyright_label.setAlignment(Qt.AlignCenter)
        copyright_label.setStyleSheet("""
            color: #999999;
            padding: 5px;
            background-color: transparent;
        """)
        self.copyright_label = copyright_label  # Guardar referência para modo escuro
        
        # Montar layout principal
        main_layout.addWidget(header_widget)
        main_layout.addLayout(toolbar_layout)
        main_layout.addWidget(self.columns_scroll, stretch=1)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(copyright_label)
        
        central.setLayout(main_layout)
        
        # Aplicar tema claro inicial
        self.apply_theme()
    
    def apply_theme(self):
        """Aplica tema claro ou escuro"""
        # Carregar cor do header salva (se houver) antes de aplicar tema
        header_color_saved = None
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    if "header_color" in settings:
                        header_color_saved = settings["header_color"]
        except:
            pass
        
        if self.dark_mode:
            # MODO ESCURO - TUDO PRETO ELEGANTE (cores fixas, não muda com cores personalizadas)
            self.header_widget.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d1b2a, stop:1 #1b263b);
                border-radius: 8px;
            """)
            self.copyright_label.setStyleSheet("""
                color: #5c5c5c;
                padding: 5px;
                background-color: transparent;
            """)
            
            # Mudar barra de título para preto no modo escuro
            try:
                hwnd = int(self.winId())
                # Preto escuro: #0d1b2a = RGB(13, 27, 42)
                color = 42 << 16 | 27 << 8 | 13  # BGR
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_CAPTION_COLOR,
                    ctypes.byref(ctypes.c_int(color)),
                    ctypes.sizeof(ctypes.c_int)
                )
            except:
                pass
            
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #0a0a0a;
                }
                QWidget {
                    background-color: #0a0a0a;
                    color: #e0e0e0;
                }
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #3d3d3d;
                    border-radius: 5px;
                    font-size: 12px;
                    background-color: #1a1a1a;
                    color: #ffffff;
                }
                QLineEdit:focus {
                    border: 2px solid #5c5c5c;
                    background-color: #2d2d2d;
                }
                QLabel {
                    color: #e0e0e0;
                    background-color: transparent;
                }
                QScrollArea {
                    background-color: #0a0a0a;
                    border: none;
                }
                QSlider::groove:horizontal {
                    background-color: #2d2d2d;
                    height: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background-color: #5c5c5c;
                    width: 18px;
                    margin: -5px 0;
                    border-radius: 9px;
                }
                QSlider::handle:horizontal:hover {
                    background-color: #7d7d7d;
                }
            """)
        else:
            # MODO CLARO - Carregar cor salva ou usar padrão
            if header_color_saved:
                # Usar cor salva
                color = QColor(header_color_saved)
                r, g, b = color.red(), color.green(), color.blue()
                self.header_widget.setStyleSheet(f"""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb({r}, {g}, {b}), 
                        stop:1 rgb({min(255, r+50)}, {min(255, g+50)}, {min(255, b+50)}));
                    border-radius: 8px;
                    padding: 10px;
                """)
            else:
                # MODO CLARO - GRADIENTE AZUL ESCURO → PRATA
                self.header_widget.setStyleSheet("""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1e3a5f, stop:1 #c0c0c0);
                    border-radius: 8px;
                """)
        
        # Garantir que logo/título mantenha cor fixa (não muda com header ou tema)
        if hasattr(self, 'title_label'):
            # Se for nome do cliente (clicável), manter estilo com cursor
            if hasattr(self.title_label, 'mousePressEvent'):
                self.title_label.setStyleSheet("color: #1e3a5f; padding: 10px; cursor: pointer;")
            else:
                self.title_label.setStyleSheet("color: #1e3a5f; padding: 10px;")
            self.copyright_label.setStyleSheet("""
                color: #999999;
                padding: 5px;
                background-color: transparent;
            """)
            
            # Mudar barra de título para azul marinho no modo claro
            try:
                hwnd = int(self.winId())
                # Azul marinho: #1e3a5f = RGB(30, 58, 95)
                color = 95 << 16 | 58 << 8 | 30  # BGR
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, DWMWA_CAPTION_COLOR,
                    ctypes.byref(ctypes.c_int(color)),
                    ctypes.sizeof(ctypes.c_int)
                )
            except:
                pass
            
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #fafafa;
                }
                QWidget {
                    background-color: #fafafa;
                }
                KanbanColumn {
                    background-color: #f5f5f5;
                }
                QLineEdit {
                    padding: 8px;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                    font-size: 12px;
                    background-color: white;
                    color: #000000;
                }
                QLineEdit:focus {
                    border: 2px solid #1e3a5f;
                }
                QLabel {
                    color: #333333;
                    background-color: transparent;
                }
                QScrollArea {
                    background-color: #fafafa;
                    border: none;
                }
            """)
    
    def toggle_theme(self, checked):
        """Alterna entre modo escuro e claro"""
        self.dark_mode = checked
        self.apply_theme()
        
        # Atualizar ícone do botão (Sol para claro, Lua para escuro)
        if self.dark_mode:
            self.theme_toggle.setText("🌙")
            self.theme_toggle.setToolTip("Modo Escuro ativo - Clique para modo claro")
        else:
            self.theme_toggle.setText("☀️")
            self.theme_toggle.setToolTip("Modo Claro ativo - Clique para modo escuro")
        
        # Atualizar todas as colunas
        for col in self.columns:
            col.update_column_style()
            # Atualizar todos os cards da coluna
            for card in col.cards:
                card.update_card_style()
        
        self.save_data()
    
    def add_initial_columns(self):
        """Adiciona colunas iniciais"""
        # TODAS AS COLUNAS COM A MESMA COR DA COLUNA "NOTAS" (#607d8b)
        cor_padrao = "#607d8b"  # Cinza azulado (cor da coluna NOTAS)
        
        initial_columns = [
            ("📋 A Fazer", cor_padrao, "todo"),
            ("⚡ Em Andamento", cor_padrao, "doing"),
            ("✔️ Feito", cor_padrao, "done"),
            ("👍 Aprovado", cor_padrao, "approved"),
            ("✅ Concluído", cor_padrao, "completed")
        ]
        
        for titulo, cor, col_id in initial_columns:
            col = KanbanColumn(titulo, cor, self, col_id)
            self.columns.append(col)
            # Inserir antes do botão "Adicionar coluna"
            self.columns_layout.insertWidget(self.columns_layout.count() - 1, col)
    
    def reorder_columns(self, old_index, new_index):
        """Reordena colunas"""
        if old_index == new_index:
            return
        
        # Mover na lista
        column = self.columns.pop(old_index)
        self.columns.insert(new_index, column)
        
        # Remover todas as colunas do layout
        for i in reversed(range(self.columns_layout.count())):
            item = self.columns_layout.itemAt(i)
            if item.widget():
                self.columns_layout.removeWidget(item.widget())
        
        # Adicionar de volta na nova ordem
        for col in self.columns:
            self.columns_layout.addWidget(col)
        
        # Salvar nova ordem
        self.save_data()
    
    def add_new_column(self):
        """Adiciona uma nova coluna"""
        # Dialog customizado mais simples
        dialog = QDialog(self)
        dialog.setWindowTitle("Nova Coluna")
        dialog.setModal(True)
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Nome
        layout.addWidget(QLabel("Nome da coluna:"))
        name_input = QLineEdit()
        name_input.setText("Nova Coluna")
        name_input.selectAll()
        layout.addWidget(name_input)
        
        # Cor - Grid de cores simples
        layout.addWidget(QLabel("Escolha uma cor:"))
        
        colors_layout = QHBoxLayout()
        color_buttons = []
        default_colors = [
            ("#2196F3", "Azul"),
            ("#ff9800", "Laranja"),
            ("#9c27b0", "Roxo"),
            ("#00bcd4", "Ciano"),
            ("#4caf50", "Verde"),
            ("#f44336", "Vermelho"),
            ("#607d8b", "Cinza"),
            ("#e91e63", "Rosa")
        ]
        
        selected_color = {"value": "#607d8b"}  # Padrão
        
        for color_hex, color_name in default_colors:
            btn = QPushButton()
            btn.setFixedSize(40, 40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color_hex};
                    border: 2px solid #ddd;
                    border-radius: 5px;
                }}
                QPushButton:hover {{
                    border: 3px solid #333;
                }}
            """)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setToolTip(color_name)
            btn.clicked.connect(lambda checked, c=color_hex: selected_color.update({"value": c}))
            colors_layout.addWidget(btn)
            color_buttons.append(btn)
        
        layout.addLayout(colors_layout)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        # Mostrar dialog
        if dialog.exec() == QDialog.Accepted:
            name = name_input.text().strip()
            if not name:
                QMessageBox.warning(self, "Erro", "Nome da coluna não pode ser vazio!")
                return
            
            # Criar coluna
            col_id = name.lower().replace(" ", "_")
            col = KanbanColumn(name, selected_color["value"], self, col_id)
            self.columns.append(col)
            
            # Inserir antes do botão "Adicionar coluna"
            self.columns_layout.insertWidget(self.columns_layout.count() - 1, col)
            
            self.save_data()
            QMessageBox.information(self, "Sucesso", f"Coluna '{name}' criada!")
    
    def remove_column(self, column):
        """Remove uma coluna"""
        if column in self.columns:
            self.columns.remove(column)
            column.deleteLater()
            self.save_data()
            QMessageBox.information(self, "Removida", f"Coluna '{column.titulo}' removida!")
        
    def setup_shortcuts(self):
        """Configura atalhos de teclado"""
        # Ctrl+N - Novo card na primeira coluna
        if self.columns:
            QShortcut(QKeySequence("Ctrl+N"), self, self.columns[0].add_card_manual)
        
        # Ctrl+F - Focar busca
        QShortcut(QKeySequence("Ctrl+F"), self, self.search_input.setFocus)
        
        # Ctrl+T - Toggle always on top
        QShortcut(QKeySequence("Ctrl+T"), self, lambda: self.toggle_btn.click())
        
        # Ctrl+Q - Sair
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        
        # F1 - Mostrar atalhos
        QShortcut(QKeySequence("F1"), self, self.show_shortcuts)
        
    def setup_tray(self):
        """Configura ícone na bandeja do sistema"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Criar ícone simples
        icon = QApplication.style().standardIcon(QApplication.style().StandardPixmap.SP_FileDialogListView)
        self.tray_icon.setIcon(icon)
        
        # Menu do tray
        tray_menu = QMenu()
        
        show_action = QAction("Mostrar", self)
        show_action.triggered.connect(self.show)
        
        quit_action = QAction("Sair", self)
        quit_action.triggered.connect(self.close)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        
        # Opção de licença (se habilitado)
        if LICENSE_ENABLED and self.license_manager:
            license_action = QAction("🔐 Ativar Licença", self)
            license_action.triggered.connect(self.show_activate_dialog)
            tray_menu.addAction(license_action)
            tray_menu.addSeparator()
        
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_activated)
        self.tray_icon.show()
        
        self.tray_icon.setToolTip("PinFlow Pro - Suas tarefas sempre no topo!")
        
    def tray_activated(self, reason):
        """Ação ao clicar no ícone da bandeja"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()
            
    def show_activate_dialog(self):
        """Mostra dialog de ativação de licença"""
        if not LICENSE_ENABLED or not self.license_manager:
            QMessageBox.information(self, "Informação", "Sistema de licenciamento não disponível.")
            return
        
        dialog = ActivateDialog(self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Sucesso", "Licença ativada com sucesso!")
    
    def show_config_dialog(self):
        """Mostra dialog de configurações do sistema"""
        dialog = QDialog(self)
        dialog.setWindowTitle("⚙️ Configurações do Sistema - PinFlow Pro")
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Título
        title = QLabel("⚙️ Configurações do Sistema")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1e3a5f; padding: 10px;")
        layout.addWidget(title)
        
        # Abas ou seções
        tabs = QTabWidget()
        
        # === ABA 1: APARÊNCIA ===
        appearance_tab = QWidget()
        appearance_layout = QVBoxLayout()
        
        # Idioma - SEMPRE MOSTRAR
        language_group = QGroupBox("🌍 Idioma / Language")
        language_layout = QVBoxLayout()
        
        language_label = QLabel("Selecione o idioma / Select language:")
        language_layout.addWidget(language_label)
        
        language_combo = QComboBox()
        if I18N_ENABLED:
            try:
                current_lang = I18nManager.get_current_language()
                for code, name in I18nManager.LANGUAGES.items():
                    language_combo.addItem(name, code)
                    if code == current_lang:
                        language_combo.setCurrentIndex(language_combo.count() - 1)
            except:
                language_combo.addItem("Português (Brasil)", "pt_BR")
        else:
            language_combo.addItem("Português (Brasil)", "pt_BR")
            language_combo.addItem("English (US)", "en_US")
            language_combo.addItem("Español", "es_ES")
        
        def change_language():
            lang_code = language_combo.currentData()
            if I18N_ENABLED:
                try:
                    if I18nManager.set_language(lang_code):
                        # Salvar preferência
                        try:
                            settings = {}
                            if os.path.exists("settings.json"):
                                with open("settings.json", "r", encoding="utf-8") as f:
                                    settings = json.load(f)
                            settings["language"] = lang_code
                            with open("settings.json", "w", encoding="utf-8") as f:
                                json.dump(settings, f, ensure_ascii=False, indent=2)
                            QMessageBox.information(dialog, "Idioma Alterado", 
                                f"Idioma alterado para: {I18nManager.get_language_name(lang_code)}\n\n"
                                "Recarregue o aplicativo para aplicar as mudanças.")
                        except Exception as e:
                            print(f"Erro ao salvar idioma: {e}")
                except:
                    pass
            else:
                # Mesmo sem I18N, salvar preferência
                try:
                    settings = {}
                    if os.path.exists("settings.json"):
                        with open("settings.json", "r", encoding="utf-8") as f:
                            settings = json.load(f)
                    settings["language"] = lang_code
                    with open("settings.json", "w", encoding="utf-8") as f:
                        json.dump(settings, f, ensure_ascii=False, indent=2)
                    QMessageBox.information(dialog, "Idioma Alterado", 
                        f"Preferência de idioma salva: {lang_code}\n\n"
                        "Recarregue o aplicativo para aplicar as mudanças.")
                except Exception as e:
                    print(f"Erro ao salvar idioma: {e}")
        
        language_combo.currentIndexChanged.connect(change_language)
        language_layout.addWidget(language_combo)
        
        language_group.setLayout(language_layout)
        appearance_layout.addWidget(language_group)
        
        # Cores do sistema
        colors_group = QGroupBox("🎨 Cores do Sistema")
        colors_layout = QVBoxLayout()
        
        # Cor do header
        header_color_layout = QHBoxLayout()
        header_color_layout.addWidget(QLabel("Cor do Header:"))
        self.header_color_btn = QPushButton("Alterar Cor")
        self.header_color_btn.clicked.connect(lambda: self.change_header_color(dialog))
        header_color_layout.addWidget(self.header_color_btn)
        
        # Botão voltar ao padrão
        self.header_reset_btn = QPushButton("↩️ Padrão")
        self.header_reset_btn.setToolTip("Voltar à cor padrão do header")
        self.header_reset_btn.clicked.connect(lambda: self.reset_header_color(dialog))
        header_color_layout.addWidget(self.header_reset_btn)
        header_color_layout.addStretch()
        colors_layout.addLayout(header_color_layout)
        
        # Cor das colunas
        column_color_layout = QHBoxLayout()
        column_color_layout.addWidget(QLabel("Cor dos Headers das Colunas:"))
        self.column_color_btn = QPushButton("Alterar Cor")
        self.column_color_btn.clicked.connect(lambda: self.change_column_header_color(dialog))
        column_color_layout.addWidget(self.column_color_btn)
        
        # Botão voltar ao padrão
        self.column_reset_btn = QPushButton("↩️ Padrão")
        self.column_reset_btn.setToolTip("Voltar à cor padrão dos headers das colunas")
        self.column_reset_btn.clicked.connect(lambda: self.reset_column_header_color(dialog))
        column_color_layout.addWidget(self.column_reset_btn)
        column_color_layout.addStretch()
        colors_layout.addLayout(column_color_layout)
        
        colors_group.setLayout(colors_layout)
        appearance_layout.addWidget(colors_group)
        
        appearance_layout.addStretch()
        appearance_tab.setLayout(appearance_layout)
        tabs.addTab(appearance_tab, "🎨 Aparência")
        
        # === ABA 2: LICENCIAMENTO ===
        license_tab = QWidget()
        license_layout = QVBoxLayout()
        
        if LICENSE_ENABLED and self.license_manager:
            license_info = self.license_manager.get_license_info()
            if license_info:
                info_text = f"""
                <b>Informações da Licença:</b><br><br>
                <b>Cliente:</b> {license_info['customer_name']}<br>
                <b>Email:</b> {license_info['customer_email']}<br>
                <b>Emitida em:</b> {license_info['issue_date']}<br>
                <b>Válida até:</b> {license_info['expiry_date']}<br>
                <b>Ativada em:</b> {license_info['activated_date']}<br>
                <b>Hardware ID:</b> {license_info['hwid']}<br>
                <b>Versão:</b> {license_info['version']}
                """
                info_label = QLabel(info_text)
                info_label.setWordWrap(True)
                license_layout.addWidget(info_label)
            else:
                no_license_label = QLabel("Nenhuma licença ativada.")
                license_layout.addWidget(no_license_label)
            
            activate_btn = QPushButton("🔐 Ativar/Verificar Licença")
            activate_btn.clicked.connect(lambda: (dialog.accept(), self.show_activate_dialog()))
            activate_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #1e3a5f, stop:1 #8b9dc3);
                    color: white;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #152d4a, stop:1 #7a8bb0);
                }
            """)
            license_layout.addWidget(activate_btn)
        else:
            no_license_label = QLabel("Sistema de licenciamento não disponível.")
            license_layout.addWidget(no_license_label)
        
        license_layout.addStretch()
        license_tab.setLayout(license_layout)
        tabs.addTab(license_tab, "🔐 Licenciamento")
        
        # === ABA 3: GERAL ===
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        
        # Informações do sistema
        system_info = QGroupBox("ℹ️ Informações do Sistema")
        system_layout = QVBoxLayout()
        
        info_text = f"""
        <b>PinFlow Pro v3.0</b><br><br>
        <b>Desenvolvedor:</b> Ede Machado<br>
        <b>Versão:</b> 3.0<br>
        <b>Python:</b> {sys.version.split()[0]}<br>
        <b>PySide6:</b> {PySide6.__version__ if hasattr(PySide6, '__version__') else 'N/A'}<br><br>
        <b>© 2025 - Criado por Ede Machado</b>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        system_layout.addWidget(info_label)
        
        system_info.setLayout(system_layout)
        general_layout.addWidget(system_info)
        
        general_layout.addStretch()
        general_tab.setLayout(general_layout)
        tabs.addTab(general_tab, "ℹ️ Sobre")
        
        layout.addWidget(tabs)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def change_header_color(self, parent_dialog):
        """Altera cor do header"""
        from PySide6.QtWidgets import QColorDialog
        # Carregar cor atual ou usar padrão
        current_color = QColor(30, 58, 95)  # Padrão
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    if "header_color" in settings:
                        current_color = QColor(settings["header_color"])
        except:
            pass
        
        color = QColorDialog.getColor(current_color, parent_dialog, "Escolha cor do Header")
        if color.isValid():
            # Salvar cor nas configurações
            try:
                settings = {}
                if os.path.exists("settings.json"):
                    with open("settings.json", "r", encoding="utf-8") as f:
                        settings = json.load(f)
                settings["header_color"] = color.name()
                with open("settings.json", "w", encoding="utf-8") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=2)
                
                # Aplicar cor imediatamente (mas manter logo/título com cor fixa)
                r, g, b = color.red(), color.green(), color.blue()
                gradient_style = f"""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb({r}, {g}, {b}), 
                        stop:1 rgb({min(255, r+50)}, {min(255, g+50)}, {min(255, b+50)}));
                    border-radius: 8px;
                    padding: 10px;
                """
                self.header_widget.setStyleSheet(gradient_style)
                # Garantir que logo/título mantenha cor fixa (não muda com header)
                if hasattr(self, 'title_label'):
                    self.title_label.setStyleSheet("color: #1e3a5f; padding: 10px;")
                
                # Atualizar cor dos botões (tom mais escuro do header)
                self.update_buttons_color(color)
                
                QMessageBox.information(parent_dialog, "Cor Alterada", 
                    f"Cor do header alterada para: {color.name()}\n\nA mudança foi aplicada imediatamente!")
            except Exception as e:
                QMessageBox.warning(parent_dialog, "Erro", f"Erro ao salvar cor: {e}")
    
    def change_column_header_color(self, parent_dialog):
        """Altera cor dos headers das colunas"""
        from PySide6.QtWidgets import QColorDialog
        # Carregar cor atual ou usar padrão
        current_color = QColor(30, 58, 95)  # Padrão
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    if "column_header_color" in settings:
                        current_color = QColor(settings["column_header_color"])
        except:
            pass
        
        color = QColorDialog.getColor(current_color, parent_dialog, "Escolha cor dos Headers das Colunas")
        if color.isValid():
            # Salvar cor nas configurações
            try:
                settings = {}
                if os.path.exists("settings.json"):
                    with open("settings.json", "r", encoding="utf-8") as f:
                        settings = json.load(f)
                settings["column_header_color"] = color.name()
                with open("settings.json", "w", encoding="utf-8") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=2)
                
                # Aplicar cor imediatamente em todas as colunas
                r, g, b = color.red(), color.green(), color.blue()
                gradient_style = f"""
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 rgb({r}, {g}, {b}), 
                        stop:1 rgb({min(255, r+30)}, {min(255, g+30)}, {min(255, b+30)}));
                    border-radius: 8px;
                    padding: 8px;
                """
                # Aplicar em todas as colunas existentes IMEDIATAMENTE
                for column in self.columns:
                    if hasattr(column, 'header_container'):
                        column.header_container.setStyleSheet(gradient_style)
                        # Forçar atualização visual imediata
                        column.header_container.update()
                        column.header_container.repaint()
                        # Também atualizar a coluna inteira
                        column.update()
                        column.repaint()
                
                # Forçar atualização da janela principal
                self.update()
                self.repaint()
                
                QMessageBox.information(parent_dialog, "Cor Alterada", 
                    f"Cor dos headers das colunas alterada para: {color.name()}\n\nA mudança foi aplicada imediatamente!")
            except Exception as e:
                QMessageBox.warning(parent_dialog, "Erro", f"Erro ao salvar cor: {e}")
    
    def reset_header_color(self, parent_dialog):
        """Volta cor do header ao padrão"""
        try:
            settings = {}
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
            if "header_color" in settings:
                del settings["header_color"]
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            
            # Aplicar cor padrão
            self.header_widget.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1e3a5f, stop:1 #8b9dc3); border-radius: 8px; padding: 10px;")
            if hasattr(self, 'title_label'):
                self.title_label.setStyleSheet("color: #1e3a5f; padding: 10px;")
            
            # Restaurar cor padrão dos botões
            default_color = QColor(30, 58, 95)  # #1e3a5f
            self.update_buttons_color(default_color)
            
            QMessageBox.information(parent_dialog, "Cor Restaurada", "Cor do header restaurada ao padrão!")
        except Exception as e:
            QMessageBox.warning(parent_dialog, "Erro", f"Erro ao restaurar cor: {e}")
    
    def reset_column_header_color(self, parent_dialog):
        """Volta cor dos headers das colunas ao padrão"""
        try:
            settings = {}
            if os.path.exists("settings.json"):
                with open("settings.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)
            if "column_header_color" in settings:
                del settings["column_header_color"]
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            
            # Aplicar cor padrão em todas as colunas IMEDIATAMENTE
            default_style = """
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3a5f, stop:1 #2a5080);
                border-radius: 8px;
                padding: 8px;
            """
            for column in self.columns:
                if hasattr(column, 'header_container'):
                    column.header_container.setStyleSheet(default_style)
                    # Forçar atualização visual imediata
                    column.header_container.update()
                    column.header_container.repaint()
                    # Também atualizar a coluna inteira
                    column.update()
                    column.repaint()
            
            # Forçar atualização da janela principal
            self.update()
            self.repaint()
            
            QMessageBox.information(parent_dialog, "Cor Restaurada", "Cor dos headers das colunas restaurada ao padrão!")
        except Exception as e:
            QMessageBox.warning(parent_dialog, "Erro", f"Erro ao restaurar cor: {e}")
    
    def update_buttons_color(self, header_color):
        """Atualiza cor de todos os botões baseado na cor do header (tom sobre tom harmonioso)"""
        # Não atualizar botões no modo escuro
        if self.dark_mode:
            return
        
        # Calcular tom harmonioso (mesma cor, mas 20-30% mais escuro para contraste)
        r, g, b = header_color.red(), header_color.green(), header_color.blue()
        
        # Tom mais escuro para botões (reduzir brilho em 25%)
        dark_r = max(0, int(r * 0.75))
        dark_g = max(0, int(g * 0.75))
        dark_b = max(0, int(b * 0.75))
        
        # Cor final do gradiente (um pouco mais clara, mas ainda escura)
        light_r = min(255, int(dark_r * 1.4))
        light_g = min(255, int(dark_g * 1.4))
        light_b = min(255, int(dark_b * 1.4))
        
        # Hover ainda mais escuro (reduzir mais 15%)
        hover_r = max(0, int(dark_r * 0.85))
        hover_g = max(0, int(dark_g * 0.85))
        hover_b = max(0, int(dark_b * 0.85))
        
        hover_light_r = min(255, int(hover_r * 1.3))
        hover_light_g = min(255, int(hover_g * 1.3))
        hover_light_b = min(255, int(hover_b * 1.3))
        
        # Estilo para botões da toolbar
        button_style = f"""
            QPushButton {{
                padding: 8px 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb({dark_r}, {dark_g}, {dark_b}), 
                    stop:1 rgb({light_r}, {light_g}, {light_b}));
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb({hover_r}, {hover_g}, {hover_b}), 
                    stop:1 rgb({hover_light_r}, {hover_light_g}, {hover_light_b}));
            }}
        """
        
        # Estilo para botões inferiores (mais largos)
        bottom_button_style = f"""
            QPushButton {{
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb({dark_r}, {dark_g}, {dark_b}), 
                    stop:1 rgb({light_r}, {light_g}, {light_b}));
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                min-width: 150px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb({hover_r}, {hover_g}, {hover_b}), 
                    stop:1 rgb({hover_light_r}, {hover_light_g}, {hover_light_b}));
            }}
            QPushButton:checked {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgb({min(255, dark_r+20)}, {min(255, dark_g+20)}, {min(255, dark_b+20)}), 
                    stop:1 rgb({min(255, light_r+20)}, {min(255, light_g+20)}, {min(255, light_b+20)}));
            }}
        """
        
        # Aplicar em todos os botões da toolbar
        if hasattr(self, 'toolbar_buttons'):
            for btn in self.toolbar_buttons:
                if btn:
                    btn.setStyleSheet(button_style)
                    btn.update()
                    btn.repaint()
        
        # Aplicar em todos os botões inferiores
        if hasattr(self, 'bottom_buttons'):
            for btn in self.bottom_buttons:
                if btn:
                    btn.setStyleSheet(bottom_button_style)
                    btn.update()
                    btn.repaint()
    
    def show_shortcuts(self):
        """Mostra dialog com atalhos"""
        msg = QMessageBox(self)
        msg.setWindowTitle("⌨️ Atalhos de Teclado")
        msg.setText("""
<b>Atalhos disponíveis:</b><br><br>
<b>Ctrl+N</b> - Novo card em "A Fazer"<br>
<b>Ctrl+F</b> - Focar na busca<br>
<b>Ctrl+T</b> - Toggle Always On Top<br>
<b>Ctrl+Q</b> - Sair<br>
<b>F1</b> - Mostrar este help<br><br>
<b>⚙️ Engrenagem</b> - Menu de opções (Editar, Arquivar, Remover, Abrir)<br>
<b>Arrastar card</b> - Mover entre colunas<br>
<b>Clicar no caminho azul</b> - Abrir pasta contendo o arquivo
        """)
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        
    def toggle_always_on_top(self, checked):
        """Toggle always on top"""
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            self.toggle_btn.setText("📌 Always On Top: ON")
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
            self.toggle_btn.setText("📌 Always On Top: OFF")
        self.show()
        
    def change_transparency(self, value):
        """Muda transparência da janela"""
        self.setWindowOpacity(value / 100.0)
        self.transparency_value_label.setText(f"{value}%")
        
    def filter_cards(self, text):
        """Filtra cards em todas as colunas"""
        if not text:
            # Mostrar todos
            for col in self.columns:
                for card in col.cards:
                    card.setVisible(True)
        else:
            # Filtrar
            for col in self.columns:
                col.filter_cards(text)
                
    def clear_completed(self):
        """Limpa cards concluídos"""
        # Procurar coluna "Concluído"
        completed_col = None
        for col in self.columns:
            if "conclu" in col.titulo.lower():
                completed_col = col
                break
        
        if not completed_col or not completed_col.cards:
            QMessageBox.information(self, "Info", "Nenhum card concluído para limpar!")
            return
            
        reply = QMessageBox.question(self, "Confirmar", 
                                     f"Remover {len(completed_col.cards)} card(s) concluído(s)?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Remover todos os cards
            for card in list(completed_col.cards):
                completed_col.remove_card(card, save=False)
            self.save_data()
            QMessageBox.information(self, "Sucesso", "Cards concluídos removidos!")
    
    def view_archived(self):
        """Abre dialog de cards arquivados"""
        dialog = ArchivedDialog(self)
        dialog.exec()
        
    def show_gantt(self):
        """Abre dialog do Gantt Chart"""
        try:
            dialog = GanttDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Erro ao abrir Gantt",
                f"Erro ao abrir Gantt Chart:\n{str(e)}\n\nDetalhes técnicos:\n{type(e).__name__}"
            )
            print(f"ERRO GANTT: {e}")
            import traceback
            traceback.print_exc()
        
    def show_dashboard(self):
        """Abre dialog do Dashboard de Estatísticas"""
        try:
            dialog = DashboardDialog(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Erro ao abrir Dashboard",
                f"Erro ao abrir Dashboard:\n{str(e)}\n\nDetalhes técnicos:\n{type(e).__name__}"
            )
            print(f"ERRO DASHBOARD: {e}")
            import traceback
            traceback.print_exc()
        
    def create_backup(self):
        """Cria backup dos dados"""
        try:
            # Pasta de backups
            backup_dir = Path("backups")
            backup_dir.mkdir(exist_ok=True)
            
            # Nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"kanban_backup_{timestamp}.json"
            
            # Copiar dados atuais
            if os.path.exists(DATA_FILE):
                import shutil
                shutil.copy2(DATA_FILE, backup_file)
                
                # Também fazer backup do arquivo
                if os.path.exists(ARCHIVE_FILE):
                    archive_backup = backup_dir / f"kanban_arquivo_backup_{timestamp}.json"
                    shutil.copy2(ARCHIVE_FILE, archive_backup)
                
                # Limpar backups antigos (manter apenas últimos 10)
                backups = sorted(backup_dir.glob("kanban_backup_*.json"), reverse=True)
                for old_backup in backups[10:]:
                    old_backup.unlink()
                    # Remover arquivo correspondente também
                    archive_old = backup_dir / old_backup.name.replace("kanban_backup", "kanban_arquivo_backup")
                    if archive_old.exists():
                        archive_old.unlink()
                
                QMessageBox.information(
                    self,
                    "💾 Backup Criado!",
                    f"✅ Backup salvo com sucesso!\n\n"
                    f"📂 Local: {backup_file}\n\n"
                    f"💡 Os últimos 10 backups são mantidos automaticamente."
                )
            else:
                QMessageBox.warning(
                    self,
                    "⚠️ Aviso",
                    "Não há dados para fazer backup ainda."
                )
        except Exception as e:
            QMessageBox.critical(
                self,
                "❌ Erro",
                f"Erro ao criar backup:\n{str(e)}"
            )
        
    def save_data(self):
        """Salva dados em JSON (colunas dinâmicas)"""
        data = {
            "columns": [],
            "settings": {
                "transparency": self.transparency_slider.value(),
                "always_on_top": self.toggle_btn.isChecked(),
                "dark_mode": self.dark_mode
            }
        }
        
        # Salvar cada coluna
        for col in self.columns:
            # Validar dados dos cards (se validação habilitada)
            cards_data = col.get_cards_data()
            if VALIDATION_ENABLED:
                validated_cards = []
                for card_data in cards_data:
                    is_valid, message, sanitized = InputValidator.validate_card_data(card_data)
                    if is_valid:
                        validated_cards.append(sanitized)
                    else:
                        print(f"⚠️ Card inválido ignorado: {message}")
                cards_data = validated_cards
            
            column_data = {
                "id": col.column_id,
                "titulo": col.titulo,
                "cor": col.cor,
                "cards": cards_data
            }
            data["columns"].append(column_data)
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def load_data(self):
        """Carrega dados do JSON (colunas dinâmicas)"""
        if os.path.exists(DATA_FILE):
            try:
                # Validar JSON antes de carregar (se validação habilitada)
                if VALIDATION_ENABLED:
                    is_valid, message, data = InputValidator.validate_json_file(DATA_FILE)
                    if not is_valid:
                        QMessageBox.warning(self, "Erro ao Carregar", 
                                           f"Erro ao carregar dados:\n{message}\n\n"
                                           "O arquivo pode estar corrompido. Um backup será criado.")
                        # Criar backup do arquivo corrompido
                        backup_name = f"{DATA_FILE}.corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        os.rename(DATA_FILE, backup_name)
                        return
                else:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                
                if not VALIDATION_ENABLED:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        data = json.load(f)
                
                # Verificar se é formato novo (com colunas)
                if "columns" in data:
                    # LIMPAR colunas existentes primeiro
                    for col in list(self.columns):
                        self.columns_layout.removeWidget(col)
                        col.deleteLater()
                    self.columns.clear()
                    
                    # Formato novo - carregar TODAS as colunas do JSON (incluindo novas)
                    for column_data in data["columns"]:
                        # CRIAR coluna dinamicamente
                        col = KanbanColumn(
                            column_data["titulo"],
                            column_data["cor"],
                            self,
                            column_data["id"]
                        )
                        self.columns.append(col)
                        self.columns_layout.addWidget(col)
                        
                        # Carregar cards
                        col.load_cards_data(column_data["cards"])
                else:
                    # Formato antigo - migrar
                    old_mapping = {
                        "todo": "todo",
                        "doing": "doing",
                        "done": "done",
                        "approved": "approved",
                        "completed": "completed"
                    }
                    
                    for old_key, col_id in old_mapping.items():
                        if old_key in data:
                            for col in self.columns:
                                if col.column_id == col_id:
                                    col.load_cards_data(data[old_key])
                                    break
                
                # Carregar configurações
                settings = data.get("settings", {})
                if "transparency" in settings:
                    self.transparency_slider.setValue(settings["transparency"])
                if "always_on_top" in settings:
                    self.toggle_btn.setChecked(settings["always_on_top"])
                    self.toggle_always_on_top(settings["always_on_top"])
                if "dark_mode" in settings:
                    self.dark_mode = settings["dark_mode"]
                    self.theme_toggle.setChecked(self.dark_mode)
                    if self.dark_mode:
                        self.theme_toggle.setText("🌙")
                        self.theme_toggle.setToolTip("Modo Escuro ativo - Clique para modo claro")
                    self.apply_theme()
                    # Atualizar colunas e cards
                    for col in self.columns:
                        col.update_column_style()
                        for card in col.cards:
                            card.update_card_style()
                    
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")
                
    def closeEvent(self, event):
        """Ao fechar, salva dados"""
        self.save_data()
        self.tray_icon.hide()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("PinFlow Pro")
    
    window = KanbanWindow()
    
    # Verificar se janela foi criada (pode ser None se licença inválida)
    if window:
        window.show()
        sys.exit(app.exec())
    else:
        # Licença inválida, sair
        sys.exit(1)


if __name__ == "__main__":
    main()
