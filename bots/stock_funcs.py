from random import random
from math import tan
from math import pi
from dotenv import load_dotenv
import os

def get_factor(x:float):
    """Calculates the factor to multiply the current price with based on a seed.

    Args:
        x (float): seed (NOTE: The seed should be in [0.5, 1].)

    Returns:
        float: The calculated factor > 0.
    """
    load_dotenv()
    return (tan(pi*x + pi/2) + 1)**(1/int(os.getenv('STOCK_STABILITY')))

def stock_update(current_price:float):
    """Updates the price of a stock.

    Args:
        current_price (float): The current price of the stock which is to be updated.

    Returns:
        float: The new price of the stock
    """
    factor_seed = random()
    
    if factor_seed >= 0.5:
        
        factor = get_factor(factor_seed)
        
    else:
        
        factor = 1/get_factor(-factor_seed)
    
    new_price = current_price * factor
    
    return new_price
