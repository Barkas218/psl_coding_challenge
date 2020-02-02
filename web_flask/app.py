from flask import Flask, request, render_template, jsonify, abort, make_response
from pyrebase import pyrebase
import os
import math

""" Init app """
app = Flask(__name__)

""" pyrebase config """
config = {
    "apiKey": "AIzaSyA86JmZLOUgMxS2A-MaBSVI-bcmJk6re_E",
    "authDomain": "tusavirus.firebaseapp.com",
    "databaseURL": "https://tusavirus.firebaseio.com",
    "projectId": "tusavirus",
    "storageBucket": "tusavirus.appspot.com",
    "messagingSenderId": "403561205401",
    "appId": "1:403561205401:web:cb8c48b634dcc202327208",
    "measurementId": "G-5RSHKVM4KZ"
}

firebase = pyrebase.initialize_app(config)

@app.route('/', strict_slashes=False)
def index():
    """ renders index """
    return render_template('index.html')


@app.route('/action_page', strict_slashes=False, methods=['POST'])
def get_data():
    if request.method == "POST":

        state = request.form.get("states")
        patient = request.form.get("patients")

        if patient.isdigit() is False:
            num_dict = {"ninety": 90, "fifty": 50, "forty": 40, "twenty":20, "thirty": 30, "eighty": 80, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
                    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
                    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "ty": 10,
                    "hundred": 100, "thousand": 1000, "million": 1000000}
            str_len = len(patient)
            i = 0
            num_list = []
            flag = 0
            while (1):
                """ check whether the string contains a member of the dict """
                for key in num_dict:
                    if patient[0:len(key)] == key:
                        num_list.append(num_dict.get(key))
                        """ slice the string and append the coincidence """
                        patient = patient[len(key):]
                        i += len(key)
                        flag = 1
                """ check if the whole string has been parsed """
                if flag == 0:
                    return jsonify({"Not a valid number" : patient})
                if i == str_len:
                    break
            """ end of infinite while """
            print(num_list)

            """ handle edge case """
            if len(num_list) >= 3:
                if num_list[0] > num_list[1] and num_list[1] < num_list[2]:
                    num_list[0] = num_list[1] + num_list[0]
                    del(num_list[1])

            """ cycle to multiply the numbers if the next is a bigger one """
            for j in range(len(num_list) - 1):
                if num_list[j] < num_list[j + 1] and num_list[j + 1] is not 0:
                    num_list[j + 1] = num_list[j] * num_list[j + 1]
                    num_list[j] = 0


            num_list = sum(num_list)
            print(patient)
            print(num_list)
            my_dict = {state: num_list}
            return jsonify(my_dict)

        else:
            patient = int(patient)
            my_dict = {state: patient}
            return jsonify(my_dict)

""" run server """
if __name__ == '__main__':
    app.run(debug=True)