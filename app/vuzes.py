from math import ceil
from app.vuz import VUZ


class VUZes:
    def __init__(self, criteria, args):
        self.criteria = criteria
        self.vuzes = args

    
    @property
    def texts_top(self):
        top = self.top
        num_pages = ceil(len(top) / 10)

        texts_top = []

        for i in range(num_pages):
            text = ''
            if i != num_pages - 1:
                end = 10*(i+1)
            else:
                end = len(top)

            for j in range(10*i, end):
                vuz = top[j]
                text += f'{j+1} место: <a href= "{vuz.url}">{vuz.name}</a> набрал {round(vuz.rating)} points\n'
            
            texts_top.append(text)
        
        return texts_top

    @property
    def texts_top_MoreInfo(self):
        top = self.top

        texts_top = []

        for i in range(len(top)):
            vuz = top[i]
            text = ''
            text += f'<b>{i+1}. <a href= "{vuz.url}">{vuz.name}</a></b>\n\n'


            text += f'<b>Факультеты (их баллы и бюджетные места): </b>\n'

            for subj, info in vuz.Faculties.items():
                subjects = ' '.join(subj.split('_'))
                text += f'{subjects}: \n'
                for faculty, bals_buds in info.items():
                    text += f'{faculty}: {bals_buds[0]} {bals_buds[1]} \n'
            
            text += f'\n'


            text += f'<b>Крутые факультеты (их баллы и бюджетные места): </b>\n'

            for subj, info in vuz.BestFaculties.items():
                subjects = ' '.join(subj.split('_'))
                text += f'{subjects}: \n'
                for faculty, bals_buds in info.items():
                    text += f'{faculty}: {bals_buds[0]} {bals_buds[1]} \n'
            
            text += f'\n'


            army = vuz.MilitaryDepartment
            if army:
                army = 'есть'
            else:
                army = 'нет'

            text += f'<b>Военная кафедра: </b>{army} \n'


            text += f'<b>Количество учеников на одного преподавателя:  </b>{round(vuz.StudentsToTeaches)} \n'


            text += f'<b>Российский рейтинг: </b>{vuz.Rating_russ} \n'


            text += f'<b>Зарубежный рейтинг: </b>{vuz.Rating_abro} \n'


            text += f'<b>Отзывы о ВУЗе: </b>{vuz.Reviews} \n'


            text += f'<b>Оценка общежития: </b>{vuz.HostelForStudents} \n'


            text += f'<b>Состояния корпусов: </b>{vuz.StateOfBuildings} \n'


            text += f'<b>Удобство их расположения: </b>{vuz.LocationOfBuildings} \n'


            text += f'<b>Качество образования: </b>{vuz.QualityOfEducation} \n'


            text += f'<b>Качество работы административного аппарата: </b>{vuz.QualityOfAdministration} \n'


            text += f'<b>Дополнительные активности: </b>{vuz.AdditionalActivities} \n'


            text += f'<b>Качество еды в столовой: </b>{vuz.PublicCatering} \n'


            text += f'<b>Средняя цена обеда: </b>{vuz.PriceOfLunch} \n'


            text += f'<b>Средние затраты на дорогу в месяц: </b>{vuz.PriceOfWay} \n'


            texts_top.append(text)



        return texts_top

    def make_top(self):
        top = []

        vuzes = self.vuzes[:]

        while vuzes:
            max_bal = 0
            for i in range(len(vuzes)):
                bal = vuzes[i].rating
                if bal > max_bal:
                    max_bal = bal
                    remem_i = i

            vuz = vuzes.pop(remem_i)
            top.append(vuz)
            
        self.top = top
            

    def rating(self):
        self.__mid()

        for vuz in self.vuzes:
            bal = 0

            crit = self.criteria['Хотел бы, чтобы в ВУЗе было, как можно больше факультетов, на которые ты можешь поступить?']
            if self.CountFaculties:
                bal += vuz.CountFaculties / self.CountFaculties * crit

            crit = self.criteria['Важно ли большое количество бюджетных мест на факультеты, на которые ты можешь поступить?']
            if self.BudsWhereUserCan:
                bal += vuz.BudsWhereUserCan / self.BudsWhereUserCan * crit

            crit = self.criteria['Хотел бы, чтобы баллы факультов были приближены к твоим?']
            if self.BalsCloseUserBals:
                bal += vuz.BalsCloseUserBals / self.BalsCloseUserBals * crit

            crit = self.criteria['Тебе все равно на какие специальности идти (1)? Или ты хочешь на более крутые (>2)?']
            if self.CountBestFaculties:
                bal += vuz.CountBestFaculties / self.CountBestFaculties * crit
            
            crit = self.criteria['А что насчет количества бюджетных мест для крутых специальностей?']
            if self.BestBudsWhereUserCan:
                bal += vuz.BestBudsWhereUserCan / self.BestBudsWhereUserCan * crit

            crit = self.criteria['А чтобы баллы крутых специальностей были приближены к твоим?']
            if self.BestBalsCloseUserBals:
                bal += vuz.BestBalsCloseUserBals / self.BestBalsCloseUserBals * crit
            
            crit = self.criteria['Поговорим об армии. Насколько тебе нужна военная кафедра?']
            if self.MilitaryDepartment:
                bal += vuz.MilitaryDepartment / self.MilitaryDepartment * crit

            crit = self.criteria['Важно ли тебе, чтобы преподаватель уделял тебе время чаще? (Посмотрим сколько студентов приходится на одного учителя.)']
            if self.StudentsToTeaches:
                bal += vuz.StudentsToTeaches / self.StudentsToTeaches * crit

            crit = self.criteria['Есть также российские рейтинги ВУЗов. Важны ли тебе они?']
            if vuz.Rating_russ:
                bal += self.Rating_russ / vuz.Rating_russ * crit
            
            crit = self.criteria['А что насчет зарубежного рейтинга?\n(QS World University Rankings)']
            if vuz.Rating_abro:
                bal += self.Rating_abro / vuz.Rating_abro * crit

            crit = self.criteria['Ценны ли тебе отзывы об этом ВУЗе?']
            if self.Reviews:
                bal += vuz.Reviews / self.Reviews * crit

            crit = self.criteria['Насколько общежитие имеет значение?']
            if self.HostelForStudents:
                bal += vuz.HostelForStudents / self.HostelForStudents * crit
            
            crit = self.criteria['Важно ли тебе состояние корпусов ВУЗа?']
            if self.StateOfBuildings:
                bal += vuz.StateOfBuildings / self.StateOfBuildings * crit

            crit = self.criteria['А что насчет удобства их расположения?']
            if self.LocationOfBuildings:
                bal += vuz.LocationOfBuildings / self.LocationOfBuildings * crit

            crit = self.criteria['Качество образования?']
            if self.QualityOfEducation:
                bal += vuz.QualityOfEducation / self.QualityOfEducation * crit

            crit = self.criteria['Качество работы административного аппарата?']
            if self.QualityOfAdministration:
                bal += vuz.QualityOfAdministration / self.QualityOfAdministration * crit

            crit = self.criteria['Нужны ли дополнительные активности в ВУЗе?']
            if self.AdditionalActivities:
                bal += vuz.AdditionalActivities / self.AdditionalActivities * crit

            crit = self.criteria['Важно ли как кормят?']
            if self.PublicCatering:
                bal += vuz.PublicCatering / self.PublicCatering * crit

            crit = self.criteria['Хотел бы меньше денег тратить в столовой?']
            if vuz.PriceOfLunch:
                bal += self.PriceOfLunch / vuz.PriceOfLunch * crit

            crit = self.criteria['А меньше тратить на дорогу?']
            if vuz.PriceOfWay:
                bal += self.PriceOfWay / vuz.PriceOfWay * crit
            
            vuz.count_rating(bal)


    
    def __mid(self):
        AdditionalActivities = []
        HostelForStudents = []
        LocationOfBuildings = []
        MilitaryDepartment = []
        PriceOfLunch = []

        PriceOfWay = []
        PublicCatering = []
        QualityOfAdministration = []
        QualityOfEducation = []
        Rating_abro = []
        Rating_russ = []

        Reviews = []
        StateOfBuildings = []
        StudentsToTeaches = []
        BudsWhereUserCan = []

        BestBudsWhereUserCan = []
        CountFaculties = []
        CountBestFaculties = []
        BalsCloseUserBals = []
        BestBalsCloseUserBals = []


        for vuz in self.vuzes:
            AdditionalActivities.append(vuz.AdditionalActivities)
            HostelForStudents.append(vuz.HostelForStudents)
            LocationOfBuildings.append(vuz.LocationOfBuildings)
            MilitaryDepartment.append(vuz.MilitaryDepartment)
            PriceOfLunch.append(vuz.PriceOfLunch)

            PriceOfWay.append(vuz.PriceOfWay)
            PublicCatering.append(vuz.PublicCatering)
            QualityOfAdministration.append(vuz.QualityOfAdministration)
            QualityOfEducation.append(vuz.QualityOfEducation)
            Rating_abro.append(vuz.Rating_abro)
            Rating_russ.append(vuz.Rating_russ)

            Reviews.append(vuz.Reviews)
            StateOfBuildings.append(vuz.StateOfBuildings)
            StudentsToTeaches.append(vuz.StudentsToTeaches)
            BudsWhereUserCan.append(vuz.BudsWhereUserCan)

            BestBudsWhereUserCan.append(vuz.BestBudsWhereUserCan)
            CountFaculties.append(vuz.CountFaculties)
            CountBestFaculties.append(vuz.CountBestFaculties)
            BalsCloseUserBals.append(vuz.BalsCloseUserBals)
            BestBalsCloseUserBals.append(vuz.BestBalsCloseUserBals)

        
        self.AdditionalActivities = sum(AdditionalActivities) / len(AdditionalActivities)
        self.HostelForStudents = sum(HostelForStudents) / len(HostelForStudents)
        self.LocationOfBuildings = sum(LocationOfBuildings) / len(LocationOfBuildings)
        self.MilitaryDepartment = sum(MilitaryDepartment) / len(MilitaryDepartment)
        self.PriceOfLunch = sum(PriceOfLunch) / len(PriceOfLunch)

        self.PriceOfWay = sum(PriceOfWay) / len(PriceOfWay)
        self.PublicCatering = sum(PublicCatering) / len(PublicCatering)
        self.QualityOfAdministration = sum(QualityOfAdministration) / len(QualityOfAdministration)
        self.QualityOfEducation = sum(QualityOfEducation) / len(QualityOfEducation)
        self.Rating_abro = sum(Rating_abro) / len(Rating_abro)
        self.Rating_russ = sum(Rating_russ) / len(Rating_russ)

        self.Reviews = sum(Reviews) + len(Reviews)
        self.StateOfBuildings = sum(StateOfBuildings) / len(StateOfBuildings)
        self.StudentsToTeaches = sum(StudentsToTeaches) / len(StudentsToTeaches)
        self.BudsWhereUserCan = sum(BudsWhereUserCan) / len(BudsWhereUserCan)

        self.BestBudsWhereUserCan = sum(BestBudsWhereUserCan) / len(BestBudsWhereUserCan)
        self.CountFaculties = sum(CountFaculties) / len(CountFaculties)
        self.CountBestFaculties = sum(CountBestFaculties) / len(CountBestFaculties)
        self.BalsCloseUserBals = sum(BalsCloseUserBals) / len(BalsCloseUserBals)
        self.BestBalsCloseUserBals = sum(BestBalsCloseUserBals) / len(BestBalsCloseUserBals)
    
