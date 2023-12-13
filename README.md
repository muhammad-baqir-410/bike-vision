# bike-vision
## Setting up OAK Device

After connecting the OAK device, follow these steps:

1. If you are using the OAK device for the first time, you need to configure the rules first. Run the following commands in the terminal:

    ```bash
    echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
    sudo udevadm control --reload-rules && sudo udevadm trigger
    ```

## Running the Model
1. Create virtual environment:

   ```bash
    conda create -n <name_of_virtualenv> python==3.9
    ```
    or
   ```bash
   python3 -m venv <name_of_virtualenv>
   ```
3. Activate the environment using the following command:

   ```bash
    source /name_of_virtualenv/bin/activate
    ```
    if conda env:
   ```bash
   conda activate name_of_virtualenv
   ```
4. Navigate to the project directory:

    ```bash
    cd <project directory>
    ```
5. Intall the requirements.

   ```bash
   pip install -r requirements.txt
   ```
7. Run the following command to execute the model:

    ```bash
    python main.py --model weights/yolov8n_openvino_2022.1_6shave.blob --config weights/yolov8n.json
    ```
