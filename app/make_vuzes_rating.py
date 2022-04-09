def make_vuzes_rating(criteria:list, vuzes_data:dict):
    vuz_rating = {}

    for name, vuz_info in vuzes_data.items(): 
        EGE, EGE_crit = vuz_info[0], criteria[0]
        budPl, budPl_crit = vuz_info[1], criteria[1]
        EGE_of3max, EGE_of3max_crit = vuz_info[2], criteria[2]
        budPl_of3max, budPl_of3max_crit = vuz_info[3], criteria[1]
        militDep,  militDep_crit = vuz_info[4], criteria[3]
        studToTeach, studToTeach_crit = vuz_info[5], criteria[4]
        rating_rus, rating_rus_crit = vuz_info[6], criteria[5]
        rating_eng, rating_eng_crit = vuz_info[7], criteria[6]
        reviews, reviews_crit = vuz_info[8], criteria[7]
        obsh, obsh_crit = vuz_info[9], criteria[8]


        rating = 0

        faculCount = len(EGE) # общее количество факультетов
        faculCount_whereCan = 0 # только факультеты, куда можешь поступить
        buds = 0 # количество бюджетных мест, куда можешь поступить