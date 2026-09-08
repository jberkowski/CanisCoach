from datetime import datetime
from extensions import db

class User(db.Model):
    __tablename__ = "users"

    usr_id = db.Column(db.Integer, primary_key=True)
    usr_email = db.Column(db.String(255), unique=True, nullable=False)
    usr_password_hash = db.Column(db.String(255), nullable=False)
    usr_join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    dogs = db.relationship("Dog", back_populates="user")
    disciplines = db.relationship("Discipline", back_populates="user")
    workouts = db.relationship("Workout", back_populates="user")
    workout_groups = db.relationship("WorkoutGroup", back_populates="user")


class Dog(db.Model):
    __tablename__ = "dogs"

    dog_id = db.Column(db.Integer, primary_key=True)
    dog_name_full = db.Column(db.String(250), nullable=False)
    dog_name_short = db.Column(db.String(100), nullable=False)

    dog_usr_id = db.Column(
        db.Integer,
        db.ForeignKey("users.usr_id"),
        nullable=False
    )

    dog_breed_id = db.Column(
        db.Integer,
        db.ForeignKey("breeds.breed_id"),
        nullable=True
    )

    dog_birth_date = db.Column(db.Date, nullable=True)
    dog_note = db.Column(db.Text, nullable=True)
    dog_active = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship("User", back_populates="dogs")
    breed = db.relationship("Breed", back_populates="dogs")
    workouts = db.relationship("Workout", back_populates="dog")

    __table_args__ = (
        db.CheckConstraint("dog_active IN (0, 1)", name="check_dog_active"),
    )


class Discipline(db.Model):
    __tablename__ = "disciplines"

    disc_id = db.Column(db.Integer, primary_key=True)
    disc_name = db.Column(db.String(100), nullable=False)

    # 0 = public, 1 = private
    disc_type = db.Column(db.Integer, nullable=False)

    # Required only when discipline is private
    disc_usr_id = db.Column(
        db.Integer,
        db.ForeignKey("users.usr_id"),
        nullable=True
    )

    disc_active = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship("User", back_populates="disciplines")
    workouts = db.relationship("Workout", back_populates="discipline")

    __table_args__ = (
        db.CheckConstraint("disc_type IN (0, 1)", name="check_disc_type"),
        db.CheckConstraint("disc_active IN (0, 1)", name="check_disc_active"),
    )


class Workout(db.Model):
    __tablename__ = "workouts"

    wout_id = db.Column(db.Integer, primary_key=True)

    wout_start_datetime = db.Column(db.DateTime, nullable=False)
    wout_end_datetime = db.Column(db.DateTime, nullable=False)
    wout_duration_minutes = db.Column(db.Integer, nullable=False)

    wout_disc_id = db.Column(
        db.Integer,
        db.ForeignKey("disciplines.disc_id"),
        nullable=False
    )

    wout_usr_id = db.Column(
        db.Integer,
        db.ForeignKey("users.usr_id"),
        nullable=False
    )

    wout_dog_id = db.Column(
        db.Integer,
        db.ForeignKey("dogs.dog_id"),
        nullable=False
    )

    wout_focus = db.Column(db.Text, nullable=True)

    # 0 = planned, 1 = completed, 2 = cancelled
    wout_status = db.Column(db.Integer, nullable=False, default=0)

    wout_score = db.Column(db.String(100), nullable=True)
    wout_note = db.Column(db.Text, nullable=True)

    wout_creation_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    wout_wgroup_id = db.Column(
        db.Integer,
        db.ForeignKey("workout_groups.wgroup_id"),
        nullable=True
    )

    wout_active = db.Column(db.Integer, nullable=False, default=1)

    user = db.relationship("User", back_populates="workouts")
    dog = db.relationship("Dog", back_populates="workouts")
    discipline = db.relationship("Discipline", back_populates="workouts")
    workout_group = db.relationship("WorkoutGroup", back_populates="workouts")

    __table_args__ = (
        db.CheckConstraint("wout_status IN (0, 1, 2)", name="check_wout_status"),
        db.CheckConstraint("wout_active IN (0, 1)", name="check_wout_active"),
        db.CheckConstraint("wout_duration_minutes >= 0", name="check_wout_duration_positive"),
    )


class WorkoutGroup(db.Model):
    __tablename__ = "workout_groups"

    wgroup_id = db.Column(db.Integer, primary_key=True)

    wgroup_usr_id = db.Column(
        db.Integer,
        db.ForeignKey("users.usr_id"),
        nullable=False
    )

    wgroup_creation_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    user = db.relationship("User", back_populates="workout_groups")
    workouts = db.relationship("Workout", back_populates="workout_group")


class Breed(db.Model):
    __tablename__ = "breeds"

    breed_id = db.Column(db.Integer, primary_key=True)
    breed_name = db.Column(db.String(100), nullable=False, unique=True)

    dogs = db.relationship("Dog", back_populates="breed")

