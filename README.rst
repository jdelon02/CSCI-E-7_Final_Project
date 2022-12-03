RecipeSite
=======================

This project is a django project to create and store recipes. 
The roadmap for this project has eveolved as I learn more in each class.
The eventual goal is to deploy this to a public hosting enviro. 

I want to evolve the site to be a social media platform, but one where the family unit (group) becomes the central hub for content.
Someone signs up, and either joins an existing family, or starts their own.  It also creates relationships between families (think sisters who are wed to others)  
Once a family has members, they can share recipes between them, plan family events, and more.  
I don't know if this will ever be completed, but it is a fun project that I have been allowed to continue evolving in each class.

The following functionality is in a working state:

* Login ability
* Create recipes
* Bookmark others recipes
* Like/unlike recipes (may evolve to a rating system)
* Scrap recipes from other sites.

The functionality I still need to develop:

* Group/Family membership (and group relations between families)
* Group Family approval process (how to approve relatinships)
* Different entities beyond recipes (think "family game night" events, picture sharing, etc...)
* Twitter-like feeds for groups.

Meta
----

Author:
    Jeremy DeLong

Status:
    maintained, in development

Version:
    1.4

Django Version:
    3.2


Usage
-----

Site can be cloned from github, and uses a sqlite3 db as backend (for now).
To run: 
* clone, 
* create migrations, 
* run migrations, 
* run server.

Documentation
-------------

#. When site is run on server, first step is to register an account.  
#. Once that is done, login to site. As logged in user, you can search, add, update, and view recipes on the site.
#. You can bookmark favorites and like recipes from other people.
#. For this project, I added abiity to scrape a recipe, and then edit it.

Libraries Used
--------------
I have added several libraries to the overall project for the current iteration.  
The list is available at https://raw.githubusercontent.com/jdelon02/CSCI-E-7_Final_Project/main/Pipfile

For the Scraper, the site uses 3 main libraries.  
One, a recipe scaper library:

* openeats-recipe-scraper

Two, I also had to add a workaround because many of the sites I attempted to scrape had Bot/DDOS protection on them provided by cloudflare.

* cloudscraper

Three, urlib to scrape images and save them.

Specific Changes for Final Project for: CSCI E-7 Section 1

#. Added abiity to scrape recipes from other sites using django form (no model, since it inherits recipe), and scraper libs.
#. Used regex to parse prep time (hh:mm).
#. Used regex to parse cook time (hh:mm).
#. Used urlib to save image to file.

Caveats
-------
* I did NOT put in a check to see if recipe was already in system.  Since I am still developing, I wanted to be able re-run exact import in order to see progress.
* If parse error occurs, it just bounces to home page.  I need to add better error control/checking.