from app.criteria_async.vuz_name import vuz_name
from app.criteria_async.militDepartment import militDepartment
from app.criteria_async.studToTeach import studToTeach_uche, studToTeach_vuzo
from app.criteria_async.rating import rating_abro, rating_russ
from app.criteria_async.obsh import obsh
from app.criteria_async.reviews import reviews
from app.criteria_async.EGE_and_budPl import EGE_and_budPl

import asyncio

# я говорю все, что хочещь знать о ВУЗе, специально для тебя
class VUZ:
    
    def __init__(self, tabi, vuzo, uche, subj):
        self.tabi = tabi
        self.vuzo = vuzo
        self.uche = uche
        self.subj = subj

        self.loop = asyncio.get_event_loop()

    def do__of_3max(self, EGE, bud_pl):
        EGE_of_3max = [0, 0, 0]
        bud_pl_of_3max = [0, 0, 0]

        for i in range(len(EGE)):
            bal = EGE[i]
            bud = bud_pl[i]

            if bal > EGE_of_3max[0]:
                EGE_of_3max[0] = bal
                bud_pl_of_3max[0] = bud
            elif bal > EGE_of_3max[1]:
                EGE_of_3max[1] = bal
                bud_pl_of_3max[1] = bud
            elif bal > EGE_of_3max[2]:
                EGE_of_3max[2] = bal
                bud_pl_of_3max[2] = bud

        return EGE_of_3max, bud_pl_of_3max


    async def async_full_info(self):
        try:
            name = await vuz_name(self.vuzo)
            EGE, budPl = await EGE_and_budPl(self.vuzo, self.subj)
            militDep = await militDepartment(self.vuzo)
            stt_v = await studToTeach_vuzo(self.vuzo)
            stt_u = await studToTeach_uche(self.uche)
            rating_rus = await rating_russ(self.uche)
            rating_eng = await rating_abro(self.uche)
            obsh_ = await obsh(self.tabi)
            reviews_ = await reviews(self.tabi)
            
        except Exception as ex:
            print(ex)
            return 'Exception'

        studToTeach = round((stt_u + stt_v) / 2, 1)
        EGE_of3max, budPl_of3max = self.do__of_3max(EGE, budPl)

        return [name, EGE, budPl, EGE_of3max, budPl_of3max, militDep, studToTeach, rating_rus, rating_eng, reviews_, obsh_]
    
    def full_info(self):
        return self.loop.run_until_complete(self.async_full_info())
    
    async def async_EGE_and_budPl(self):
        try: 
            EGE, budPl = await EGE_and_budPl(self.vuzo, self.subj)
        except Exception as ex:
            print(ex)
            return 'Exception'

        EGE_of3max, budPl_of3max = self.do__of_3max(EGE, budPl)

        return [EGE, budPl, EGE_of3max, budPl_of3max]