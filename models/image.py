from models.base_model import BaseModel
from models.user import User
from flask import Flask, flash, render_template, request, redirect, url_for
import peewee as pw
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    caption = pw.CharField(null=True)
    filename = pw.CharField(null=False, unique=False)
    user = pw.ForeignKeyField(User, backref="images")

    @hybrid_property
    def image_url(self):
        return f"https://hansnextagram.s3-ap-southeast-1.amazonaws.com/{self.filename}"

    @hybrid_property
    def total_donations(self):
        from models.donation import Donation
        total = 0
        for donation in Donation.select().where(Donation.image_id == self.id):
            total = total + donation.amount
        return round(total)
