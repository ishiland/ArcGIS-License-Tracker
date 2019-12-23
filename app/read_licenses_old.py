import os, subprocess
from datetime import datetime
from app.models import Product, Updates, User, History, Server, Workstation
from app.arcgis_config import license_servers, lm_util, products


def check_year(server_id):
    """
    lmutil.exe does not provide a year with license data, this is a work-around to account for that. Checks in
    all licences if there is a difference between current year and the year of any checked out licenses.
    :param server_id: Id of server
    """
    checked_out = History.time_in_none(server_id)
    for r in checked_out:
        if datetime.now().year != r.time_out.year:
            Product.reset(server_id)
            History.reset(server_id)
            break


def reset(uid, sid, e_msg):
    """
    Checks in all licences on error.
    :param uid: User ID
    :param sid: Server ID
    :param e_msg: Error message
    """
    Product.reset(sid)
    History.reset(sid)
    Updates.end(uid, 'ERROR', e_msg)


def read():
    """
    Entry point for updating licenses. This script can optionally be run stand alone (cron job or windows task scheduler).
    Relies on the lmutil.exe to collect server information.
    """
    checked_out_history_ids = []
    has_error = False
    try:
        for server in license_servers:
            print('Reading from {} on port {}...'.format(server['name'], server['port']))
            s = server['name']
            port = server['port']
            info = None
            status = None
            server_id = Server.upsert(server)
            update_id = Updates.start(server_id)
            check_year(server_id)
            try:
                # Server info
                process = subprocess.Popen([lm_util, "lmstat", "-c", "{}@{}".format(port, s)], stdout=subprocess.PIPE,
                                           bufsize=1, universal_newlines=True)
                lm_util_lines = process.stdout.readlines()
                if len(lm_util_lines) == 0:
                    m = 'Unable to read license data. Check path to lmutil.exe and license server parameters are correct.'
                    raise Exception(m)
                for idx, line in enumerate(lm_util_lines):
                    l = line.split(':')
                    if 'error' in line.lower():
                        raise Exception(line)
                    elif status is None:
                        if l[0] == s:
                            info = l[1].strip()
                            if 'license server up' in info.lower():
                                status = 'OK'
                                info = None
                                break
                            else:
                                raise Exception(
                                    'Unable to parse license data. Check license server is functioning properly.')
                    elif (idx + 1) == len(lm_util_lines) and status is None:
                        raise Exception('No license data from lmutil.exe')
            except Exception as e:
                reset(update_id, server_id, str(e))
                has_error = True
                continue

            try:
                # Product info
                for idx, val in enumerate(products):
                    process = subprocess.Popen(
                        [lm_util, "lmstat", "-c", "{} {}@{}".format(val['internal-name'], port, s)],
                        stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
                    for idx, line in enumerate(process.stdout.readlines()):
                        if 'Users of ' + val['internal-name'] in line:
                            lic = line.lower().split('total of ')
                            lic_total = int(lic[1][:2])
                            lic_out = int(lic[2][:2])
                            Product.upsert(server_id=server_id,
                                           internal_name=val['internal-name'],
                                           common_name=val['common-name'],
                                           category=val['category'],
                                           type=val['type'],
                                           license_out=lic_out,
                                           license_total=lic_total)

                        # User info
                        if ") (" + s + "/" + port in line:
                            cols = line.split()
                            if 'activated' in line.lower():
                                user = 'BORROWED'
                                computer = cols[2]
                            else:
                                user = cols[0]
                                computer = cols[1]

                            # Format date for sql
                            month = cols[-2].split("/")[0]
                            day = cols[-2].split("/")[1]
                            if len(day) == 1:
                                day = '0' + day
                            if len(month) == 1:
                                month = '0' + month
                            t = cols[-1]
                            hour = t.split(":")[0]
                            min = t.split(":")[1]
                            date_4_db = datetime(datetime.now().year, int(month), int(day), int(hour), int(min))
                            workstation_id = Workstation.add(workstation=computer)
                            user_id = User.add(username=user)
                            product_id = Product.query(val['internal-name'], server_id)
                            history_id = History.add(user_id, workstation_id, server_id, product_id, update_id,
                                                     date_4_db)
                            checked_out_history_ids.append(history_id)

                    dt = datetime.now().replace(second=0, microsecond=0)
                    checked_out = History.time_in_none(server_id)
                    for c in checked_out:
                        if c.id not in checked_out_history_ids:
                            History.update(c.id, dt, server_id)
                    Updates.end(update_id, status, info)

            except Exception as e:
                reset(update_id, server_id, str(e))
                print(e)
                has_error = True
                continue

    except Exception as e:
        has_error = True
        print(e)
    finally:
        print("Read process finished.")
        return has_error