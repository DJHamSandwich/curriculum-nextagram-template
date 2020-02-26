from models.base_model import BaseModel
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
import peewee as pw


class User(BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=False, unique=False)
