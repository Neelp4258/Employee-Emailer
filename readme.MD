Bulk Interview Emailer Web App
This application provides a simple web interface to send bulk interview emails using a Zoho account.

How to Set Up and Run
Follow these steps to get the application running on your computer. You only need to do the setup once.

Step 1: Create a Project Folder
Create a new folder on your computer where you will store the application files. Let's call it BulkEmailer.

Inside the BulkEmailer folder, create another folder named templates.

Place all the files I provided into the correct locations:

app.py -> inside the BulkEmailer folder.

requirements.txt -> inside the BulkEmailer folder.

index.html -> inside the templates folder.

results.html -> inside the templates folder.

Your folder structure should look like this:

BulkEmailer/
├── app.py
├── requirements.txt
└── templates/
    ├── index.html
    └── results.html

Step 2: Install Python
If you don't have Python installed, download and install it from the official website: python.org

Step 3: Install Required Packages
Open your computer's command prompt or terminal.

Navigate into your BulkEmailer folder using the cd command. For example:

cd path/to/your/BulkEmailer

Run the following command to install the necessary Python libraries:

pip install -r requirements.txt

Step 4: Run the Web Application
Make sure you are still in the BulkEmailer folder in your command prompt or terminal.

Run the following command to start the web server:

python app.py

You will see some output in the terminal, including a line that looks like this:
* Running on http://127.0.0.1:5000/

Step 5: Use the Application
Open your web browser (like Chrome, Firefox, or Edge).

Go to the address: http://127.0.0.1:5000/

You will see the web form. Fill it out:

Your Zoho Email: Your full Zoho email address.

Your Zoho App Password: If you have Two-Factor Authentication (2FA) enabled, you must generate and use an "App-Specific Password" from your Zoho account security settings. Otherwise, you can use your regular password.

Recipients CSV File: Upload the .csv file containing the candidate data.

Company Logo: Optionally, upload your company's logo (.png file).

Click "Send Emails". The application will process the file and show you a report of which emails were sent successfully and which failed.

To stop the server, go back to the command prompt/terminal window and press Ctrl + C.