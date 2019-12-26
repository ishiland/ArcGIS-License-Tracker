from parse import *
from datetime import datetime
import subprocess
from app.arcgis_config import products, license_servers, lm_util
from app.models import Server, Product, Updates, History, User, Workstation


def check_year(s_id):
    """
    lmutil.exe does not provide a year with license data, this is a work-around to account for that. Checks in
    all licences if there is a difference between current year and the year of any checked out licenses.
    :param s_id: Id of server
    """
    checked_out = History.time_in_none(s_id)
    for r in checked_out:
        if datetime.now().year != r.time_out.year:
            Product.reset(s_id)
            History.reset(s_id)
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


def split_license_data(text):
    return text.replace("\n\n", "\n").upper().split("USERS OF")


def parse_server_info(lines):
    return parse("{:^}:\n{}: LICENSE SERVER {:w} (MASTER) V11.16.2{:^}", lines, case_sensitive=False)


def add_product(text, server_id):
    """
    Adds a licensed product into the database
    :param text: text to be parsed
    :param server_id: ID of server where product is licensed from
    :return: product ID or None
    """
    product = {}
    split_text = text.split("\n")
    data = split_text[0].strip()
    quantity_result = parse("{}:  (Total of {:d} {:w} issued;  Total of {:d} {:w} in use)", data)
    valid_product = products.get(quantity_result[0], None)
    if valid_product:
        product.update(valid_product)
        product['server_id'] = server_id
        product['internal_name'] = quantity_result[0].upper()
        product['license_out'] = quantity_result[3]
        product['license_total'] = quantity_result[1]
        if len(data) > 0:
            version_result = parse('{:^} v{}, vendor: {}, expiry: {}', split_text[1].strip(), case_sensitive=False)
            if version_result:
                product['version'] = version_result[1]
                product['expires'] = version_result[3]
        return Product.upsert(**product)
    return None


def add_users_and_workstations(text, server_id):
    data = []
    split_line = text.split('FLOATING LICENSE')
    product_search_string = split_line[0]
    product_id = add_product(product_search_string, server_id=server_id)
    users_search_string = split_line[-1]
    if users_search_string:
        result = findall('{} {} {} (v{}) ({}/{}), start {:w} {:d}/{:d} {:d}:{:d}',
                         users_search_string.replace("\n", "").strip())
        for r in result:
            user_id = User.add(username=r[0])
            workstation_id = Workstation.add(workstation=r[1])
            date_4_db = datetime(datetime.now().year, r[7], r[8], r[9], r[10])
            data.append(
                {'product_id': product_id, 'user_id': user_id, 'workstation_id': workstation_id, 'time_out': date_4_db})
    return data


def read():
    for s in license_servers:
        try:
            info = ''

            server_id = Server.upsert(s['hostname'], s['port'])
            update_id = Updates.start(server_id)
            check_year(server_id)

            checked_out_history_ids = []

            process = subprocess.Popen([lm_util, "lmstat", "-f -c {}@{}".format(s['port'], s['hostname'])],
                                       stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
            lines = process.stdout.read()

            license_data = split_license_data(lines)

            # for update model
            updates = {'update_id': update_id, 'status': None}

            server_information = parse_server_info(lines)

            if server_information:
                updates['status'] = server_information[2]
            else:
                updates['status'] = "DOWN"
                reset(update_id, server_id, '{}@{} is DOWN'.format(s['port'], s['hostname']))
                break

            for lic in license_data:
                users_and_workstations = add_users_and_workstations(lic, server_id)
                for kwargs in users_and_workstations:
                    history_id = History.add(update_id=update_id, server_id=server_id, **kwargs)
                    print('history_id', history_id)
                    #         checked_out_history_ids.append(history_id)
                    # dt = datetime.now().replace(second=0, microsecond=0)
                    # checked_out = History.time_in_none(server_id)
                    # for c in checked_out:
                    #     if c.id not in checked_out_history_ids:
                    #         History.update(c.id, dt, server_id)

        except Exception as e:
            info = "{}: {}".format("Error", str(e))
            print(info)
            pass
        finally:
            Updates.end(update_id, updates['status'], info)


read()
