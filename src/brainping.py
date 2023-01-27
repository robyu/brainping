import json
import argparse
import sender
import scheduler
from datetime import datetime
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="""
""", formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument("config_fname", help="fname of config json file")
    parser.add_argument("email_pwd_fname", help="fname of file containing email server password")
    parser.add_argument("-t", "--today-date-str", default="", help="""date string used in place of "now"; YYYY-mm-dd string""")
    parser.add_argument("-s", "--send-startup-msg", action="store_true", default=False, help="send a message upon init")
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
                 startup_msg_flag=False):
                 
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
        
        self.scheduler = scheduler.Scheduler(start_time_str = str(self.start_time_dt.time()),
                                              stop_time_str = str(self.stop_time_dt.time()),
                                              num_pings = self.num_pings)
        if startup_msg_flag:
            self._send_startup_msg()
        #

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

    def run_one_day():
        now_dt = datetime.now()
        
        while now_dt.date()==self.today_dt.date() and self.stop_time_dt <= now_dt: 
            
            time.sleep(30)
        #

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
                   startup_msg_flag = args.send_startup_msg)
    bp.run_one_day()


