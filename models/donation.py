from models.base_model import BaseModel
from models.user import User
from models.image import Image
from flask import Flask, flash, render_template, request, redirect, url_for
import peewee as pw
from playhouse.hybrid import hybrid_property


class Donation(BaseModel):
    amount = pw.DecimalField()
    image = pw.ForeignKeyField(Image, backref="donations")
    user = pw.ForeignKeyField(User, backref="donations")
