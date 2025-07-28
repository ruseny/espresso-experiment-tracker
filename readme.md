# Espresso experiment tracker

_This is still a work in progress._

This project was born out of a personal need to find a convenient way to track my experiments with making espresso at home (trying different coffee types, optimising the parameters, as well as my personal evaluation of the results). I also want to store the data in a way that will enable me to analyse it systematically in the future.

The app consists of (1) a database that keep the information, (2) a backend/API that writes to and reads from the database, and (3) a frontend to facilitate data entry and analyses. The current stage is as follows:
- The database has been populated with mock data
- The backend/API has been developed to mediate between the frontend and the database
- The frontend has been developed to define new coffee varieties and equipment, add these to the user's inventory, enter new espresso experiments, and visualise existing espresso data

The project uses `MySQL` for database, `fastAPI` for backend/API, and `streamlit` for frontend with `plotly` for visualisations. 

A demo for the data visualisation page is deployed on [Streamlit Community Cloud](https://espr-app-demo.streamlit.app).