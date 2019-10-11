import argparse
import ruamel.yaml
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-yf", "--yaml_file", dest="yaml_file", required=True)
args = parser.parse_args()


yaml = ruamel.yaml.YAML()


def main():
    if os.path.exists(args.yaml_file) and ".yaml" in args.yaml_file:
        with open(args.yaml_file) as yf:
            yaml_dict = yaml.load(yf)
            yaml.dump(yaml_dict, sys.stdout)


if __name__ == '__main__':
    main()

