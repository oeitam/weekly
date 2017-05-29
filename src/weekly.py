# oeitam

import sys
from src.db import db as database
from src.gtd import gtd as gettingthingsdone
from src.server import server


db = database.Db()
proc = gettingthingsdone.Gtd(db)
server = server.Server(proc)
server.server_process()

input("Press enter to finish the program")














# end


