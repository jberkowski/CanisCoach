# CanisCoach

Web application created for dog owners and trainers. Its essence is to help effectively
schedule workouts with dogs and keep track of their results.

The Problem:

Dog owners that want to regularly do sport sessions often have trouble keeping records.
This issue is inflated when one person has multiple dogs which participate in many different
disciplines. Keeping track of primary/secondary/supplemental trainings is a tedious task.

The Solution:

CanisCoach makes it all easier, giving user one-stop solution to schedule future workouts
and review the past ones. The rich statistical database helps keep track of the most important KPIs
history.

The user:
User is a person (human), usually a dog owner or dedicated trainer. Each user has separate account.
Each account can create multiple dog profiles linked to this handler account.


## MVP functions:

    - User can register their account, login, logout
    - One user's data is not visible to another users
    - User can add/delete/edit multiple dogs profiles linked to their account
        - Any deletion within system is really a deactivation. No data is ever lost,
          only set to non-visible/not accounted
    - User can schedule workouts with minimum data like:
        - date and time
        - duration
        - discipline
        - dog involved (including multiple dogs*)
            - for multiple dogs workouts, every dog gets their own training record
        - goals for this particular workout
    - User can mark workout as completed or cancelled
        - for completed workouts, user can add/edit duration, score and note
    - User can review history of their past workouts


## Main database tables:
    - users (info about user, like id, user email, password hash, creation date)
    - dogs (info about dog, like id, owner id, breed, birth date)
    - disciplines (list of discilines, can be default/public or private)
    - workouts (each data workout, separated by user, dog, discipline, planned/completed/cancelled)
        - Each workout record belongs to exactly one dog
    - workout_groups (helps create multiple workouts for many dogs from one workout form)
    - breeds (list of dog breeds)

## Business rules:

    - each user can see only their own data
    - each dog belongs to one user
    - each workout belongs to one user
    - each workout belongs to exactly one dog
    - one planning form can create multiple workout records
    - public disciplines are visible to all users
    - private disciplines are visible only to the user who created them
    - planned workouts do not require score
    - completed workouts may have score and/or note
    - cancelled workouts are not counted as completed workouts in statistics
    - workout duration is calculated from start and end time, but can be manually adjusted

## Files structure

### app.py

Contains main body of application. Starts with importing all necessary models and functions.

Configures SQLite database, initializes application, migrates DB models.

Contains all routes used in the project. Routes are segregated into groups:
one group is responsible for functions regarding dogs (presentation, edition, insertion, deletion), the next is responsible for authorization, the next for workouts.

### models.py

Describes models used in project database.

### extensions.py

Defines base class. Also, since db models are in a file separate from app.py, extension 
objects had to be included in third file to avoid cyclical import.

### helpers.py

Contains one helper function - login_required.

### templates/

Templates folder holds all .html files that will be filed with data and create my application pages.

### migrations/

Migrations folder and first migration file has been created by Flask-Migrate.
Second and third migrations have been created by me to seed breeds and disciplines tables.

## Next steps:

    - User can view basic statistics, including:
        - number of workouts per dog/discipline
        - duration of workouts per dog/discipline
        - workout scores
        - date range filter with optional quick presets like week, month, year,
        all time
    - User can add their own disciplines. Disciplines added by users are for their use only
    - Add browsing system, so users can search and view other users and their dogs
    - Message system, so users can talk to each other
    - Developed UI - including profile pictures for users and dogs
    - Advanced Statistics for dogs/users, like "Best round" in given discipline
    - Dogs sharing between multiple accounts
    - Changing password option
    - User Roles (like owner, breeder, trainer)
    - Adding dogs to favorite (creating a watchlist)
