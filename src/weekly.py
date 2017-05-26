# oeitam

import sys
from src.db import db as database
from src.gtd import gtd as gettingthingsdone
from src.server import server
import logging


db = database.Db()
proc = gettingthingsdone.Gtd(db)
server = server.Server()















# end


