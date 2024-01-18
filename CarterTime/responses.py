import bot
import datetime
import re


#-----------------------------------------------------------------GENERAL RESPONSE HANDLING
def handle_response(message, name) -> str:
    #-----------------------------------------------------------------LATE/ON TIME RESPONSES
    if message == 'LATE':
        return f'{name} has failed us... how unreliable...'
    if message == 'ON TIME':
        return f'{name} has arrived on time... well done!'
    
    ##-----------------------------------------------------------------ANALYZE PROMISE PROMPT
    p_message = message.lower()

    pattern = "(be on)( at| around)+ ([0-9]+:[0-9]+|[0-9]+)"
    time = re.compile(pattern)
    if time.search(p_message):
        time = re.split(pattern, p_message)
        time = time[len(time)-2] #extract time from the regex

        fTime = format_time(time)
        #print(datetime.datetime.now().time())
        bot.schedule[name] = fTime
        return f'We will expect your arrival, {name}, at exactly {fTime}'

    #-----------------------------------------------------------------MISC RESPONSES
    if p_message == '!help':
        return "1. Shut down your computer\n2. Go to bed you degenerate its 4am\n3. Seek therapy\n4. Profit"
    
def format_time(time) -> str:
    if re.search(':', time):
        time = time.replace(':', '')
        print(time)
    else:
        time = time + '00'
        
    h, m = divmod(int(time), 100)
    return datetime.time(hour=h, minute=m)
    