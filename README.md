Questioner
---

The questioner app is a web that allows users who are attendees of a meetup to be able to raise questions they would like to discuss in the meetup. The questions are then voted on by fellow users to determine which has more priority over the others. The question with most votes is deemed as one with a highest priority.

## QUESTIONER API V1
---

Badges
---
[![Build Status](https://travis-ci.org/kburudi/the-Questioner-Api.svg?branch=develop)](https://travis-ci.org/kburudi/the-Questioner-Api)
[![Coverage Status](https://coveralls.io/repos/github/kburudi/the-Questioner-Api/badge.svg?branch=develop)](https://coveralls.io/github/kburudi/the-Questioner-Api?branch=develop) :smiley:


## What is required

- Python3
- Flask
- Postman
- Pytest
- Git
- Python3 pip

## How to get started

1. Clone the repo

   > `https://github.com/kburudi/the-Questioner/`

2) Checkout delelop branch

   > `git checkout develop`

## First install

1. python3

   > `sudo apt-get install python3`

2. install python3 pip

   > `sudo apt-get install python3-pip`

3. install vitual environment

   > `pip3 install virtualenv`

4. checkout develop branch

   > `git checkout develop`

5. create the virtual environment

   > `virtualenv env`

6. Activate the vitualenv in the parent directory of your **"env"**

   > `source env/bin/activate`

7. Install requirement

   > `pip install -r requirements.txt`

8. Run the app

   > `python3 run.py`


## Endpoints to use on postman

   | Endpoints                                  |               Functions                |
   | ------------------------------------------ | :------------------------------------: |
   | POST/api/v1/signup                         |            create new user             |
   | POST/api/v1/login                          |        sign in to your account         |
   | POST/api/v1/meetups                        |             create meetups             |
   | GET/api/v1/meetups                         |            get all meetupss            |
   | GET/api/v1/meetups/&lt;id&gt;              |         get a specific meetups         |
   | GET/api/v1/meetups/upcoming                |        get all upcoming meetups        |
   | POST/api/v1/questions                      |       add question for a meetups       |
   | GET/api/v1/questions                       | view all questions for a given meetups |
   | POST/api/v1/meetups/&lt;id&gt;/rsvp        |     respond to meetups invitation      |
   | PATCH/api/v1/questions/&lt;id&gt;/upvote   |           upvote a question            |
   | PATCH/api/v1/questions/&lt;id&gt;/downvote |          downvote a question           |
   | POST/api/v1/questions/&lt;id&gt;/          |        view a specific question        |
   | POST/api/v1/questions/&lt;id&gt;/comment   |         comment on a question          |
   | GET/api/v1/questions/&lt;id&gt;/comment    |    view all comments on a question     |
   | DELETE/api/v1/meetups/&lt;id&gt;           |            delete a meetups            |


## Authors

Trevor Kurland

## Acknowledgements

1. Andela-Workshops
2. Team-mates
