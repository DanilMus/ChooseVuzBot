from app.criteria_async.AdditionalActivities import AdditionalActivities 
from app.criteria_async.Faculties import Faculties 
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
from app.handlers.start import criteria


from app.vuz import VUZ

class VUZes():
    def __init__(self, criteria, *args):
        self.criteria = criteria
        self.vuzes = args

    async def rating(self, vuz: VUZ):
        await self.mid()

        for vuz in self.vuzes:
            bal = 0

            crit = self.criteria['Хотел бы, чтобы в ВУЗе было, как можно больше факультетов, на которые ты можешь поступить?']
            if self.CountFaculties:
                bal += vuz.CountFaculties / self.CountFaculties * crit

            crit = self.criteria['Важно ли большое количество бюджетных мест?']
            if self.Buds:
                bal += vuz.AllBuds / self.AllBuds * crit

            crit = self.criteria['Хотел бы, чтобы баллы ВУЗов были приближены к твоим?']
            if self.AverageBals:
                bal += vuz.BalsCloseUserBals / self.BalsCloseUserBals * crit

            crit = self.criteria['Тебе все равно на какие специальности идти (1)? Или ты хочешь на более крутые (>2)?']
            if self.CountBestFaculties:
                bal += vuz.CountBestFaculties / self.CountBestFaculties * crit
            
            crit = self.criteria['А что насчет количества бюджетных мест для крутых специальностей?']
            if self.BestAllBuds:
                bal += vuz.BestAllBuds / self.BestAllBuds * crit

            crit = self.criteria['А чтобы баллы крутых специальностей были приближены к твоим?']
            if self.BestBalsCloseUserBals:
                bal += vuz.BestBalsCloseUserBals / self.BestBalsCloseUserBals * crit
            
            crit = self.criteria[]
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit
            
            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit
            
            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit

            crit = self.criteria['']
            if :
                bal +=  /  * crit
            
            vuz.count_bal(bal)


    
    async def mid(self, vuz: VUZ):
        self.AdditionalActivities = []
        # self.Faculties = []
        self.HostelForStudents = []
        self.LocationOfBuildings = []
        self.MilitaryDepartment = []
        self.PriceOfLunch = []
        self.PriceOfWay = []
        self.PublicCatering = []
        self.QualityOfAdministration = []
        self.QualityOfEducation = []
        self.Rating_abro = []
        self.Rating_russ = []
        self.Reviews = []
        self.StateOfBuildings = []
        self.StudentsToTeaches = []
        self.AverageBals = []
        self.AllBuds = []
        # self.BestFaculties = []
        self.BestAverageBals = []
        self.BestAllBuds = []
        self.CountFaculties = []
        self.CountBestFaculties = []
        self.BalsCloseUserBals = []
        self.BestBalsCloseUserBals = []


        for vuz in self.vuzes:
            self.AdditionalActivities.append(vuz.AdditionalActivities)
            # self.Faculties.append(vuz.Faculties)
            self.HostelForStudents.append(vuz.HostelForStudents)
            self.LocationOfBuildings.append(vuz.LocationOfBuildings)
            self.MilitaryDepartment.append(vuz.MilitaryDepartment)
            self.PriceOfLunch.append(vuz.PriceOfLunch)
            self.PriceOfWay.append(vuz.PriceOfWay)
            self.PublicCatering.append(vuz.PublicCatering)
            self.QualityOfAdministration.append(vuz.QualityOfAdministration)
            self.QualityOfEducation.append(vuz.QualityOfEducation)
            self.Rating_abro.append(vuz.Rating_abro)
            self.Rating_russ.append(vuz.Rating_russ)
            self.Reviews.append(vuz.Reviews)
            self.StateOfBuildings.append(vuz.StateOfBuildings)
            self.StudentsToTeaches.append(vuz.StudentsToTeaches)
            self.AverageBals.append(vuz.AverageBals)
            self.AllBuds.append(vuz.AllBuds)
            # self.BestFaculties.append(vuz.BestFaculties)
            self.BestAverageBals.append(vuz.BestAverageBals)
            self.BestAllBuds.append(vuz.BestAllBuds)
            self.CountFaculties.append(vuz.CountFaculties)
            self.CountBestFaculties.append(vuz.CountBestFaculties)
            self.BalsCloseUserBals.append(vuz.BalsCloseUserBals)
            self.BestBalsCloseUserBals.append(vuz.BestBalsCloseUserBals)

        
        self.AdditionalActivities = sum(self.AdditionalActivities) / len(self.AdditionalActivities)
        # self.Faculties = sum(self.Faculties) / len(self.Faculties)
        self.HostelForStudents = sum(self.HostelForStudents) / len(self.HostelForStudents)
        self.LocationOfBuildings = sum(self.LocationOfBuildings) / len(self.LocationOfBuildings)
        self.MilitaryDepartment = sum(self.MilitaryDepartment) / len(self.MilitaryDepartment)
        self.PriceOfLunch = sum(self.PriceOfLunch) / len(self.PriceOfLunch)
        self.PriceOfWay = sum(self.PriceOfWay) / len(self.PriceOfWay)
        self.PublicCatering = sum(self.PublicCatering) / len(self.PublicCatering)
        self.QualityOfAdministration = sum(self.QualityOfAdministration) / len(self.QualityOfAdministration)
        self.QualityOfEducation = sum(self.QualityOfEducation) / len(self.QualityOfEducation)
        self.Rating_abro = sum(self.Rating_abro) / len(self.Rating_abro)
        self.Rating_russ = sum(self.Rating_russ) / len(self.Rating_russ)
        self.Reviews = sum(self.Reviews) + len(self.Reviews)
        self.StateOfBuildings = sum(self.StateOfBuildings) / len(self.StateOfBuildings)
        self.StudentsToTeaches = sum(self.StudentsToTeaches) / len(self.StudentsToTeaches)
        self.Bals = sum(self.Bals) / len(self.Bals)
        self.Buds = sum(self.Buds) / len(self.Buds)
        # self.BestFaculties = sum(self.BestFaculties) / len(self.BestFaculties)
        self.BestBals = sum(self.BestBals) / len(self.BestBals)
        self.BestBuds = sum(self.BestBuds) / len(self.BestBuds)
        self.CountFaculties = sum(self.CountFaculties) / len(self.CountFaculties)
        self.CountBestFaculties = sum(self.CountBestFaculties) / len(self.CountBestFaculties)
        self.BalsCloseUserBals = sum(self.BalsCloseUserBals) / len(self.BalsCloseUserBals)
        self.BestBalsCloseUserBals = sum(self.BestBalsCloseUserBals) / len(self.BestBalsCloseUserBals)
    