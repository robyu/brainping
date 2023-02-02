import json
import argparse
import sender
import scheduler
from datetime import datetime
from pathlib import Path
import time

def parse_args():
    parser = argparse.ArgumentParser(description="""
""", formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument("config_fname", help="fname of config json file")
    parser.add_argument("email_pwd_fname", help="fname of file containing email server password")
    parser.add_argument("-s", "--send-startup-msg", action="store_true", default=False, help="send a message upon init")
    #
    # debug options
    parser.add_argument("-t", "--today-date-str", default="", help="""date string used in place of "now"; YYYY-mm-dd string""")
    parser.add_argument("--debug-fast-fwd", default=False, action="store_true", help="""increment rapidly through time (instead of real time)""")
    args = parser.parse_args()

    return args

class BrainPing:
    def __init__(self, email_user,
                 email_pwd_fname,
                 email_dest,
                 start_time_str,
                 stop_time_str,
                 num_pings,
                 today_date_str='',
                 startup_msg_flag=False,
                 fast_fwd_flag=False):
                 
        self.sender = sender.Sender(email_user = email_user,
                                    email_pwd_fname = email_pwd_fname)
        self.email_dest = email_dest

        if len(today_date_str) <= 0:
            self.today_dt = datetime.now()
        else:
            self.today_dt = datetime.strptime(today_date_str, "%Y-%m-%d")
        #
        
        self.start_time_dt = self._combine_date_time(self.today_dt, start_time_str)
        self.stop_time_dt = self._combine_date_time(self.today_dt, stop_time_str)
        self.num_pings = num_pings
        self.dest_addr = email_dest
        
        s = scheduler.Scheduler(start_time_str = str(self.start_time_dt.time()),
                                stop_time_str = str(self.stop_time_dt.time()),
                                num_pings = self.num_pings,
                                today_date_str = today_date_str)
        self.schedule_sec_l = s.get_schedule()
        print(self.schedule_sec_l)
        if startup_msg_flag:
            self._send_startup_msg()
        #
        self.debug_fast_fwd_flag = fast_fwd_flag

    def _combine_date_time(self, dt, time_str):
        new_dt = datetime.combine(dt.date(), dt.strptime(time_str, "%H:%M:%S").time())
        return new_dt

    def _send_startup_msg(self):
        subject = "brainping startup"
        msg = f"""
        start time: {self.start_time_dt.time() }
        stop time: {self.stop_time_dt.time() }
        num pings: {self.num_pings}
        today's date: {self.today_dt.date() }"""
        self.sender.send(self.email_dest, subject, msg)

    def get_schedule(self, as_timedate_flag=True):
        s = ''
        for n, sec in enumerate(self.schedule_sec_l):
            if as_timedate_flag:
                dt = datetime.fromtimestamp(sec)
                s += f"{n:2} {str(dt)}\n"
            else:
                s += f"{n:2} {sec}\n"
            #
        #
        return s


    def run_one_day(self):
        if self.debug_fast_fwd_flag:
            now_dt = self.today_dt
        else:
            now_dt = datetime.now()
        #
        print("ping schedule:")
        print(self.get_schedule(as_timedate_flag=True))

        print(f"starting time {now_dt}")
        while self.stop_time_dt.time() >  now_dt.time() and len(self.schedule_sec_l) > 0:
            print(now_dt, end='')
            sched0_sec = self.schedule_sec_l[0]
            if now_dt.timestamp() >= sched0_sec:

                # send ping
                # say self.num_pings = 6
                # say len(schedule_sec_l) = 6
                # then index = 6 - 6 + 1
                ping_index = self.num_pings - len(self.schedule_sec_l) + 1
                self.schedule_sec_l.pop(0)
                msg = f"""
#brainping
ping ({ping_index} / {self.num_pings}) @ {datetime.fromtimestamp(sched0_sec)}"""

                print(f" <---- PING: {ping_index} / {self.num_pings} @ {datetime.fromtimestamp(sched0_sec)}")
                self.sender.send(self.email_dest,
                                 "BRAINPING",
                                 msg)

            else:
                print("")  # newline
            #
            
            # time.sleep(30)
            # now_dt = datetime.now()
            if self.debug_fast_fwd_flag:
                now_dt = datetime.fromtimestamp(now_dt.timestamp() + 30)
            else:
                now_dt = datetime.now()
                time.sleep(45)
            #
        #
        print(f"finished @ {now_dt}")

if __name__=="__main__":
    args = parse_args()
        
    assert Path(args.config_fname).exists()
    assert Path(args.email_pwd_fname).exists()
    with open(args.config_fname, "r") as f:
        config_d = json.load(f)
    #
        
    #
    bp = BrainPing(config_d['email_user'],
                   args.email_pwd_fname,
                   config_d['email_dest'],
                   config_d['start_time'],
                   config_d['stop_time'],
                   config_d['num_pings'],
                   today_date_str = args.today_date_str,
                   startup_msg_flag = args.send_startup_msg,
                   fast_fwd_flag = args.debug_fast_fwd)
    bp.run_one_day()


