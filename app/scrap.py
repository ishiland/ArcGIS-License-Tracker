from app.models import History, Product, db, Server, Updates
from sqlalchemy import func, desc, and_

server_id = 1

checked_out = History.time_in_none(server_id)

for c in checked_out:
    print(c.time_out.year)