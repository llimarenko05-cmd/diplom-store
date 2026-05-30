from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'

    def ready(self):
        try:
            from django.conf import settings
            from django.contrib.auth.models import User, Group

            admin_group, _ = Group.objects.get_or_create(name='Администратор')
            Group.objects.get_or_create(name='Продавец')
            Group.objects.get_or_create(name='Мерчендайзер')

            username = getattr(settings, 'ADMIN_USERNAME', 'admin')
            password = getattr(settings, 'ADMIN_PASSWORD', 'admin12345')
            email = getattr(settings, 'ADMIN_EMAIL', 'admin@example.com')

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': True,
                    'is_superuser': True,
                }
            )

            if created:
                user.set_password(password)
                user.save()

            if not user.groups.filter(name='Администратор').exists():
                user.groups.add(admin_group)

        except Exception:
            pass
