INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom apps
    'account.apps.AccountConfig',
    'catalog.apps.CatalogConfig',
    
    # Dependency
    'rest_framework',
    'rest_framework_simplejwt',
]      

