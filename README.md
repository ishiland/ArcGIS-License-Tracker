FlexLM - Script and Schema
================================
This branch contains only the database models and script to collect license information from a Flexera license manager using the `lmutil.exe`.

The resulting database can be used in a web application or queried using a tool like [DB Browser for SQL Lite](https://sqlitebrowser.org/)

## Features
 * Get current and historically perspectives on license usage by User, Workstation or License Server
 * Supports multiple license servers

## Requirements
 * `lmutil.exe` included with your license server manager.
 * python 3

## Getting Started

1. Clone the repo and checkout this branch
  ```
  > git clone https://github.com/ishiland/flexlm-flask.git
  > cd flexlm-flask
  > git checkout script-n-schema
  ```


2. Setup a virtual environment (optional), then install the dependencies:
  ```
  > pip install -r requirements.txt
  ```
  
3. In `config.py`, configure the following:
  * `license_servers` - List of license servers to track. Default port is 27000.
  * `lm_util` - Path to your lmutil.exe. Default is the root directory.
  * `products` - List of products to track. Comment/uncomment those applicable to your organization, default may work for most.
    
4. test your configuration and do a first read of your license server:
  ```
  > python read.py
  ```
Any issues should be written to the log file.

5. setup as a scheduled task to automate the updates.
