from subprocess import Popen, PIPE
import os
import argparse
import time


parser = argparse.ArgumentParser()
parser.add_argument("-exp", "--exp_dir", dest="exp_dir", required=True,
                    help="The directory in which the subdirectories live, which contain the env.yaml and tracker.yaml "
                         "file for the experiment")
parser.add_argument("-g", "--gpu", dest="gpu", default="0",
                    help="The gpu used by cuda on which to run the experiments executed by this worker")
parser.add_argument("-nt", "--no_test", dest="test", default="0", action="store_false",
                    help="Test: If test, don't make actual shell call")
parser.set_defaults(test=True)
args = parser.parse_args()

if args.test:
    for i in range(0, 10):
        print("THIS IS A TEST RUN, supply --no_test argument to actually execute the shell comannds")


def run_experiment(exp_id, exp_dir):
    """
    Executes a specific hiob experiment, by compiling the shell call with the tracker and environment for that
    experiment.
    :param exp_id: The id of that experiment
    :param exp_dir: The directory of that experiment, which contains the tracker and environment files
    :return: Tuple of ("Status", exp_id)
    """
    # prepare paths to the files to use for this experiment
    env_path = os.path.join(exp_dir, "environment.yaml")
    tracker_path = os.path.join(exp_dir, "tracker.yaml")

    # set se parameter according to exp type (baseline is without se)
    if "baseline" in os.path.basename(exp_dir):
        se_str = "-no_se"
    else:
        se_str = "-se"

    # prepare the shell call
    shell_call = "python hiob_cli.py -t {} -e {} -g {} {}".format(
        tracker_path,
        env_path,
        args.gpu,
        se_str)
    print(shell_call, flush=True)

    # the actual shell call
    if not args.test:
        p = Popen(shell_call, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode

        # make sure experiment terminated successfully
        if "frame_rate" not in err.decode():
            print("EXPERIMENT " + exp_id + " FAILED!", flush=True)
            print("Here comes the log: ", flush=True)
            print(err.decode(), flush=True)
            return "Failure", exp_id
        else:
            print("Finished experiment " + exp_id, flush=True)
            return "Success", exp_id

    else:
        print("TEST RUN, shell call has not been executed...", flush=True)
        return "Test", exp_id


def main():
    # get all experiments folder
    todo_exps = os.listdir(args.exp_dir)

    # paths to logging txt files
    doing_txt = os.path.join(args.exp_dir, "doing.txt")
    completed_txt = os.path.join(args.exp_dir, "completed.txt")
    fail_txt = os.path.join(args.exp_dir, "failed.txt")

    # go over all exps
    for exp in todo_exps:
        exp_id = exp.split("_")[0]
        exp_dir = os.path.join(args.exp_dir, exp)

        # make sure its a valid experiment with environment and tracker files
        if (os.path.isdir(exp_dir)
                and "tracker.yaml" in os.listdir(exp_dir)
                and "environment.yaml" in os.listdir(exp_dir)):
            print("Checking experiment: " + str(exp_id), flush=True)

            # check whether current id has already been completed
            try:
                with open(completed_txt, "r+") as txt:
                    completed_ids = txt.readlines()
                    completed_ids = [c_id.replace("\n", "") for c_id in completed_ids]
                    print("Completed exp_ids: " + str(completed_ids), flush=True)

                    if exp_id in completed_ids:
                        print("Experiment {} has already been completed, next...".format(exp_id), flush=True)
                        continue
                    else:
                        print("Experiment {} not yet completed...".format(exp_id), flush=True)
            except FileNotFoundError:
                # if no completed file is found, we continue. This just means no experiment completed previously
                pass

            # check whether current id has already been failed
            try:
                with open(fail_txt, "r+") as txt:
                    fail_ids = txt.readlines()
                    fail_ids = [f_id.replace("\n", "") for f_id in fail_ids]
                    print("Failed exp_ids: " + str(fail_ids), flush=True)

                    if exp_id in fail_ids:
                        print("Experiment {} has failed previously, skipping...".format(exp_id), flush=True)
                        continue
                    else:
                        print("Experiment {} hasn't failed before...".format(exp_id), flush=True)
            except FileNotFoundError:
                # if no fail file is found, we continue. This just means no experiment failed previously
                pass

            # if not completed, not failed, check whether experiment is in doing
            try:
                with open(doing_txt, "r") as txt:
                    doing_ids = txt.readlines()
                    doing_ids = [helper_id.replace("\n", "") for helper_id in doing_ids]
                    print("Current doing exp_ids: " + str(doing_ids), flush=True)
            except FileNotFoundError:
                # if no doing file is found, we continue. This just means there are currently no other experiments
                # running
                doing_ids = []

            # check whether current id is in doing
            if exp_id in doing_ids:
                print("Experiment {} is already in doing, skipping...".format(exp_id), flush=True)
                continue
            else:
                with open(doing_txt, "a+") as txt:
                    print("Experiment {} is also not in doing, starting...".format(exp_id), flush=True)
                    # for prev_line in doing_ids:
                    #     txt.write(prev_line + "\n")
                    txt.write(str(exp_id) + "\n")

            # do actual processing, if not completed and not already doing
            print("Starting exp {} now...".format(exp_id), flush=True)
            status = run_experiment(exp_id, exp_dir)
            time.sleep(10)

            # read new doings (including the one we did but finished now
            with open(doing_txt, "r") as txt:
                current_doing_ids = txt.readlines()

            # write current doings but without the one we just finished
            with open(doing_txt, "w+") as txt:
                print("Finished exo {}, removing from doing...".format(exp_id), flush=True)
                current_doing_ids.remove(str(exp_id) + "\n")
                txt.writelines(current_doing_ids)

            # depending on status write to corresponding txt
            if status[0] == "Success":
                # write completed experiment to the done txt file
                with open(completed_txt, "a+") as txt:
                    print("Status = Success: Writing exp {} to success file".format(exp_id), flush=True)
                    txt.write(str(exp_id) + "\n")

            elif status[0] == "Failure":
                # write completed experiment to the done txt file
                with open(fail_txt, "a+") as txt:
                    print("Status = Failure: Write exp {} to fail file".format(exp_id), flush=True)
                    txt.write(str(exp_id) + "\n")

            elif status[0] == "Test":
                print("Status = Test: not marking exp as done", flush=True)

    print("No new experiments left", flush=True)


if __name__ == '__main__':
    main()
