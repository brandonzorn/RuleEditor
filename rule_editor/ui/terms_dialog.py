from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
)


class TermsInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ввод термов")
        self.layout = QVBoxLayout(self)
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Количество термов:"))
        self.count_spin = QSpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setMaximum(1000)
        count_layout.addWidget(self.count_spin)
        btn_set_count = QPushButton("Создать поля")
        btn_set_count.clicked.connect(self._create_term_fields)
        count_layout.addWidget(btn_set_count)
        self.layout.addLayout(count_layout)
        self.terms_container = QVBoxLayout()
        self.layout.addLayout(self.terms_container)
        buttons_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)
        buttons_layout.addStretch()
        buttons_layout.addWidget(btn_ok)
        buttons_layout.addWidget(btn_cancel)

        self.layout.addLayout(buttons_layout)

        self.term_fields = []

    def _create_term_fields(self):
        for widget in self.term_fields:
            widget.deleteLater()
        self.term_fields = []

        count = self.count_spin.value()
        for i in range(count):
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Терм {i + 1}")
            self.terms_container.addWidget(line_edit)
            self.term_fields.append(line_edit)

    def get_terms(self):
        return [field.text() for field in self.term_fields if field.text().strip() != ""]
