# import pandas as pd
# import numpy as np

########################## fake data generation ###################
# #################### the fake data generation have some kind of wierd parts, but the idea here is to
# #####################make the data doable for logistic regression

# Set the random seed for reproducibility
# np.random.seed = 42

# Create a DataFrame with 200 rows and specified columns
# df = pd.DataFrame({
#     'age_of_house': np.random.uniform(10, 70, 200),
#     'material_factor': np.random.uniform(0, 1, 200),
#     'cracks_length': np.random.uniform(0, 30, 200),
#     'cracks_width': np.random.uniform(0, 2, 200),
#     'leakage_radius': np.random.uniform(0, 5, 200),
#     'catastrophe_level': np.random.uniform(0, 1, 200),
#     'location_level': np.random.uniform(0, 1, 200),
# })

# #Simulating 'time_until_claim' (number of months until the next fault) using a simple model
# #Assuming a linear combination of features influences the rate parameter 'lambda' for Poisson distribution
# #Note: This is a simplistic approach for demonstration. The actual relationship might be more complex.
# #Calculate a base lambda from features, this is a simplified model for demonstration purposes
# df['lambda'] = (df['age_of_house'] / 10 - df['material_factor'] * 2 + df['cracks_length'] / 10 +
#                 df['cracks_width'] * 5 + df['leakage_radius'] * 2 - df['catastrophe_level'] * 3 +
#                 df['location_level'] * 2)

# #Ensure lambda is positive
# df['lambda'] = df['lambda'].apply(lambda x: np.abs(x) + 1)

# #Simulate 'time_until_claim' from a Poisson distribution based on the 'lambda' rate
# df['time_until_claim'] = np.random.poisson(df['lambda'])

# df.head()
#want the mean of the lambda to be 1/12, on average takes 12 month to file a claim
#new_lambda = 1/12
#df["lambda"] = (df["lambda"]/np.mean(df["lambda"])) * new_lambda
#df['time_until_claim'] = 1/df["lambda"]


############################ Logistic model ###################
#Import the necessary library
# import statsmodels.api as sm

# #Define a binary outcome based on 'time_until_claim'
# #For this example, let's assume a claim will be filed if 'time_until_claim' is less than or equal to 12 months
# df['will_file_claim'] = (df['time_until_claim'] <= 12).astype(int)


# #Predictor variables
# X = df[['age_of_house', 'material_factor', 'cracks_length', 'cracks_width', 'leakage_radius', 'catastrophe_level','location_level']] #
# y = df['will_file_claim']

# #Add a constant to the predictor variable set to include an intercept in the model
# X = sm.add_constant(X)

# #Fit a logistic regression model
# logit_model = sm.Logit(y, X).fit()

# #Print the summary of the model
# print(logit_model.summary())

if __name__ == "__main__":

    import pickle
    import numpy as np
    # # Save the model
    # with open('./logit_model.pickle', 'wb') as f:
    #     pickle.dump(logit_model, f)

    # Load the model
    with open('./logit_model.pickle', 'rb') as f:
        logit_model = pickle.load(f)


    # make prediction for a single data
    # assume new data for now, since the data is so limited

    print("we randomly pick a sample with the age_of_house: 30 years, material_factor: 0.2, cracks_length: 0,\
    cracks_width:2,leakage_radius: 0, catastrophe_level: 0, location_level:0, to predict the probability of filing a file within 6 month")
    sample = [[1,30,0.2,0,2,0,0,0]]
    prob = logit_model.predict(sample)
    print("The probability of filing a claim within 6 month is: {}".format(np.round(prob[0],2)))
