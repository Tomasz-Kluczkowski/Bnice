# def populate_models(sender, **kwargs):
#     """
#     Create Parents and Children groups. Set appropriate permissions.
#     """
#     print('Creating User groups...')
#     from django.contrib.auth.models import Group, Permission
#     from django.contrib.contenttypes.models import ContentType
#     parents = Group.objects.get_or_create(name='Parents')
#     children = Group.objects.get_or_create(name='Children')
