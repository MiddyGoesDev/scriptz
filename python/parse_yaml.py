import ruamel.yaml
import os
import sys


def main():

    yaml_path = "/data/5rietz/ROOT_HIOB/hiob_logs/hiob-execution-wtmpc30-2019-10-09-20.12.39.959490/tracker.yaml"
    yaml = ruamel.yaml.YAML()

    if os.path.exists(yaml_path) and ".yaml" in yaml_path:
        with open(yaml_path) as yf:
            yaml_dict = yaml.load(yf)
            yaml.dump(yaml_dict, sys.stdout)


if __name__ == '__main__':
    main()

