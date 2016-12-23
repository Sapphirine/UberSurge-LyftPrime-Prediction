# UberSurge-LyftPrime-Prediction
Big Data Analytics Project at Columbia University (Fall 2016)

---
name: Yiwen Luo, Yu Gu, Siyan Yue
date: Dec 22, 2016
Course: Big Data Analytics Project
Project: Final Project
---

## Dataset
DataRepo Contains a very small fraction of our actual dataset (around 2.5G)
Link : https://drive.google.com/open?id=0B5hOAHMAiNjcSmJHY2tEd1IwVmM

## Repository Directory
### Data-Collecion
This package contains the data retrieving code from Uber and Lyft API of the project. 
It also contains the handler of DynamoDB for data storage.

## Application-Implementation
This package is the main part of this project, which contains the model, training, testing and API part of the predictive algorithm. 
Moreover, it could read raw data from DynamoDB and do the data parsing, cleaning and preparation.

## Algorithm-Reference
This part contains the references of the major algorithms utilized by this project.

## Frontend
As it named, this part contains the frontend user interface of the project. It parses user's inputs and talks to the backend API.