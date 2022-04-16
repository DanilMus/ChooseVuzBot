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
        
        EGE = faculCount_whereCan
        budPl = buds
        EGE_of3max = faculCount_whereCan_of3max
        budPl_of3max = buds_of3max

        vuz_info[0] = EGE
        vuz_info[1] = budPl
        vuz_info[2] = EGE_of3max
        vuz_info[3] = budPl_of3max

        vuzes_rating[vuz_name] = [faculCount_whereCan, faculCount]
    

    # составление средних значений
    mid = [0] * len_crit
    for vuz_info in vuzes_data.values():
        for i in range(len(vuz_info)):
            mid[i] += vuz_info[i]

    len_vuzes = len(vuzes_data)
    for i in range(len(mid)):
        mid[i] /= len_vuzes
    
    EGE_mid = mid[0]
    budPl_mid = mid[1]
    EGE_of3max_mid = mid[2]
    budPl_of3max_mid = mid[3]
    militDep_mid = mid[4]
    studToTeach_mid = mid[5]
    rating_rus_mid = mid[6]
    rating_eng_mid = mid[7]
    reviews_mid = mid[8] 
    obsh_mid = mid[9]

    #  посчет рейтинга
    for vuz_name, vuz_info in vuzes_data.items(): 
        EGE, EGE_crit = vuz_info[0], criteria[1]
        budPl, budPl_crit = vuz_info[1], criteria[2]
        EGE_of3max, EGE_of3max_crit = vuz_info[2], criteria[3]
        budPl_of3max, budPl_of3max_crit = vuz_info[3], criteria[4]
        militDep,  militDep_crit = vuz_info[4], criteria[5]
        studToTeach, studToTeach_crit = vuz_info[5], criteria[6]
        rating_rus, rating_rus_crit = vuz_info[6], criteria[7]
        rating_eng, rating_eng_crit = vuz_info[7], criteria[8]
        reviews, reviews_crit = vuz_info[8], criteria[9]
        obsh, obsh_crit = vuz_info[9], criteria[10]


        score = 0

        # разделяем на:
        #   если чем больше тем лучше, то знач / ср.знач. (vuzes_data / middle)
        #   если чем меньше тем лучше, то ср.знач. / знач. (middle / vuzes_data)
        if_bigger_thanBetter = [budPl, budPl_of3max, militDep, reviews, obsh]
        if_lower_thanBetter = [EGE, EGE_of3max, studToTeach, rating_rus, rating_eng]
        if_bigger_thanBetter_mid = [budPl_mid, budPl_of3max_mid, militDep_mid, reviews_mid, obsh_mid]
        if_lower_thanBetter_mid =  [EGE_mid, EGE_of3max_mid, studToTeach_mid, rating_rus_mid, rating_eng_mid]
        if_bigger_thanBetter_crit = [budPl_crit, budPl_of3max_crit, militDep_crit, reviews_crit, obsh_crit]
        if_lower_thanBetter_crit = [EGE_crit, EGE_of3max_crit, studToTeach_crit, rating_rus_crit, rating_eng_crit]

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