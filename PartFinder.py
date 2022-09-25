import os
import random
import asyncio
import time

import discord
# from dotenv import load_dotenv
from discord.ext import commands

import requests
from bs4 import BeautifulSoup

reqHeaders = {'user-agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
TOKEN = ''
GUILD = ''

def AndymarkFinder(key:str):
    productLink = "https://www.andymark.com/search?q="+key
    html = requests.get(productLink)
    soup = BeautifulSoup(html.text, "html.parser")
    embed = discord.Embed(title="Andymark Finding Results", url=productLink)
    if soup.find('div', attrs={'class':'search-results'}) == None:

        #find product Name and ID
        productName = soup.find('h1', attrs={'itemprop':'name'}).text.strip()
        productID = soup.find('span', attrs={'itemprop':'productID'}).text.strip()
        embed.add_field(name='ID', value=productID, inline=True)
        embed.add_field(name='Name', value=productName, inline=True)

        #find Price
        div = soup.find('div', attrs={'itemprop':'offers'})
        tag = div.find_all('p', attrs={'class':'product-prices__price'})
        con = []
        for p in tag:
            con += p.text.strip()
        productPrice = ""
        for w in con:
            if w != '\n' and w != ' ':
                productPrice += w
        if productPrice.find('–') == -1:
            x = productPrice.find('$',2)
            if x != -1:
                productPrice = "~~" + productPrice[0:x] + "~~ -> " + productPrice[x:len(productPrice)-1]
        embed.add_field(name='Price', value=productPrice, inline=False)

        #find Documents
        div = soup.find('div', attrs={'class':'product-documents'})
        tag = div.find_all('div', attrs={'class':'product-documents__list--item'})
        alldoc = ""
        for d in tag:
            li = d.find_all('a')
            for a in li:
                alldoc += f"[{a.text.strip()}]({a.get('href')})\n"
        embed.add_field(name='Documents', value=alldoc, inline=False)

        embed.set_footer(text='Product')

    else:
        divs = soup.find_all('div', attrs={'class':'product-summary__info'})
        for d in divs:
            name = d.find('a', attrs={'itemprop':'url'}).text.strip()
            Id = d.find('p', attrs={'class':'product-summary__sku'}).text.strip()
            url = "https://www.andymark.com/search?q=" + str(Id)
            embed.add_field(name=Id, value=f'[{name}]({url})', inline=True)
        embed.set_footer(text='Search')
    
    return embed
        
      



bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}(id:{bot.user.id})')
    print("-------")

@bot.command(help='Find input on andymark.If input is not a code, will return search page.', usage='Find index on andymark')
async def findam(ctx, x:str):
    embed = AndymarkFinder(x)
    await ctx.send(embed=embed)

# @bot.command()
# async def help(ctx):
#     embed = discord.Embed(title="usage of Andymark Finder")
#     embed.add_field(name='findam (index)', value='find things on andymark.com. if it is not a code, finder will return search page')
#     await ctx.send(embed=embed)


bot.run(TOKEN)
