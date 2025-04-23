# Espresso experiment tracker

_This is a work in progress in early stages._

This project was born out of a personal need to find a convenient way to track my experiments with making espresso at home (trying different coffee types, optimising the parameters, as well as my personal evaluation of the results). I also want to store the data in a way that will enable me to analyse it systematically in the future.

The idea is to have (1) a database that will keep the information, (2) a backend that will write to and read from the database, and (3) a frontend to facilitate data entry and analyses. The current stage is as follows:
- A fundamental database structure has been defined
- The backend has been developed to provide what the frontend needs at the current stage
- The frontend has been implemented for basic functions
- Currently, it is functional for storing information about espresso experiments, as well as entering the necessary data (equipment and coffee beans). Data analysis features have not yet been implemented.

The project uses `MySQL` for database, `fastAPI` for backend, and `streamlit` for frontend. 