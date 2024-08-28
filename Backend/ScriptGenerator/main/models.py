from django.utils import timezone
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

class LowLevelDesign(models.Model):
    file = models.FileField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="LLDs", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def generateScript(self):
        result = Script(content="")
        
        # Iterate through each router associated with this LowLevelDesign
        for router in self.routers.all():
            result.content += f"\n------------------------------------------------\nrouter: {router.name}\n------------------------------------------------\n"
            
            # Iterate through each physical interface associated with the router
            for phyInterface in router.physicalInterfaces.all():
                result.content += f"#\ninterface {phyInterface.name}\ndescription To_{phyInterface.radioSite.name}\nundo shutdown\n#\n"
                
                # 2G Logical Interfaces
                for logInterface2G in phyInterface.logicalInterfaces_2g.all():
                    result.content += f"interface {logInterface2G.name}\nvlan-type dot1q {logInterface2G.vlan}\ndescription 2G_{phyInterface.radioSite.name}\nip binding vpn-instance vpn_name(2G)\nip address {logInterface2G.ip_address} 255.255.255.252\n#\n"
                
                # 3G Logical Interfaces
                for logInterface3G in phyInterface.logicalInterfaces_3g.all():
                    result.content += f"interface {logInterface3G.name}\nvlan-type dot1q {logInterface3G.vlan}\ndescription 3G_{phyInterface.radioSite.name}\nip binding vpn-instance vpn_name(3G)\nip address {logInterface3G.ip_address} 255.255.255.252\n#\n"
                
                # Management Logical Interfaces
                for logInterfaceManagement in phyInterface.logicalInterfaces_management.all():
                    result.content += f"interface {logInterfaceManagement.name}\nvlan-type dot1q {logInterfaceManagement.vlan}\ndescription Management_{phyInterface.radioSite.name}\nip binding vpn-instance vpn_name(Management)\nip address {logInterfaceManagement.ip_address} 255.255.255.252\n#\n"
                
                # 4G Logical Interfaces
                for logInterface4G in phyInterface.logicalInterfaces_4g.all():
                    result.content += f"interface {logInterface4G.name}\nvlan-type dot1q {logInterface4G.vlan}\ndescription 4G_{phyInterface.radioSite.name}\nip binding vpn-instance vpn_name(4G)\nip address {logInterface4G.ip_address} 255.255.255.252\n#\n"
        
        # Save the generated script
        result.save()
        return result
    
    def generateScript_Co_Trans(self):
        result = Script(content="")
        
        # Iterate through each router associated with this LowLevelDesign
        for router in self.routers.all():
            result.content += f"\n------------------------------------------------\nrouter: {router.name}\n------------------------------------------------\n"
            result.content += f"display bgp vpnv4 vpn-instance 3G-MP routing-table {router.o_and_m_route.destination} 30\ndisplay bgp vpnv4 vpn-instance 4G_UP&CP routing-table {router.tdd_route.destination} 30\n"
            result.content += f"\nip route-static vpn-instance 3G-MP {router.o_and_m_route.destination} 255.255.255.252 {router.o_and_m_route.next_hop} description TO_3G-MP_{router.o_and_m_route.radio_site}_CO_TRANS"
            result.content += f"\nip route-static vpn-instance 4G_UP&CP {router.tdd_route.destination} 255.255.255.252 {router.tdd_route.next_hop} description TO_4G_UP&CP_{router.tdd_route.radio_site}_CO_TRANS\n"

        result.save()
        return result
    
class RadioSite(models.Model):
    name = models.CharField(max_length=255)
    lld = models.ForeignKey(LowLevelDesign, on_delete=models.CASCADE, related_name='radio_sites')

    def __str__(self):
        return self.name
    

class StaticRoute(models.Model):
    destination = models.GenericIPAddressField()
    next_hop = models.GenericIPAddressField()
    radio_site = models.ForeignKey(RadioSite, on_delete=models.CASCADE, null=True, blank=True, related_name='static_routes')

    def __str__(self):
        return f"destination : {self.destination}, next-hop : {self.next_hop}"

class Router(models.Model):
    name = models.CharField(max_length=255)
    lld = models.ForeignKey('LowLevelDesign', on_delete=models.CASCADE, related_name='routers')
    o_and_m_route = models.OneToOneField(StaticRoute, on_delete=models.CASCADE, null=True, blank=True, related_name='router_o_and_m')
    tdd_route = models.OneToOneField(StaticRoute, on_delete=models.CASCADE, null=True, blank=True, related_name='router_tdd')

    def __str__(self):
        return self.name


class PhysicalInterface(models.Model):
    rate = models.CharField(max_length=100) 
    name = models.CharField(max_length=255)
    router = models.ForeignKey(Router, on_delete=models.CASCADE, related_name='physicalInterfaces')
    radioSite = models.OneToOneField(RadioSite, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class LogicalInterface(models.Model):
    ip_address = models.GenericIPAddressField()
    vlan = models.IntegerField()
    connectedTo = models.GenericIPAddressField(null=True, blank=True)
    name = models.CharField(max_length=255) 
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE)

    class Meta:
        abstract = True  

    def save(self, *args, **kwargs):
        if self.physicalInterface:
            self.name = f"{self.physicalInterface.name}.{self.vlan}"
        super().save(*args, **kwargs)  


class Interface2G(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_2g')

    def __str__(self):
        return f"2G Interface: {self.ip_address}"

class Interface3G(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_3g')

    def __str__(self):
        return f"3G Interface: {self.ip_address}"

class Interface4G(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_4g')

    def __str__(self):
        return f"4G Interface: {self.ip_address}"

class ManagementInterface(LogicalInterface):
    physicalInterface = models.ForeignKey(PhysicalInterface, on_delete=models.CASCADE, related_name='logicalInterfaces_management')

    def __str__(self):
        return f"Management Interface: {self.ip_address}"


class Script(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    lld = models.OneToOneField(LowLevelDesign, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content

