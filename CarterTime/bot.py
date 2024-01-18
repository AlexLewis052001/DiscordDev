import discord
from discord.ext import commands, tasks
import responses
import time
import datetime
import re

schedule = dict()

#--------------------------------------------------------------------------CONFIGURE/RUN BOT
def run_discord_bot():
    #--------------------------------------------------------------------------BOT CONFIG SETTINGS
    with open('token.txt') as f:
        TOKEN = f.readline()
    channel_id = 1164238604940349501
    
    intents=discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True
    client = discord.Client(intents=intents)

    #--------------------------------------------------------------------------HELPER FUNCTIONS
    #-------------------------------------------- GENERATE AND SEND MESSAGE
    async def send_message(user_message, name): 
        #Generate response based on user message
        response = responses.handle_response(user_message, name)

        #create channel and send response message
        channel = client.get_channel(int(channel_id))
        await channel.send(response)

    #--------------------------------------------------------------------------BOT EVENTs
    #Loop to track the username and times dictionary
    #Runs every 10 seconds, will check every entry in dictionary for expired times
    #If expired time found, it will send a message of dissapointment in chat
    @tasks.loop(seconds = 10)
    async def track_time():
        print("Schedule: ", schedule)
        for x in list(schedule):
            if schedule[x] <= datetime.datetime.now().time():
                del schedule[x]
                await send_message('LATE', x)
    
    #Detects and reacts to a user joining a voice channel
    #If user was being timed it removes them from the list and sends a celebratory message
    @client.event
    async def on_voice_state_update(member, before, after):
        for x in list(schedule):
            if x == str(member.display_name): #check if user is being timed
                if str(after.channel) != 'None': #check if user joined any channel
                    #if here member has arrived on time
                    del schedule[x] #remove member from dictionary
                    await send_message('ON TIME', x) #send message of approval
        
    @client.event
    async def on_ready():
        #start the time tracking loop
        track_time.start()
        print(f'{client.user} is now running!\n\n')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author.display_name)
        user_message = str(message.content)

        await send_message(user_message, username)

    #--------------------------------------------------------------------------RUN BOT
    client.run(TOKEN)
            