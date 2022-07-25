def money_result(keys,values):
    dict_list = dict(zip(keys, values))
    print(dict_list)
    summ = 0
    for k, v in dict_list.items():
        summ += float(v)
    price_per = summ/len(keys)    
    list_res = []
    for i in range(len(values)):
        if (float(values[i]) - price_per) == 0:
            continue
        list_res.append(float(values[i]) - price_per)
    dict_list_res = dict(zip(keys, list_res))
    sorted_dict_list = sorted(dict_list_res.items(), key=lambda x: x[1], reverse=False)
    for i in range(len(sorted_dict_list)):
        sorted_dict_list[i] = list(sorted_dict_list[i])
    res = []
    while len(sorted_dict_list) > 1:        
        if sorted_dict_list[0][1] + sorted_dict_list[-1][1] > 0:
            res.append(f'{sorted_dict_list[0][0]} отправляет {abs(round(sorted_dict_list[0][1], 2))} шекелей {sorted_dict_list[-1][0]}')
            sorted_dict_list[-1][1] += sorted_dict_list[0][1]
            sorted_dict_list.pop(0)

        elif sorted_dict_list[0][1] + sorted_dict_list[-1][1] < 0:
            sorted_dict_list[0][1] += sorted_dict_list[-1][1]
            res.append(f'{sorted_dict_list[0][0]} отправляет {abs(round(sorted_dict_list[-1][1],2))} шекелей {sorted_dict_list[-1][0]}')
            sorted_dict_list.pop(-1)
        elif sorted_dict_list[0][1] + sorted_dict_list[-1][1] == 0 :
            res.append(f'{sorted_dict_list[0][0]} отправляет {abs(round(sorted_dict_list[0][1], 2))} шекелей {sorted_dict_list[-1][0]}')
            sorted_dict_list[0][1] += sorted_dict_list[-1][1]
            sorted_dict_list.pop(-1)
            sorted_dict_list.pop(0)
    result = ""
    for i in res:
        result += (i +'\n')
    return result 

