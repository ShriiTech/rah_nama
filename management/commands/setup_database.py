import os
import time
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Setup database with migrations and initial data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create a superuser if it does not exist',
        )
        parser.add_argument(
            '--load-fixtures',
            action='store_true',
            help='Load initial fixtures',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting database setup...')
        )

        # Wait for database to be ready
        self._wait_for_db()
        
        # Create migrations
        self._create_migrations()
        
        # Apply migrations
        self._apply_migrations()
        
        # Create superuser if requested
        if options['create_superuser']:
            self._create_superuser()
            
        # Load fixtures if requested
        if options['load_fixtures']:
            self._load_fixtures()
            
        # Collect static files
        self._collect_static()
        
        self.stdout.write(
            self.style.SUCCESS('✅ Database setup completed successfully!')
        )

    def _wait_for_db(self):
        """Wait for database to be available"""
        self.stdout.write('⏳ Waiting for database...')
        
        db_up = False
        max_retries = 30
        retry_count = 0
        
        while not db_up and retry_count < max_retries:
            try:
                connection.ensure_connection()
                db_up = True
                self.stdout.write(
                    self.style.SUCCESS('✅ Database is available!')
                )
            except Exception as e:
                retry_count += 1
                self.stdout.write(
                    f'❗ Database unavailable, waiting 1 second... ({retry_count}/{max_retries})'
                )
                time.sleep(1)
                
        if not db_up:
            raise CommandError(
                f'❌ Database unavailable after {max_retries} attempts'
            )

    def _create_migrations(self):
        """Create migrations for all apps"""
        self.stdout.write('📦 Creating migrations...')
        
        try:
            # Create general migrations
            call_command('makemigrations', verbosity=1)
            
            # Create specific app migrations
            apps_to_migrate = ['account']  # Add your app names here
            
            for app in apps_to_migrate:
                try:
                    call_command('makemigrations', app, verbosity=1)
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Created migrations for {app}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️ Could not create migrations for {app}: {e}')
                    )
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Migration creation warning: {e}')
            )

    def _apply_migrations(self):
        """Apply database migrations"""
        self.stdout.write('⚙️ Applying migrations...')
        
        try:
            call_command('migrate', verbosity=1)
            self.stdout.write(
                self.style.SUCCESS('✅ Migrations applied successfully!')
            )
        except Exception as e:
            raise CommandError(f'❌ Migration failed: {e}')

    def _create_superuser(self):
        """Create superuser if it doesn't exist"""
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        if not User.objects.filter(username=username).exists():
            self.stdout.write('👤 Creating superuser...')
            try:
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Superuser "{username}" created successfully!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to create superuser: {e}')
                )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Superuser "{username}" already exists')
            )

    def _load_fixtures(self):
        """Load initial fixtures"""
        fixtures = os.getenv('DJANGO_FIXTURES', '').split()
        
        for fixture in fixtures:
            if fixture.strip():
                try:
                    call_command('loaddata', fixture.strip())
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ Loaded fixture: {fixture}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️ Could not load fixture {fixture}: {e}')
                    )

    def _collect_static(self):
        """Collect static files if needed"""
        if os.getenv('DJANGO_COLLECT_STATIC', 'false').lower() == 'true':
            self.stdout.write('📦 Collecting static files...')
            try:
                call_command('collectstatic', '--noinput', verbosity=1)
                self.stdout.write(
                    self.style.SUCCESS('✅ Static files collected successfully!')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Static files collection warning: {e}')
                )