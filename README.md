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
The server is currently running at: http://vcm-52575.vm.duke.edu:5000

**MIT License**

Copyright (c) 2026 Nika Ilieva and Ella Fortenbery 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
