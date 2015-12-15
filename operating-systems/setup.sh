#!/bin/sh
sudo cp -avr os-coursework /etc/
echo "alias os-coursework='source /etc/os-coursework/os-coursework.sh'" >> ~/.bashrc
while true; do
	read -p 'Do you wish to create desktop entry? ' yn
	case $yn in
		[Yy]* ) 
			cd ~/.local/share/applications && echo '[Desktop Entry]' > os-coursework.desktop
			echo 'Name=OSCoursework' >> os-coursework.desktop
			echo 'Exec=sh /etc/os-coursework/os-coursework.sh' >> os-coursework.desktop
			echo 'Terminal=false' >> os-coursework.desktop
			echo 'Type=Application' >> os-coursework.desktop
			echo 'Icon=/etc/os-coursework/os-coursework.png' >> os-coursework.desktop
			echo 'NoDisplay=false' >> os-coursework.desktop;
			break;;
		[Nn]* ) break;;
		* ) echo 'Please answer yes or no.';;
	esac
done