#!/usr/bin/env python
# coding: utf-8

# Discrete Choice Model Estimation with Biogeme

import os
import logging
import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta
from pathlib import Path
from datetime import datetime


def estimate_mnl(ms_scenario="default", no_validation_slices=10, is_uam=False):
    data_path = "Biogeme/" + ms_scenario    # MATSim scenario
    scenario_name = "mnl_validation_0812"   # Estimation scenario

    # Switch to data directory
    Path(data_path).mkdir(parents=True, exist_ok=True)
    original_wd = os.getcwd()
    os.chdir(data_path)

    # Read Data

    logging.info("Reading data")

    df = pd.read_csv("sioux_falls_0812.dat")
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


    # UAM-only parameters and variables
    if is_uam:
        ASC_UAM = Beta('ASC_UAM', 0, None, None, 0)
        TIME_UAM = time_uam
        COST_UAM = cost_uam

        V4 = ASC_UAM + B_TIME * TIME_UAM + B_COST * COST_UAM

        V.update({4: V4})

    # (availability)
    av = None


    # Switch to output dir
    time_str = datetime.now().strftime("%m%d-%H%M")
    output_dir_str = scenario_name + "/out-" + time_str
    Path(output_dir_str).mkdir(parents=True, exist_ok=True)
    os.chdir(output_dir_str)

    logging.info("Estimating Biogeme model")

    # Model definition: Contribution of each parameter to the log likelihood+
    logprob = models.loglogit(V, av, CHOICE)

    # Biogeme object with settings
    biogeme = bio.BIOGEME(database, logprob)
    biogeme.modelName = scenario_name
    biogeme.saveIterations = False  # don't save the iterations, but start from scratch each time

    # Estimate parameters
    results = biogeme.estimate()

    logging.info("Done")

    # Validation

    # skip if 0 slices desired
    if no_validation_slices == 0:
        return results, None, scenario_name, time_str

    logging.info("Validation")

    validation_data = database.split(slices=no_validation_slices)

    validation_results = biogeme.validate(results, validation_data)

    ll_list = []
    for slide in validation_results:
        ll_list.append(slide["Loglikelihood"].sum())

    # Change back to original working directory
    os.chdir(original_wd)

    return results, ll_list, scenario_name, time_str
