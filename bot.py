import discord
from discord.ext import commands
from os import listdir, environ
from os.path import isfile, join
from boto.s3.connection import S3Connection
TOKEN = S3Connection(environ['TOKEN'])
invite_link = "https://discord.com/api/oauth2/authorize?client_id=517177680375054336&permissions=8&scope=bot"
client = commands.Bot(command_prefix=".")

# Initialize modules
cog_folder = "modules"
cogs = [
    f"{cog_folder}.{name.replace('.py', '')}" for name in listdir(cog_folder)
    if isfile(join(cog_folder, name))]

for cog in cogs:
    client.load_extension(cog)
    print(f"{cog} loaded")


@client.command()
async def load(ctx, extension):
    """loads module

    Arguments:
        extension {str} -- module to be loaded
    """
    try:
        client.load_extension(f"{cog_folder}.{extension}")
        await ctx.send(f"Loaded {extension} successfully")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"Module {extension} already loaded")
    except commands.ExtensionNotFound:
        await ctx.send(f"Module {extension} couldn't be found")


@client.command()
async def unload(ctx, extension):
    """unloads module

    Arguments:
        extension {str} -- module to be unloaded
    """
    try:
        client.unload_extension(f"{cog_folder}.{extension}")
        await ctx.send(f"Unloaded {extension} successfully")
    except commands.ExtensionNotLoaded:
        await ctx.send(f"Module {extension} already unloaded or doesn't exist")


@client.command()
async def logout(ctx):
    """terminates bot
    """
    print("Disconnecting...")
    await client.logout()

print(invite_link)
client.run(TOKEN)
