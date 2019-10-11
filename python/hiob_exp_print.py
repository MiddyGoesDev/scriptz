import os
import ruamel.yaml


def main():
    root_dir = "/data/5rietz/ROOT_HIOB/hiob_logs"

    for ch_dir in os.listdir(root_dir):

        print(ch_dir)

        full_path = os.path.join(root_dir, ch_dir)

        yaml = ruamel.yaml.YAML()
        yaml_file = os.path.join(full_path, "tracker.yaml")

        # parse yaml config file
        if os.path.exists(yaml_file) and ".yaml" in yaml_file:
            with open(yaml_file) as yf:
                yaml_dict = yaml.load(yf)
                print("static_update_val: " + str(yaml_dict["scale_estimator"]["static_update_val"]))

        # read eval txt file
        eval_file = os.path.join(full_path, "evaluation.txt")
        if os.path.exists(eval_file):
            with open(eval_file) as txt:
                lines = txt.readlines()

                print(lines[25].replace("\n", ""))
                print(lines[26])


if __name__ == "__main__":
    main()