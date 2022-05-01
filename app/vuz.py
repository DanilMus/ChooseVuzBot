from app.criteria_async.vuz_name import vuz_name
from app.criteria_async.militDepartment import militDepartment
from app.criteria_async.studToTeach import studToTeach_uche, studToTeach_vuzo
from app.criteria_async.rating import rating_abro, rating_russ
from app.criteria_async.obsh import obsh
from app.criteria_async.reviews import reviews
from app.criteria_async.EGE_and_budPl import EGE_and_budPl
from app.criteria_async.vuz_url import vuz_url

from app.criteria_async.state_of_buildings import state_of_buildings
from app.criteria_async.location_of_buildings import location_of_buildings
from app.criteria_async.quality_of_education import quality_of_education
from app.criteria_async.quality_of_administration import qulity_of_administration
from app.criteria_async.additional_activities import additional_activities
from app.criteria_async.public_catering import public_catering
from app.criteria_async.price_of_lunch import price_of_lunch
from app.criteria_async.price_of_way import price_of_way


import asyncio
import logging 

logger = logging.getLogger(__name__)

# я говорю все, что хочещь знать о ВУЗе, специально для тебя
class VUZ:
    
    def __init__(self, tabi, vuzo, uche, subj):
        self.tabi = tabi
        self.vuzo = vuzo
        self.uche = uche
        self.subj = subj

        self.loop = asyncio.get_event_loop()

    def do__stt(self, stt_u, stt_v):
        if (stt_u == 0) and (stt_v == 0):
            return 0
        if stt_u == 0:
            return stt_v
        if stt_v == 0:
            return stt_u
        return round((stt_u + stt_v) / 2, 1)

    def do__of_3max(self, faculties):
        faculties_of3max = {}
        faculties_names_of3max = ['', '', '']
        EGE_of3max = [0, 0, 0]
        budPl_of3max = [0, 0, 0]

        for faculty_name, faculty_info in faculties.items():
            bal = faculty_info[0]
            bud = faculty_info[1]

            if bal > EGE_of3max[0]:
                EGE_of3max[0] = bal
                budPl_of3max[0] = bud
                faculties_names_of3max[0] = faculty_name
            elif bal > EGE_of3max[1]:
                EGE_of3max[1] = bal
                budPl_of3max[1] = bud
                faculties_names_of3max[1] = faculty_name
            elif bal > EGE_of3max[2]:
                EGE_of3max[2] = bal
                budPl_of3max[2] = bud
                faculties_names_of3max[2] = faculty_name
        
        for i in range(len(faculties_names_of3max)):
            if (faculties_names_of3max[i]) and (EGE_of3max[i]) and (budPl_of3max[i]):
                faculties_of3max[faculties_names_of3max[i]] = [EGE_of3max[i], budPl_of3max[i]]

        return faculties_of3max


    async def async_full_info(self):
        try:
            name = await vuz_name(self.vuzo)
            faculties = await EGE_and_budPl(self.vuzo, self.subj)
            militDep = await militDepartment(self.vuzo)
            stt_v = await studToTeach_vuzo(self.vuzo)
            stt_u = await studToTeach_uche(self.uche)
            rating_rus = await rating_russ(self.uche)
            rating_eng = await rating_abro(self.uche)
            obsh_ = await obsh(self.tabi)
            reviews_ = await reviews(self.tabi)
            stateOfBuildings = await state_of_buildings(self.tabi)
            locationOfBuildings = await location_of_buildings(self.tabi)
            qualityOfEducation = await quality_of_education(self.tabi)
            qualityOfAdministration = await qulity_of_administration(self.tabi)
            additionalActivities = await additional_activities(self.tabi)
            publicCatering = await public_catering(self.tabi)
            priceOfLunch = await price_of_lunch(self.tabi)
            priceOfWay = await price_of_way(self.tabi)
            vuz_url_ = await vuz_url(self.tabi)
            
        except Exception as ex:
            logger.warning(ex)
            return 'Exception'

        studToTeach = self.do__stt(stt_u, stt_v)
        faculties_of3max = self.do__of_3max(faculties)

        ans = [
            name, 
            faculties, 
            faculties_of3max, 
            militDep, 
            studToTeach, 
            rating_rus, 
            rating_eng, 
            reviews_, 
            obsh_, 
            stateOfBuildings, 
            locationOfBuildings, 
            qualityOfEducation, 
            qualityOfAdministration, 
            additionalActivities, 
            publicCatering, 
            priceOfLunch, 
            priceOfWay, 
            vuz_url_
        ]

        return ans
    
    def full_info(self):
        return self.loop.run_until_complete(self.async_full_info())
    
    async def async_EGE_and_budPl(self):
        try: 
            faculties = await EGE_and_budPl(self.vuzo, self.subj)
        except Exception as ex:
            logger.warning(ex)
            return 'Exception'

        faculties_of3max = self.do__of_3max(faculties)

        return [faculties, faculties_of3max]
    
    async def async_info_to_update_base(self):
        # try:
        militDep = await militDepartment(self.vuzo)
        stt_v = await studToTeach_vuzo(self.vuzo)
        stt_u = await studToTeach_uche(self.uche)
        rating_rus = await rating_russ(self.uche)
        rating_eng = await rating_abro(self.uche)
        obsh_ = await obsh(self.tabi)
        reviews_ = await reviews(self.tabi)
        stateOfBuildings = await state_of_buildings(self.tabi)
        locationOfBuildings = await location_of_buildings(self.tabi)
        qualityOfEducation = await quality_of_education(self.tabi)
        qualityOfAdministration = await qulity_of_administration(self.tabi)
        additionalActivities = await additional_activities(self.tabi)
        publicCatering = await public_catering(self.tabi)
        priceOfLunch = await price_of_lunch(self.tabi)
        priceOfWay = await price_of_way(self.tabi)
        vuz_url_ = await vuz_url(self.tabi)

        # except Exception as ex:
        #     logger.warning(ex)
        #     return 'Exception'
        
        studToTeach = self.do__stt(stt_u, stt_v)

        ans = [
            militDep, 
            studToTeach, 
            rating_rus, 
            rating_eng, 
            reviews_, 
            obsh_, 
            stateOfBuildings, 
            locationOfBuildings, 
            qualityOfEducation, 
            qualityOfAdministration, 
            additionalActivities, 
            publicCatering, 
            priceOfLunch, 
            priceOfWay, 
            vuz_url_
        ]

        return ans