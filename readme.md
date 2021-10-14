### by S Midianko
### spring 2021

See the screeshots of the mplemented application here: https://www.figma.com/file/reizHCaHHSsg09HOfkFX8r/CS162-assi?node-id=0%3A1

## Structure of the submitted .zip:
\kanban-app
  \__pycache__
  \static
   \js
     -function.js
   \styles
     -kanbanapp.css
 \templates
   -index.html
 \test
   -test_todo.py
 -kanban.db
 -kanbanapp.py
 -testing.db

## Specific details about the files:
- Main application routing is defined in `kanbanapp.py`
- In `static` we have: 
  - Javascript function is used to implement a dynamic frontend that enables the user to open the form for submitting another todo, wip, or done task
  - kanbanapp defines 11 necessary css classes for styling
- In `templates` we have: 
  - html code defining markdown for the page
- Furthermore, there are two databases, one for actual application and the other is for testing.

## Unit tests implemented
By running `python3 -m unittest discover test` you can check if the implementation passes three of the defined tests (for adding, modifying, and deleting the task).

## Extra features implemented: 
1/ tags for each task -- given my own experience, I decided to implement tags per task feature, allowing users to see which tasks are of what type. 

## Improvements that could be made: 
1/ allow a user to define the tag on his own and store it in the db. 
2/ login & authentification of the user.

## You can also see Figma here
https://www.figma.com/file/reizHCaHHSsg09HOfkFX8r/CS162-assi

