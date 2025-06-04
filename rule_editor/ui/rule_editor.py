from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QSizePolicy,
)

from models.rule import Rule


class ConditionLayout(QHBoxLayout):
    def __init__(self, project):
        super().__init__()
        self.project = project

        self.label = QLabel("ЕСЛИ")
        self.addWidget(self.label)

        self.attr_combo = QComboBox()
        self.attr_combo.addItems(
            [a.get_name() for a in self.project.attributes],
        )
        self.attr_combo.currentIndexChanged.connect(self._on_attr_changed)
        self.addWidget(self.attr_combo)

        self.addWidget(QLabel("="))

        self.input_widget = QLineEdit()
        self.input_widget.setPlaceholderText("Значение")
        self.input_widget.textChanged.connect(self._validate_input)
        self.addWidget(self.input_widget)

    def _on_attr_changed(self):
        self.input_widget.deleteLater()

        attr_name = self.attr_combo.currentText()
        attr = next(
            (a for a in self.project.attributes if a.get_name() == attr_name),
            None,
        )

        values = attr.get_valid_values() if attr else []
        if values:
            combo = QComboBox()
            combo.setSizePolicy(
                QSizePolicy(
                    QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Fixed,
                ),
            )
            combo.addItems(values)
            combo.currentTextChanged.connect(self._validate_input)
            self.input_widget = combo
        else:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText("Значение")
            line_edit.textChanged.connect(self._validate_input)
            self.input_widget = line_edit
        self.addWidget(self.input_widget)

    def _validate_input(self):
        attr_name = self.attr_combo.currentText()
        attr = next(
            (a for a in self.project.attributes if a.get_name() == attr_name),
            None,
        )
        value = (
            self.input_widget.currentText()
            if isinstance(self.input_widget, QComboBox)
            else self.input_widget.text()
        )
        if attr and not attr.validate(value):
            self.input_widget.setStyleSheet("border: 1px solid red")
        else:
            self.input_widget.setStyleSheet("")

    def set_state(self, state: int):
        if state == 0:
            self.label.setText("ЕСЛИ")
        elif state == 1:
            self.label.setText("И")
        elif state == 2:
            self.label.setText("ТО")

    def to_rule(self):
        attr_id = self.attr_combo.currentIndex()
        value = (
            self.input_widget.currentText()
            if isinstance(self.input_widget, QComboBox)
            else self.input_widget.text()
        )
        return Rule(attr_id, value)

    def from_rule(self, rule: Rule | None):
        if rule is None:
            return
        attr_id = int(rule.attr_id)
        value = rule.value
        self.attr_combo.setCurrentIndex(attr_id)
        if isinstance(self.input_widget, QComboBox):
            i = self.input_widget.findText(value)
            if i != -1:
                self.input_widget.setCurrentIndex(i)
        else:
            self.input_widget.setText(value)

class RuleEditor(QWidget):
    def __init__(self, project, /):
        super().__init__()
        self.setWindowTitle("Редактор правил")
        self.project = project
        self.conditions: list[ConditionLayout] = []

        self.layout = QVBoxLayout(self)

        self.conditions_layout = QVBoxLayout()
        self.layout.addLayout(self.conditions_layout)

        self.buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("+ Добавить условие")
        self.add_button.clicked.connect(self.add_condition_row)
        self.buttons_layout.addWidget(self.add_button)

        self.apply_button = QPushButton("Сохранить правила")
        self.apply_button.clicked.connect(self.apply_conditions)
        self.buttons_layout.addWidget(self.apply_button)

        self.layout.addLayout(self.buttons_layout)

    def add_condition_row(self, rule=None):
        row_layout = ConditionLayout(self.project)
        if rule:
            row_layout.from_rule(rule)
        if self.conditions_layout.count() > 1:
            self.conditions_layout.children()[-1].set_state(1)
            row_layout.set_state(2)
        if self.conditions_layout.count() == 1:
            row_layout.set_state(2)
        self.conditions_layout.addLayout(row_layout)

    def apply_conditions(self):
        self.project.rules.clear()
        for ch in self.conditions_layout.children():
            self.project.rules.append(ch.to_rule())

    def refresh(self):
        for ch in reversed(self.conditions_layout.children()):
            ch.deleteLater()
        for rule in self.project.rules:
            self.add_condition_row(rule)
