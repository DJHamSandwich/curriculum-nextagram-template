from models.base_model import BaseModel
from flask import Flask, flash, render_template, request, redirect, url_for
import peewee as pw


class Session(BaseModel):
    email = pw.CharField(unique=False)
    password = pw.CharField(null=False, unique=False)
