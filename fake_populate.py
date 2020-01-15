import random
from datetime import timedelta, datetime
from app.models import Server, Product, Updates, History, User, Workstation
from app.arcgis_config import products

users = ['Ann', 'Amy', 'Ben', 'Dan',
         'Ean', 'Gus', 'Ike', 'Liz',
         'Pam', 'Sam', 'Jon', 'Moe',
         'Ted', 'Pat', 'Kim', 'Bob',
         'Alf', 'Sue', 'Lin', 'Joe']

workstations = ['computer-1', 'computer 2', 'computer-3', 'computer 4', 'computer-5', 'computer 6']


def filter_core_products():
    return {k: v for k, v in products.items() if v['type'] == 'core'}

def filter_ext_products():
    return {k: v for k, v in products.items() if v['type'] == 'extension'}

def random_date():
    start = datetime.strptime('1/1/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
    end = datetime.strptime('1/15/2020 4:50 AM', '%m/%d/%Y %I:%M %p')
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def add_fake_sessions(update_id, server_id):
    history_ids = []
    core_products = filter_core_products()
    ext_products = filter_ext_products()
    for i in range(10):
        random_product_key = random.sample(list(core_products), 1)[0]
        core_product_id = Product.upsert(server_id, random_product_key, **core_products[random_product_key])
        username = random.choice(users)
        workstation = random.choice(workstations)
        user_id = User.add(username)
        workstation_id = Workstation.add(workstation)
        history_id = History.add(update_id=update_id,
                                 server_id=server_id,
                                 user_id=user_id,
                                 product_id=core_product_id,
                                 workstation_id=workstation_id,
                                 time_out=random_date())
        history_ids.append(history_id)

        random_product_key = random.sample(list(ext_products), 1)[0]
        ext_product_id = Product.upsert(server_id, random_product_key, **ext_products[random_product_key])
        username = random.choice(users)
        workstation = random.choice(workstations)
        user_id = User.add(username)
        workstation_id = Workstation.add(workstation)
        history_id = History.add(update_id=update_id,
                                 server_id=server_id,
                                 user_id=user_id,
                                 product_id=ext_product_id,
                                 workstation_id=workstation_id,
                                 time_out=random_date())
        history_ids.append(history_id)
    return history_ids


def random_checkin(server_id, history_ids):
    random_items = random.choices(population=history_ids, k=8)
    dt = datetime.now().replace(second=0, microsecond=0)
    for h in random_items:
        History.update(h, dt, server_id)


server_1 = Server.upsert('prod-server-1', 27000)
update_1 = Updates.start(server_id=server_1)
history_ids_1 = add_fake_sessions(update_1, server_1)
Updates.end(update_id=update_1)
random_checkin(server_1, history_ids_1)

server_2 = Server.upsert('prod-server-2', 27000)
update_2 = Updates.start(server_id=server_2)
history_ids_2 = add_fake_sessions(update_2, server_2)
Updates.end(update_id=update_2)
random_checkin(server_2, history_ids_2)

server_3 = Server.upsert('backup-server-3', 27000)
update_3 = Updates.start(server_id=server_2)
history_ids_3 = add_fake_sessions(update_3, server_3)
Updates.end(update_id=update_3)
random_checkin(server_3, history_ids_3)
