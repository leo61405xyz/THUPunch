# THUPunch

This is a Python program for automatic clock-in and clock-out designed for Tunghai University members. It aims to save you the hassle of the tedious attendance process.

## Installing

It is recommended to install the following Python packages in Python 3.12:

- ``selenium``
- ``webdriver-manager``
- ``pillow``
- ``pytesseract``

To download and install Tesseract OCR, follow these steps:

1. **Visit the Official Tesseract OCR Page**
   - Go to the following URL: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
2. **Download Tesseract Installer**

   - Scroll down to find the installation instructions for your operating system (Windows, macOS, or Linux).
   - For **Windows**, download the executable file (e.g., `.exe`) provided in the release section.
3. **Install Tesseract OCR**

   - Run the downloaded installer and follow the on-screen instructions.
   - Make a note of the installation directory (e.g., `C:\Program Files\Tesseract-OCR`).
4. **Add Tesseract to System Path** (Optional but recommended)

You can also create an environment using `environment.yml` after installing Conda. Follow these steps:

1. **Run the Command to Create the Environment**
   
   Open a terminal or command prompt, navigate to the directory containing `environment.yml`, and execute the following command:

   ```bash
   conda env create -f environment.yml
   ```
2. **Activate the Environment**
   
   After the environment is created, activate it using:

   ```bash
   conda activate THUPunch
   ```

This approach ensures that all required dependencies are installed in a clean environment, avoiding conflicts.

## Executing program

Here's a step-by-step guide to modify and run the script:

1. **Open the `Job_Description.json` File**

   - Locate the `Job_Description.json` file in the project directory.
   - Open it using a text editor (e.g., Notepad, VSCode, or any JSON editor).
2. **Modify the File Contents**

   ```json
   {
       "account": "your_tunghai_account",
       "password": "your_password",
       "punch_in_time": "08:30",
       "punch_out_time": "17:30",
       "where_and_do_what": [
           ["Office", "Review documents"],
           ["Lab", "Conduct experiments"],
           ["Library", "Prepare reports"],
           ["Conference Room", "Attend meetings"],
           ["Cafeteria", "Discuss project ideas"]
       ]
   }
   ```
   - Replace `your_tunghai_account` and `your_password` with your Tunghai University account and password.
   - Set `punch_in_time` and `punch_out_time` to your actual work hours (in HH:MM format).
   - Customize `where_and_do_what` to list your real work locations and corresponding tasks.
3. **Save the File**

   - Save the changes to `Job_Description.json`.
4. **Run the Script**

   Open a terminal or command prompt in the project directory and execute the following command:

   ```bash
   python THUPunch.py
   ```
5. **What Happens Next**

   - On regular working days, the program will automatically log into the Tunghai University attendance system at the specified `punch_in_time` and `punch_out_time`.
   - It will randomly select a work location and task from the list to complete the work log.
   - The script will not run on weekends.
