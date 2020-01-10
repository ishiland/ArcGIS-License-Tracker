from parse import *
from datetime import datetime
import subprocess
from app.arcgis_config import products, license_servers, lm_util
from app.models import Server, Product, Updates, History, User, Workstation
from app.logger_setup import logger


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
            logger.info('check_year reset for server id {}'.format(s_id))
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
    logger.error(e_msg)

def parse_error_info(lines):
    result = parse('{:^}Error getting status:{}\n', lines, case_sensitive=False)
    if result:
        if len(result.fixed):
            return result[-1].strip()
    return None

def split_license_data(text):
    return text.replace("\n\n", "\n").upper().split("USERS OF")


def parse_server_info(lines):
    return parse("{:^}:\n{}: LICENSE SERVER {:w} (MASTER) V11.16.2{:^}", lines, case_sensitive=False)


def parse_product_info(lines):
    return parse("{}:  (Total of {:d} {:w} issued;  Total of {:d} {:w} in use)", lines, case_sensitive=False)


def parse_version_info(text):
    return parse('{:^} v{}, vendor: {}, expiry: {}', text, case_sensitive=False)


def parse_users_and_workstations(lines):
    return findall('    {} {} {} (v{}) ({}/{}), start {:w} {:d}/{:d} {:d}:{:d}', lines, case_sensitive=False)


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
    quantity_result = parse_product_info(data)
    if quantity_result:
        valid_product = products.get(quantity_result[0], None)
        if valid_product:
            product.update(valid_product)
            product['server_id'] = server_id
            product['internal_name'] = quantity_result[0].upper()
            product['license_out'] = quantity_result[3]
            product['license_total'] = quantity_result[1]
            if len(data) > 0:
                version_result = parse_version_info(split_text[1].strip())
                if version_result:
                    product['version'] = version_result[1]
                    product['expires'] = version_result[3]
            return Product.upsert(**product)
    return None


def map_product_id(product_id, arr):
    out = []
    for a in arr:
        a['product_id'] = product_id
        out.append(a)
    return out


def add_users_and_workstations(text):
    data = []
    if text:
        result = parse_users_and_workstations(text)
        for r in result:
            user_id = User.add(username=r[0])
            workstation_id = Workstation.add(workstation=r[1])
            date_4_db = datetime(datetime.now().year, r[7], r[8], r[9], r[10])
            data.append(
                {'user_id': user_id, 'workstation_id': workstation_id, 'time_out': date_4_db})
    return data


def read():
    for s in license_servers:
        try:
            info = ''
            server_id = Server.upsert(s['hostname'], s['port'])
            update_id = Updates.start(server_id)
            check_year(server_id)
            checked_out_history_ids = []
            process = subprocess.Popen([lm_util, "lmstat", "-f", "-c", "{}@{}".format(s['port'], s['hostname'])],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
            lines = process.stdout.read()
            has_error = parse_error_info(lines)
            if has_error:
                reset(update_id, server_id, '{}@{}: {}'.format(s['port'], s['hostname'], has_error))
                raise Exception(has_error)
            license_data = split_license_data(lines)
            updates = {'update_id': update_id, 'status': None}
            server_information = parse_server_info(lines)
            if server_information:
                updates['status'] = server_information[2]
            else:
                updates['status'] = "DOWN"
                reset(update_id, server_id, '{}@{} is DOWN'.format(s['port'], s['hostname']))
                raise Exception(has_error)
            for lic in license_data:
                split_line = lic.split('FLOATING LICENSE')
                product_id = add_product(split_line[0], server_id=server_id)
                users_and_workstations = add_users_and_workstations(split_line[-1])
                if product_id and len(users_and_workstations):
                    data = map_product_id(product_id, users_and_workstations)
                    for kwargs in data:
                        history_id = History.add(update_id=update_id, server_id=server_id, **kwargs)
                        checked_out_history_ids.append(history_id)
            dt = datetime.now().replace(second=0, microsecond=0)
            checked_out = History.time_in_none(server_id)
            for c in checked_out:
                if c.id not in checked_out_history_ids:
                    History.update(c.id, dt, server_id)
        except Exception as e:
            info = "{} error: {}".format(s['hostname'], str(e))
            logger.error(str(e))
            pass
        finally:
            logger.info(
                'Finished reading data from \'{}\'. '
                'Update details | id:{} | status:{} | info:{}.'.format(s['hostname'],
                                                                       update_id,
                                                                       updates['status'],
                                                                       info))
            Updates.end(update_id, updates['status'], info)
