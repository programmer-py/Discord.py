import discord
import asyncio
from discord import Member
import random
from discord import Guild
import time
from discord.ext import commands


client = discord.Client()
antworten = ["Ja", "Nein", "eher ja", "eher nein", "sehr wahrscheinlich", "unmöglich",
             "Sieht so aus", "Sieht nicht so aus"]

autoroles = {
    639479169973092378: {"memberroles": [709469160987426947]}
}

@client.event
async def on_ready():
    print ("Der Bot {}".format(client.user.name) + " ist ready!")
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game("www.twitch.tv/MightyMike_93"), status=discord.Status.online)
        await asyncio.sleep(8)
        await client.change_presence(activity=discord.Game("Schau gerne vorbei!"), status=discord.Status.online)
        await asyncio.sleep(3)
        
    
def is_not_pinned(mess):
    return not mess.pinned

@client.event
async def on_member_join(member):
    user = (member.name)
    channel = discord.utils.get(member.guild.channels, name= "👋-willkommen")
    await channel.send("Willkommen "+(user)+ ", auf dem Community-Server von **MightyCrew**! Bitte lese die Regeln durch und halte dich daran! 👍😊 Nun wünsche ich dir viel Spaß!")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '!help' in message.content:
        await message.channel.send('**Hilfe zum Mighty-Bot**\r\n'
                                   '!help - Zeigt diese Hilfe an\r\n'
                                   '!userinfo (User) - Die Information des angegebenen Users.\r\n'
                                   '!clear (Anzahl)  - Löscht die Anzahl Nachrichten im Channel. (Nur für Moderatoren und Admins.)\r\n'
                                   '!8ball (Frage) - Befrage das Orakel nach deinem Schicksal\r\n'
                                   '\r\n'
                                   'Bei Fehlern oder bei Vorschlägen wende dich an **ifstatement**')
    if message.content.startswith('!userinfo'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinfo für {}'.format(member.name),
                                      description='Dies ist eine Userinfo für den User {}'.format(member.mention),
                                      color=0x22a7f0)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text="developed by ifstatement")
                mess = await message.channel.send(embed=embed)

    if message.content.startswith("!clear"):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(" ")
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send("{} Nachrichten erfolgreich gelöscht.". format(len(deleted)-1))
    if message.content.startswith("!8ball"):
        args = message.content.split(" ")
        if len(args) >= 2:
            frage = " ".join(args[1:])
            mess = await message.channel.send("Die Antwort von `{0}` wird gesucht...".format(frage))
            await asyncio.sleep(2)
            await mess.edit(content= "Das Orakel sagt voraus...")
            await asyncio.sleep(2)
            await mess.edit(content= "Deine Antwort zur Frage `{0}` lautet: `{1}`".format(frage, random.choice(antworten)))



client.run("NzI0NjY3NDI4MTg0Nzg0OTI4.XvDhfw.fAsS1_g7wR7uVsAk1IJXzJ-Kbww")