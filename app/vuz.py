from app.criteria_async.vuz_name import vuz_name
from app.criteria_async.milit_department import milit_department
from app.criteria_async.stud_to_teach import stud_to_teach_uche, stud_to_teach_vuzo
from app.criteria_async.rating import rating_abro, rating_russ
# from app.criteria_async.
# from app.criteria_async.
# from app.criteria_async.



import asyncio
from bs4 import BeautifulSoup
import aiohttp

class vuz:
    
    def __init__(self, tabi, vuzo, uche):
        self.tabi = tabi
        self.vuzo = vuzo
        self.uche = uche
        self.loop = asyncio.get_event_loop()
    

    def vuz_name(self):
        return self.loop.run_until_complete(vuz_name(self.vuzo))
    
    def milit_dep(self):
        return self.loop.run_until_complete(milit_department(self.vuzo))
    
    def stud_to_teach(self):
        stt_v = self.loop.run_until_complete(stud_to_teach_vuzo(self.vuzo)) 
        stt_u = self.loop.run_until_complete(stud_to_teach_uche(self.uche))
        return round((stt_u + stt_v) / 2, 1)
    
    def rating_rus(self):
        return self.loop.run_until_complete(rating_russ(self.uche))
    
    # def (self):
    #     return self.loop.run_until_complete()
    
    # def (self):
    #     return self.loop.run_until_complete()