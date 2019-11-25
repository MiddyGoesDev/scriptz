import datetime
import time
import psutil
import smtplib
import os
import argparse
import setproctitle
import subprocess

# setup argparse
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dir", type=str, help="Dir to observe", required=True)
parser.add_argument("-u", "--user", default="logmemiddy@gmail.com", type=str, help="Gmail account")
parser.add_argument("-p", "--passwd", type=str, help="Password for gmail account")
parser.add_argument("-i", "--init", action="store_true", help="use this script to init the main experiment")
parser.add_argument("-e", "--exp", type=str, help="the experiment folder for the que exp script")
parser.add_argument("-g", "--gpu", type=str, default="0", help="GPU for this experiment")
args = parser.parse_args()


# nicer print message, prefix helps when multiple scripts all print to stdout
def prefixed_print(msg=""):
    prefix = "| WATCHER | "
    print(prefix + str(msg), flush=True)


class Observer:
    def __init__(self):
        self.watch_dir = args.dir
        self.prev_dir_contents = [datetime.datetime.now(), list(os.walk(self.watch_dir))]  #  list of timestamp and contents of self.watch_dir
        self.cur_dir_contents = None
        self.dir_changed = False
        self.mem_usage = None
        self._user = args.user
        self._pass = args.passwd
        self.second_since_change = 0
        self.email_timestamp = datetime.datetime.now()
	
        # try logging into the email account with the provided credentials (gmail account must allow less secure apps)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self._user, self._pass)
            prefixed_print("Email authenticated successfully.")
        except:
            prefixed_print("Couldn't log into Gmail account. Alert Emails won't be send!")

    def compare_dir_states(self):
        """
        Compares the last state of the target directory with the current state of the target directory and sets class attributes according to change or no change
	"""  
        self.cur_dir_contents = [datetime.datetime.now(), list(os.walk(args.dir))]
        # if dir content did not change
        if self.prev_dir_contents[1] == self.cur_dir_contents[1]:  
            self.dir_changed = False
            self.second_since_change = (self.cur_dir_contents[0] - self.prev_dir_contents[0]).seconds  # update the "no change" counter
        else:
            self.dir_changed = True
            self.prev_dir_contents = self.cur_dir_contents
            self.second_since_change = 0

    def send_mail(self, passed_since_cahnge):
        """
        sends an email to me
        """
        sent_from = self._user
        to = ['finnrietz@googlemail.com']
        subject = 'Experiment timed out'
        body = """
        Dir has not changed since {} minutes.
        Experiment does not appear to be running.
        Current memory usage: {}%
        """.format(passed_since_cahnge, self.mem_usage)

        message = 'Subject: {}\n\n{}'.format(subject, body)  # some formatting so that email server properly display subject and main body
	
        # try logging into email account and send mail
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(self._user, self._pass)
            server.sendmail(sent_from, to, message)
            server.close()

            prefixed_print("Timeout alert email has been sent to {}.".format(to))
        except:
            prefixed_print("Failed to sent timeout alert email")


if __name__ == "__main__":
    # set the name of this process. Important, because this script automatically restart the experimt with "killall python", thus this script needs a different name
    setproctitle.setproctitle("dirwatcher")  
    observer = Observer()
    prefixed_print("Start observing dir {} for changes...".format(observer.watch_dir))
    prefixed_print()

    if args.init and args.exp:
        prefixed_print("Init arg given: Initialising experiment...")

        cmd = "python que_exp.py -exp {} -g {} --no_test".format(args.exp, args.gpu)
        output_logfile = "EXECUTION_" + str(datetime.datetime.now()).replace(" ", "@") + "_LOG.txt"  # create logfile for subprocess to redirect output to

        prefixed_print("Initial call: " + cmd)
        prefixed_print("Initial log file: " + output_logfile)

        with open(output_logfile, "w") as output:  # start subprocess and redirect stdout
            command1 = subprocess.Popen(
                cmd,
                stdout=output,
                shell=True)

    #  do forever but except keyboard interrupt
    try:
        while True:
            time.sleep(10)

            observer.mem_usage = psutil.virtual_memory()._asdict()["percent"]
            observer.compare_dir_states()
            now = datetime.datetime.now()

            if observer.dir_changed:
                status = """| WATCHER | Timestamp: {}\n| WATCHER | Watchdir: {}\n| WATCHER | Status: DIR CHANGED!!!\n| WATCHER | Dir change detected at {}\n| WATCHER | Experiment appears to be running\n| WATCHER | Current memory usage: {}%""".format(
                    now,
                    observer.watch_dir,
                    observer.cur_dir_contents[0],
                    observer.mem_usage)

                print(status, flush=True)

            else:
                minutes_since_change = observer.second_since_change / 60

                status = """| WATCHER | Timestamp: {}\n| WATCHER | Watchdir: {}\n| WATCHER | Status: DIR SAME!!!\n| WATCHER | No change since {} minutes\n| WATCHER | Experiment does not appear to be running\n| WATCHER | Current memory usage: {}%""".format(
                    now,
                    observer.watch_dir,
                    minutes_since_change,
                    observer.mem_usage)

                print(status, flush=True)

                # if more than 30 minutes elapsed without a change in the directory, send email and kill all python processes of user 5rietz, then restart experiment			
                if minutes_since_change > 30:
                    # if (now - observer.email_timestamp).seconds / 60 > 1:
                    if (now - observer.email_timestamp).seconds / 60 > 30:
                        observer.email_timestamp = now
                        observer.send_mail(minutes_since_change)

                    # kill all running python process,
                    # this script wont die, because it has been renamed to "dirwatcher"...
                    prefixed_print("Killing all python processes")
                    os.system("killall python -u 5rietz")
                    time.sleep(10)

                    cmd = "python que_exp.py -exp {} -g {} --no_test".format(args.exp, args.gpu)
                    output_logfile = "EXECUTION_" + str(datetime.datetime.now()).replace(" ", "@") + "_LOG.txt"

                    restart_msg = """| WATCHER | restart command: {}\n| WATCHER | restart logfile: {}""".format(cmd, output_logfile)

                    # since we are spawning a subprocess here, out script will continue running and not pause the control flow
                    with open(output_logfile, "w") as output:
                        command1 = subprocess.Popen(
                            cmd,
                            stdout=output,
                            shell=True)

                    time.sleep(10)
                    prefixed_print("Restarted exp kernel")

            prefixed_print()

    except KeyboardInterrupt:
        prefixed_print("Keyboard interrupt: Stopping observation")
