from discord.ext import commands
import os
import requests
import discord 
from dotenv import load_dotenv
import paypalrestsdk
import logging

load_dotenv()
updatePURL = os.getenv('UP_URL')
removePURL = os.getenv('RP_URL')
getPURL = os.getenv('GP_URL')

paypalrestsdk.configure({
    "mode": "sandbox", # sandbox or live
    "client_id": "Ad9HmmkIPQKJrQyJ6nsAblfs8PU718bjq4rzf-97X3p-EUpTKeNvqsTv_rFr4iKvG8XGDrg-7yf2WgLv",
    "client_secret": "EMaT4vBU7Y--OAIYwryfhrebixNanHgpUkmkJBzhNgDJyTS91injyrTK95s-w0h3qCisJhiFz3_NJOHg" })

class Premium(commands.Cog, name="Premium"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")
    
    @commands.command()
    async def premium(self, ctx):
        paypalrestsdk.configure({
        "mode": "sandbox", # sandbox or live
        "client_id": "Ad9HmmkIPQKJrQyJ6nsAblfs8PU718bjq4rzf-97X3p-EUpTKeNvqsTv_rFr4iKvG8XGDrg-7yf2WgLv",
        "client_secret": "EMaT4vBU7Y--OAIYwryfhrebixNanHgpUkmkJBzhNgDJyTS91injyrTK95s-w0h3qCisJhiFz3_NJOHg" })

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment/execute",
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "item",
                        "sku": "item",
                        "price": "5.00",
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": "5.00",
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            print("Payment created successfully")
        else:
            print(payment.error) 

    

def setup(bot):
    bot.add_cog(Premium(bot))