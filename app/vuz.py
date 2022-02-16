from app.criteria_async.vuz_name import vuz_name
from app.criteria_async.milit_department import milit_department
from app.criteria_async.stud_to_teach import stud_to_teach_uche, stud_to_teach_vuzo
from app.criteria_async.rating import rating_abro, rating_russ
from app.criteria_async.obsh import obsh
from app.criteria_async.reviews import reviews
from app.criteria_async.EGE_and_bud_pl import EGE_and_bud_pl

import asyncio

# сам класс обработки
class VUZ:
    
    def __init__(self, tabi, vuzo, uche, subj):
        self.tabi = tabi
        self.vuzo = vuzo
        self.uche = uche
        self.subj = subj

        self.loop = asyncio.get_event_loop()

    async def async_full_info(self):
        name = await vuz_name(self.vuzo)
        EGE, bud_pl, EGE_of_3max, bud_pl_of_3max = await EGE_and_bud_pl(self.vuzo, self.subj)
        milit_dep = await milit_department(self.vuzo)
        stt_v = await stud_to_teach_vuzo(self.vuzo)
        stt_u = await stud_to_teach_uche(self.uche)
        rating_rus = await rating_russ(self.uche)
        rating_eng = await rating_abro(self.uche)
        obsh_ = await obsh(self.tabi)
        reviews_ = await reviews(self.tabi)
        
        stud_to_teach = round((stt_u + stt_v) / 2, 1)
        return [name, EGE, bud_pl, EGE_of_3max, bud_pl_of_3max, milit_dep, stud_to_teach, rating_rus, rating_eng, reviews_, obsh_]
    
    def full_info(self):
        return list(self.loop.run_until_complete(self.async_full_info()))
    
    async def async_EGE_and_bud_pl(self):
        pomosh = await EGE_and_bud_pl(self.vuzo, self.subj)
        pomosh = list(pomosh)
        return pomosh

    def EGE_and_bud_pl(self):
        return list(self.loop.run_until_complete(EGE_and_bud_pl(self.vuzo, self.subj)))

    def name(self):
        return self.loop.run_until_complete(vuz_name(self.vuzo))

    def EGE(self):
        self.EGE_and_bud_pl = self.loop.run_until_complete(EGE_and_bud_pl(self.vuzo, self.subj))
        return self.EGE_and_bud_pl[0]
    
    def bud_pl(self):
        return self.EGE_and_bud_pl[1]

    def EGE_of_3max(self):
        return self.EGE_and_bud_pl[2]
    
    def bud_pl_of_3max(self):
        return self.EGE_and_bud_pl[3]
    
    def milit_dep(self):
        return self.loop.run_until_complete(milit_department(self.vuzo))
    
    def stud_to_teach(self):
        stt_v = self.loop.run_until_complete(stud_to_teach_vuzo(self.vuzo)) 
        stt_u = self.loop.run_until_complete(stud_to_teach_uche(self.uche))
        return round((stt_u + stt_v) / 2, 1)
    
    def rating_rus(self):
        return self.loop.run_until_complete(rating_russ(self.uche))
    
    def rating_eng(self):
        return self.loop.run_until_complete(rating_abro(self.uche))
    
    def obsh(self):
        return self.loop.run_until_complete(obsh(self.tabi))
    
    def reviews(self):
        return self.loop.run_until_complete(reviews(self.tabi))
    
    