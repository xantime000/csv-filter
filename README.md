# CSV-фильтрация и агрегация

Скрипт обрабатывает CSV-файл с возможностью фильтрации и агрегации.

## Запуск

```bash
python csvscript.py --file=test_phones.csv --where="price>500"
python csvscript.py --file=test_phones.csv --aggregate="price=avg"
