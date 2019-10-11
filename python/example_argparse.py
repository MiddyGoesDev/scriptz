import argparse

parser = argparse.ArgumentParser()

# provide a list as arg, required
# python argparse.py -l 1234 2345 3456 4567
parser.add_argument("-l","--list", nargs="+", help="<Required> Set flag", required=True)

# provide a default value, gets converted to type String
parser.add_argument("-blah", dest="blah_blah", default="blub", type=str, help="dummy arg")

# if -se is given, we store True in use_se
# NOTE: type=bool is not supported...
parser.add_argument("-se", "--use_se", dest="use_se", action="store_true")

# if -no_se is guven, we store False in use_se
parser.add_argument("-no_se", "--dont_use_se", dest="use_se", action="store_false")

# another dummy
parser.add_argument("-s", "--silent", dest="silent", action="store_true")

# set default values for destinations
parser.set_defaults(silent=False, use_se=False)

args = parser.parse_args()

