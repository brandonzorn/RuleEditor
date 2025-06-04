from PySide6.QtWidgets import (
    QMainWindow,
    QTabWidget,
    QFileDialog,
    QMenuBar,
    QMessageBox,
    QInputDialog,
)
from ui.attribute_editor import AttributeEditor
from ui.rule_editor import RuleEditor
from models.project import Project


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор продукционных правил")
        self.resize(800, 600)

        self.project = Project()

        self.tabs = QTabWidget()
        self.attr_tab = AttributeEditor(self.project)
        self.rule_tab = RuleEditor(self.project)

        self.tabs.addTab(self.attr_tab, "Атрибуты")
        self.tabs.addTab(self.rule_tab, "Правила")
        self.setCentralWidget(self.tabs)

        self.create_menu()

    def create_menu(self):
        menubar = QMenuBar(self)

        file_menu = menubar.addMenu("Файл")
        open_action = file_menu.addAction("Открыть проект")
        open_action.triggered.connect(self.open_project)
        save_action = file_menu.addAction("Сохранить проект")
        save_action.triggered.connect(self.save_project)

        project_menu = menubar.addMenu("Проект")
        set_id_action = project_menu.addAction("Задать название проекта")
        set_id_action.triggered.connect(self.set_project_name)

        self.setMenuBar(menubar)

    def set_project_name(self):
        name, ok = QInputDialog.getText(
            self,
            "Идентификатор проекта",
            "Введите название проекта:",
        )
        if ok and name:
            self.project.name = name
            QMessageBox.information(
                self,
                "Проект",
                f"Название проекта задано: {name}",
            )

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить проект",
            "",
            "JSON Files (*.json)",
        )
        if path:
            self.project.save(path)
            QMessageBox.information(
                self,
                "Сохранено",
                "Проект сохранён успешно.",
            )

    def open_project(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Открыть проект",
            "",
            "JSON Files (*.json)",
        )
        if path:
            self.project.load(path)
            self.attr_tab.refresh()
            self.rule_tab.refresh()
            QMessageBox.information(
                self,
                "Загружено",
                "Проект успешно загружен.",
            )
