#imports dependencies
from flask import Blueprint, request, jsonify
import json
import pandas as pd
import ast

#imports the functions to be used in the api calls
import myfunctions

api = Blueprint('api', __name__)

@api.route('/api/getRequirements', methods=['POST'])
def get_requirements():
    data = request.json
    major = data["Major"]
    
    majors = {
        "Computer Science" : "CMSC",
        "Computer Engineering" : "CMPE",
        "Mathematics" : "MATH",
        "Statistics": "STAT",
    }
    major = majors[major]
    
    requirements = {'CMPE' : {'Required Core Classes' : ['ENGL 100', 'ENES 101', 'CHEM 101', 'PHYS 121', 'PHYS 122', 'BIOL 141', 'BIOL 142', 'MATH 151', 'MATH 152', 'CMSC 201', 'CMSC 202', 'CMSC 203', 'CMPE 212', 'PHYS 220', 'MATH 221', 'PHYS 224', 'PHYS 225', 'MATH 225', 'MATH 251', 'CMPE 306', 'CMPE 310', 'CMPE 311', 'CMPE 314', 'CMSC 341', 'CMPE 349', 'CMSC 411', 'CMSC 421', 'CMPE 450', 'CMPE 451'], 
                              'CMPE Technical Electives (A)' : ['CMPE 315', 'CMPE 321', 'CMPE 323', 'CMPE 330', 'CMPE 415', 'CMPE 419', 'CMPE 422', 'CMPE 423', 'CMSC 426', 'CMPE 447', 'CMSC 478', 'CMSC 479', 'CMSC 481', 'CMPE 491'],
                              'CMPE Technical Electives (B)' : ['CMSC 345', 'ENME 403', 'CMSC 422', 'CMSC 425', 'CMSC 426', 'CMSC 431', 'CMSC 435', 'CMSC 441', 'CMSC 442', 'CMSC 443', 'CMSC 455', 'CMSC 483', 'CMSC 486']},
                    'CMSC' : {'Required Core Classes' : ['CMSC 201', 'CMSC 202', 'CMSC 203', 'CMSC 304', 'CMSC 313', 'CMSC 331', 'CMSC 341', 'CMSC 411', 'CMSC 421', 'CMSC 441', 'CMSC 447'], 
                              'CMSC Electives and Technical Electives' : ['CMSC 426', 'CMSC 427', 'CMSC 428', 'CMSC 431', 'CMSC 433', 'CMSC 435', 'CMSC 436', 'CMSC 437', 'CMSC 438', 'CMSC 442', 'CMSC 443', 'CMSC 438', 'CMSC 442', 'CMSC 444', 'CMSC 446', 'CMSC 448', 'CMSC 449', 'CMSC 451', 'CMSC 452', 'CMSC 453', 'CMSC 455', 'CMSC 456', 'CMSC 457', 'CMSC 461', 'CMSC 462', 'CMSC 471', 'CMSC 473', 'CMSC 474', 'CMSC 475', 'CMSC 476', 'CMSC 477', 'CMSC 478', 'CMSC 479', 'CMSC 481', 'CMSC 483', 'CMSC 486', 'CMSC 487', 'CMSC 491', 'CMSC 493'], 
                              'Required MATH Classes' : {'MATH 151', 'MATH 152', 'MATH 221', 'STAT 355'}, 
                              'Science Classes' : ['SCI 101L', 'CHEM 101', 'CHEM 102', 'CHEM 102L', 'PHYS 121', 'PHYS 122', 'PHYS122L', 'BIOL 141', 'BIOL 142', 'GES 286']},
                    'MATH' : {'Required Core Classes' : ['Math 151', 'Math 152', 'CMSC 201', 'MATH 221', 'MATH 225', 'MATH 251', 'MATH 300', 'MATH 301'], 
                              'MATH Upper Level Electives' : ['MATH 306', 'MATH 341', 'MATH 355', 'MATH 365', 'MATH 380', 'MATH 385', 'MATH 390', 'MATH 401', 'MATH 404', 'MATH 407', 'MATH 408', 'MATH 409', 'MATH 410', 'MATH 411', 'MATH 413', 'MATH 421', 'MATH 423', 'MATH 426', 'MATH 427', 'MATH 430', 'MATH 432', 'MATH 441', 'MATH 447', 'MATH 452', 'MATH 456', 'MATH 465', 'MATH 469', 'MATH 475', 'MATH 476', 'MATH 479', 'MATH 480', 'MATH 481', 'MATH 482', 'MATH 483', 'MATH 484', 'MATH 485', 'MATH 486', 'MATH 487', 'MATH 490', 'MATH 495', 'MATH 496', 'MATH 497', 'MATH 499', ], 
                              'Supplementary Requirements' : ['PHYS 121', 'PHYS 122', 'CMSC 203', 'ENME 217', 'PHYS 224', 'PHIL 248', 'ENCH 300', 'PHYS 303', 'ECON 311', 'ENME 315', 'EDUC 320', 'PHYS 321', 'CMPE 323', 'CMSC 341', 'ENME 342', 'PHIL 346', 'PHIL 372', 'ECON 374', 'CHEM 401', 'PHYS 407', 'ENME 410', 'CHEM 415', 'ECON 417', 'ECON 421', 'PHYS 424', 'EDUC 426', 'MATH 432', 'PHYS 440', 'CMSC 441', 'CMSC 442', 'CMSC 443', 'CMSC 451', 'CMSC 452', 'CMSC 453', 'BIOL 463']},
                    'STAT' : {'Required Core Classes' : {'MATH 151', 'MATH 152', 'MATH 221', 'MATH 251', 'STAT 350', 'STAT 351', 'STAT 355', 'ENGL 393' 'STAT 433', 'STAT 451', 'STAT 453', 'STAT 454'},
                              'MATH/STAT Upper Level Electives' : ['CMSC 201', 'CMSC 202', 'MATH 301', 'POLI 301', 'MATH 302', 'PSYC 311', 'PSYC 312', 'CMSC 331', 'CMSC 341', 'MATH 341', 'MATH 355', 'STAT 365', 'MATH 381', 'MATH 385', 'STAT 405', 'IS 410', 'STAT 414', 'STAT 417', 'STAT 418', 'STAT 419', 'SOCY 419', 'IS 420', 'ECON 421', 'ECON 422', 'ECON 423' 'MATH 426', 'IS 427', 'MATH 430', 'STAT 432', 'MATH 441', 'MATH 452', 'STAT 455', 'STAT 470', 'STAT 490', 'STAT 496', 'STAT 499']}
                    }
    
    major_requirements = requirements.get(major, {})
    # Convert sets to lists
    major_requirements_serializable = {key: list(value) for key, value in major_requirements.items()}

    response = jsonify(major_requirements_serializable)
    return response, 200

@api.route('/api/getRecommendations', methods=['POST'])
def get_recommendations(completed_courses, major):
    recs = myfunctions.get_recs(completed_courses, major)
    return jsonify(recs)