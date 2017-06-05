# TO-DO LIST

1. Complete .config files
    - server.config
    - variable.config

2. Add method/function to import .config files into DB and update as required.
    - config files should be able to be imported by a common method/function

3. METHOD: DB connection

4. METHOD: create collections

5. METHOD: add documents
    - cable types
    - cable runs

 6. METHOD: Export function
    - Allows export of reports etc.
    - Makes use of aggregation and map/reduce capabilities of the software.

 7. METHOD: display data via UI
    - allow grouping by equipment number

 8. METHOD: Tag generation
    - Allow generation of tags via simple syntax

 9. METHOD: search function

 10. METHOD: add/update documents
     - Method to allow modification/addition of documents

 11. METHOD size cable/cable run

 12. MongoDB: Define/update collections for:
    - Instrument list
    - Cable Schedule
    - Area list
    - Drawing list
    - Equipment list → update to act a datasheets for the equipment
    - Variable storage → contain the latest numbers for tags, etc

13. METHOD: select cable

14. How do you create and use templates for equipment contained within the database? You should be able to have a base class and then add to it depending on the details that it requires.

15. JSON objects should be addressed by functions within the code?

16. Each collection should be a a class.

17. Should `voltRating` be an embedded document that allows the phase-earth and phase-phase voltages of the cables to be defined? This would have merit.
