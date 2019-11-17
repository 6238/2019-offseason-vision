# copies an input file to the raspberry pi as uploaded.py
deploy:
	@scp $$input pi@frcvision.local:uploaded.py
	@scp runCamera pi@frcvision.local:runCamera

install: 
	@echo Please enter the path to the install image \(\.img file\);
	@read image;\
	echo Please enter the path to the disk you wish to install on \(ex. /dev/rdisk2\):;\
	read disk;\
	echo Are you sure you want to write to $$disk ? This cannot be undone. [y/n];\
	read yesno;\
	if [ "$$yesno" == "y" ] || [ "$$yesno" == "Y" ];\
	then\
		sudo dd bs=1m if=$$image of=$$disk conv=sync;\
	fi