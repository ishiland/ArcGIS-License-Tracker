import os

# Update interval in minutes to read from license server
UPDATE_INTERVAL = 5

# license server names and ports. Default port is 27000.
license_servers = [
    {"hostname": "gv-gislicense", "port": "27000"},
    # {"name": "MY-2ND-LICENSE-SERVER", "port": "27000"}
]

# Path to the lmutil.exe.
lm_util = r"C:\Program Files (x86)\ArcGIS\LicenseManager\bin\lmutil.exe"
# lm_util = os.path.abspath(r"Program Files (x86)/ArcGIS/LicenseManager/bin/lmutil.exe")
# lm_util = os.path.join( "C:\\", "Program Files (x86)", "ArcGIS", "LicenseManager", "bin", "lmutil.exe" )
# list of products to check for and track on license server.
products = {

    # See https://desktop.arcgis.com/en/license-manager/latest/feature-names-for-arcgis-option-file.htm

    # ---------------
    # Desktop Products
    # ---------------

    # Core Products
    'ARC/INFO': {'common_name': 'Desktop Advanced', 'category': 'ArcGIS Desktop', 'type': 'core'},
    'EDITOR': {'common_name': 'Desktop Standard', 'category': 'ArcGIS Desktop', 'type': 'core'},
    'VIEWER': {'common_name': 'Desktop Basic', 'category': 'ArcGIS Desktop', 'type': 'core'},

    # Extensions
    'TIN': {'common_name': '3D Analyst Desktop', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'TRACKING': {'common_name': 'Tracking Analyst Desktop', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'INTEROP': {'common_name': 'Data Interoperability Desktop', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'GRID': {'common_name': 'Spatial Analyst Desktop', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'NETWORK': {'common_name': 'Network Analyst Desktop', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'GEOSTATS': {'common_name': 'Geostatistical Analyst', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'PUBLISHER': {'common_name': 'Publisher', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'DATAREVIEWER': {'common_name': 'Data Reviewer', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'SCHEMATICS': {'common_name': 'Schematics Desktop', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'BUSINESS': {'common_name': 'Business Analyst Basic', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'BUSINESSPREM': {'common_name': 'Business Analyst Standard', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'AERONAUTICAL': {'common_name': 'Aviation Charting', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'AERONAUTICALB': {'common_name': 'Aviation Airports', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'NAUTICAL': {'common_name': 'Maritime Charting', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'NAUTICALB': {'common_name': 'Maritime Bathymetry', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'DEFENSE': {'common_name': 'Defense Mapping', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'HIGHWAYS': {'common_name': 'Esri Roads and Highways', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'VIDEO': {'common_name': 'Full Motion Video Desktop', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'FOUNDATION': {'common_name': 'Production Mapping', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'JTX': {'common_name': 'Workflow Manager', 'category': 'ArcGIS Desktop', 'type': 'extension'},
    'LOCREFDESKTOP': {'common_name': 'Location Referencing Desktop', 'category': 'ArcGIS Desktop', 'type': 'extension'},

    # ArcGIS Engine
    'STANDARDENGINE': {'common_name': 'ArcGIS Engine', 'category': 'ArcGIS Engine', 'type': 'core'},
    '3DENGINE': {'common_name': '3D Analyst Engine', 'category': 'ArcGIS Engine', 'type': 'extension'},
    'GDBEDIT': {'common_name': 'Geodatabase Update', 'category': 'ArcGIS Engine', 'type': 'extension'},
    'INTEROPENGINE': {'common_name': 'Data Interoperability Engine', 'category': 'ArcGIS Engine', 'type': 'extension'},
    'SCHEMATICENGINE': {'common_name': 'Schematics Engine', 'category': 'ArcGIS Engine', 'type': 'extension'},
    'SPATIALENGINE': {'common_name': 'Spatial Analyst Engine', 'category': 'ArcGIS Engine', 'type': 'extension'},
    'TRACKINGENGINE': {'common_name': 'Tracking Analyst Engine', 'category': 'ArcGIS Engine', 'type': 'extension'},
    'NETWORKENGINE': {'common_name': 'Network Analyst Engine', 'category': 'ArcGIS Engine', 'type': 'extension'},

    # Esri City Engine
    'CITYENGADV': {'common_name': 'CityEngine Advanced', 'category': 'Esri City Engine', 'type': 'core'},

    # ---------------
    # Pro Products
    # ---------------

    # Core Products
    'DESKTOPADVP': {'common_name': 'ArcGIS Pro Advanced', 'category': 'ArcGIS Pro', 'type': 'core'},
    'DESKTOPSTDP': {'common_name': 'ArcGIS Pro Standard', 'category': 'ArcGIS Pro', 'type': 'core'},
    'DESKTOPBASICP': {'common_name': 'ArcGIS Pro Basic', 'category': 'ArcGIS Pro', 'type': 'core'},

    # Extensions
    '3DANALYSTP': {'common_name': '3D Analyst Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'AIRPORTSP': {'common_name': 'Aviation Airports Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'AVIATIONP': {'common_name': 'Aviation Charting Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'BUSINESSSTDP': {'common_name': 'Business Analyst Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'DATAREVIEWERP': {'common_name': 'Data Reviewer Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'DATAINTEROPP': {'common_name': 'Data Interoperability Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'GEOSTATANALYSTP': {'common_name': 'Geostatistical Analyst Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'DEFENSEP': {'common_name': 'Defense Mapping Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'LOCREFP': {'common_name': 'Location Referencing Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'NETWORKANALYSTP': {'common_name': 'Network Analyst Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'SPATIALANALYSTP': {'common_name': 'Spatial Analyst Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'WORKFLOWMGRP': {'common_name': 'Workflow Manager Pro', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'SMPNAMERICAP': {'common_name': 'StreetMap Premium North America', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'SMPEUROPEP': {'common_name': 'StreetMap Premium Europe', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'SMPMIDEAFRICAP': {'common_name': 'StreetMap Premium Middle East & Africa', 'category': 'ArcGIS Pro',
                       'type': 'extension'},
    'SMPASIAPACIFICP': {'common_name': 'StreetMap Premium Asia Pacific', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'SMPLAMERICAP': {'common_name': 'StreetMap Premium Latin America', 'category': 'ArcGIS Pro', 'type': 'extension'},
    'SMPJAPANP': {'common_name': 'StreetMap Premium Japan', 'category': 'ArcGIS Pro', 'type': 'extension'},

    # -------------
    # Entitlements
    # -------------
    # 'SPATIALANALYSTN': {'common_name': 'Spatial Analyst', 'category': 'Entitlement', 'type': 'extension'},
    # 'NETWORKANALYSTN': {'common_name': 'Network Analyst', 'category': 'Entitlement', 'type': 'extension'},
    # 'PUBLISHERN': {'common_name': 'Publisher', 'category': 'Entitlement', 'type': 'extension'},
}
