def sort_dic(dictionary):
    
    new_dic = {}
    
    values = list(dictionary.values())
    values.sort(reverse=True)
    
    for value in values:
        
        for key in dictionary:
            
            if dictionary[key] == value:
                
                if key not in new_dic:
                    
                    new_dic[key] = value
                    
    return new_dic

def get_params():
    
    params = {}
    
    with open('.params.txt', 'r') as file:
        
        lines = file.readlines()

        for line in lines:
            
            split = line.split('=')
            params[split[0]] = float(split[1])
            
    return params