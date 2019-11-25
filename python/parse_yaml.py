import ruamel.yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as dq
import os

# for correctly storing list in yaml.
def yaml_list(*l):
   ret = ruamel.yaml.comments.CommentedSeq(l)
   ret.fa.set_flow_style()
   return ret


def main():

    yaml_path = "/data/5rietz/ROOT_HIOB/hiob_logs/hiob-execution-wtmpc30-2019-10-09-20.12.39.959490/tracker.yaml"
    yaml = ruamel.yaml.YAML()

    if os.path.exists(yaml_path) and ".yaml" in yaml_path:
        # load yaml file into ordereddict
        with open(yaml_path) as f:
            yaml_file = yaml.load(f)
            
            # dome some processing
            yaml_file["some_key"] = "some_vale"
            
            # store list in yaml like value: ["abc", "dfg"]
            yaml_file["some_other_key"] = yaml_list(100, 100)
            
            # store list in yaml like value: 
            #                            - "abc"
            #                            - "dfg"
            yaml_file["yet_another_key"] = ["abc", "dfg"]
            
            
           
        # overwrite the old yaml file with the loaded, manipulated new dict
        with open(yaml_path, 'w') as f:
            yaml.dump(yaml_file, f)

if __name__ == '__main__':
    main()

