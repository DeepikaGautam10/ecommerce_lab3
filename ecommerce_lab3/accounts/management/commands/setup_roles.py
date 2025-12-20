from django.core.management.base import BaseCommand
from accounts.models import Role, Permission, User, UserRole

class Command(BaseCommand):
    help = 'Setup initial roles and permissions'

    def handle(self, *args, **kwargs):
        # Create Permissions
        permissions_data = [
            ('View Products', 'view_products', 'Can view products'),
            ('Manage Products', 'manage_products', 'Can create, update, delete products'),
            ('View Orders', 'view_orders', 'Can view orders'),
            ('Manage Orders', 'manage_orders', 'Can manage orders'),
            ('Manage Users', 'manage_users', 'Can manage users'),
        ]
        
        for name, codename, desc in permissions_data:
            Permission.objects.get_or_create(
                codename=codename,
                defaults={'name': name, 'description': desc}
            )
            self.stdout.write(f"✓ Permission: {name}")
        
        # Create Roles
        viewer_role, _ = Role.objects.get_or_create(
            name='viewer',
            defaults={'description': 'Can browse products only'}
        )
        self.stdout.write("✓ Viewer role created")
        
        accountant_role, _ = Role.objects.get_or_create(
            name='accountant',
            defaults={'description': 'Can view orders and generate reports'}
        )
        self.stdout.write("✓ Accountant role created")
        
        admin_role, _ = Role.objects.get_or_create(
            name='admin',
            defaults={'description': 'Full access to everything'}
        )
        self.stdout.write("✓ Admin role created")
        
        # Assign admin role to superusers
        superusers = User.objects.filter(is_superuser=True)
        for user in superusers:
            UserRole.objects.get_or_create(
                user=user,
                role=admin_role
            )
            self.stdout.write(f"✓ Admin role assigned to {user.username}")
        
        self.stdout.write(self.style.SUCCESS('\n✓ Roles and permissions setup complete!'))