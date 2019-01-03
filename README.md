FlexLM Flask
============

FlexLM Flask collects and displays license information from a Flexera license manager using the `lmutil.exe`. It can be used to assess licensed product usage, inventory users and computers, and monitor license servers.

Data is collected over time for a current and historical perspective of license usage.

This tool is intended to be used for tracking Esri ArcGIS concurrent use licenses but may also be adaptable to other Flexera licensed applications.

### Script and Database Models only

Check out the [scripts-n-schema](https://github.com/ishiland/flexlm-flask/tree/script-n-schema) branch for a stripped down version of this project which only includes the script and database schema to collect license usage.

## Features
 * [Flask](http://flask.pocoo.org/)
 * [SQLAlchemy](https://www.sqlalchemy.org/)
 * [SQLite](https://www.sqlite.org/)
 * [Apscheduler](https://apscheduler.readthedocs.io/en/latest/) for syncing license data as a background task.
 * [ChartJs](http://www.chartjs.org/) for product visualization.
 * [MomentJS](https://momentjs.com/) and [humanize-duration.js](https://evanhahn.github.io/HumanizeDuration.js/) for time display.

## Requirements
 * Developed with Python 3.6. This app may work with older versions of python although they have not been tested.
 * `lmutil.exe` included with your license server manager.

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
  
4. In `app/toolbox/lm_config.py`, configure the following:
  * `UPDATE_INTERVAL` - Frequency to collect license data. Default is 5 minutes.
  * `license_servers` - List of license servers to track. Default port is 27000.
  * `lm_util` - Path to your lmutil.exe. Default is in the `toolbox` directory.
  * `products` - List of products to track. Comment/uncomment those applicable to your organization, default may work for most.
    
5. Initialize the database:
  ```
  > python manage.py initdb
  ```

6. Test your license server configuration:
  ```
  > python manage.py read
  ```


7. Run the development server:
  ```
  > python manage.py runserver
  ```

8. Navigate to [http://localhost:5000](http://localhost:5000)


Tip:
 * A background data-sync task is started when you run the development server, so keep the server running to reflect the most accurate usage information. Ideally this application should be deployed to a production web server. See below for more info.

## Deploy to production
Flask can be deployed to a number of self-hosted production web servers. Instructions on how to do this are located [here](http://flask.pocoo.org/docs/0.12/deploying/).


## Screenshots

![Dashboard](https://ishiland.github.io/flexlm-flask/screenshots/dashboard.png)
![Product](https://ishiland.github.io/flexlm-flask/screenshots/product.png)