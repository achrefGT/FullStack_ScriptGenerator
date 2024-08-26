from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Router, PhysicalInterface, Interface2G, Interface3G, Interface4G, ManagementInterface, LowLevelDesign, LowLevelDesign_Co_trans,RadioSite, Script
from .forms import LowLevelDesignForm
from .constants import *
from .serializers import LowLevelDesignSerializer, ScriptSerializer, UserSerializer
from .utils import get_column_value,validate_ip_address

from rest_framework import generics, status # type: ignore
from rest_framework.permissions import IsAuthenticated, AllowAny # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore

import pandas as pd # type: ignore

def index(request):
    return redirect('http://localhost:5173/')

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ScripListCreate(generics.ListCreateAPIView):
    serializer_class = ScriptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the currently authenticated user
        user = self.request.user
        
        # Return scripts that belong to the authenticated user
        return Script.objects.filter(lld__user=user)




@api_view(['POST'])
def download_script_api(request):
    try:
        script_content = request.POST.get('script_content', '')

        response = HttpResponse(script_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="script.txt"'

        return response

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def upload_lld_api(request):
    try:
        # Initialize the form with the POST data and files
        form = LowLevelDesignForm(request.POST, request.FILES)
        
        if form.is_valid():
        
            if 'file' not in request.FILES:
                return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve the uploaded file
            excel_file = request.FILES['file']
            
            # Load the Excel file
            xls = pd.ExcelFile(excel_file)
            
            # Read sheets by name or fallback to sheet index if needed
            try:
                ip_plan_df = pd.read_excel(xls, 'IP PLAN')
            except ValueError:
                ip_plan_df = pd.read_excel(xls, sheet_name=0)  # Fallback to the first sheet

            try:
                interface_2g_df = pd.read_excel(xls, '2G')
            except ValueError:
                interface_2g_df = pd.read_excel(xls, sheet_name=1)  # Fallback to the second sheet

            try:
                interface_3g_df = pd.read_excel(xls, '3G')
            except ValueError:
                interface_3g_df = pd.read_excel(xls, sheet_name=2)  # Fallback to the third sheet

            try:
                interface_4g_df = pd.read_excel(xls, '4G')
            except ValueError:
                interface_4g_df = pd.read_excel(xls, sheet_name=3)  # Fallback to the fourth sheet

            # Create a LowLevelDesign instance
            lld = LowLevelDesign.objects.create(file=excel_file, user=request.user)  

            # Process IP Plan sheet
            for _, row in ip_plan_df.iloc[1:].iterrows():
                router_name = get_column_value(row, 'Router', IP_PLAN_COLUMNS['Router'], 'IP PLAN')
                radio_site_name = get_column_value(row, 'radio_site_name', IP_PLAN_COLUMNS['radio_site_name'], 'IP PLAN')
                
                if router_name and radio_site_name:
                    router, created = Router.objects.get_or_create(name=router_name, lld=lld)
                    radio_site, created = RadioSite.objects.get_or_create(name=radio_site_name, lld=lld)

                    PhysicalInterface.objects.create(
                        name=get_column_value(row, 'Interface', IP_PLAN_COLUMNS['Interface'], 'IP PLAN'), 
                        router=router, 
                        radioSite=radio_site
                    )

            # Process 2G interfaces
            for _, row in interface_2g_df.iterrows():
                physical_iface_name = get_column_value(row, 'NE40 Interface', INTERFACE_2G_COLUMNS['NE40 Interface'], '2G')
                router_name = get_column_value(row, 'NE40', INTERFACE_2G_COLUMNS['NE40'], '2G')
                router = Router.objects.get(name=router_name, lld=lld)
                phy_iface = PhysicalInterface.objects.get(name=physical_iface_name, router=router)

                Interface2G.objects.create(
                    ip_address=get_column_value(row, 'NE40 GW', INTERFACE_2G_COLUMNS['NE40 GW'], '2G'), 
                    vlan=get_column_value(row, 'VLAN', INTERFACE_2G_COLUMNS['VLAN'], '2G'), 
                    connectedTo=get_column_value(row, 'Radio_Site address', INTERFACE_2G_COLUMNS['Radio_Site address'], '2G'), 
                    physicalInterface=phy_iface,
                )

            # Process 3G interfaces
            for _, row in interface_3g_df.iterrows():
                physical_iface_name = get_column_value(row, 'NE40 Interface', INTERFACE_3G_COLUMNS['NE40 Interface'], '3G')
                router_name = get_column_value(row, 'NE40', INTERFACE_3G_COLUMNS['NE40'], '3G')
                router = Router.objects.get(name=router_name, lld=lld)
                phy_iface = PhysicalInterface.objects.get(name=physical_iface_name, router=router)

                Interface3G.objects.create(
                    ip_address=get_column_value(row, '3G UP&CP GW IP', INTERFACE_3G_COLUMNS['3G UP&CP GW IP'], '3G'), 
                    vlan=get_column_value(row, 'UP&CP VLAN', INTERFACE_3G_COLUMNS['UP&CP VLAN'], '3G'), 
                    connectedTo=get_column_value(row, '3G UP&CP IP', INTERFACE_3G_COLUMNS['3G UP&CP IP'], '3G'), 
                    physicalInterface=phy_iface,
                )

                ManagementInterface.objects.create(
                    ip_address=get_column_value(row, 'Management IP', INTERFACE_3G_COLUMNS['Management IP'], '3G'), 
                    vlan=get_column_value(row, 'Management VLAN', INTERFACE_3G_COLUMNS['Management VLAN'], '3G'), 
                    connectedTo=get_column_value(row, 'OMCH IP', INTERFACE_3G_COLUMNS['OMCH IP'], '3G'), 
                    physicalInterface=phy_iface,
                )

            # Process 4G interfaces
            for _, row in interface_4g_df.iterrows():
                physical_iface_name = get_column_value(row, 'NE40 Interface', INTERFACE_4G_COLUMNS['NE40 Interface'], '4G')
                router_name = get_column_value(row, 'NE40', INTERFACE_4G_COLUMNS['NE40'], '4G')
                router = Router.objects.get(name=router_name, lld=lld)
                phy_iface = PhysicalInterface.objects.get(name=physical_iface_name, router=router)

                Interface4G.objects.create(
                    ip_address=get_column_value(row, '4G UP&CP GW IP', INTERFACE_4G_COLUMNS['4G UP&CP GW IP'], '4G'), 
                    vlan=get_column_value(row, 'VLAN', INTERFACE_4G_COLUMNS['VLAN'], '4G'), 
                    connectedTo=get_column_value(row, '4G UP&CP IP', INTERFACE_4G_COLUMNS['4G UP&CP IP'], '4G'), 
                    physicalInterface=phy_iface,
                )
            
            # Generate the script
            script = lld.generateScript() 

            # Save the script with the user attribute
            script.lld = lld
            script.save()

            lld_serializer = LowLevelDesignSerializer(lld)
            return Response({"script_content": script.content, "lld": lld_serializer.data, "id":script.id}, status=status.HTTP_200_OK) 

    except Exception as e:
        print("Error occurred:", str(e))  # Debug: Print the error to the console
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Invalid form submission"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload_lld_Co_Trans_api(request):
    try:
        # Initialize the form with the POST data and files
        form = LowLevelDesignForm(request.POST, request.FILES)

        if form.is_valid():
            excel_file = request.FILES['file']
            lld_data_df = pd.read_excel(excel_file, sheet_name=0)

            # Create LowLevelDesign instance with user and created_at attribute
            lld = LowLevelDesign_Co_trans.objects.create(file=excel_file, user=request.user)

            o_and_m_next_ip = request.POST.get('o_and_m_next')
            tdd_next_ip = request.POST.get('TDD_next')

            if not validate_ip_address(o_and_m_next_ip) and not validate_ip_address(tdd_next_ip):
                return Response({"error": "Invalid IP addresses."}, status=status.HTTP_400_BAD_REQUEST)

            if not validate_ip_address(o_and_m_next_ip):
                return Response({"error": "Invalid IP address for O&M Next."}, status=status.HTTP_400_BAD_REQUEST)

            if not validate_ip_address(tdd_next_ip):
                return Response({"error": "Invalid IP address for TDD Next."}, status=status.HTTP_400_BAD_REQUEST)

            lld.o_and_m_next = o_and_m_next_ip
            lld.TDD_next = tdd_next_ip

            # Process the first row of the DataFrame (assuming it contains the data)
            for _, row in lld_data_df[1:].iterrows():
                router_name = get_column_value(row, 'NE40/NE8000', LLD_CO_TRANS_COLUMNS['NE40/NE8000'], 'Sheet1')
                site_name = get_column_value(row, 'site  ', LLD_CO_TRANS_COLUMNS['site  '], 'Sheet1')
                o_and_m_ip = get_column_value(row, 'Config O&M', LLD_CO_TRANS_COLUMNS['Config O&M'], 'Sheet1')
                tdd_ip = get_column_value(row, 'Config TDD', LLD_CO_TRANS_COLUMNS['Config TDD'], 'Sheet1')

                if router_name and site_name:
                    router, created = Router.objects.get_or_create(name=router_name, lld=lld)
                    radio_site, created = RadioSite.objects.get_or_create(name=site_name, lld=lld)
                    lld.o_and_m = o_and_m_ip
                    lld.TDD = tdd_ip
                    lld.save()
                    
            # Generate the script
            script = lld.generateScript(site_name)
            
            # Save the script with the user attribute
            script.lld = lld
            script.save()

            lld_serializer = LowLevelDesignSerializer(lld)
            return Response({"script_content": script.content, "lld": lld_serializer.data, "id":script.id}, status=status.HTTP_200_OK)

    except Exception as e:
        print("Error occurred:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"error": "Invalid form submission"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def edit_script(request, pk):
    try:
        script = Script.objects.get(pk=pk)
    except Script.DoesNotExist:
        return Response({'error': 'Script not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ScriptSerializer(script, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
