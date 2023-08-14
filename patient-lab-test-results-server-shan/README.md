# patient-lab-test-results-server-shan
patient-lab-test-results-server-shan created by GitHub Classroom
Author: Shanshan Gao

# Introduction to the code
This repository contains codes of a centralized patient test results server that can receive GET and POST requests from two general types of users:
Physician: can enter patient information, order tests, and get test results
Lab technician: can get what tests were ordered and upload the results of tests
# Instruction on the code
1. Activate the server by running db_server.py
2. create a client file that conducts the following five requests
   
* POST /patient/new_patient allows information about a new patient to be added to the server. It should accept JSON input as follows:
  {
      "patient_mrn": <medical_record_number>,
      "attending_email": <attending_email>, 
      "patient_age": <patient_age>

  }
 * POST /patient/new_request allows the attending physician to request that a test be performed on a patient. It takes a JSON as input as follows:

  {
      "patient_mrn": <medical_record_number>,
      "test_name": <test_name>
  }
 * GET /lab/open_requests returns information about test requests that have been submitted to the server but not yet been completed. This route should return a list where each entry in the list is a dictionary representing a single test request. This dictionary should be formatted as follows:

  { 
     "patient_mrn": <medical_record_number>,
     "test_name": <test_name>,
     "request_date": <request_date_time>
  }  
 * POST /lab/new_result allows the lab to post new test results to the server. It takes a JSON input as follows:
  { 
     "patient_mrn": <medical_record_number>,
     "test_name": <test_name>,
     "test_result": <test_result>
  }  
 * GET /patient/results/<patient_mrn>/<test_name> returns a list of all available test results for the specified type of test for the specified patient. The <patient_mrn> portion of the URL should contain the medical record number of the patient of interest. The <test_name> portion of the URL should contain the test name of interest.
This route should return a list of numeric values (not numeric strings). If there are no results for the specified test for the specified patient, the route should return an empty list.

where  
<medical_record_number> is the unique medical record number for the patient, <attending_email> is a string containing an e-mail address
<patient_age> is the patient's age in years.
<test_name> is a string containing the name of the test to be performed
<request_date> is a string containing the date/time stamp of when the request was received. It should be in the format as shown by this example: 2018-03-09 11:00:36
<test_name> is the name of the test performed
<test_result> is a numeric value (int or float) with the result of the test

3. run the client file


# Software license
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


  
   
   


