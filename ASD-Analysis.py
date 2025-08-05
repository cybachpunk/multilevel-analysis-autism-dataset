# ----------------------------------------------------------------
# 1. IMPORT PACKAGES AND LOAD DATA
# ----------------------------------------------------------------
import numpy as np
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt

print("--- Loading and Preparing Data ---")
# Read in the Autism Data from the CSV file
# Ensure 'autism.csv' is in the same directory as this script.
try:
    dat = pd.read_csv("autism.csv")
except FileNotFoundError:
    print("Error: 'autism.csv' not found. Please place it in the correct directory.")
    exit()

# Drop rows with any missing values to clean the dataset
dat = dat.dropna()
print("Data loaded successfully. Shape after dropping NA's:", dat.shape)
print(dat.head())
print("\n" + "="*40 + "\n")


# ----------------------------------------------------------------
# 2. EXPLORATORY DATA ANALYSIS
# ----------------------------------------------------------------
print("--- Generating Exploratory Plots ---")
# The dataset only tracks specific ages when the child was measured: 2, 3, 5, 9, and 13.
# These plots help visualize the relationship between age and socialization.

# Scatterplot to show the general trend
plt.figure(figsize=(10, 6))
sns.scatterplot(x="age", y="vsae", data=dat, alpha=0.6)
plt.title('Socialization Score (VSAE) vs. Age')
plt.xlabel('Age (years)')
plt.ylabel('VSAE Score')
plt.grid(True)
plt.show()

# Boxplot to see distribution at each specific age
plt.figure(figsize=(10, 6))
sns.boxplot(x="age", y="vsae", data=dat)
plt.title('Distribution of VSAE Scores at Each Measured Age')
plt.xlabel('Age (years)')
plt.ylabel('VSAE Score')
plt.show()
print("Plots have been generated and displayed.")
print("\n" + "="*40 + "\n")


# ----------------------------------------------------------------
# 3. MODEL 1: RANDOM INTERCEPTS MULTILEVEL MODEL
# ----------------------------------------------------------------
print("--- Fitting Model 1: Random Intercepts ---")
# This model includes a random intercept for each child to account for
# repeated measures. 'C(sicdegp)' treats the numeric variable as categorical.

# Specify the model formula
mlm_mod1 = sm.MixedLM.from_formula(
    formula='vsae ~ age + C(sicdegp)',
    groups='childid',
    data=dat
)

# Fit the model using Maximum Likelihood Estimation (MLE)
# REML=False is specified for MLE to allow for likelihood ratio tests between models.
mlm_result1 = mlm_mod1.fit(reml=False)

# Print the summary of the model fit
print(mlm_result1.summary())
print("\n" + "="*40 + "\n")


# ----------------------------------------------------------------
# 4. MODEL 2: RANDOM INTERCEPTS AND SLOPES MODEL
# ----------------------------------------------------------------
print("--- Fitting Model 2: Random Intercepts and Slopes ---")
# This model allows each child to have a unique starting point (intercept)
# and a unique rate of change over time (slope for age).
# Centering the 'age' variable is a common practice for random slope models
# to aid in interpretation and model stability.

dat["age_cen"] = dat["age"] - dat["age"].mean()

# Specify the model with a random intercept and a random slope for centered age.
# The `re_formula="~ age_cen"` specifies a random intercept (implied) and
# a random slope for the 'age_cen' variable.
mlm_mod2 = sm.MixedLM.from_formula(
    formula='vsae ~ age + C(sicdegp)',
    groups='childid',
    re_formula="~ age_cen",
    data=dat
)

# Fit the model
mlm_result2 = mlm_mod2.fit(reml=False)

# Print the summary of the fit
print(mlm_result2.summary())
print("\n" + "="*40 + "\n")