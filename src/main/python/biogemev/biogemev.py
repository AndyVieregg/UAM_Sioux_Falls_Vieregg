#!/usr/bin/env python
# coding: utf-8

# Discrete Choice Model Estimation with Biogeme

### Includes

import pandas as pd
from src.main.python.biogemev.biogemev import Beta


def estimate_mnl():


    ### Data Import and Preparation

    data_path = "Biogeme/non_uam_bl_0719/"    # MATSim scenario
    scenario_name = "test_mnl_0726"           # Estimation scenario


    # Read Data
    df = pd.read_csv(data_path + "sioux_falls.dat")
    database = db.Database('sioux_falls', df)

    # import variable names to Python variables
    globals().update(database.variables)

    # Get estimation data sample


    ### Variable Definitions



    # Parameters beta to be estimated, given as (varname, defaultvalue, lowerbound, upperbound, lock)
    ASC_CAR = Beta('ASC_CAR', 0, None, None, 1)    # ASC for car is normalised to 0
    ASC_PT = Beta('ASC_PT', 0, None, None, 0)
    ASC_WALK = Beta('ASC_WALK', 0, None, None, 0)
    B_TIME = Beta('B_TIME', 0, None, None, 0)
    B_COST = Beta('B_COST', 0, None, None, 0)

    # Independent Variables (from database)
    TIME_CAR = time_car
    TIME_PT = time_pt
    TIME_WALK = time_walk
    COST_CAR = cost_car
    COST_PT = cost_pt
    COST_WALK = cost_walk

    # Dependent variable: choice
    CHOICE = choice

    # Utility Functions
    V1 = ASC_CAR    + B_TIME * TIME_CAR    + B_COST * COST_CAR
    V2 = ASC_PT     + B_TIME * TIME_PT     + B_COST * COST_PT
    V3 = ASC_WALK   + B_TIME * TIME_WALK   + B_COST * COST_WALK

    # Association between utility functions and numbering of alternatives
    V = {1: V1, 2: V2, 3: V3}

    # (availability)
    av = None


    ### Define model and run


    # Model definition: Contribution of each parameter to the log likelihood+
    logprob = models.loglogit(V, av, CHOICE)

    # Biogeme object with settings
    biogeme = bio.BIOGEME(database, logprob)
    biogeme.modelName = scenario_name
    biogeme.saveIterations = False          # don't save the iterations, but start from scratch each time
    biogeme.generateHtml = False
    biogeme.generatePickle = False          # don't output any files, results will be output to SQL

    # Estimate parameters
    results = biogeme.estimate()

    return results

