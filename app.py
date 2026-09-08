from datetime import datetime, timedelta
from extensions import db, migrate
from flask import Flask, redirect, render_template, request, flash, session, url_for
from helpers import login_required
from models import User, Dog, Discipline, Workout, WorkoutGroup, Breed
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
# Configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cc.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"
# initialize the app with the extension
# migrate models into db
db.init_app(app)
migrate.init_app(app, db)


@app.route("/")
def index():
    """Main page - welcome"""

    return render_template("index.html")


@app.route("/dogs")
@login_required
def dogs():
    """Display list of all user dogs"""

    user_id = session["user_id"]
    user = User.query.filter_by(usr_id=user_id).first()

    user_dogs = Dog.query.filter_by(dog_usr_id=user_id).all()

    dog_breeds = Breed.query.all()
    breed_dict = {b.breed_id: b.breed_name for b in dog_breeds}

    return render_template(
        "dogs.html",
        user=user,
        user_dogs=user_dogs,
        breed_dict=breed_dict)


@app.route("/dogs/add", methods=["GET", "POST"])
@login_required
def add_dog():
    """Add dog"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check and validate form values
        name_full=request.form.get("name_full")
        if not name_full:
            flash("Wpisz pełne imię", "error")
            return redirect("/dogs/add")
        
        name_short=request.form.get("name_short")
        if not name_short:
            flash("Wpisz skrócone imię", "error")
            return redirect("/dogs/add")

        breed_id=request.form.get("breed_id")
        if breed_id == "":
            breed_id = None
        else:
            try:
                breed_id = int(breed_id)
            except ValueError:
                flash("Nieprawidłowa rasa", "error")
                return redirect("/dogs/add")
            
        birth_date=request.form.get("birth_date")
        if birth_date == "":
            birth_date = None
        else:
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                flash("Niepoprawna data", "error")
                return redirect("/dogs/add")
            
        note=request.form.get("note")
        if note == "":
            note = None

        user_id=session["user_id"]

        # Create dog
        new_dog = Dog(
            dog_name_full=name_full,
            dog_name_short=name_short,
            dog_usr_id=user_id,
            dog_breed_id=breed_id,
            dog_birth_date=birth_date,
            dog_note=note
        )

        # Add user to db
        db.session.add(new_dog)
        db.session.commit()

        flash("Pies został dodany.", "success")
        return redirect("/dogs")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        user_id = session["user_id"]
        user = User.query.filter_by(usr_id=user_id).first()

        breeds = Breed.query.all()

        return render_template("dogs_add.html", user=user, breeds=breeds)
    

@app.route("/dogs/dog/<int:dog_id>/edit", methods=["GET", "POST"])
@login_required
def edit_dog(dog_id):
    """Edit dog"""
    user_id = session["user_id"]

    dog = Dog.query.filter_by(
            dog_id=dog_id,
            dog_usr_id=user_id,
            dog_active=1
        ).first()
    
    if dog is None:
        flash("Nie znaleziono psa.", "error")
        return redirect("/dogs")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check and validate form values
        name_full=request.form.get("name_full")
        if not name_full:
            flash("Wpisz pełne imię", "error")
            return redirect(url_for("edit_dog", dog_id=dog_id))
        
        name_short=request.form.get("name_short")
        if not name_short:
            flash("Wpisz skrócone imię", "error")
            return redirect(url_for("edit_dog", dog_id=dog_id))

        breed_id=request.form.get("breed_id")
        if breed_id == "":
            breed_id = None
        else:
            try:
                breed_id = int(breed_id)
            except ValueError:
                flash("Nieprawidłowa rasa", "error")
                return redirect(url_for("edit_dog", dog_id=dog_id))
            
        birth_date=request.form.get("birth_date")
        if birth_date == "":
            birth_date = None
        else:
            try:
                birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                flash("Niepoprawna data", "error")
                return redirect(url_for("edit_dog", dog_id=dog_id))
            
        note=request.form.get("note")
        if note == "":
            note = None

        # Update dog
        dog.dog_name_full=name_full
        dog.dog_name_short=name_short
        dog.dog_usr_id=user_id
        dog.dog_breed_id=breed_id
        dog.dog_birth_date=birth_date
        dog.dog_note=note

        # Commit changes to db
        db.session.commit()

        flash("Pies został edytowany.", "success")
        return redirect("/dogs")

    else:
        user = User.query.filter_by(usr_id=user_id).first()
        breeds = Breed.query.all()
        return render_template(
            "dogs_edit.html",
            dog=dog,
            user=user,
            breeds=breeds)


@app.route("/dogs/dog/<int:dog_id>")
@login_required
def dog(dog_id):
    """Display data about single dog"""

    # Check if this dog belongs to the user
    dog = Dog.query.filter_by(
        dog_id=dog_id,
        dog_usr_id=session["user_id"]
    ).first()

    if dog is None:
        flash("To nie Twój pies", "error")
        return redirect("/dogs")

    return render_template("dog.html", dog=dog)


@app.route("/dogs/dog/<int:dog_id>/delete", methods=["POST"])
@login_required
def delete_dog(dog_id):
    user_id = session["user_id"]

    dog = Dog.query.filter_by(
        dog_id=dog_id,
        dog_usr_id=user_id,
        dog_active=1
    ).first()

    if dog is None:
        flash("Nie znaleziono psa.", "error")
        return redirect("/dogs")
    
    dog.dog_active=0

    db.session.commit()

    flash("Pies został usunięty.", "success")
    return redirect(url_for("dogs"))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Ensure username was submitted
        if not email:
            flash("Niepoprawny login.", "error")
            return redirect("/login")

        # Ensure password was submitted
        elif not password:
            flash("Niepoprawne hasło.", "error")
            return redirect("/login")

        # Confirm users exists
        existing_user = User.query.filter_by(usr_email=email).first()

        if not existing_user:
            flash("Niepoprawny login.", "error")
            return redirect("/login")
        
        # Confirm password
        real_hash = existing_user.usr_password_hash
        password_match = check_password_hash(real_hash, password)

        if not password_match:
            flash("Niepoprawne hasło.", "error")
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = existing_user.usr_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

        
@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/profile")
@login_required
def profile():
    """Show page about user"""

    user_id = session["user_id"]
    user = User.query.filter_by(usr_id=user_id).first()

    return render_template("profile.html", user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")


        # Ensure all data was submitted
        if not email or not password or not password_confirm:
            flash("Wypełnij wszystkie pola.", "error")
            return redirect("/register")


        # Ensure password is provided correctly twice
        if password != password_confirm:
            flash("Hasła nie są takie same.", "error")
            return redirect("/register")

        # Usernames must be unique
        existing_user = User.query.filter_by(usr_email=email).first()

        if existing_user:
            flash("Konto z takim adresem email już istnieje.", "error")
            return redirect("/register")
        
        # Hash password
        password_hash = generate_password_hash(password)

        # Create user
        new_user = User(
            usr_email=email,
            usr_password_hash=password_hash
        )

        # Add user to db
        db.session.add(new_user)
        db.session.commit()

        flash("Konto zostało utworzone. Możesz się teraz zalogować.", "success")
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
    

@app.route("/workouts")
@login_required
def workouts():
    """Display main page for workouts"""

    user_id = session["user_id"]
    user = User.query.filter_by(usr_id=user_id).first()

    date_now = datetime.now()

    workouts = Workout.query.filter(
        Workout.wout_usr_id==user_id,
        Workout.wout_active==1).order_by(
            Workout.wout_start_datetime.desc()).all()
    
    disciplines = Discipline.query.all()
    disc_dict = {d.disc_id: d.disc_name for d in disciplines}

    dogs = Dog.query.filter_by(dog_usr_id=user_id).all()
    dogs_dict = {d.dog_id: d.dog_name_short for d in dogs}

    status_dict = {0: 'Zaplanowany', 1: 'Zakończony', 2: 'Anulowany'}

    calendar_events = []

    for workout in workouts: 
        calendar_events.append({
            "id": workout.wout_id,
            "title": disc_dict[workout.wout_disc_id],
            "start": workout.wout_start_datetime.isoformat(),
            "end": workout.wout_end_datetime.isoformat() if workout.wout_end_datetime else None,
        })

    return render_template(
        "workouts.html",
        user=user,
        workouts=workouts,
        disc_dict=disc_dict,
        dogs_dict=dogs_dict,
        calendar_events=calendar_events,
        date_now=date_now,
        status_dict=status_dict
        )


@app.route("/workouts/add", methods=["GET", "POST"])
@login_required
def add_workout():
    """Add workout"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check and validate form values
        start_raw = request.form.get("start_datetime")
        duration_raw = request.form.get("duration_minutes")
        disc_id_raw = request.form.get("disc_id")
        dog_ids_raw = request.form.getlist("dog_ids")
        focus = request.form.get("focus")
        status = request.form.get("status")
        score = request.form.get("score")
        note = request.form.get("note")

        user_id = session["user_id"]

        if not start_raw:
            flash("Podaj datę rozpoczęcia treningu.")
            return redirect("/workouts/add")

        if not duration_raw:
            flash("Podaj czas trwania treningu.")
            return redirect("/workouts/add")

        if not disc_id_raw:
            flash("Wybierz dyscyplinę.")
            return redirect("/workouts/add")

        if not dog_ids_raw:
            flash("Wybierz co najmniej jednego psa.")
            return redirect("/workouts/add")

        try:
            status = int(status)
        except (ValueError, TypeError):
            flash("Nieprawidłowy status.")
            return redirect("/workouts/add")

        if status not in (0, 1, 2):
            flash("Wybierz status treningu.")
            return redirect("/workouts/add")

        try:
            start_datetime = datetime.fromisoformat(start_raw)
        except ValueError:
            flash("Nieprawidłowy format daty rozpoczęcia.")
            return redirect("/workouts/add")

        try:
            duration_minutes = int(duration_raw)
        except ValueError:
            flash("Czas trwania musi być liczbą.")
            return redirect("/workouts/add")

        if duration_minutes <= 0:
            flash("Czas trwania musi być większy od zera.")
            return redirect("/workouts/add")

        try:
            disc_id = int(disc_id_raw)
            dog_ids = [int(dog_id) for dog_id in dog_ids_raw]
        except ValueError:
            flash("Nieprawidłowe dane formularza.")
            return redirect("/workouts/add")
        
        # Validate ownership for discipline and dog
        discipline = Discipline.query.filter_by(disc_id=disc_id).first()

        if discipline is None:
            flash("Wybrana dyscyplina nie istnieje.")
            return redirect("/workouts/add")
        
        if discipline.disc_active != 1:
            flash("Wybrana dyscyplina jest nieaktywna.")
            return redirect("/workouts/add")

        if discipline.disc_type == 1 and discipline.disc_usr_id != user_id:
            flash("Nie masz dostępu do tej dyscypliny.")
            return redirect("/workouts/add")

        # Remove duplicate dog IDs
        dog_ids = list(set(dog_ids))

        # Get only dogs selected in the form
        dogs_data = Dog.query.filter(
            Dog.dog_id.in_(dog_ids),
            Dog.dog_usr_id == user_id,
            Dog.dog_active == 1
        ).all()

        # Every submitted ID must match one active dog belonging to the user
        if len(dogs_data) != len(dog_ids):
            flash(
                "Co najmniej jeden z wybranych psów nie istnieje, "
                "jest nieaktywny lub nie należy do Ciebie."
            )
            return redirect("/workouts/add")

        end_datetime = start_datetime + timedelta(minutes=duration_minutes)

        # Create workout group and add it to db
        new_workout_group = WorkoutGroup(
            wgroup_usr_id=user_id,
            wgroup_creation_date=datetime.now()
        )

        db.session.add(new_workout_group)
        # Flush to get workout_group id
        db.session.flush()
        wgroup_id = new_workout_group.wgroup_id

        # Create workout for each dog and add it to db
        for dog_id in dog_ids:
            new_workout = Workout(
                wout_start_datetime=start_datetime,
                wout_end_datetime=end_datetime,
                wout_duration_minutes=duration_minutes,
                wout_disc_id=disc_id,
                wout_usr_id=user_id,
                wout_dog_id=dog_id,
                wout_focus=focus,
                wout_status=status,
                wout_score=score,
                wout_note=note,
                wout_creation_date=datetime.now(),
                wout_wgroup_id=wgroup_id,
                wout_active=1
            )
            db.session.add(new_workout)

        # Commit changes to db
        db.session.commit()

        flash("Trening został dodany.", "success")
        return redirect("/workouts")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        user_id = session["user_id"]
        user = User.query.filter_by(usr_id=user_id).first()

        disciplines = Discipline.query.filter(
            or_(
                Discipline.disc_type == 0,
                Discipline.disc_usr_id == user_id
            ),
            Discipline.disc_active == 1
        ).all()

        dogs = Dog.query.filter(
            Dog.dog_usr_id == user_id,
            Dog.dog_active == 1
        ).all()

        return render_template(
            "workouts_add.html",
            user=user,
            disciplines=disciplines,
            dogs=dogs)
    

