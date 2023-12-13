# bike-vision
## Setting up OAK Device

After connecting the OAK device, follow these steps:

1. If you are using the OAK device for the first time, you need to configure the rules first. Run the following commands in the terminal:

    ```bash
    echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
    sudo udevadm control --reload-rules && sudo udevadm trigger
    ```

## Running the Model

1. Navigate to the `Documents` directory:

    ```bash
    cd Documents
    ```

2. Activate the environment using the following command:

    ```bash
    source environments/depthai/bin/activate
    ```

3. Navigate to the `yolo_project` directory:

    ```bash
    cd yolo_project
    ```

4. Run the following command to execute the model:

    ```bash
    python yolo.py --model yolov8n_openvino_2022.1_6shave.blob --config yolov8n.json
    ```
