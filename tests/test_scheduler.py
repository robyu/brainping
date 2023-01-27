import sys
sys.path.insert(0, './tests')
sys.path.insert(0, './src')

import unittest
import scheduler
from  datetime import datetime

class TestScheduler(unittest.TestCase):
    def test_midnight_epoch_is_midnight(self):
        num_pings = 10
        s = scheduler.Scheduler(start_time_str="08:00:00",
                                stop_time_str="18:00:00",
                                num_pings = num_pings)
        
        #
        # convert back to datetime obj
        midnight_dt = datetime.fromtimestamp(s.midnight_sec)

        # make sure that midnight_dt corresponds to today's date + midnight
        now_dt = datetime.now()
        self.assertTrue(midnight_dt.year==now_dt.year)
        self.assertTrue(midnight_dt.month==now_dt.month)
        self.assertTrue(midnight_dt.day==now_dt.day)

        self.assertTrue(midnight_dt.hour==0)
        self.assertTrue(midnight_dt.minute==0)
        self.assertTrue(midnight_dt.second==0)

    def test_ping_schedule_within_interval(self):
        test_date_str = "2023-01-21"
        num_pings = 10
        start_time_str = "08:00:00"
        stop_time_str = "18:00:00"

        s = scheduler.Scheduler(start_time_str=start_time_str,
                                stop_time_str=stop_time_str,
                                num_pings = num_pings,
                                test_date_str = test_date_str)
        schedule_l = s.get_schedule(as_datetime=True)
        
        #
        # convert test parameters into datetime obj
        test_date_dt = datetime.strptime(test_date_str, "%Y-%m-%d")
        start_dt = s._synthesize_datetime_obj(test_date_dt, start_time_str)
        stop_dt = s._synthesize_datetime_obj(test_date_dt, stop_time_str)
        
        print(test_date_dt.date())
        for s_dt in schedule_l:
            print(f"{s_dt}")
            #
            # schedule entry's date matches the test date
            self.assertTrue(s_dt.date() == test_date_dt.date())

            # schedule falls within start-stop interval
            self.assertTrue(start_dt <= s_dt)
            self.assertTrue(s_dt <= stop_dt)
        #

    def test_ping_schedule_monotonic(self):
        test_date_str = "2023-01-21"
        num_pings = 10
        start_time_str = "08:00:00"
        stop_time_str = "20:00:00"

        s = scheduler.Scheduler(start_time_str=start_time_str,
                                stop_time_str=stop_time_str,
                                num_pings = num_pings,
                                test_date_str = test_date_str)
        schedule_l = s.get_schedule(as_datetime=True)
        
        prev_dt = schedule_l[0]
        for n in range(1, len(schedule_l)):
            print(f"{n:2}: {schedule_l[n]}")
            self.assertTrue(schedule_l[n] > prev_dt)
            prev_dt = schedule_l[n]
        #
        
        
        
        
        

            
