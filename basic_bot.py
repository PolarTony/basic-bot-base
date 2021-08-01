import discord 
from discord.ext import commands 
import datetime
import asyncio
import random

client = commands.Bot(command_prefix = ".") # You can set your own custom prefixes
client.remove_command("help")



@client.event
async def on_ready():
    print('[Bot] The bot is ready!')

@client.command()
async def ping(ctx):
    embed = discord.Embed(title = "Bot Latency (Ping)", description = f"Pong! {round(client.latency * 1000)} ms", color = discord.Color.dark_green())
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Current Bot latency, asked by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.command(aliases=['user', 'userinfo'])
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name, description = member.mention, color = discord.Color.red())
    embed.add_field(name = "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Avatar requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@client.event
async def on_ready():
    # This will set the "Streaming ..." game activity
    await client.change_presence(activity=discord.Streaming(name="Bot Base", url = "https://twitch.tv/noriumbotbeta"))

    print("[Bot] Launched Bot!")

@client.command(aliases=["ub"])
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc, = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member.disc):

            await ctx.guild.unban(user)
            await ctx.send(member_name +"has been unbanned successfully!")
            return

    await ctx.send(member_name +" was not found and could not be unbanned.")

@client.command(aliases=["m"])
@commands.has_permissions(kick_members=True)
async def mute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(871055691840884809)

    await member.add_roles(muted_role) # Adds the muted role

    await ctx.send(member.mention + " has been muted successfully!")

@client.command(aliases=["um"])
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(871055691840884809) # Put your own muted role ID in get_role(yourid)

    await member.remove_roles(muted_role) # Removes the muted role

    await ctx.send(member.mention + " has been unmuted successfully!")

filtered_words = ["filtered word"] # Add your own filtered words

@client.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()

    await client.process_commands(msg)

@client.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit = amount)

@client.command(aliases=['k'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, reason="No proper reason provided."):
    await member.send("You have been kicked from a server!\nReason: " +reason)
    await member.kick(reason=reason)

@client.command(aliases=['b'])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, reason="No proper reason provided."):
    await member.send("You have been banned from a server!\nReason: " +reason)
    await member.ban(reason=reason)

@client.command(aliases=['8ball', 'ball', 'ask']) # Alternate command triggers (aliases)
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."
                ]
    embed = discord.Embed(title = "You asked, and 8ball decided...", description = f"Question: {question}\nAnswer: {random.choice(responses)}", color = discord.Color.purple())
    embed.set_footer(icon_url = "https://cdn.discordapp.com/attachments/871082094858760283/871286996075692072/DV_8_5907571_01_4c_DE_20170919221656.jpg", text = "8ball")
    await ctx.send(embed=embed)

@client.command(aliases=["h", "commands", "commandlist"])
async def help(ctx):
    embed = discord.Embed(title = "**Help - My prefix is .**", description = "**Fun**\n.8ball - Ask the 8ball a question\n\n**Moderation**\n.kick - Kick a member and provide a reason\n.mute - Mute a member\n.ban - Ban a member and provide a reason\n.unban - Unban a member via mention/ID\n.warn - Warn a user and provide a reason\n.clear - Clears a specific amount of messages\n\n**Utility**\n.ping - See the bot's latency\n\n\nNew commands coming soon with v1.0release.", color = discord.Color.green())
    embed.set_footer(icon_url = "https://cdn.discordapp.com/attachments/871082094858760283/871286996075692072/DV_8_5907571_01_4c_DE_20170919221656.jpg", text = "Help")
    await ctx.send(embed=embed)

@client.command(aliases=["funsection", "funhelp"])
async def funcommands(ctx):
    embed = discord.Embed(title = "**Commands for section 'Fun'**", description = "**Fun**\n.8ball - Ask the 8ball a question\n.ping - See the bot's latency", color = discord.Color.green())
    embed.set_footer(icon_url = "https://cdn.discordapp.com/attachments/871082094858760283/871286996075692072/DV_8_5907571_01_4c_DE_20170919221656.jpg", text = "Help (Fun)")
    await ctx.send(embed=embed)

@client.command(aliases=['w'])
@commands.has_permissions(kick_members=True)
async def warn(ctx, member : discord.Member, reason="No proper reason provided."):
    embed = discord.Embed(title = "Warned", description = f"{member.mention} has been warned.\nReason: " +reason, color = discord.Color.green())
    embed.set_footer(icon_url = "https://cdn.discordapp.com/attachments/871082094858760283/871286996075692072/DV_8_5907571_01_4c_DE_20170919221656.jpg", text = "Warn")
    await ctx.send(embed=embed)
    await member.send("You have been warned in a server.\nReason: " + reason)
@client.command(aliases=["modsection", "modhelp"])
async def modcommands(ctx):
    embed = discord.Embed(title = "**Commands for section 'Moderation'**", description = "**Moderation**\n.clear - Clears a specific amount of messages | *Aliases: .purge*\n.kick - Kicks a user and provides a reason | *Aliases: .k*\n.warn - Warns a user and provides a reason | *Aliases: .w*\n.ban - Bans a user and provides a reason | *Aliases: .b*\n.unban - Unbans a user | *Aliases: .ub*\n.mute - Mutes a user and provides a reason | *Aliases: .m*\n.unmute - Unmutes a user | *Aliases: .um*", color = discord.Color.green())
    embed.set_footer(icon_url = "https://cdn.discordapp.com/attachments/871082094858760283/871286996075692072/DV_8_5907571_01_4c_DE_20170919221656.jpg", text = "Help (Moderation)")
    await ctx.send(embed=embed)

@client.command(aliases=["gstart", "give"])
@commands.has_role("Giveaways")
async def giveaway(ctx, mins : int, *, prize: str, user):
    embed = discord.Embed(title = "A giveaway is being hosted!", description = f"{prize}", color = ctx.author.color)

    embed.add_field(text = "Hosted by", value = f"{user.mention}")

    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)

    embed.set_footer(icon_url = "https://cdn.discordapp.com/attachments/871082094858760283/871286996075692072/DV_8_5907571_01_4c_DE_20170919221656.jpg", text = f"Ends {mins} minutes from now!")

    my_msg = await ctx.send(embed = embed)


    await my_msg.add_reaction("🎉")

    await asyncio.sleep(mins*60)

    new_msg = await ctx.channel.fetch_message(my_msg.id)


    users = new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Congratulations, {winner.mention}! You won **{prize}**!")

@client.command()
@commands.has_role("Giveaways")
async def gw(ctx, convert, time):
    await ctx.send("Let's host a giveaway! Answer these questions within **15 seconds!**")

    questions = ["Which channel should this giveaway be hosted in?",
                "What is the duration of the giveaway?",
                "What is the prize of this giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(1)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You didn't answer in time, you'll get it next time!")
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Example: #example-channel")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the duration with a proper unit! Available units: s/m/h/d")
        return
    elif time == -2:
        await ctx.send("The duration must be an integer! Enter an integer next time!")
        return

    prize = answers[2]

    await ctx.send(f"The giveaway will be hosted in {channel.mention} and lasts {answers[1]}")

    embed = discord.Embed(title = "Giveaway Time!", description = f"{prize}", color = ctx.author.color)

    embed.add_field(name = "Hosted by:", value = ctx.author.mention)

    embed.set_footer(text = f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)


    await my_msg.add_reaction("🎉")


    await asyncio.sleep(time)


client.run('yourtoken') # Incase if you are dumb, put your actual bot token in (Discord Developer Portal)