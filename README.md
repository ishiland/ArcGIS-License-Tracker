ArcGIS License Monitor
============
ArcGIS License Monitor is a tool to display current and historical license usage from a concurrent use (floating) license server. 

## Features
* Access license data through the browser
* View and export license data - users, products and workstations. 
* Supports multiple license servers

## Requirements
 * Python >= 3.6
 * Windows OS
 * Local access to the `lmutil.exe` included with the license server. The default location of this command line tool is in `C:\Program Files (x86)\ArcGIS\LicenseManager\bin\`.

## Getting Started

1. Clone the repo
  ```
  > git clone https://github.com/ishiland/arcgis-license-monitor.git
  > cd arcgis-license-monitor
  ```

2. Initialize and activate a virtualenv:
  ```
  > python -m virtualenv venv
  > venv\Scripts\activate
  ```

3. Install the dependencies:
  ```
  > pip install -r requirements.txt
  ```
  
4. In `app/arcgis_config.py`, configure the following:
  * `UPDATE_INTERVAL` - Frequency to collect license data. Default is every 5 minutes.
  * `license_servers` - List of license servers to track. The default port is 27000.
  * `lm_util` - Path to your lmutil.exe. 
    
5. Initialize the database:
  ```
  > python manage.py recreate_db
  ```

6. Test your license server configuration:
  ```
  > python manage.py read_once
  ```

7. Run the development server:
  ```
  > python manage.py runserver
  ```

8. Navigate to [http://localhost:5000](http://localhost:5000)


## Note
The Flask application must always be running to accurately reflect license usage. Deploy to a production web server for best results. Instructions on how to do this are located [here](http://flask.pocoo.org/docs/0.12/deploying/).


## Development and Tests
Tests can be ran using `python manage.py test`

Pull requests are welcome. The following diagram outlines the database design:

![alt text](database.PNG "Title")