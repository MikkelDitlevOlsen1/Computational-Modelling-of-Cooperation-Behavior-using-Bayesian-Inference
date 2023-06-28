# Computational-Modelling-of-Cooperation-Behavior-using-Bayesian-Inference

Welcome to the project repository! This repository contains seven notebook files located in `Models` folder. These notebooks are the main files used for various tasks related to the project.

## Folder Structure

The repository has the following structure:

- `Models`: Contains the main notebook files for the project.
- `Data_Processing`: Contains the `Data_collection.py` file, which is required to run before using the main notebooks. Please note that this folder does not contain any data, and the user needs to provide the necessary data for processing.
- `MCMC_results`: Contains the results from MCMC runs.
- `Python_scripts`: Contains all the Python functions imported in the models.

## Getting Started

To use the notebooks in this repository, please follow the steps below:

1. Make sure you have the necessary dependencies and libraries installed. You can find the required libraries in the `requirements.txt` file. You can install them using the following command:

pip install -r requirements.txt

2. Run the `Data_collection.py` script located in the `Data_Processing` folder. This script is responsible for collecting and processing the data required for the main notebooks. Please provide the necessary data files or sources as instructed by the script. The processed data will be saved for later use in the main notebooks.

3. Once the data collection and processing are complete, you can proceed to use the main notebook files located in the `Models` folder. These notebooks contain the core functionality and analysis for the project.

## Notebooks

The following is a brief description of each notebook file in the `model` folder:

1. `Classifier.ipynb`: contains classification of the best-fit model for each subject 
2. `Evaluating_mcmc_multi.ipynb`: contains evaluations of the model support and model selection results
3. `Evaluating_mcmc_one.ipynb`: contains evaluations of results from MCMC on the Fehr-Schmidt model
4. `Fehr_schmidt.ipynb`: fits the Fehr-Schmidt model on each subject
5. `MCMC_multi.ipynb`: runs MCMC with the Fehr-Schmidt model and the five alternative utility functions
6. `MCMC_one.ipynb`: runs MCMC on the Fehr-Schmidt model
7. `Utility_maping.ipynb`: maps out the Fehr-Schmidt model and the five alternative utility functions


Feel free to explore and use these notebooks according to your needs.

## Contributing

If you would like to contribute to this project, please follow the standard guidelines for open source contributions. Fork this repository, make your changes, and submit a pull request explaining the purpose and impact of your changes.

## Issues

If you encounter any issues or have suggestions for improvement, please open an issue in the repository. We appreciate your feedback and will address the issues as soon as possible.

Thank you for using this project repository!
