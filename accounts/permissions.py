"""
A common file to declare access keys and permissions per groups / objects.
"""
# Object types
INSTANCE = 'instance'

# Group keys
PARENTS = 'Parents'

# App keys
ACCOUNTS = 'accounts'
DASHBOARD = 'dashboard'

# Permission verb keys
ADD = 'add'

# Model keys
USER = 'user'
CHILD = 'child'
SMILEY = 'smiley'
OOPSY = 'oopsy'

GROUPS = [PARENTS]

GROUP_PERMISSIONS = {
    PARENTS: {
        ACCOUNTS: {
            ADD: [USER, CHILD]
        },
        DASHBOARD: {
            ADD: [SMILEY, OOPSY]
        }
    }
}
