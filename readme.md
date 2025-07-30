# Espresso experiment tracker

_This is a work in progress._

This project was born out of a personal need to find a convenient way to track my experiments with making espresso at home (trying different coffee types, optimising the parameters, as well as my personal evaluation of the results). I also want to store the data in a way that will enable me to analyse it systematically in the future.

The app consists of (1) a database that keep the information, (2) a backend/API that writes to and reads from the database, and (3) a frontend to facilitate data entry and analyses. The project uses `MySQL` for database, `fastAPI` for backend/API, and `streamlit` for frontend with `plotly` for visualisations. 

The current stage is as follows:

- The database has been filled with mock data for testing and demonstration purposes
- The backend/API has been developed to mediate between the frontend and the database
- The frontend has been developed to provide an interface where the user can define new coffee varieties and equipment, add these to the user's inventory, enter new espresso experiments, and visualise existing espresso data

A demo for the data visualisation page is deployed on [Streamlit Community Cloud](https://espr-app-demo.streamlit.app).

Features being developed and planned:

- A chat assistant that uses online resources as context and the user's data as input: a prototype has been implemented in the notebooks.
- An ML model that predicts certain outcomes (e.g. brew ratio, evaluation) from given parameters (e.g. bean type, dose, extraction time)
