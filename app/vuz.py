from app.criteria_async.AdditionalActivities import AdditionalActivities 
from app.criteria_async.Faculties import Faculties 
from app.criteria_async.GTO_GoldMedal import GTO_GoldMedal
from app.criteria_async.HostelForStudents import HostelForStudents 
from app.criteria_async.LocationOfBuildings import LocationOfBuildings
from app.criteria_async.MilitaryDepartment import MilitaryDepartment 
from app.criteria_async.PriceOfLunch import PriceOfLunch 
from app.criteria_async.PriceOfWay import PriceOfWay 
from app.criteria_async.PublicCatering import PublicCatering 
from app.criteria_async.QualityOfAdministration import QualityOfAdministration 
from app.criteria_async.QualityOfEducation import QualityOfEducation 
from app.criteria_async.Rating import Rating_abro, Rating_russ 
from app.criteria_async.Reviews import Reviews 
from app.criteria_async.StateOfBuildings import StateOfBuildings 
from app.criteria_async.StudentsToTeaches import StudentsToTeaches
from app.criteria_async.VuzName import VuzName
from app.criteria_async.VuzUrl import VuzUrl

import logging

logger = logging.getLogger(__name__)

class VUZ:
    def __init__(self, tabi, vuzo, uche, subjects_bals: dict, GTO_GoldMedal):
        self.tabi = tabi
        self.vuzo = vuzo
        self.uche = uche 
        self.subj_ege = subjects_bals
        self.subj_ege['Вступительные'] = 0
        self.subj = subjects_bals.keys()
        self.ege = sum(subjects_bals.values())
        self.rating = 0
        self.GTO_GoldMedal = GTO_GoldMedal
    


    async def start(self):
        # for i in range(3):
        #     try:
        self.name = await VuzName(self.vuzo)
        self.url = await VuzUrl(self.tabi)

        self.AdditionalActivities = await AdditionalActivities(self.tabi)
        self.Faculties = await Faculties(self.vuzo, self.subj)
        self.GTO, self.GoldMedal = await GTO_GoldMedal(self.vuzo)
        self.HostelForStudents = await HostelForStudents(self.tabi)
        self.LocationOfBuildings = await LocationOfBuildings(self.tabi)
        self.MilitaryDepartment = await MilitaryDepartment(self.vuzo)
        self.PriceOfLunch = await PriceOfLunch(self.tabi)
        self.PriceOfWay = await PriceOfWay(self.tabi)
        self.PublicCatering = await PublicCatering(self.tabi)
        self.QualityOfAdministration = await QualityOfAdministration(self.tabi)
        self.QualityOfEducation = await QualityOfEducation(self.tabi)
        self.Rating_abro = await Rating_abro(self.uche)
        self.Rating_russ = await Rating_russ(self.uche)
        self.Reviews = await Reviews(self.tabi)
        self.StateOfBuildings = await StateOfBuildings(self.tabi)
        self.StudentsToTeaches = await StudentsToTeaches(self.vuzo, self.uche)
    
        await self.__count_ege_for_subj()

        self.Bals = await self. __bals(self.Faculties)
        self.BudsWhereUserCan = await self.__buds_where_user_can(self.Faculties)
        self.CountFaculties = await self. __count_faculties(self.Bals)
        self.BalsCloseUserBals = await self. __bals_close_user_bals(self.Bals)

        self.BestFaculties = await self. __best_faculties()

        self.BestBals = await self. __bals(self.BestFaculties)
        self.BestBudsWhereUserCan = await self.__buds_where_user_can(self.BestFaculties)
        self.CountBestFaculties = await self. __count_faculties(self.BestBals)
        self.BestBalsCloseUserBals = await self. __bals_close_user_bals(self.BestBals)

            #     return 'ok'

            # except Exception as ex:
            #     logger.warning(ex)
            #     return Exception

    def count_rating(self, n: int):
        self.rating += n

    @property
    def urls(self):
        ans = {
            'tabi': self.tabi,
            'vuzo': self.vuzo,
            'uche': self.uche
        }
        return ans







    async def __count_ege_for_subj(self):
        ans = {}

        for subj in self.Faculties.keys():
            ege = 0
            if 'GTO' in self.GTO_GoldMedal:
                ege += self.GTO 
            if 'GoldMedal' in self.GTO_GoldMedal:
                ege += self.GoldMedal

            subjects = subj.split('_')
            for subject in subjects:
                ege += self.subj_ege[subject]
            
            ans[subj] = ege
        
        self.subj_ege = ans

    
    async def __bals(self, faculties: dict):
        ans = {}
        
        for subj in faculties.keys():
            help = []
            for name, info in faculties[subj].items():
                help.append(info[0])
            
            ans[subj] = help

        return ans
    
    
    async def  __buds_where_user_can(self, faculties: dict):
        ans = []
        for subj, info_ in faculties.items():
            ege = self.subj_ege[subj]
            for info in info_.values():
                if ege > info[0]:
                    ans.append(info[1])
        
        ans = sum(ans)

        return ans
    
    async def  __best_faculties(self):
        def find_max(faculties: dict, last_maxes: list, subj: str):
            help1, help2, help3 = '', 0, 0

            for name, info in faculties[subj].items():
                bal, bud = info[0], info[1]

                if (bal > help2) and (name not in last_maxes):
                    help1, help2, help3 = name, bal, bud
        
            return help1, help2, help3
        
        subjects = self.Faculties.keys()

        ans = {}
        for subj in subjects:
            ans[subj] = {}

        for i in range(3):
            for subj in subjects:
                help = find_max(self.Faculties, ans[subj].keys(), subj)
                if help[0]:
                    ans[subj][help[0]] = [help[1], help[2]]
            
        return ans
    
    async def  __count_faculties(self, bals: dict):
        count = 0

        for subj, info in bals.items():
            ege = self.subj_ege[subj]
            
            for bal in info:
                if ege > bal:
                    count += 1

        return count

    async def  __bals_close_user_bals(self, bals: dict):
        ans = {}

        for subj, info in bals.items():
            ans[subj] = []
            ege = self.subj_ege[subj]
            max_bal = (len(subj.split('_'))*100 + 10)
            for bal in info:
                ans[subj].append(max_bal - abs(bal - ege))
        
        ans_ = []

        for subj, info in ans.items():
            ans_ += info[:]
        
        if ans_:
            ans_ = sum(ans_) / len(ans_)
        else:
            ans_ = 0

        return ans_