import os
import ruamel.yaml


def yaml_list(*l):
    # formats the given list so its stored as an actual list in the yaml file
    ret = ruamel.yaml.comments.CommentedSeq(l)
    ret.fa.set_flow_style()
    return ret


yaml = ruamel.yaml.YAML()

# iterate over all items in dir
for item in os.listdir("."):
    if os.path.isdir(item):
        print(item)
	
        # the dirname (name of the experiment will be changed according to parameter change)
        new_item = item.replace("mask46", "mask200")

        # change the name of the environemnt (using the new_item name)
        env_path = os.path.join(item, "environment.yaml")
        print(env_path)
        
        # read the yaml environment file 
        with open(env_path) as f:
            yaml_file = yaml.load(f)
            yaml_file["log_dir"] = "./" + new_item + "/"
            yaml_file["data_dir"] = "/data/5rietz/"  # must be set according to machine

        # save the yaml environment file
        with open(env_path, "w") as f:
            yaml.dump(yaml_file, f)

        # read the tracker yaml file
        tracker_path = os.path.join(item, "tracker.yaml")
        print(tracker_path)
        with open(tracker_path) as f:
            yaml_file = yaml.load(f)
            yaml_file["mask_size"] = yaml_list(200, 200)  # here we make the actual change to the tracker parameter

        # save the changes made to the tracker yaml config file
        with open(tracker_path, "w") as f:
            yaml.dump(yaml_file, f)

        # finally rename the experiment/dir of this specific experiment
        os.rename(item, new_item)
