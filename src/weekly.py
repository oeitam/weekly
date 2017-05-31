# oeitam

import sys
from src.db import db as database
from src.gtd import gtd as gettingthingsdone
from src.server import server


db = database.Db()
gtd = gettingthingsdone.Gtd(db)
server = server.Server(gtd)
server.server_process()

input("Press enter to finish the program")














# end


