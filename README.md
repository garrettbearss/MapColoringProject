# MapColoringProject
Problem Description:
Write a four color map coloring program for counties of Ohio (or states in USA) using
constraint based programming. Color the water sources such as lakes and sea blue, and
adjoining counties (or states) with four colors different than the counties.

Problem Solution:
Using a json file containing Ohio's counties and the following heuristics:
- Most Constrained
- Most Contraining
- Least Constrained

Color the map of Ohio's counties with each county having different colors than neighboring
counties. The graph is displayed at each step along with the lookahead table. After giving
the inital county it employs the heurisitics to recursively color the map checking with the
lookahead table to make sure there is a viable solution to the map at each state.

Note:
In order to run the program you will need to modify the path of the json file to where it is
stored on the machine running the program.
