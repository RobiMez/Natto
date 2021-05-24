import concurrent.futures
import time

def cum(viscousity):
    print('owo ',viscousity)
    time.sleep(viscousity)
    print('hiyaaah ',viscousity)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(cum,[1,2,3,4,5,6,7,8,9])