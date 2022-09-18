from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Order(models.Model):
    owner = User
    choices = [("BTC", "BitCoin"), ("ETH", "Etherium"), ("LTC", "LiteCoin"), ("KINGM", "KINGM"), ("EOS", "EOS"), ("ADA", "ADA"), ("XRP", "XRP"), ("DOGE", "DogeCoin"), ("SHIB", "ShibaCoin")]
    product = models.CharField(max_length=20, choices=choices)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.amount)
