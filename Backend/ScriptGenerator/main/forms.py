from django import forms
from django.forms import FileInput, inlineformset_factory
from .models import Script, LowLevelDesign, Router, PhysicalInterface, Interface2G, Interface3G, Interface4G, ManagementInterface, RadioSite  # Import RadioSite
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, ButtonHolder, Submit



class LowLevelDesignForm(forms.ModelForm):
    class Meta:
        model = LowLevelDesign
        fields = ['file']
        widgets = {
            'file': FileInput(attrs={
                'class': "custom-file-input",
            })
        }

    def __init__(self, *args, **kwargs):
        super(LowLevelDesignForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Fieldset(
                'Low-Level Design Details',
                'file'
            )
        )

class RadioSiteForm(forms.ModelForm):
    class Meta:
        model = RadioSite  
        fields = ['name', 'lld']

    def __init__(self, *args, **kwargs):
        super(RadioSiteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Radio Site Details',
                'name',
                'lld',
            )
        )

class RouterForm(forms.ModelForm):
    class Meta:
        model = Router
        fields = ['name', 'lld']

    def __init__(self, *args, **kwargs):
        super(RouterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Router Details',
                'name',
                'lld',
            )
        )

class PhysicalInterfaceForm(forms.ModelForm):
    radioSite = forms.ModelChoiceField(
        queryset=RadioSite.objects.all(),
        required=True,  
        label='Radio Site' 
    )
    class Meta:
        model = PhysicalInterface
        fields = ['rate', 'name', 'router', 'radioSite']

    def __init__(self, *args, **kwargs):
        super(PhysicalInterfaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Physical Interface Details',
                'rate',
                'name',
                'router',
                'radioSite'
            )
        )

# Inline formsets without delete checkbox
PhysicalInterfaceFormSet = inlineformset_factory(
    Router, PhysicalInterface, form=PhysicalInterfaceForm, extra=1, can_delete=False
)

class Interface2GForm(forms.ModelForm):
    class Meta:
        model = Interface2G
        fields = ['ip_address', 'vlan', 'connectedTo', 'name', 'physicalInterface']

    def __init__(self, *args, **kwargs):
        super(Interface2GForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '2G Interface Details',
                'ip_address',
                'vlan',
                'connectedTo',
                'name',
                'physicalInterface',
            )
        )

# Inline formsets without delete checkbox
Interface2GFormSet = inlineformset_factory(
    PhysicalInterface, Interface2G, form=Interface2GForm, extra=1, can_delete=False
)

class Interface3GForm(forms.ModelForm):
    class Meta:
        model = Interface3G
        fields = ['ip_address', 'vlan', 'connectedTo', 'name', 'physicalInterface']

    def __init__(self, *args, **kwargs):
        super(Interface3GForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '3G Interface Details',
                'ip_address',
                'vlan',
                'connectedTo',
                'name',
                'physicalInterface',
            )
        )

# Inline formsets without delete checkbox
Interface3GFormSet = inlineformset_factory(
    PhysicalInterface, Interface3G, form=Interface3GForm, extra=1, can_delete=False
)

class Interface4GForm(forms.ModelForm):
    class Meta:
        model = Interface4G
        fields = ['ip_address', 'vlan', 'connectedTo', 'name', 'physicalInterface']

    def __init__(self, *args, **kwargs):
        super(Interface4GForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                '4G Interface Details',
                'ip_address',
                'vlan',
                'connectedTo',
                'name',
                'physicalInterface',
            )
        )

# Inline formsets without delete checkbox
Interface4GFormSet = inlineformset_factory(
    PhysicalInterface, Interface4G, form=Interface4GForm, extra=1, can_delete=False
)

class ManagementInterfaceForm(forms.ModelForm):
    class Meta:
        model = ManagementInterface
        fields = ['ip_address', 'vlan', 'connectedTo', 'name', 'physicalInterface']

    def __init__(self, *args, **kwargs):
        super(ManagementInterfaceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Management Interface Details',
                'ip_address',
                'vlan',
                'connectedTo',
                'name',
                'physicalInterface',
            )
        )

# Inline formsets without delete checkbox
ManagementInterfaceFormSet = inlineformset_factory(
    PhysicalInterface, ManagementInterface, form=ManagementInterfaceForm, extra=1, can_delete=False
)

class ScriptForm(forms.ModelForm):
    class Meta:
        model = Script
        fields = ['content']
