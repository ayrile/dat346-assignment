import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
from math import pi

def sample_pi(n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    random.seed()
    print("Hello from a worker")
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s


def compute_pi(args):
    random.seed(1)
    n = int(args.steps / args.workers)
    
    p = multiprocessing.Pool(args.workers)
    s = p.map(sample_pi, [n]*args.workers)

    n_total = n*args.workers
    s_total = sum(s)
    pi_est = (4.0*s_total)/n_total
    print(" Steps\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, pi-pi_est))

import time

used_time = []
speedup = []
f = []
s_total = []

if __name__ == "__main__":
    for corenum in ['1','2','4','8','16','32']:
        start = time.process_time()
        parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')
        parser.add_argument('--workers', '-w',
                            default=corenum,
                            type = int,
                            help='Number of parallel processes')
        parser.add_argument('--steps', '-s',
                            default='1000',
                            type = int,
                            help='Number of steps in the Monte Carlo simulation')
        args = parser.parse_args()
        compute_pi(args)
        end = time.process_time()
        duration = end - start
        used_time.append(duration)

        speed = used_time[0]/duration
        speedup.append(speed)

        prop = (used_time[0]-duration) / duration
        f.append(prop) 

        s = 1 / ((1-prop) + prop/speed)
        s_total.append(s)
        
        # if used_time != NULL:
        #     used_time.append(used_time[0]/duration)
        # else：
        #     used_time.append(duration)
        print("Time used:", used_time) 
        print("Speedup:", speedup)
        print("f", f)
        print("s total:", s_total)



