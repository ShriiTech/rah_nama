INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'apps.account.apps.AccountConfig',
    'apps.catalog.apps.CatalogConfig',
    
    # Dependency
    'rest_framework'

]      

