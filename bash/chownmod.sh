#!/bin/bash

# -------------------------------------------------------------------------------------
# |	Run with sudo, we need sudo for chmod and chown...			     |
# |										     |	
# |	Sets given user as owner for a directory and all items in that directory     |
# |	alongside giving that user read, write and execute permissions for           |
# |	that directory. Script can also be use to take right away for a user, but    |
# |     primary usecase is to conveniently give all rights, hence the default args.  |
# |										     |	
# |	Example usage: 								     |
# |     $ ./chownmod /path/to/target_dir				       	     |	
# |	This binds the only given (unnamed) argument to the $TARGET_DIR variable     |	
# |	and uses the default values for the other args.				     |	
# |										     |	
# |	$ ./chownmod user="username" access="a" op=+" perms="rwx" dir="dir/path"     |	
# |	Here we provide all arguments directly via CLI.				     |	
# |										     |	
# |										     |	
# |	@author: Finn Rietz							     |	
# -------------------------------------------------------------------------------------
echo ""
echo "Following arguments can be given:"
echo "    + user=\"username\": User to make oner of file/dir. Default \$user"
echo "    + access=\"[ugoa]\": The access type to change with chmod. Default \"a\""
echo "    + op=\"[+-=]\": The operation for permission manipulation for chmod. Default \"+\""
echo "    + dir=\"path/to/file\": Required, the dir/file to which the changes are applied. Can also be given as single, unnamed argument" 

for ARGUMENT in "$@"
do

    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   

    case "$KEY" in
            user)              USER=${VALUE} ;;
            access)            ACCESS=${VALUE} ;;     
	    perms)             PERMS=${VALUE} ;;
	    op)                OP=${VALUE} ;;
	    dir) 	       TARGET_DIR=${VALUE} ;;
            *)  	       TARGET_DIR=$ARGUMENT ;; 
    esac    

done

# check whether all variables are set
# $USER is set by default on linux systems
if [ -z "$USER" ]
then 
	echo "Argument 'user' can not be empty."
	echo "Please provide like: ./chownmod.sh user=\"username\""
	exit 2
fi

# the directory to which we want to apply chown and chmod
if [ -z "$TARGET_DIR" ]
then 
	echo "Argument 'dir' can not be empty."
	echo "Please provide liek: ./chownmod.sh dir=\"target/dir\""
	exit 2
fi

# which access to change with chmod
if [ -z "$ACCESS" ]
then 
	ACCESS="a"
fi

# which permissions to apply with chmod
if [ -z "$PERMS" ]
then 
	PERMS="rwx"
fi

# which operator to apply with chmod (give perms, take perms etc)
if [ -z "$OP" ]
then 
	OP="+"
fi

echo ""
echo "Got the following argument values:"
echo "USER: $USER"
echo "ACCESS: $ACCESS"
echo "OP: $OP"
echo "PERMS: $PERMS"
echo "TARGET_DIR: $TARGET_DIR"
echo ""

echo "executing resulting calls:"
echo "sudo chown -R $USER $DIR"
echo "sudo chmod -R $ACCESS$OP$PERMS $TARGET_DIR"
echo ""

sudo chown -R $USER $TARGET_DIR
if [ ! $? -eq 0 ]; then
	echo "Looks like chown call failed, exiting."
	exit 1
fi

sudo chmod -R $ACCESS$OP$PERMS $TARGET_DIR
if [ $? -eq 0 ]; then
	echo "Done"
	exit 0
else
	echo "Looks like chmod call failed, exiting."
	exit 1
fi

exit 0

