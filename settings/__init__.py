from settings.settings_common import *

# Conditionally import additional settings depending on whether we're developing or in production

# Can be set, for example by checking for a given environmental variable, or by detecting the hostname
production = False

if production:
    #from settings.settings_prod import *
    print('production')
else:
    from settings.settings_dev import *