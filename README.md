# backend_AQ

# Инструкции по установке библиотек

Для установки всех необходимых библиотек проекта выполните следующие шаги:

1. **Убедитесь, что у вас установлен Python и pip**:
   - Python 3.8 или выше
   - pip (обычно идет с Python)

2. **Создайте виртуальное окружение** (рекомендуется):
   ```bash
   python -m venv venv
   ```

3. **Активируйте виртуальное окружение**:
   - Для Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Для macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Установите все библиотеки из requirements.txt**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Проверьте, что все библиотеки установлены**:
   ```bash
   pip list
   ```

### Список основных библиотек:
- Django
- Django REST framework
- django-cors-headers
- django-filter
- drf-yasg
- mysqlclient
- Pillow
- python-dotenv

### Прямые команды для установки библиотек:
```bash
pip install Django
pip install djangorestframework
pip install django-cors-headers
pip install django-filter
pip install drf-yasg
pip install mysqlclient
pip install Pillow
pip install python-dotenv
pip install pymysql
pip install django-extensions werkzeug


```
### Самоподисанный сертификат 
```bash
pip install pyOpenSSL
```


Если у вас возникнут проблемы с установкой, убедитесь, что у вас установлены все необходимые системные зависимости для работы с MySQL и другими библиотеками.

mkdir backend_AQ/static

python manage.py collectstatic --noinput