**Patient Lab Results Server** \
 **Team Members** \
 Nika Ilieva \
 Ella Fortenbery 

 **Purpose**  
 This repository contains a server for managing patient lab results and requests. It supports two types of users: attending physicians who can register patients and order tests, and lab technitians, who can retrieve open test requests and upload results. The server has an automated email sendin feature, which sends email notifications to the lab when a new test is requested and to the physician when a result is abnormal. 
 
Avaliable tests are:
HR - Heart Rate 
HDL - HDL Cholesterol 
LDL - LDL CHolesterol 
TSH - Thyroid-Stimulating Hormone

 **Repository Structure** 
 - lab_server.py: Flask routes for all lab-related features 
 - patient_server.py: Flask routes for patient data 
 - patient_database.py: In-memory storage and access functions for patient records 
 - test_dict.py: In-memory storage and access functions for test requests and results 
 - test_lab_server.py ; test_patient_server.py: Unit tests for relevant functions
 - server.py: creates the Flask app and registers all routes
 - test_test_dict.py: Unit testing for test_dict.py

 **How to run the program** 
   1. Clone the repository 
   2. Create and activate a virtual environment 
   3. Install dependencies 
   4. Start the server by running server.py (runs on http://localhost:5000 by default)

**Deployed Server** 
The server is currently running at: vcm-1000.vm.duke.edu:5000

**License** 

   
