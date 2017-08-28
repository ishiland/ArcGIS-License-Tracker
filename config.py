import os

# Root project folder
basedir = os.path.abspath(os.path.dirname(__file__))

# Flask config
DEBUG = True
SECRET_KEY = "SO_SECURE"
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASK_DEBUG_DISABLE_STRICT = True
# BOOTSTRAP_SERVE_LOCAL = True
# SEND_FILE_MAX_AGE_DEFAULT = 0
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://localhost\\SQLEXPRESS/IIT_GIS_FLEXNET?driver=SQL+Server+Native+Client+11.0"

# license server names and ports
license_servers = [
    {"name": "arcviewkey", "port": "27000"},
    {"name": "stgarcgis100", "port": "27000"}  # failover
]

# Path to the lmutil.exe.
lm_util = os.path.join(basedir, "lmutil.exe")

# list of products to check for and track on license server.
products = [

    # See http://desktop.arcgis.com/en/license-manager/latest/feature-names-for-arcgis-options-file.htm
    # For script optimization, comment out products that are not applicable to your organization.

    # ---------------
    # Desktop Products
    # ---------------

    # Core Products
    {'internal-name': 'ARC/INFO', 'common-name': 'Desktop-Advanced', 'category': 'ArcGIS-Desktop', 'type': 'core'},
    {'internal-name': 'Editor', 'common-name': 'Desktop-Standard', 'category': 'ArcGIS-Desktop', 'type': 'core'},
    {'internal-name': 'Viewer', 'common-name': 'Desktop-Basic', 'category': 'ArcGIS-Desktop', 'type': 'core'},

    # Extensions
    {'internal-name': 'TIN', 'common-name': '3D-Analyst-Desktop', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Tracking', 'common-name': 'Tracking-Analyst-Desktop', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Interop', 'common-name': 'Data-Interoperability-Desktop', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Grid', 'common-name': 'Spatial-Analyst-Desktop', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Network', 'common-name': 'Network-Analyst-Desktop', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'GeoStats', 'common-name': 'Geostatistical-Analyst', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Publisher', 'common-name': 'Publisher', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'DataReViewer', 'common-name': 'Data-Reviewer', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Schematics', 'common-name': 'Schematics-Desktop', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Business', 'common-name': 'Business-Analyst-Basic', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'BusinessPrem', 'common-name': 'Business-Analyst-Standard', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Aeronautical', 'common-name': 'Aviation-Charting', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'AeronauticalB', 'common-name': 'Aviation Airports', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Nautical', 'common-name': 'Maritime-Charting', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'NauticalB', 'common-name': 'Maritime-Bathymetry', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Defense', 'common-name': 'Defense-Mapping', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Highways', 'common-name': 'Esri-Roads-and-Highways', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Video', 'common-name': 'Full-Motion-Video-Desktop', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'Foundation', 'common-name': 'Production-Mapping', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'JTX', 'common-name': 'Workflow-Manager', 'category': 'ArcGIS-Desktop', 'type': 'extension'},
    {'internal-name': 'LocRefDesktop', 'common-name': 'Location-Referencing-Desktop', 'category': 'ArcGIS-Desktop', 'type': 'extension'},

    # ArcGIS Engine
    {'internal-name': 'StandardEngine', 'common-name': 'ArcGIS-Engine', 'category': 'ArcGIS-Engine', 'type': 'core'},
    {'internal-name': '3DEngine', 'common-name': '3D-Analyst-Engine', 'category': 'ArcGIS-Engine', 'type': 'extension'},
    {'internal-name': 'GDBEdit', 'common-name': 'Geodatabase-Update', 'category': 'ArcGIS-Engine', 'type': 'extension'},
    {'internal-name': 'InteropEngine', 'common-name': 'Data-Interoperability-Engine', 'category': 'ArcGIS-Engine', 'type': 'extension'},
    {'internal-name': 'SchematicEngine', 'common-name': 'Schematics-Engine', 'category': 'ArcGIS-Engine', 'type': 'extension'},
    {'internal-name': 'SpatialEngine', 'common-name': 'Spatial-Analyst-Engine', 'category': 'ArcGIS-Engine', 'type': 'extension'},
    {'internal-name': 'TrackingEngine', 'common-name': 'Tracking-Analyst-Engine', 'category': 'ArcGIS-Engine', 'type': 'extension'},
    {'internal-name': 'NetworkEngine', 'common-name': 'Network-Analyst-Engine', 'category': 'ArcGIS-Engine', 'type': 'extension'},

    # Esri City Engine
    {'internal-name': 'CityEngAdv', 'common-name': 'CityEngine-Advanced', 'category': 'Esri-City-Engine', 'type': 'core'},

    # ---------------
    # Pro Products
    # ---------------

    # Core Products
    {'internal-name': 'desktopAdvP', 'common-name': 'ArcGIS-Pro-Advanced', 'category': 'ArcGIS-Pro', 'type': 'core'},
    {'internal-name': 'desktopStdP', 'common-name': 'ArcGIS-Pro-Standard', 'category': 'ArcGIS-Pro', 'type': 'core'},
    {'internal-name': 'desktopBasicP', 'common-name': 'ArcGIS-Pro-Basic', 'category': 'ArcGIS-Pro', 'type': 'core'},

    # Extensions
    {'internal-name': '3DAnalystP', 'common-name': '3D-Analyst-Pro', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    {'internal-name': 'dataReviewerP', 'common-name': 'Data-Reviewer-Pro', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    {'internal-name': 'dataInteropP', 'common-name': 'Data-Interoperability-Pro', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    {'internal-name': 'geostatAnalystP', 'common-name': 'Geostatistical-Analyst-Pro', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    {'internal-name': 'locRefP', 'common-name': 'Location-Referencing-Pro', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    {'internal-name': 'networkAnalystP', 'common-name': 'Network-Analyst-Pro', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    {'internal-name': 'spatialAnalystP', 'common-name': 'Spatial-Analyst-Pro', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    {'internal-name': 'workflowMgrP', 'common-name': 'Workflow-Manager-Pro', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    {'internal-name': 'smpNAmericaP', 'common-name': 'StreetMap-Premium-North-America', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    # {'internal-name': 'smpEuropeP', 'common-name': 'StreetMap-Premium-Europe',  'category': 'ArcGIS-Pro', 'type': 'extension'},
    # {'internal-name': 'smpMidEAfricaP', 'common-name': 'StreetMap-Premium-Middle-East-&-Africa', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    # {'internal-name': 'smpAsiaPacificP', 'common-name': 'StreetMap-Premium-Asia-Pacific', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    # {'internal-name': 'smpLAmericaP', 'common-name': 'StreetMap-Premium-Latin-America', 'category': 'ArcGIS-Pro', 'type': 'extension'},
    # {'internal-name': 'smpJapanP', 'common-name': 'StreetMap-Premium-Japan', 'category': 'ArcGIS-Pro', 'type': 'extension'},
]
