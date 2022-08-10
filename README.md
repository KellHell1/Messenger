Выполнить по очереди команды в терминале IDE:

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

Ключ дешифровки для сообщений:
Вам необходимо сгенерировать ENCRYPT_KEY, используя описанный ниже процесс.

Откройте терминал в вашей виртуальной среде, где установлен модуль python криптографии.
Импортируйте Fernet.
from cryptography.fernet import Fernet

Сгенерировать ключ.
Fernet.generate_key()

Сохраните ключ в файле настроек.
fernet_key = ваш ключ

Создаем суперюзера:

python manage.py createsuperuser

запуск проекта:

python manage.py runserver

