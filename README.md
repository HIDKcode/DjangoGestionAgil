dependencies:
pip install pymysql

## Instalar MYSQL
crear usuario con: GESTIONAGIL
clave: GESTION123

## Consola cuando todo esté listo

cd MaestranzaSA   

.\venv\Scripts\activate 

## Crear base de datos desde powershell en Visual Studio 

mysql -u root -p
DROP DATABASE inventario;
CREATE DATABASE inventario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

## Desde consola nuevamente

cd MaestranzaSA   

.\venv\Scripts\activate 
py inventario_project/manage.py makemigrations
py inventario_project/manage.py migrate
py inventario_project/manage.py createsuperuser

Usuario debe ser:
GESTIONAGIL
GESTION123

py inventario_project/manage.py runserver
