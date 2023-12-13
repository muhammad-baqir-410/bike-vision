# bike-vision
After connecting OAK device:
--If you are using the OAK device for the first time, you need to configure the rules first.
	echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
	sudo udevadm control --reload-rules && sudo udevadm trigger


For running the model.
cd Documents
-- Activate the environment by following command
	source environments/depthai/bin/activate
cd yolo_project
-- run the command
	python yolo.py --model yolov8n_openvino_2022.1_6shave.blob --config yolov8n.json