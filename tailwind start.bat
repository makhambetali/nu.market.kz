@ECHO OFF
cd /d %~dp0 & "venv\Scripts\activate" & python manage.py tailwind start
cmd /k