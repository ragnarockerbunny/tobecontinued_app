# To Be Continued
#### Video Demo: https://youtu.be/_DPFseEaMJw
#### Description:
To Be Continued is a web app built to solve the issue of keeping track what films a user wants to watch. As such, users can create an account, they will be given a watchlist and by consuming the The Movie Database's web api, they can keep track of films they want to watch. Built with HTML, CSS, JINJA, SQL and Python.

Here's a breakdown of each file in the project:
- app.py:
They python flask app that handles web routing
- data.db:
The database that contains the tables for user watchlists and user login data
- requirements.txt:
the requirements text document which tells  the hosting server which python modules require installing
- README.md:
This file which explains the project
- addedToList.html:
a page users are directed to confirming a film was added to their watchlist
- error.html:
An html page that users are redirected to when the app encounters an error or unexpected user behaviour
- home.html:
The home page which shows the user their watchlist
- layout.html:
The layout that every web page extends with JINJA containing elements such as the nav and footer
- login.html:
A page with a log in form for users
- logout.html:
A page users are directed to after a succesful log out
- register.html:
A page with a form for registering users
- searchresults.html
A page that displays the results of a search.

My thought process on design wasn't particularly complex. I knew that I wanted to have user accounts and thus required databases and therefore SQL. My first thought was to simply use the python SQLite library, however this proved unworkable. SQLite works fine enough on a single thread deployment server but locally throws errors, especially since I was developing from a Windows 10 computer with a multicore processor capable of handling several threads. After some research I came upon the SQLAlchemy library, and this worked wonderfully. My database design was rather pimitive in itself though. I have two tables, one for users and one for the items each user adds to their watchlist. A user watchlist is simply an SQL query that fetches every watchlist item attached to a specific user ID, which is stored in a user session. My initial idea was to give each user their own table but this quickly proved infeasible. Simplifying was the smart choice here.

For the sitemap I also decided to keep it as simple as possible. A home page that displays everything the user needs to see and while there was a dedicated search page early in the project's lifespan, I ultimately moved the search functionality to the nav element for quick and easy access. The other main pages include a "log in" page, a "register" page, a page for search results and the homepage. Minimum clicks.

As for the film database I briefly considered populating a database of my own or asking users to populate the database for me but in the end decided to rather go with a free API. This required learning a bit about using APIs in conjunction with Python and Flask but amounted mostly to just including the requests library and using the get method provided, as well as reading through the documentation.

I created a little SVG logo using the program Inkscape to serve both as a link to return to home and as a branding touch in the nav element.

For the front end I imported the bootstrap CSS library as well as the bootstrap icons library, and combined it with my own CSS. I tried to simplify down to a three colors and keep the scheme unified that way. 

There are many other unnamed, perhaps even unconscious decisions that I've made regarding the design of the web app, I feel that I have touched on all the most important aspects. In conclusion, and this was CS50!