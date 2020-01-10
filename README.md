ArcGIS License Tracker
============
ArcGIS License Tracker is a tool to display current and historical license usage from a concurrent use (floating) license server.

## Features
* Access license usage through the browser
* Export license data - users, products and workstations to multiple file formats. 
* Support for multiple license servers

## Requirements
 * Python >= 3.6
 * Windows OS
 * Local access to the `lmutil.exe` included with the license server. The default location of this command line tool is in `C:\Program Files (x86)\ArcGIS\LicenseManager\bin\`.

## Getting Started

1. Clone the repo
  ```
  > git clone https://github.com/ishiland/arcgis-license-tracker.git
  > cd arcgis-license-tracker
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
    
5. Initialize the database

  Initialize the database using:
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


## Production deployment
To run in production mode, set the `FLASK_ENV` variable to `production` then initialize a production database using `python manage.py recreate_db`.

Some helpful guides and tools for deploying to IIS:
 - [GitHub Gist](https://gist.github.com/bparaj/ac8dd5c35a15a7633a268e668f4d2c94)
 - [wfastcgi](https://pypi.org/project/wfastcgi/)
 
 A summary of other deployment options [here](https://flask.palletsprojects.com/en/1.1.x/deploying/)

 I have also included a sample web.config for reference. 
 
## Tests
Tests can be ran using `python manage.py test`

## Development
A few things - 
 - To specify a development environment, open a powershell window and enter the following:
   `$env:FLASK_ENV = "development"`
 - When running in the dev environment, the app will not automatically start a background process for license reading. This is because the development server will spawn a duplicate background process due to the flask "reloader" feature. The command `python manage.py read_once` will run a one-time read process.  
 - The database design is as follows:
    
   ![alt text](database.PNG "Database Diagram")