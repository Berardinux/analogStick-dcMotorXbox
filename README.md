evtest & evdev {

	sudo apt install evtest python3-evdev python3-numpy

	sudo evtest /dev/input/event0
}

Connect Xbox Controller to bluetooth {

	bluetoothctl

	scan on

	pair XX:XX:XX:XX:XX:XX

	trust XX:XX:XX:XX:XX:XX

	connect XX:XX:XX:XX:XX:XX
}
