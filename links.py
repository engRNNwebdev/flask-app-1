import os

def links_prod():
    links = {}
    links['Long Island (LI)'] = os.getenv('WEB_LI')
    links['New Jersey (NJ)'] = os.getenv('WEB_NJ')
    links['Lower Hudson Valley (LHV)'] = os.getenv('WEB_HV')
    return links

def links_it():
    links = {}
    links['Password Change'] = os.getenv('WEB_PASS_CHANGE')
    links['Service Desk'] = os.getenv('WEB_SERVICE_DESK')
    links['Outlook Web Mail'] = os.getenv('WEB_MAIL')
    links['Reset Password'] = os.getenv('WEB_RESET_PASS')
    links['Device Manager'] = os.getenv('WEB_DEVICE_MAN')
    return links

def links_ftp():
    links = {}
    links['FTP1'] = os.getenv('WEB_FTP_1')
    links['Crispin FTP'] = os.getenv('WEB_FTP_CRISPIN')
    links['Clearleap'] = os.getenv('WEB_FTP_CLEARLEAP')
    links['Extreme Reach'] = os.getenv('WEB_EXTREME_REACH')
    links['Pitch Blue'] = os.getenv('WEB_PITCH_BLUE')
    return links

def  links_broadcast():
    links = {}
    links['Volicon'] = os.getenv('WEB_VOLICON')
    links['EAS'] = os.getenv('WEB_EAS')
    return links

def links():
    links = {}
    links['Long Island (LI)'] = os.getenv('WEB_LI')
    links['New Jersey (NJ)'] = os.getenv('WEB_NJ')
    links['Lower Hudson Valley (LHV)'] = os.getenv('WEB_HV')
    links['Password Change'] = os.getenv('WEB_PASS_CHANGE')
    links['Service Desk'] = os.getenv('WEB_SERVICE_DESK')
    links['Outlook Web Mail'] = os.getenv('WEB_MAIL')
    links['Reset Password'] = os.getenv('WEB_RESET_PASS')
    links['FTP1'] = os.getenv('WEB_FTP_1')
    links['Crispin FTP'] = os.getenv('WEB_FTP_CRISPIN')
    links['Clearleap'] = os.getenv('WEB_FTP_CLEARLEAP')
    links['Extreme Reach'] = os.getenv('WEB_EXTREME_REACH')
    links['Pitch Blue'] = os.getenv('WEB_PITCH_BLUE')
    links['Volicon'] = os.getenv('WEB_VOLICON')
    links['EAS'] = os.getenv('WEB_EAS')
    links['Device Manager'] = os.getenv('WEB_DEVICE_MAN')
    return links
