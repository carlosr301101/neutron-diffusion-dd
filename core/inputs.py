config_dict = {
    'num_regions': 1,
    'num_zones': 1,
    'NC': [100],                  
    'HR': [100],                  
    'IZL': [1],                     
    'SCT': [1.0],                   
    'SCS': [0.9],                  
    'Q': [0],                     
    'N': 4,             
    'reflex_izq': False,
    'reflex_der': False,
    'bound_left': [1,1],
    'bound_right': [0,0]        
}


config_dict_fino = {
    'num_regions': 3,
    'num_zones': 3,
    'NC': [20,60,20],                    
    'HR': [10,30,10],                  
    'IZL': [1,2,3],                     
    'SCT': [1.0,0.6,1],                   
    'SCS': [0.99,0.4,0.9],                  
    'Q': [2,0,0],                     
    'N': 4,          
    'reflex_izq': True,
    'reflex_der': False,
    'bound_left': [0,0],
    'bound_right': [0,0]               
}