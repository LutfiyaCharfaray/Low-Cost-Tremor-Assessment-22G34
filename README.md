# README
This is a low-cost tremor assessment application created for android tablets using Python and Kivy. This application is designed to detect tremors found in patients with Parkinson's disease and Essential Tremor. This is achieved by digitising the traditional pen-and-paper spiral drawing evaluation and performing signal processing on the drawings to produce results for the physician. 
This application is designed for the University of Witwatersrand, School of EIE, ELEN4012 Investigation Project 2022.

## App Title
Low Cost Tremor Assessment App

## Collaborators
- Lutfiya Charfaray
- Maria Botha

## How to use the code
- The main code is found under the main folder, "Low-Cost-Tremor-Assessment-22G34" 
- The code is copied and adjusted to meet the specifications of a Samsung Galaxy Tab S7 FE 
  tablet. This code is found under the folder "Tablet code".
- The Tablet code can be packaged for android using Google Colab and Buildozer. Follow these
  guidelines for using Google Colab to package the app
   https://towardsdatascience.com/3-ways-to-convert-python-app-into-apk-77f4c9cd55af

## How to use the app
- Enter the password to log into the app. 
- Select an existing patient on the database or fill in the form for a new patient. 
- Start the assessment by pressing on the start assessment button. 
- Draw a straight line on the template provided then press next to navigate to the 
  spiral screens.
- Start the timer before tracing the spirals using your dominant and non-dominant hands. 
- Stop the timer by pressing stop when you are done with each spiral drawing.
- The app performs signal processing and your results should display on two results screens.
- The drawings and results save automatically in the tablet's DCIM folder.
- You can then navigate back to the menu screen or login page.

## Future Recommendations
- Change the password in the _tremor.kv_ file _loginWindow_ class
  or let the user enter a password and save it to the database.
- Improve the app's security.
- Make the new patient form scroll up.
- Add more signal processing features such as zero crossing. 

# END OF README