@app.route("/workouts/workout/<int:wout_id>")
@login_required
def workout(wout_id):
    """Display data about single workout"""

    user_id=session["user_id"]

    # Check if this workout belongs to the user
    workout = Workout.query.filter_by(
        wout_id=wout_id,
        wout_usr_id=user_id
    ).first()

    if workout is None:
        flash("To nie Twój trening", "error")
        return redirect("/workouts")

    disciplines = Discipline.query.all()
    disc_dict = {d.disc_id: d.disc_name for d in disciplines}

    dogs = Dog.query.filter_by(dog_usr_id=user_id).all()
    dogs_dict = {d.dog_id: d.dog_name_short for d in dogs}

    return render_template(
        "workout.html",
        workout=workout,
        disc_dict=disc_dict,
        dogs_dict=dogs_dict)


@app.route("/workouts/workout/<int:wout_id>/cancel", methods=["POST"])
@login_required
def cancel_workout(wout_id):
    user_id = session["user_id"]

    workout = Workout.query.filter_by(
        wout_id=wout_id,
        wout_usr_id=user_id,
        wout_active=1
    ).first()

    if workout is None:
        flash("Nie znaleziono treningu.", "error")
        return redirect("/workouts")
    
    workout.wout_status = 2

    db.session.commit()

    flash("Trening został anulowany.", "success")
    return redirect(url_for("workouts"))


