import os, asyncio, keep_alive, ipapi

os.system('python3 -m pip install --upgrade -r requirements.txt')

keep_alive.keep_alive()
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord_slash import SlashCommand

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

client = commands.Bot(case_insensitive=True,
                      command_prefix="!",
                      intents=intents)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.green(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)


client.help_command = MyHelpCommand()
confirmEmoji = '\U00002705'


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(ipapi.location())
    await client.change_presence(activity=discord.Activity(
        type=discord.ActivityType.playing, name='Clash of Clans'))


@client.command(description="Sends the BOTS ping.")
async def ping(message):
    await message.message.delete()
    async with message.typing():
        await asyncio.sleep(1)
        await message.send(
            f'Websocket latency: {round(client.latency * 1000)}ms')


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=870129121353674825)
    channel = client.get_channel(870122139964047380)
    embed = discord.Embed(
        title=f"Welcome {member.name}",
        description=
        f"Welcome to {member.guild.name}, {member.mention}!\n\n#{member.guild.member_count} member!"
    )
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)
    await member.add_roles(role)


@client.event
async def on_member_remove(member):
    channel = client.get_channel(870122139964047380)
    embed = discord.Embed(title=f"{member.name} just left ;-;",
                          description=f"#{member.guild.member_count} members")
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)


@client.command()
async def ConfirmMessage(ctx):
    global confirmEmoji
    channel = client.get_channel(870128321164369920)
    message = await channel.send(embed=discord.Embed(
        title="Verify here",
        description=
        "Click the checkmark below to verify. This is to stop any bots."))
    await message.add_reaction(emoji=confirmEmoji)

    def check(reaction, user):
        if reaction.emoji == confirmEmoji:
            return True
        else:
            return False

    while True:
        try:
            reaction, user = await client.wait_for("reaction_add",
                                                   check=check,
                                                   timeout=10)
        except:
            pass
        roleToRemove = discord.utils.get(ctx.guild.roles,
                                         id=870129121353674825)
        memberToRemoveRole = discord.utils.get(ctx.guild.members,
                                               name=user.display_name)
        await memberToRemoveRole.remove_roles(roleToRemove)


TOKEN = os.environ['TOKEN']
client.run(TOKEN)
