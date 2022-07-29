
# Discrete Choice Model Estimation with Biogeme

### Includes


import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.models as models
from biogeme.expressions import Beta


### Data Import and Preparation

scenario_name = "test_scale"           # Estimation scenario

# Read Data
df = pd.read_csv("sioux_falls.dat")
database = db.Database('sioux_falls', df)

# import variable names to Python variables
globals().update(database.variables)

# Get estimation data sample

### Variable Definitions

# Parameters beta to be estimated, given as (varname, defaultvalue, lowerbound, upperbound, lock)
ASC_CAR = Beta('ASC_CAR', 0, None, None, 1)    # ASC for car is normalised to 0
ASC_PT = Beta('ASC_PT', 0, None, None, 0)
ASC_WALK = Beta('ASC_WALK', 0, None, None, 0)
ASC_UAM = Beta('ASC_UAM', 0, None, None, 0)
B_TIME = Beta('B_TIME', 0, None, None, 0)
B_COST = Beta('B_COST', 0, None, None, 0)
SCALE = Beta('SCALE', 1, 0,None, 0)

# Independent Variables (from database)
TIME_CAR = time_car
TIME_PT = time_pt
TIME_WALK = time_walk
TIME_UAM = time_uam
COST_CAR = cost_car
COST_PT = cost_pt
COST_WALK = cost_walk
COST_UAM = cost_uam

# Dependent variable: choice
CHOICE = choice

# Utility Functions
V1 = ASC_CAR    + B_TIME * TIME_CAR    + B_COST * COST_CAR
V2 = ASC_PT     + B_TIME * TIME_PT     + B_COST * COST_PT
V3 = ASC_WALK   + B_TIME * TIME_WALK   + B_COST * COST_WALK
V4 = ASC_UAM    + B_TIME * TIME_UAM    + B_COST * COST_UAM

# Association between utility functions and numbering of alternatives
V = {1: SCALE*V1, 2: SCALE*V2, 3: SCALE*V3, 4: SCALE*V4}

# (availability)
av = None


### Define model and run


# Model definition: Contribution of each parameter to the log likelihood+
logprob = models.loglogit(V, av, CHOICE)

# Biogeme object
biogeme = bio.BIOGEME(database, logprob)
biogeme.modelName = scenario_name

# Estimate parameters
results = biogeme.estimate()

# Return results as df
dfResults = results.getEstimatedParameters()
print(dfResults)

