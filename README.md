# project1-noah-psutka

[Visit my site here](https://lingering-dew-8484.fly.dev/)

## _Project Info_

The following project was created by utilizing the following elements.
Python: This is used to run the backend for our server
Flask: [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#virtual-environments) is the framework we use for web development

Required libraries for this project can be located within the requirements.txt file in this repository.
(We will go through downloading these required libraries in Project Setup)


APIs used in this project: TMDB, MediaWiki
TMDB is an API that allows us to pull inforation on movies from their database
MediaWiki is used in this project to generate a wikipedia link correlated to the movie we got from TMDB

## _Project Setup_

### Step 1: Clone this repo

```
git clone git@github.com:noahpsutka/project1-noah-psutka.git
```

### Step 2: Download required libraries

Run the following code in your console.

```
python -m pip install -r requirements.txt
```

### Step 3: Setup API

Acquire an API key from the [TMDB](https://www.themoviedb.org/) website for the API used in this project.
Create a .env file in the folder of your cloned project
it should contain the following,

```
APP_SECRET_KEY = "make a secure random key here"

TMDB_API_KEY = "API key from TMDB"
```

### Step 4: Install Flyctl and Login

We are ready to start working with Fly and that means we need `flyctl`, the CLI app for managing apps on Fly.[Installation guide](https://fly.io/docs/hands-on/install-flyctl/) for installing Fly. Once that is installed you'll want to create an account and [login to Fly](https://fly.io/docs/hands-on/sign-in/).

### Step 5: Configure the App for Fly

Each Fly application needs a `fly.toml` file to tell the system how we'd like to deploy it. That file can be automatically generated with the command `flyctl launch` command. This file is already generated for you this in repository. 
The following is Fly's builtin deployment configurations for Python to generate a fly.toml file.
When running this command we recommend you use the default options.

```cmd
flyctl launch
```

The command `flyctl launch` will also generate a Procfile, the text below shows how it should look

```
web: gunicorn 'insert python file name here':app
```

### Step 6: Deploying the App

The final step required to have your app running on fly.io is by running the follow command.

```
flyctl deploy
```

After deploying your site, use `flyctl status` to see more details.


## _Questions about Project_
What are at least 2 technical issues you encountered with your project? How did you fix them?

```
Issue 1: 
"Error failed to fetch an image or build from source: app does not have a Dockerfile or buildpacks
configured. See https://fly.io/docs/reference/configuration/#the-build-section"

Solution - I had to run the command "fly auth login" before running "flyctl launch" in order to properly
generate Procfile and fly.toml
I was able to find this solution by reaching out to my peers who encountered similar problems.

Issue 2:
"Failed due to unhealthy allocations - no stable job version to auto revert to"

Solution - I had to update my requirements.txt to include all of the libraries that were used in my project
I was able to find this solution by reading the console log, the following line on 
my console told me which library I forgot to add to my requirements.txt
- [info]ModuleNotFoundError: No module named 'dotenv'
```

What are at least 2 known problems (still existing), if any, with your project? (If none, what are two things you would improve about your project if given more time?)

```
1: If I had more time to work on this project I would like to add a more visually appealing frontend layout.
I would have liked to spend more time updating my cascading style sheet.

2: I would also like to add a functionality for users to generate a random movie that matches a user selected genre.
Having a button to rerun the random movie on the site would be easy, but I would want to allow the user to get a random movie from a genre that they like.
```