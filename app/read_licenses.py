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
    split_text =  text.split("\n")
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

def add_users_and_workstations(text):
    search_string = text.split('FLOATING LICENSE')
    data = []
    if search_string:
        result = findall('\n{} {} {} (v{}) ({}/{}), start {:w} {:d}/{:d} {:d}:{:d}', search_string[-1])
        for r in result:
            user_id = User.add(username=r[0])
            workstation_id = Workstation.add(workstation=r[1])
            date_4_db = datetime(datetime.now().year, r[7], r[8], r[9], r[10])
            data.append({'user_id': user_id, 'workstation_id': workstation_id, 'date': date_4_db})
    return data


def product_has_users(text, server_id):
    product = {}

    product_id = None
    workstation_id = None
    user_id = None
    date_4_db = None

    license_lines = text.split("\n")

    for idx, val in enumerate(license_lines):

        quantity_result = parse("{:^}:  (Total of {:d} {:w} issued;  Total of {:d} {:w} in use)",
                                val, case_sensitive=False)
        version_result = parse('{:^} v{}, vendor: {}, expiry: {}', val, case_sensitive=False)

        # user_result = parse('{:^} {} ,{} (v{}) ({}), start {:w} {:d}/{:d} {:d}:{:d}', val,
        #                     case_sensitive=False)
        users_and_workstation_ids = add_users_and_workstations(val)

        # if quantity_result:
        #     product_name = quantity_result.fixed[0].upper()
        #     valid_product = products.get(product_name, None)
        #     if valid_product:
        #         product.update(valid_product)
        #         product['server_id'] = server_id
        #         product['internal_name'] = product_name
        #         product['license_out'] = quantity_result[3]
        #         product['license_total'] = quantity_result[1]
        #         product_id = Product.upsert(**product)
        #
        # if version_result:
        #     product['version'] = version_result[1]
        #     product['expires'] = version_result[3]
        #     product_id = Product.upsert(**product)

        # if user_result:
        #     user_id = User.add(username=user_result[0])
        #     workstation_id = Workstation.add(workstation=user_result[1])
        #     date_4_db = datetime(datetime.now().year, user_result[6], user_result[7], user_result[8], user_result[9])

        if product_id and workstation_id and user_id:
            return {'product_id': product_id, 'workstation_id': workstation_id, 'user_id': user_id,
                    'server_id': server_id, 'date_4_db': date_4_db}
            # history_id = History.add(user_id, workstation_id, server_id, product_id, update_id,
            #                          date_4_db)
            # checked_out_history_ids.append(history_id)

        if idx == len(license_lines):
            return None


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

            for idx, val in enumerate(license_data):
                processed_data = product_has_users(val, server_id)
                if processed_data:
                    history_id = History.add(update_id, **processed_data)

                    checked_out_history_ids.append(history_id)
            dt = datetime.now().replace(second=0, microsecond=0)
            checked_out = History.time_in_none(server_id)
            for c in checked_out:
                if c.id not in checked_out_history_ids:
                    History.update(c.id, dt, server_id)

        except Exception as e:
            info = "{}: {}".format("Error", str(e))
            pass
        finally:
            Updates.end(update_id, updates['status'], info)