@app.route("/workouts/workout/<int:wout_id>/complete", methods=["POST"])
@login_required
def complete_workout(wout_id):
    user_id = session["user_id"]

    workout = Workout.query.filter_by(
        wout_id=wout_id,
        wout_usr_id=user_id,
        wout_active=1
    ).first()

    if workout is None:
        flash("Nie znaleziono treningu.", "error")
        return redirect("/workouts")
    
    workout.wout_status = 1

    db.session.commit()

    flash("Trening został ukończony.", "success")
    return redirect(url_for("workouts"))


@app.route("/workouts/workout/<int:wout_id>/delete", methods=["POST"])
@login_required
def delete_workout(wout_id):
    user_id = session["user_id"]

    workout = Workout.query.filter_by(
        wout_id=wout_id,
        wout_usr_id=user_id,
        wout_active=1
    ).first()

    if workout is None:
        flash("Nie znaleziono treningu.", "error")
        return redirect("/workouts")
    
    workout.wout_active=0

    db.session.commit()

    flash("Trening został usunięty.", "success")
    return redirect(url_for("workouts"))


@app.route("/workouts/workout/<int:wout_id>/edit", methods=["GET", "POST"])
@login_required
def edit_workout(wout_id):
    user_id = session["user_id"]

    workout = Workout.query.filter_by(
        wout_id=wout_id,
        wout_usr_id=user_id,
        wout_active=1
    ).first()

    if workout is None:
        flash("Nie znaleziono treningu.", "error")
        return redirect("/workouts")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Check and validate form values
        start_raw = request.form.get("start_datetime")
        duration_raw = request.form.get("duration_minutes")
        disc_id_raw = request.form.get("disc_id")
        focus = request.form.get("focus")
        status = request.form.get("status")
        score = request.form.get("score")
        note = request.form.get("note")

        user_id = session["user_id"]

        if not start_raw:
            flash("Podaj datę rozpoczęcia treningu.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        if not duration_raw:
            flash("Podaj czas trwania treningu.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        if not disc_id_raw:
            flash("Wybierz dyscyplinę.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        if not status:
            flash("Wybierz status treningu.")
            return redirect(url_for("edit_workout", wout_id=wout_id))
        
        try:
            status = int(status)
        except (ValueError, TypeError):
            flash("Nieprawidłowy status.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        if status not in (0, 1, 2):
            flash("Wybierz status treningu.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        try:
            start_datetime = datetime.fromisoformat(start_raw)
        except ValueError:
            flash("Nieprawidłowy format daty rozpoczęcia.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        try:
            duration_minutes = int(duration_raw)
        except ValueError:
            flash("Czas trwania musi być liczbą.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        if duration_minutes <= 0:
            flash("Czas trwania musi być większy od zera.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        try:
            disc_id = int(disc_id_raw)
        except ValueError:
            flash("Nieprawidłowa dyscyplina.")
            return redirect(url_for("edit_workout", wout_id=wout_id))
        
        # Validate ownership for discipline and dog
        discipline = Discipline.query.filter_by(disc_id=disc_id).first()

        if discipline is None:
            flash("Wybrana dyscyplina nie istnieje.")
            return redirect(url_for("edit_workout", wout_id=wout_id))
        
        if discipline.disc_active != 1:
            flash("Wybrana dyscyplina jest nieaktywna.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        if discipline.disc_type == 1 and discipline.disc_usr_id != user_id:
            flash("Nie masz dostępu do tej dyscypliny.")
            return redirect(url_for("edit_workout", wout_id=wout_id))

        end_datetime = start_datetime + timedelta(minutes=duration_minutes)

        # Update workout
        workout.wout_start_datetime = start_datetime
        workout.wout_end_datetime = end_datetime
        workout.wout_duration_minutes = duration_minutes
        workout.wout_disc_id = disc_id
        workout.wout_focus = focus
        workout.wout_status = status
        workout.wout_score = score
        workout.wout_note = note

        # Commit changes to db
        db.session.commit()

        flash("Trening został edytowany.", "success")
        return redirect("/workouts")
    else:

        disciplines = Discipline.query.filter(
            or_(
                Discipline.disc_type == 0,
                Discipline.disc_usr_id == user_id
            ),
            Discipline.disc_active == 1
        ).all()

        dogs = Dog.query.filter(
            Dog.dog_usr_id == user_id,
        ).all()

        return render_template(
            "workouts_edit.html",
            workout=workout,
            disciplines=disciplines,
            dogs=dogs
        )