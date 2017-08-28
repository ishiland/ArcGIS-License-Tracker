import os, sys
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from models import Product, Update, User, History, Server, Workstation
from config import license_servers, lm_util, products

year = str(datetime.now().year)

checked_out_history_ids = []


# Check in products on error
def reset(uid, sid, e_msg):
    Product.reset(sid)
    History.reset(sid)
    Update.end(uid, 'ERROR', e_msg)


# check-in product if user not in current checked-out history list
def update_history(uid, sid):
    try:
        dt = datetime.now().replace(second=0, microsecond=0)
        checked_out = History.time_in_none(sid)
        for c in checked_out:
            if c.id not in checked_out_history_ids:
                History.update(c.id, dt, sid)
    except Exception as e:
        reset(uid, sid, str(e))


def run():
    for server in license_servers:
        print('Updating ' + server['name'] + ' license data...')
        s = server['name']
        port = server['port']
        info = None
        status = None
        server_id = Server.upsert(server)
        update_id = Update.start(server_id)

        try:
            # Server info
            lm_util_lines = os.popen(lm_util + " lmstat -c " + port + "@" + s).readlines()
            if len(lm_util_lines) == 0:
                m = 'Unable to read license data. Check path to lmutil.exe and license server parameters are correct.'
                raise Exception(m)
            for idx, line in enumerate(lm_util_lines):
                l = line.split(':')
                if status is None:
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
            print(e)
            sys.exit(1)

        try:
            # Product info
            for p in products:
                lm_util_lines = os.popen(
                    lm_util + " lmstat -f " + p['internal-name'] + " -c " + port + "@" + s).readlines()
                for idx, line in enumerate(lm_util_lines):
                    if 'Users of ' + p['internal-name'] in line:
                        lic = line.lower().split('total of ')
                        lic_total = int(lic[1][:2])
                        lic_out = int(lic[2][:2])
                        Product.upsert(server_id=server_id,
                                       internal_name=p['internal-name'],
                                       common_name=p['common-name'],
                                       category=p['category'],
                                       type=p['type'],
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
                        sql_date = year + month + day + ' ' + t
                        workstation_id = Workstation.exists_or_insert(workstation=computer)
                        user_id = User.exists_or_insert(user=user)
                        product_id = Product.query(p['internal-name'], server_id)
                        history_id = History.exists_or_insert(user_id, workstation_id, server_id, product_id, update_id,
                                                              sql_date)
                        checked_out_history_ids.append(history_id)

            update_history(update_id, server_id)
            Update.end(update_id, status, info)

        except Exception as e:
            reset(update_id, server_id, str(e))
            print(e)
            sys.exit(1)


if __name__ == '__main__':
    run()
