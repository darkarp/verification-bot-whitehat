import os
import time
import random
import discord
import imgur_uploader

from string import ascii_uppercase, digits
from captcha.image import ImageCaptcha
from discord.ext import commands

client_id = "6eab73a88018de0"
client_secret = "335b4d6c9882f36e0f73cab80bdcbc15b5130fe6"

# client_id = os.environ(["C_ID"])
# client_secret = os.environ(["C_SECRET"])

to_be_verified = {}


def generate_text(N=5):
    print(digits)
    digit_list = digits.replace("01", "")
    print(digit_list)
    return ''.join(random.choices(ascii_uppercase + digit_list, k=N))


def new_captcha(text, username):
    im_client = imgur_uploader.ImgurClient(client_id, client_secret)
    image = ImageCaptcha(fonts=['fonts/font1.ttf'])
    data = image.generate(text)
    captcha_file = "{text}.png"
    image.write(text, captcha_file)
    captcha_link = im_client.upload_from_path(f"{captcha_file}")["link"]
    embed = discord.Embed(colour=discord.Colour(
        0x6b75aa), url="https://discordapp.com")
    embed.set_image(url=f"{captcha_link}")
    embed.set_author(
        name=f"Captcha Verification for {username}", icon_url="https://cdn.discordapp.com/avatars/517177680375054336/730098542337d1c0e38a893d48a53917.webp?size=256")
    embed.add_field(name="Please write the characters you see",
                    value="It is NOT case-sensitive")
    return embed


class Verify(commands.Cog):
    global to_be_verified

    def __init__(self, client):
        self.client = client

    async def send_captcha(self, author, ctx):
        text = generate_text()
        embed = new_captcha(text, author)
        to_be_verified[author] = text
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("."):
            return 0
        author = str(message.author)
        if author in to_be_verified:
            text_input = message.content
            if text_input == to_be_verified[author]:
                await message.channel.send(f"{author} verified")
            else:
                await message.channel.send("Not verified. Captcha Failed!")

    @ commands.command()
    async def verify(self, ctx):
        text = generate_text()
        author = str(ctx.message.author)
        if author not in to_be_verified.keys():
            await ctx.send("Generating your captcha...")
            to_be_verified[author] = text
        else:
            return await ctx.send("Please Complete your current verification.\n\
If you need another captcha, issue the command `.new_captcha`")
        await self.send_captcha(author, ctx)

    async def new_captcha(self, ctx):
        author = str(ctx.message.author)
        if author in to_be_verified.keys():
            await self.send_captcha(author, ctx)


def setup(client):
    client.add_cog(Verify(client))
