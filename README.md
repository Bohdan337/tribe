# **Tribe**
> ## Requirements
> ### 1. Install [Python](https://www.python.org/downloads/)
> ### 2. Install [git](https://git-scm.com/downloads)

> ## Get template code
> ```
> git clone HEADache297/tribe
> ```

> ## Initialize virtual environment
> ```
> python -m venv venv // Create venv
> source venv/bin/activate // Activation for MacOS or Win with CMD
> .\venv\Scripts\activate.bat // Activation for win with Power Shell
> ```

> ## Install requirements.txt
> ```
> pip install -r requirements.txt
> ```

> ## Create superuser
> ```
> python manage.py createsuperuser --username=<admin> --email=<admin@example.com>
> ```

> ## Run localy (make sure port 8000 is free to use)
> ```
> python manage.py runserver
> ```