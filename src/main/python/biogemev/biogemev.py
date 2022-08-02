#!/usr/bin/env python
# coding: utf-8

# Discrete Choice Model Estimation with Biogeme

### Includes

import os
import pandas as pd
#import numpy as np
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta
from pathlib import Path


def estimate_mnl():
    data_path = "Biogeme/non_uam_bl_0719/"  # MATSim scenario
    scenario_name = "test_mnl_0726"  # Estimation scenario

    # Switch to data directory
    Path(data_path).mkdir(parents=True, exist_ok=True)
    original_wd = os.getcwd()
    os.chdir(data_path)

    # Read Data
    print(os.getcwd())
    df = pd.read_csv("sioux_falls.dat")
    database = db.Database('sioux_falls', df)

    # import variable names to Python variables
    globals().update(database.variables)

    # Variable definitions
    # Parameters beta to be estimated, given as (varname, defaultvalue, lowerbound, upperbound, lock)
    ASC_CAR = Beta('ASC_CAR', 0, None, None, 1)  # ASC for car is normalised to 0
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
    V1 = ASC_CAR + B_TIME * TIME_CAR + B_COST * COST_CAR
    V2 = ASC_PT + B_TIME * TIME_PT + B_COST * COST_PT
    V3 = ASC_WALK + B_TIME * TIME_WALK + B_COST * COST_WALK

    # Association between utility functions and numbering of alternatives
    V = {1: V1, 2: V2, 3: V3}

    # (availability)
    av = None

    # Model definition: Contribution of each parameter to the log likelihood+
    logprob = models.loglogit(V, av, CHOICE)

    # Biogeme object with settings
    biogeme = bio.BIOGEME(database, logprob)
    biogeme.modelName = scenario_name
    biogeme.saveIterations = False  # don't save the iterations, but start from scratch each time

    # Estimate parameters
    results = biogeme.estimate()

    # Change back to original working directory
    os.chdir(original_wd)

    return results
