#!/bin/bash
#use like: rsync_all_ext.ssh -s '/some/source/folder' -d '/some/dest/folder' -e 'some.extension'


# create named arguments
while getopts ":s:d:e:" opt; do
  case $opt in
    s) source_folder="$OPTARG"
    ;;
    d) dest_folder="$OPTARG"
    ;;
    e) extension="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

printf "Argument source_folder is %s\n" "$source_folder"
printf "Argument dest_folder is %s\n" "$dest_folder"
printf "Argument exentsion is %s\n" "$extension"




for i in "$source_folder*$extension"; do
	
	# -a archive mode: preserve permissions, ownership, edit times etc
	# -v verbose output
	# -z compression during transer
	# -h humanm readable output
	# --info=progress2 total progres percentage
	# --ignore-existing prevents files from being copied over that already exist on the the destination	
	rsync -avzh --info=progress2 --ignore-existing $i $dest_folder;
done
