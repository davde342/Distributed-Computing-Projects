#!/usr/bin/env python3

import argparse
import csv
import collections
import logging
from random import expovariate, sample, seed

import pandas as pd
import matplotlib.pyplot as plt

from discrete_event_sim import Simulation, Event


CSV_COLUMNS = ['lambd', 'mu', 'max_t', 'n', 'd', 'w']



class Queues(Simulation):
    """Simulation of a system with n servers and n queues. """



    def __init__(self, lambd, mu, n, d, max_t):


        super().__init__()

        self.running = [None] * n  # if not None, the id of the running job (per queue)
  
        self.time = {} 
      
        self.queues = [collections.deque() for _ in range(n)]  # FIFO queues of the system
        
        # NOTE: we don't keep the running jobs in self.queues

        self.arrivals = {}  # dictionary mapping job id to arrival time
        self.completions = {}  # dictionary mapping job id to completion time
        self.lambd = lambd
        self.n = n
        self.d = d
        self.mu = mu
        self.max_t = max_t
        
        self.arrival_rate = lambd * n  # frequency of new jobs is proportional to the number of queues
        self.schedule(expovariate(lambd), Arrival(0))  # schedule the first arrival
        self.schedule(0, Monitor(1))

    def schedule_arrival(self, job_id):
        """Schedule the arrival of a new job."""

        # schedule the arrival following an exponential distribution, to compensate the number of queues the arrival
        # time should depend also on "n"

        # memoryless behavior results in exponentially distributed times between arrivals (we use `expovariate`)
        # the rate of arrivals is proportional to the number of queues

        self.schedule(expovariate(self.arrival_rate), Arrival(job_id))

    def schedule_completion(self, job_id, queue_index):  # TODO: complete this method
        """Schedule the completion of a job."""
        
        # schedule the time of the completion event
        
        self.schedule(expovariate(self.mu), Completion(job_id, queue_index))

    def queue_len(self, i):
        """Return the length of the i-th queue."""

        return (self.running[i] is not None) + len(self.queues[i])


class Arrival(Event):
    """Event representing the arrival of a new job."""

    def __init__(self, job_id):
        self.id = job_id

    def process(self, sim: Queues):  # TODO: complete this method
        sim.arrivals[self.id] = sim.t  # set the arrival time of the job
        sample_queues = sample(range(sim.n), sim.d)  # sample the id of d queues at random
        queue_index = min(sample_queues, key=sim.queue_len)  # shortest queue among the sampled ones

        # implement the following logic:
        if sim.running[queue_index] is not None: # if there are running job in the queue:
            sim.queues[queue_index].append(self.id)# put the job into the queue
        else:
            sim.running[queue_index] = self.id # otherwise, set the incoming one
            sim.schedule_completion(self.id, queue_index)  # schedule its completion
        sim.schedule_arrival(self.id+1)  # schedule the arrival of the next job

class Completion(Event):
    """Job completion."""

    def __init__(self, job_id, queue_index):
        self.job_id = job_id  # currently unused, might be useful when extending
        self.queue_index = queue_index

    def process(self, sim: Queues):
        queue_index = self.queue_index
        assert sim.running[queue_index] == self.job_id  # the job must be the one running
        sim.completions[self.job_id] = sim.t
        queue = sim.queues[queue_index]
        if queue:  # queue is not empty
            sim.running[queue_index] = new_job_id = queue.popleft()  # assign the first job in the queue
            sim.schedule_completion(new_job_id, queue_index)  # schedule its completion
        else:
            sim.running[queue_index] = None  # no job is running on the queue

class Monitor(Event):

    def __init__(self, interval=5):
        self.interval = interval

    def process(self, sim):
        for x in range(0, sim.n):
            if ( sim.queue_len(x)  in sim.time):
                sim.time[ sim.queue_len(x) ] += 1
            else :
                sim.time[ sim.queue_len(x)  ] = 1
            
        tot = 0
        list_key = list(sim.time.keys())
        list_key.sort(reverse = True)

        for x in sim.time.keys():
            tot += sim.time[x]
        
        for x in sim.time.keys():
            sim.time[x] = sim.time[x]/tot

        for x in range(1, len(list_key)):
            sim.time[list_key[x]] += sim.time[list_key[x-1]]
        sim.schedule(self.interval, self)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--lambd', type=float, default=0.99, help="arrival rate")
    parser.add_argument('--mu', type=float, default=1, help="service rate")
    parser.add_argument('--max-t', type=float, default=1_000_000, help="maximum time to run the simulation")
    parser.add_argument('--n', type=int, default=10, help="number of servers")
    parser.add_argument('--d', type=int, default=5, help="number of queues to sample")
    parser.add_argument('--csv', help="CSV file in which to store results")
    parser.add_argument('--csv_ql', help="CSV file in which to store results")
    parser.add_argument("--seed", help="random seed")
    parser.add_argument("--verbose", action='store_true')
    args = parser.parse_args()

    params = [getattr(args, column) for column in CSV_COLUMNS[:-1]]

    #check if lambd, mu, max-t n and d are all positive
    if any(x <= 0 for x in params):
        logging.error("lambd, mu, max-t, n and d must all be positive")
        exit(1)

    if args.seed:
        seed(args.seed)  # set a seed to make experiments repeatable
    if args.verbose:
        # output info on stderr
        logging.basicConfig(format='{levelname}:{message}', level=logging.INFO, style='{')

    if args.lambd >= args.mu:
        logging.warning("The system is unstable: lambda >= mu")

    sim = Queues(args.lambd, args.mu, args.n, args.d, args.max_t)
    sim.run(args.max_t)

    completions = sim.completions
    W = ((sum(completions.values()) - sum(sim.arrivals[job_id] for job_id in completions)) / len(completions))
    print(f"Average time spent in the system: {W}")
    if args.mu == 1 and args.lambd != 1:
        print(f"Theoretical expectation for random server choice (d = 1): {1 / (1 - args.lambd)}")

    if args.csv is not None:
        with open(args.csv, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(params + [W])
            f.close()

    if args.csv_ql is not None:
        with open(args.csv_ql, mode='a', newline='') as file:
            writer = csv.writer(file)
            for key, value in sim.time.items():
                writer.writerow([sim.d, sim.lambd, value, key])
            
if __name__ == '__main__':
    main()
