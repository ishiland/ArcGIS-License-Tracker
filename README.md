FlexLM Flask
============

A python approach to concurrent use license tracking. 

FlexLM Flask collects and displays license information from a Flexera license manager using the `lmutil.exe`. Data is collected over time for a current and historical perspective on license usage.
This tool is intended to be used for tracking Esri ArcGIS concurrent use licenses but should also adaptable to other Flexera licensed applications (AutoCAD, MATLAB, IBM Rational, CATIA, and Petrel). 

## Requirements
* Python 2.7/3+
* SQL Server 2008+ or SQL Server Express. Future support for other RDBMS is expected.
* `lmutil.exe` included with the license server.

## Getting Started

1. Clone the repo
  ```
  > git clone https://github.com/ishiland/flexlm-flask.git
  > cd flexlm-flask
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
  
4. In `config.py`, configure the following:
  * `SQLALCHEMY_DATABASE_URI` - Database connection 
  * `license_servers` - List of license servers to track 
  * `lm_util` - Path to the lmutil.exe, default is the root directory.
  * `products` - List of products to track
    
5. Setup the database:
  ```
  > python scripts/create_models.py
  ```

6. Create a scheduled task:

    Run `scripts/read_license_data.py` every 5-10 min. 

7. Run the development server:
  ```
  > python flaskapp.py
  ```

8. Navigate to [http://localhost:5000](http://localhost:5000)



## Next Steps

1. Add support for other RDBMS. Pull requests welcomed. 
2. Integrate LDAP with role based viewing privileges.
3. Integrate an Organization table to get users agency, division and contact information.
4. Allow end users to send notification to admin/other users when licenses are not available.


## Screenshots

![Pages](https://ishiland.github.io/flexlm-flask/screenshots/dashboard.PNG)

![Pages](https://ishiland.github.io/flexlm-flask/screenshots/products.PNG)

![Pages](https://ishiland.github.io/flexlm-flask/screenshots/product-name.PNG)

![Pages](https://ishiland.github.io/flexlm-flask/screenshots/users.PNG)

![Pages](https://ishiland.github.io/flexlm-flask/screenshots/username.PNG)

![Pages](https://ishiland.github.io/flexlm-flask/screenshots/workstations.PNG)

![Pages](https://ishiland.github.io/flexlm-flask/screenshots/servers.PNG)

![Pages](https://ishiland.github.io/flexlm-flask/screenshots/servername.PNG)