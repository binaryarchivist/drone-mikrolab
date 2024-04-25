sudo apt-get update

sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame

pip3 install PyYAML mavproxy --user
sudo pip install pymavlink
sudo pip install mavproxy
sudo pip install dronekit


Check if drone is ready to use by running the following command in RPi terminal

mavproxy.py --master=/dev/ttyS0 --baudrate 921600 --aircraft MyDrone


Place the drone in a flyable zone and run command :


python take_off.py --connect /dev/ttyS0
