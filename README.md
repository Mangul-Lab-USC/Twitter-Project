# Twitter-Project
This project focuses on analysing the PubMed data in terms of usage of twitter by biomedical researchers. The github repository contains the links to the datasets 
and the code that was used for our study : ["Unlocking the microblogging potential for science and medicine"](). The repository is under development. 

**Table of contents**

* [How to cite this study](#how-to-cite-this-study)
* [Reproducing results](#reproducing-results)
  * [Modules](#modules)
  * [Data](#data)
  * [Scripts](#scripts)
  * [Notebooks and Figures](#notebooks-and-figures)
* [License](#license)
* [Contact](#contact)


# How to cite this study

> Have to add.


# Reproducing results

## Modules

We have evaluated the PubMed data which contains around 11 million scientists collected from 1.8 million papers which were published between 2000 and 2020. Python modules 
used for analysing data are Scholarly, Tweepy, Email, Smtplib, Beautiful Soup 4 and Google API. We have also used NLP techniques like Google BERT, Convolutional neural networks (CNNS),
Random forests and Naive Bayes for classification of tweets. For NLP training of our model, we have used Keras, NLTK and Tensorflow.


## Data

Data we used for our study is PubMed data which contains basic information about the scientists like their first name, last name and journal name. Then we extracted Twitter 
data using Tweepy and their essential information like affiliation, citations, h-index etc. using Scholarly module. For NLP purpose, we used the open-sourced dataset provided
by NLTK python module and manually labelled dataset which was prepared by USC researchers. 

## Scripts

The scripts to prepare the dataset are present in the repository. 

## Notebooks and Figures

We have prepared Jupyter Notebooks that utilize the data described above to reproduce the results and figures presented in our manuscript.

* [Figure1 Jupyter Notebook]()
* [Figure2 Jupyter Notebook]()
* [Figure3 Jupyter Notebook]()
* [Figure4 Jupyter Notebook]()
* [Figure5 Jupyter Notebook]()
* [Supplementary Figures Jupyter Notebook]()

# License

This repository is under MIT license. For more information, please read our [LICENSE.md](LICENSE) file.


# Contact

Please do not hesitate to contact us (mangul@usc.edu) if you have any comments, suggestions, or clarification requests regarding the study or if you would like to contribute to this resource.