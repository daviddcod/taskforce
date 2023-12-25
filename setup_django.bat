@echo off
cd /d "C:\Users\atlas\DjangoProjects\taskforce"
call "C:\Users\atlas\DjangoProjects\taskforce\env\Scripts\activate.bat"
pip install django
pip install psycopg2
django-admin startproject taskforce .
django-admin startapp auth_app
django-admin startapp task_manager
django-admin startapp project_manager
django-admin startapp health_tracker
django-admin startapp mind_wellness
django-admin startapp time_tracker
django-admin startapp seo_tools
django-admin startapp communication
django-admin startapp data_analysis
django-admin startapp shop_manager
django-admin startapp payment_processor
django-admin startapp custom_software_dev
django-admin startapp lifestyle_consultancy
django-admin startapp user_groups_management
django-admin startapp project_export_import
django-admin startapp project_title_level_system
django-admin startapp priority_table_management
