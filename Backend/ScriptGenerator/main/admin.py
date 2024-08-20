from django.contrib import admin

from .models import Script, LowLevelDesign, RadioSite, Router, PhysicalInterface, Interface2G, Interface3G, Interface4G, ManagementInterface

admin.site.register(Script)
admin.site.register(LowLevelDesign)
admin.site.register(RadioSite)
admin.site.register(Router)
#admin.site.register(Interface2G)
#admin.site.register(Interface3G)
#admin.site.register(Interface4G)
#admin.site.register(ManagementInterface)
#admin.site.register(PhysicalInterface)