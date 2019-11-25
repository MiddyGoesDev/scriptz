import os

# for all items in dir
for item in os.listdir("."):
	if os.path.isdir(item):
		# if dir contains one of the identifying criterions
		if ("baseline" in item) or ("cand" in item) or ("dsst") in item:
			archive_name = item + ".tar.gz"

			# prepare the command strin
			call = "tar -czvf " + archive_name + " " +item
			print("Executing: " + call)
			
			# execute the actual command			
			os.system(call)
