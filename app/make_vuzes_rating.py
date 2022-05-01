def vuzes_data_without_faculties_names(vuzes_data:dict):
    for vuz_name, vuz_info in vuzes_data.items():
        EGE_and_budPl = vuz_info[0]
        EGE_and_budPl_of3max = vuz_info[1]

        EGE = []
        budPl = []
        for val in EGE_and_budPl.values():
            EGE.append(val[0])
            budPl.append(val[1])
        
        EGE_of3max = []
        budPl_of3max = []
        for val in EGE_and_budPl_of3max.values():
            EGE_of3max.append(val[0])
            budPl_of3max.append(val[1])
        
        vuzes_data[vuz_name] = [EGE, budPl, EGE_of3max, budPl_of3max] + vuz_info[2:]

    return vuzes_data


def make_vuzes_rating(criteria:list, vuzes_data:dict):
    vuzes_rating = {}

    vuzes_data = vuzes_data_without_faculties_names(vuzes_data)

    # сначала работаем с EGE, budPl, EGE_of3max, budPl_of3ma
    for vuz_name, vuz_info in vuzes_data.items(): 
        len_crit = len(vuz_info)
        EGE, EGE_now = vuz_info[0], criteria[0]
        budPl = vuz_info[1]
        EGE_of3max = vuz_info[2]
        budPl_of3max = vuz_info[3]


        faculCount = len(EGE) # общее количество факультетов
        faculCount_whereCan = 0 # только факультеты, куда можешь поступить
        buds = 0 # количество бюджетных мест, куда можешь поступить


        for i in range(len(EGE)):
            bal = EGE[i]
            bud = budPl[i]

            if EGE_now >= (bal - 2):
                faculCount_whereCan += 1
                buds += bud
            
        faculCount_of3max = 0
        faculCount_whereCan_of3max = 0
        buds_of3max = 0
        for i in range(len(EGE_of3max)):
            bal = EGE_of3max[i]
            bud = budPl_of3max[i]

            if EGE_now >= (bal - 2):
                faculCount_of3max += 1
                faculCount_whereCan_of3max += 1
                buds_of3max += bud
        
        faculties = faculCount_whereCan
        budPl = buds
        faculties_of3max = faculCount_whereCan_of3max
        budPl_of3max = buds_of3max

        vuz_info[0] = faculties
        vuz_info[1] = budPl
        vuz_info[2] = faculties_of3max
        vuz_info[3] = budPl_of3max

        vuzes_rating[vuz_name] = [faculCount_whereCan, faculCount]
    

    # составление средних значений
    mid = [0] * (len_crit -1)
    for vuz_info in vuzes_data.values():
        for i in range(len(vuz_info) -1): # не включаем ссылку на сайт ВУЗа
            mid[i] += vuz_info[i]

    len_vuzes = len(vuzes_data)
    for i in range(len(mid)):
        mid[i] /= len_vuzes
    
    faculties_mid = mid[0]
    budPl_mid = mid[1]
    faculties_of3max_mid = mid[2]
    budPl_of3max_mid = mid[3]
    militDep_mid = mid[4]
    studToTeach_mid = mid[5]
    rating_rus_mid = mid[6]
    rating_eng_mid = mid[7]
    reviews_mid = mid[8] 
    obsh_mid = mid[9]
    stateOfBuildings_mid = mid[10]
    locationOfBuildings_mid = mid[11]
    qualityOfEducation_mid = mid[12]
    qualityOfAdministration_mid = mid[13]
    additionalActivities_mid = mid[14]
    publicCatering_mid = mid[15]
    priceOfLunch_mid = mid[16]
    priceOfWay_mid = mid[17]

    #  посчет рейтинга
    for vuz_name, vuz_info in vuzes_data.items(): 
        faculties, faculties_crit = vuz_info[0], criteria[1]
        budPl, budPl_crit = vuz_info[1], criteria[2]
        faculties_of3max, faculties_of3max_crit = vuz_info[2], criteria[3]
        budPl_of3max, budPl_of3max_crit = vuz_info[3], criteria[4]
        militDep,  militDep_crit = vuz_info[4], criteria[5]
        studToTeach, studToTeach_crit = vuz_info[5], criteria[6]
        rating_rus, rating_rus_crit = vuz_info[6], criteria[7]
        rating_eng, rating_eng_crit = vuz_info[7], criteria[8]
        reviews, reviews_crit = vuz_info[8], criteria[9]
        obsh, obsh_crit = vuz_info[9], criteria[10]
        stateOfBuildings, stateOfBuildings_crit = vuz_info[10], criteria[11]
        locationOfBuildings, locationOfBuildings_crit = vuz_info[11], criteria[12]
        qualityOfEducation, qualityOfEducation_crit = vuz_info[12], criteria[13]
        qualityOfAdministration, qualityOfAdministration_crit = vuz_info[13], criteria[14]
        additionalActivities, additionalActivities_crit = vuz_info[14], criteria[15]
        publicCatering, publicCatering_crit = vuz_info[15], criteria[16]
        priceOfLunch, priceOfLunch_crit = vuz_info[16], criteria[17]
        priceOfWay, priceOfWay_crit = vuz_info[17], criteria[18]


        score = 0

        # разделяем на:
        #   если чем больше тем лучше, то знач / ср.знач. (vuzes_data / middle)
        #   если чем меньше тем лучше, то ср.знач. / знач. (middle / vuzes_data)
        if_bigger_thanBetter = [
            faculties, 
            faculties_of3max, 
            budPl, 
            budPl_of3max, 
            militDep, 
            reviews, 
            obsh, 
            stateOfBuildings, 
            locationOfBuildings, 
            qualityOfEducation, 
            qualityOfAdministration, 
            additionalActivities, 
            publicCatering, 
        ]
        if_lower_thanBetter = [studToTeach, rating_rus, rating_eng, priceOfLunch, priceOfWay]
        if_bigger_thanBetter_mid = [
            faculties_mid, 
            faculties_of3max_mid, 
            budPl_mid, 
            budPl_of3max_mid, 
            militDep_mid, 
            reviews_mid, 
            obsh_mid, 
            stateOfBuildings_mid, 
            locationOfBuildings_mid, 
            qualityOfEducation_mid, 
            qualityOfAdministration_mid, 
            additionalActivities_mid, 
            publicCatering_mid, 
        ]
        if_lower_thanBetter_mid =  [studToTeach_mid, rating_rus_mid, rating_eng_mid, priceOfLunch_mid, priceOfWay_mid]
        if_bigger_thanBetter_crit = [
            faculties_crit, 
            faculties_of3max_crit, 
            budPl_crit, 
            budPl_of3max_crit, 
            militDep_crit, 
            reviews_crit, 
            obsh_crit, 
            stateOfBuildings_crit, 
            locationOfBuildings_crit, 
            qualityOfEducation_crit, 
            qualityOfAdministration_crit, 
            additionalActivities_crit, 
            publicCatering_crit, 
        ]
        if_lower_thanBetter_crit = [studToTeach_crit, rating_rus_crit, rating_eng_crit, priceOfLunch_crit, priceOfWay_crit]

        # если чем больше тем лучше, то знач / ср.знач. * приоритет (vuzes_data / middle) *  priority
        for i in range(len(if_bigger_thanBetter)):
            vuz_criteria = if_bigger_thanBetter[i]
            middle_criteria = if_bigger_thanBetter_mid[i]
            priority_criteria = if_bigger_thanBetter_crit[i]
            
            if middle_criteria != 0:
                score += vuz_criteria / middle_criteria * priority_criteria
        
        for i in range(len(if_lower_thanBetter)):
            vuz_criteria = if_lower_thanBetter[i]
            middle_criteria = if_lower_thanBetter_mid[i]
            priority_criteria = if_lower_thanBetter_crit[i]
            
            if vuz_criteria != 0:
                score += middle_criteria / vuz_criteria * priority_criteria

        
        vuzes_rating[vuz_name] = [score] + vuzes_rating[vuz_name]


    return vuzes_rating