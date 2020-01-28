import random
from datetime import timedelta, datetime
from app.models import Server, Product, Updates, History, User, Workstation
from app.arcgis_config import products


def get_server_id(name):
    return Server.upsert(name, 27000)


def get_workstation_id(name):
    return Workstation.add(name)


def get_user_id(name):
    return User.add(name)


def get_product_id(server_id, internal_name, in_use, total):
    p = products[internal_name]
    p['license_out'] = in_use
    p['license_total'] = total
    return Product.upsert(server_id=server_id, internal_name=internal_name, **p)


def random_date():
    """
    This function will return a random datetime between two datetime
    objects.
    """
    start_date = datetime.now() + timedelta(-15)
    start = datetime.strptime(start_date.strftime('%Y-%m-%d %I:%M:%S'), '%Y-%m-%d %I:%M:%S')
    end = datetime.strptime(datetime.now().strftime('%Y-%m-%d %I:%M:%S'), '%Y-%m-%d %I:%M:%S')
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def check_in(server_id, h, data):
    while True:
        dt = random_date()
        if dt < data['time_out']:
            History.update(h, dt, server_id)
            return

def populate():
    server_1 = get_server_id('gis-license-1')

    server_2 = get_server_id('gis-license-2')

    update_1 = Updates.start(server_1)

    update_2 = Updates.start(server_2)



    dummy_data = [
        # server 1
        (update_1, server_1, {'user_id': get_user_id('Gus'),
                              'workstation_id': get_workstation_id('Gus-PC'),
                              'product_id': get_product_id(server_1, 'ARC/INFO', 0, 3),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Ted'),
                              'workstation_id': get_workstation_id('Ted-PC'),
                              'product_id': get_product_id(server_1, 'ARC/INFO', 0, 3),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Lin'),
                              'workstation_id': get_workstation_id('Lin-PC'),
                              'product_id': get_product_id(server_1, 'VIEWER', 0, 5),
                              'time_out': random_date()}, True),
        (update_1, server_1, {'user_id': get_user_id('Sue'),
                              'workstation_id': get_workstation_id('Ted-PC'),
                              'product_id': get_product_id(server_1, 'EDITOR', 5, 10),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Ike'),
                              'workstation_id': get_workstation_id('Ike-PC'),
                              'product_id': get_product_id(server_1, 'EDITOR', 5, 10),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Mary'),
                              'workstation_id': get_workstation_id('Mary-PC'),
                              'product_id': get_product_id(server_1, 'EDITOR', 5, 10),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Sally'),
                              'workstation_id': get_workstation_id('Sally-PC'),
                              'product_id': get_product_id(server_1, 'EDITOR', 5, 10),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Ron'),
                              'workstation_id': get_workstation_id('Ron-PC'),
                              'product_id': get_product_id(server_1, 'EDITOR', 5, 10),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Bill'),
                              'workstation_id': get_workstation_id('Bill-PC'),
                              'product_id': get_product_id(server_1, 'EDITOR', 5, 10),
                              'time_out': random_date()}, True),
        (update_1, server_1, {'user_id': get_user_id('Nancy'),
                              'workstation_id': get_workstation_id('Nancy-PC'),
                              'product_id': get_product_id(server_1, 'EDITOR', 5, 10),
                              'time_out': random_date()}, True),
        (update_1, server_1, {'user_id': get_user_id('Will'),
                              'workstation_id': get_workstation_id('Will-PC'),
                              'product_id': get_product_id(server_1, 'EDITOR', 5, 10),
                              'time_out': random_date()}, True),
        (update_1, server_1, {'user_id': get_user_id('Sam'),
                              'workstation_id': get_workstation_id('Sam-PC'),
                              'product_id': get_product_id(server_1, 'DESKTOPBASICP', 2, 2),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Pat'),
                              'workstation_id': get_workstation_id('Pat-PC'),
                              'product_id': get_product_id(server_1, 'DESKTOPBASICP', 2, 2),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Alf'),
                              'workstation_id': get_workstation_id('Alf-PC'),
                              'product_id': get_product_id(server_1, 'DESKTOPADVP', 1, 4),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Sam'),
                              'workstation_id': get_workstation_id('Sam-PC'),
                              'product_id': get_product_id(server_1, '3DANALYSTP', 2, 4),
                              'time_out': random_date()}, False),
        (update_1, server_1, {'user_id': get_user_id('Pat'),
                              'workstation_id': get_workstation_id('Pat-PC'),
                              'product_id': get_product_id(server_1, '3DANALYSTP', 2, 4),
                              'time_out': random_date()}, False),

        # server 2
        (update_2, server_2, {'user_id': get_user_id('Bob'),
                              'workstation_id': get_workstation_id('Pat-PC'),
                              'product_id': get_product_id(server_2, 'ARC/INFO', 2, 3),
                              'time_out': random_date()}, False),
        (update_2, server_2, {'user_id': get_user_id('Kim'),
                              'workstation_id': get_workstation_id('Alf-PC'),
                              'product_id': get_product_id(server_2, 'ARC/INFO', 2, 3),
                              'time_out': random_date()}, False),
        (update_2, server_2, {'user_id': get_user_id('Joe'),
                              'workstation_id': get_workstation_id('Joe-PC'),
                              'product_id': get_product_id(server_2, 'VIEWER', 0, 10),
                              'time_out': random_date()}, True),
        (update_2, server_2, {'user_id': get_user_id('Liz'),
                              'workstation_id': get_workstation_id('Joe-PC'),
                              'product_id': get_product_id(server_2, 'VIEWER', 0, 10),
                              'time_out': random_date()}, True),
        (update_2, server_2, {'user_id': get_user_id('Pam'),
                              'workstation_id': get_workstation_id('Pam-PC'),
                              'product_id': get_product_id(server_2, 'EDITOR', 1, 10),
                              'time_out': random_date()}, False),
        (update_2, server_2, {'user_id': get_user_id('Ann'),
                              'workstation_id': get_workstation_id('Ann-PC'),
                              'product_id': get_product_id(server_2, 'DESKTOPBASICP', 0, 2),
                              'time_out': random_date()}, True),
        (update_2, server_2, {'user_id': get_user_id('Bob'),
                              'workstation_id': get_workstation_id('Bob-PC'),
                              'product_id': get_product_id(server_2, 'NETWORK', 2, 2),
                              'time_out': random_date()}, False),
        (update_2, server_2, {'user_id': get_user_id('Kim'),
                              'workstation_id': get_workstation_id('Kim-PC'),
                              'product_id': get_product_id(server_2, 'NETWORK', 2, 2),
                              'time_out': random_date()}, False),
    ]

    for d in dummy_data:
        id = History.add(d[0], d[1], **d[2])
        if d[3]:
            check_in(server_id=d[1], h=id, data=d[2])

    Updates.end(update_1, 'UP', '')
    Updates.end(update_2, 'UP', '')


if __name__ == "__main__":
    populate()