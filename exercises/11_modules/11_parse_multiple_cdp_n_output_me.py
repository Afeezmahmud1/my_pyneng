from parse_cdp_nei_me import parse_cdp_neighbors

def multiple_cdp_nei(filename_list):
    multiple_dict = {}
    for filename in filename_list:
       with open (filename) as f:
           multiple_dict.update(parse_cdp_neighbors(f.read()))
    return multiple_dict

def create_unique_dict(param_dict):
    uniq_dict = {}
    dup_key_value =[]
    for dict_key in param_dict.keys():
        if dict_key in param_dict.values():
            dup_key_value.append(param_dict[dict_key])
        if dict_key not in dup_key_value:
            uniq_dict[dict_key] = param_dict[dict_key]
    return uniq_dict
if __name__ == "__main__":
    var1 = '/root/Desktop/PYNENG-FOLDER/exercises/11_modules/sh_cdp_n_r1.txt'
    var2 = '/root/Desktop/PYNENG-FOLDER/exercises/11_modules/sh_cdp_n_r2.txt'
    var3 = '/root/Desktop/PYNENG-FOLDER/exercises/11_modules/sh_cdp_n_r3.txt'
    var4 = '/root/Desktop/PYNENG-FOLDER/exercises/11_modules/sh_cdp_n_sw1.txt'
    input_list = [var1,var2,var3,var4]
    multiple_cdp_dict = multiple_cdp_nei(input_list)
    unique_cdp_out = create_unique_dict(multiple_cdp_dict)
    for item in unique_cdp_out.items():
        print(item)




