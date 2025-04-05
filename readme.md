# Espresso experiment tracker

_This is a work in progress in early stages._

This project was born out of a personal need to find a convenient way to store the information about my amateurish experimentation with making espresso at home (trying different coffee types, optimising the parameters, as well as my personal evaluation of the results). I also want to store the data in a way that will enable me to analyse it systematically in the future.

The idea is to have (1) a database that will keep the information, (2) a backend that will write new information to the database, and provide data from the database for analyses, and (3) a frontend to facilitate data entry and analyses. The current stage is as follows:
- A basic database structure has been defined
- Preliminary ideas about the backend endpoints have been implemented
- The frontend has been minimally created, only enough to test these preliminary ideas

The project uses MySQL for database, and fastAPI for backend. The frontend pages are implemented from within fastAPI through jinja templating.