from models.base_model import BaseModel
from flask import Flask, flash, render_template, request, redirect, url_for
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=False, unique=False)

    def validate(self):
        password_length = len(str(request.form.get('password')))
        duplicate_emails = User.get_or_none(User.email == self.email)
        password_len_check = User.get_or_none(password_length <= 6)

        if password_len_check and not self.id:
            flash("Password must have more than 6 characters")
            self.errors.append("Password must have more than 6 characters")

        if duplicate_emails and not self.id == duplicate_emails.id:
            flash("Email has already been taken")
            self.errors.append("Email has already been taken")

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
