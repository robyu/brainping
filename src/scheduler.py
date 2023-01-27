import sys
from datetime import datetime 
import random
import numpy as np
# from numpy.random import MT19937
# from numpy.random import RandomState, SeedSequence
from numpy import random

class Scheduler():
    def __init__(self, start_time_str = "08:00:00", stop_time_str ="20:00:00", num_pings = 10, test_date_str=None):
        """
        test_date_str = baseline date for testing (rather than actual date)--basically rand seed; format is "YYYY-MM-DD"
        """
        if test_date_str==None:
            now_dt = datetime.now()
        else:
            now_dt = datetime.strptime(test_date_str, "%Y-%m-%d")
        #

        self.midnight_sec = self._synthesize_datetime_obj(now_dt, "00:00:00").timestamp()
        self.start_sec = self._synthesize_datetime_obj(now_dt, start_time_str).timestamp()
        self.stop_sec = self._synthesize_datetime_obj(now_dt, stop_time_str).timestamp()
        self.num_pings = num_pings
        self.min_interval_sec = 60

        randseed = int(datetime.timestamp(now_dt))
        self.ping_sec_list = self._generate_ping_schedule(randseed, num_pings)

    def get_schedule(self, as_datetime=False):
        """
        return list of ping times
        as_datetime: False = return as epoch seconds
                     True = return as datetime objects
        """
        if as_datetime==False:
            retval =  self.ping_sec_list
        else:
            retval = [datetime.fromtimestamp(s) for s in self.ping_sec_list]
        #
        return retval
        
    def _generate_ping_schedule(self, randseed, num_pings):
        #
        # ridiculous code to seed and create a random num generator
        # see https://numpy.org/doc/stable/reference/random/generated/numpy.random.RandomState.seed.html#numpy.random.RandomState.seed
        rs = random.RandomState(random.MT19937(random.SeedSequence(randseed)))
        
        delta_sec = self.stop_sec - self.start_sec
        assert delta_sec > 0

        rand_limit = int(delta_sec / self.min_interval_sec)
        assert rand_limit > 0

        vals = rs.randint(0, high=rand_limit,size=num_pings)

        ping_sec_l = [self.start_sec + (v * self.min_interval_sec) for v in vals]
        ping_sec_l.sort()

        return ping_sec_l

    def _synthesize_datetime_obj(self, now_dt, time_str):
        """
        take the date from now_dt (datetime) and a  time string of format "HH:mm:ss",
        return a datetime object
        """
        #
        # "synthesize" a midnight datetime object from today's date + "00:00:00"
        new_dt = datetime.combine(now_dt, datetime.strptime(time_str, "%H:%M:%S").time())
        return new_dt

    

        

