import os
from datetime import datetime
from app.models import Product, Updates, User, History, Server, Workstation
from app.toolbox.lm_config import license_servers, lm_util, products

year = datetime.now().year


def check_year(server_id):
    """
    lmutil.exe does not provide a year with license data, this is a work-around to account for that. Checks in
    all licences if there is a difference between current year and the year of any checked out licenses.
    :param server_id: Id of server
    """
    checked_out = History.time_in_none(server_id)
    for r in checked_out:
        if year != r.time_out.year:
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


def run():
    """
    Entry point for updating licenses. This script can optionally be run stand alone (cron job or windows task scheduler).
    Relies on the lmutil.exe to collect server information.
    """
    checked_out_history_ids = []
    error = False
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
                lm_util_lines = os.popen(lm_util + " lmstat -c " + port + "@" + s).readlines()
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
                            else:
                                raise Exception(
                                    'Unable to parse license data. Check license server is functioning properly.')
                    elif (idx + 1) == len(lm_util_lines) and status is None:
                        raise Exception('No license data from lmutil.exe')
            except Exception as e:
                reset(update_id, server_id, str(e))
                error = True
                continue

            try:
                # Product info
                for idx, val in enumerate(products):
                    lm_util_lines = os.popen(
                        lm_util + " lmstat -f " + val['internal-name'] + " -c " + port + "@" + s).readlines()
                    for idx, line in enumerate(lm_util_lines):
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
                            date_4_db = datetime(year, int(month), int(day), int(hour), int(min))
                            workstation_id = Workstation.add(workstation=computer)
                            user_id = User.add(username=user)
                            product_id = Product.query(val['internal-name'], server_id)
                            history_id = History.add(user_id, workstation_id, server_id, product_id, update_id, date_4_db)
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
                error = True
                continue

    except Exception as e:
        error = True
        print(e)
    finally:
        print("Read process finished.")
        return error
