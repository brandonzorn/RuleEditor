from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QLineEdit,
    QComboBox,
    QHBoxLayout, QDialog,
)

from models.attribute import Attribute, AttributeTypeEnum
from ui.terms_dialog import TermsInputDialog


class AttributeEditor(QWidget):
    def __init__(self, project, /):
        super().__init__()
        self.project = project

        self.layout = QVBoxLayout(self)

        self.attr_input_layout = QHBoxLayout()

        self.attr_name_input = QLineEdit()
        self.attr_name_input.setPlaceholderText("Название атрибута")

        self.attr_type_list = QComboBox()
        self.attr_type_list.addItems(
            [at.value.NAME for at in AttributeTypeEnum],
        )

        self.add_button = QPushButton("Добавить атрибут")
        self.add_button.clicked.connect(self.add_attribute)

        self.attr_input_layout.addWidget(self.attr_name_input)
        self.attr_input_layout.addWidget(self.attr_type_list)
        self.attr_input_layout.addWidget(self.add_button)

        self.layout.addLayout(self.attr_input_layout)

        self.attr_list = QListWidget()
        self.layout.addWidget(self.attr_list)

        for attr in self.project.attributes:
            self.attr_list.addItem(attr.get_name())

    def add_attribute(self):
        attr_id = self.attr_list.count()
        name = self.attr_name_input.text().strip()
        attr_type = AttributeTypeEnum.from_id(
            self.attr_type_list.currentIndex(),
        )
        non_def_values = None
        if attr_type == AttributeTypeEnum.LINGUISTIC_VAR:
            def open_terms_dialog():
                dialog = TermsInputDialog()
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    terms = dialog.get_terms()
                    return terms
                return []
            non_def_values = open_terms_dialog()
        if name:
            attribute = Attribute(attr_id, name, attr_type, non_def_values)
            self.project.attributes.append(attribute)
            self.attr_list.addItem(attribute.get_name())
            self.attr_name_input.clear()

    def refresh(self):
        self.attr_list.clear()
        self.attr_name_input.clear()
        self.attr_type_list.setCurrentIndex(0)

        for attribute in self.project.attributes:
            self.attr_list.addItem(attribute.get_name())
