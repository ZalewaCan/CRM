from django.core.management.base import BaseCommand
from crm.models import User, Customer, Comment

class Command(BaseCommand):
    help = 'Create demo users and sample data'

    def handle(self, *args, **options):
        # Create demo users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'user_type': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write('Created admin user')

        user_user, created = User.objects.get_or_create(
            username='user',
            defaults={
                'email': 'user@example.com',
                'user_type': 'user'
            }
        )
        if created:
            user_user.set_password('user')
            user_user.save()
            self.stdout.write('Created user user')

        viewer_user, created = User.objects.get_or_create(
            username='viewer',
            defaults={
                'email': 'viewer@example.com',
                'user_type': 'viewer'
            }
        )
        if created:
            viewer_user.set_password('viewer')
            viewer_user.save()
            self.stdout.write('Created viewer user')

        # Create sample customers
        sample_customers = [
            {
                'business_name': 'Tech Solutions Inc.',
                'contact_name': 'John Smith',
                'email': 'john@techsolutions.com',
                'phone': '555-0101',
                'address': '123 Business Ave, Tech City, TC 12345'
            },
            {
                'business_name': 'Green Energy Corp',
                'contact_name': 'Sarah Johnson',
                'email': 'sarah@greenenergy.com',
                'phone': '555-0202',
                'address': '456 Solar Street, Eco Town, ET 67890'
            },
            {
                'business_name': 'Creative Design Studio',
                'contact_name': 'Mike Wilson',
                'email': 'mike@creativedesign.com',
                'phone': '555-0303',
                'address': '789 Art Boulevard, Design District, DD 13579'
            }
        ]

        for customer_data in sample_customers:
            customer, created = Customer.objects.get_or_create(
                business_name=customer_data['business_name'],
                defaults={
                    **customer_data,
                    'created_by': admin_user
                }
            )
            if created:
                self.stdout.write(f'Created customer: {customer.business_name}')
                
                # Add sample comments
                Comment.objects.create(
                    customer=customer,
                    user=admin_user,
                    text=f'Initial contact established with {customer.contact_name}.'
                )
                Comment.objects.create(
                    customer=customer,
                    user=user_user,
                    text='Follow-up call scheduled for next week.'
                )

        self.stdout.write(self.style.SUCCESS('Demo data created successfully!'))