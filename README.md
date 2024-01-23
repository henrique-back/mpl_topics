# mpl_topics

## Overview

This GitHub project is part of ongoing research, and its results are currently under consideration for publication. The purpose of sharing this code publicly is to facilitate reproducibility and provide transparency in the methods used.

A significant portion of the code relies on third-party libraries and modules, contributing to the robustness and efficiency of the implementation. Notably, we leverage popular libraries such as scikit-learn and BERTopic, both of which are publicly available and widely used in the research community.

Please feel free to explore the project, reproduce our findings, and contribute to the development. Feedback and contributions are highly appreciated!

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Data](#data)
4. [Model Training](#model-training)
5. [Results](#results)

## Installation
Before starting, make sure you have all the required dependencies installed.
To ensure reproducibility, make sure to have the following versions installed:

- OS Windows 11
- Python 3.7.16
- Bertopic version: 0:15:0

## Usage
This project is organized into three folders, each corresponding to a different stage of the analysis:

1. **get_data**: Access to the SCOPUS API and construction of the dataset.
2. **NER**:  Named-entity recognition. Focuses on oceanic basin classification.
3. **bertopic**: Involves topic modeling, a combined analysis for the two classifications, and meta-data analysis, primarily publication dates and citation counts.

### Data

Unfortunately, the complete process to retrieve data from SCOPUS cannot be fully reproduced due to the confidentiality of the API key used. However, this does not impact the usage of the project since the complete dataset (`alldata.csv`) is stored in this repository for your convenience.

If you have access to your own SCOPUS API key, you can update the dataset by following these steps:

1. Open the `scopusapi.ipynb` file.
2. Replace the existing API key with your own.
3. Optionally, modify the query to suit your needs.
4. Run the notebook to fetch and update the dataset.

## Model Training
To train the topic model, follow these steps:

1. **Generate Embeddings**: Start by running the `generate_embeddings.ipynb` file. This notebook pre-calculates embeddings to speed up the topic modeling process. The generated embeddings are stored and then passed to BERTopic during model generation.

2. **Hyperparameter Tuning**: Run the `hyperparameter_tuning.ipynb` file. This notebook conducts a randomized search on several parameters of BERTopic, generating 100 models. These models are then assessed and a decision is made on which model to use for the topic modeling task.

3. **Review BERTopic**: Finally, run the `review_bertopic.ipynb` file. This notebook provides the core analysis of the research.

## Results
The main results can be found in the 'graphs' folder. All results can be visualized in the .ipynb files. Figures will only display if using an appropriate renderer (not the case in GitHub)
