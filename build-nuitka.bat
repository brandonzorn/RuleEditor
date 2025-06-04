nuitka ^
  --onefile ^
  --windows-console-mode=disable ^
  --enable-plugin=pyside6 ^
  --follow-imports ^
  --product-version="1.0.0.0" ^
  --file-version="1.0.0.0" ^
  --company-name="brandonzorn" ^
  --product-name="RuleEditor" ^
  -o "Rule-Editor" ^
  --output-dir=build_nuitka/ ^
  rule_editor/main.py
