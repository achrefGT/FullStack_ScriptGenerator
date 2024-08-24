import pandas as pd # type: ignore
from django.core.validators import validate_ipv4_address, validate_ipv6_address
from django.core.exceptions import ValidationError

def get_column_value(row, column_name, column_index, sheet_name):
    try:
        return row[column_name]
    except KeyError:
        result = row[column_index]
        if not pd.isna(result):  
            return result
    
        raise ValueError(f"Failed to find the column '{column_name}' in sheet '{sheet_name}'.")

def validate_ip_address(ip):
    try:
        validate_ipv4_address(ip)
        return True
    except ValidationError:
        pass
    
    try:
        validate_ipv6_address(ip)
        return True
    except ValidationError:
        pass
    
    return False
    
