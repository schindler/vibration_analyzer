folder=/usr/local/src/flightmonitor/
mkdir $folder
cp ./*.py $folder
cp ./flightd.sh /etc/init.d/flightd
sudo chmod 755 /etc/init.d/flightd
sudo chown root:root /etc/init.d/flightd
sudo update-rc.d flightd defaults
sudo update-rc.d flightd enable
