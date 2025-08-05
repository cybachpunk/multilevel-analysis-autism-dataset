# Multilevel Modeling of Child Socialization Scores
This project analyzes a longitudinal dataset to explore the relationship between a child's age, expressive language skills, and their socialization development. A multilevel modeling approach is used to account for the correlated, repeated measurements taken from each child over several years.

This work is a critical foundation in assessing health not just in children with ASD but those that could have a form of PDD-NOS, which is inclusive of a range of developmental deficits that do not fall under ASD. As social expectations increase later in childhood and adulthood, poor social awareness in ASD becomes more evident and marked by difficulty in understanding and expressing emotions, deficits in the social aspects of language, as well as failure to notice or comprehend more subtle nonverbal social cues. Most importantly, individuals with ASD who received more total hours of a specific intervention and began participating at younger ages were more likely to have better expressive language outcome and to be placed in a mainstream rather than a special education classroom setting.

Healthcare data is a wide field of vast importance. Building on this work could include more modern datasets with additional named dependent variables, speech to text, computer vision, sentiment analysis, and working with diagnostic overshadowing.

## Dataset: The Child Psychology Journal Autism Study
The analysis is based on data from the following longitudinal study, which provides the context for our variables and methodology. Social deficits have been observed as early as the first year of life, prior to measurement in this dataset.

Anderson, D., Oti, R., Lord, C., and Welch, K. (2009). Patterns of growth in adaptive social abilities among children with autism spectrum disorders. Journal of Abnormal Child Psychology, 37(7), 1019-1034. [National Library of Medicine](https://pmc.ncbi.nlm.nih.gov/articles/PMC2893550/#S1)

### Study Abstract
Adaptive social skills were assessed longitudinally at approximately ages 2, 3, 5, 9, and 13 years in a sample of 192 children with a clinical diagnosis of Autism (n = 93), PDD-NOS (Pervasive Developmental Disorder-Not Otherwise Specified, n = 51), or nonspectrum developmental disabilities (n = 46) at age 2. Growth curve analyses with SAS proc mixed were used to analyze social trajectories over time... The gap between children with autism and the other two diagnostic groups widened with time as the social skills of the latter groups improved at a higher rate.

### Analyzed Dataset Variables Explained
childid (Identifier): A unique ID for each child in the study. This acts as the grouping variable for the random effects in our model.

vsae (Dependent Variable): The Vineland Socialization Age Equivalent score. This continuous variable measures a child's socialization skills and is the primary outcome we are modeling.

age2 (Independent Variable): The age of the child in years at the time of measurement. Note: This is not a continuous measure; data was only collected at ages 2, 3, 5, 9, and 13.

sicdegp (Independent Variable): An Expressive Language Group classification assigned at age two. This is a categorical variable with three levels (1, 2, 3), where higher values indicate more developed expressive language skills.

## Statistical Methodology
This section provides a deeper look into the statistical methods and statsmodels features used in the analysis.

### 1. Modeling Longitudinal Data with Multilevel Models
Standard linear regression assumes that all observations are independent. This assumption is violated here because we have repeated measurements from the same children over time. A Multilevel Model (MLM), or Mixed-Effects Model, is the appropriate tool for this type of longitudinal data as it accounts for the nested structure of the observations.

### 2. Handling Categorical Data: The C(sicdegp) Feature
In the model formula (vsae ~ age2 + C(sicdegp)), the C() wrapper is critical for telling statsmodels to treat sicdegp as a categorical variable.

Why it's necessary: The sicdegp values (1, 2, 3) are labels for distinct groups, not points on a continuous scale.

How it works (Dummy Variables): statsmodels automatically converts the single sicdegp column into a set of binary "dummy variables." It selects one group as the reference level (sicdegp=1) and creates indicator columns for the other levels.

Interpreting the Output: The model's main Intercept represents the baseline vsae for the reference group. The coefficients for C(sicdegp)[T.2] and C(sicdegp)[T.3] show the difference in vsae between Group 2 vs. Group 1 and Group 3 vs. Group 1, respectively.

### 3. Model 1: Random Intercepts for Baseline Differences
This first model assumes that each child has a unique baseline socialization score but that their rate of development over time is consistent. It estimates a random intercept for each child, capturing how much an individual's socialization score consistently differs from the population average across all ages.

### 4. Model 2: Random Slopes for Individual Growth Trajectories
This more flexible model allows each child to have both a unique starting point and a unique growth rate. It estimates both a random intercept and a random slope, capturing how the effect of age on socialization varies from child to child.

### 5. Key Model Parameters and Arguments Explained
groups='childid': This argument specifies the grouping factor for the random effects. It tells the model that observations are nested within each childid.

age_cen: This is a new variable created by "centering" the age variable (age - age.mean()). This is done to make the intercept interpretable (as the value at the mean age rather than at age=0) and to improve the numerical stability of the model fitting process.

re_formula="~ age_cen": This argument in Model 2 specifies the random effects structure. It tells statsmodels to fit a random intercept (implied by default) and a random slope for the age_cen variable.

reml=False: This argument instructs the model to use Maximum Likelihood Estimation (MLE) instead of the default Restricted Maximum Likelihood (REML). MLE is used here to allow for statistically valid comparisons of goodness-of-fit between nested models (i.e., comparing Model 1 to Model 2).