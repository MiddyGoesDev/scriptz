### Main command:

+ -d: the directory to watch for changes
+ -p: passwort for sender email account
+ -i: experiment has not been started externally, start by initializing the experiment from within the script
+ -e: the directory containing the different experiment settings (see example)

python oswalk_dirwatcher.py -d "/data/5rietz/ROOT_HIOB" -p "INSERT_PW_HERE" -i -e "/path/to/example_experiment" > watch_log.txt

### Monitor logfile:

tail -f watch_log.txt 

