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

    #TODO: Change the logic to first check for context, if correct context found, look for number (time)
    #Once time found, call format time to handle reformatting time and storing correct values
    #confirm context -> be on, getting on, etc...
    #refine context -> at/around, in, etc...
        #if in context found, look for units hrs,hours,min,minutes, default min
    #find number in text -> add time (if necessary) -> format time
    pattern = "(be on)( at| around)+ ([0-9]+:[0-9]+|[0-9]+)"
    time = re.compile(pattern)
    if time.search(p_message):
        time = re.split(pattern, p_message)
        time = time[len(time)-2] #extract time from the regex



        fTime = format_time(time)
        print(str(fTime))
        #print(datetime.datetime.now().time())
        bot.schedule[name] = fTime
        return f'We will expect your arrival, {name}, at exactly {fTime}'

    #-----------------------------------------------------------------MISC RESPONSES
    if p_message == '!help':
        return "1. Shut down your computer\n2. Go to bed you degenerate its 4am\n3. Seek therapy\n4. Profit"
    
#3 ways time can be given, xx, xx:xx, xxxx. Must check which way
#Assume always talking about pm, will catch anything from 1-11pm. Ignore 1am and 12pm/am cases for now
def format_time(time) -> str:
    print('before: ', time)
    if re.search('[0-9]{3,4}', time):#xxxx case
        if re.search('[0-9]{4}', time):
            temp = 12 + int(time[:2])
        else:
            temp = 12 + int(time[:1])
        temps = time[len(time)-2:]
        time = str(temp) + temps
        print('xxxx case')
    elif re.search('[0-9][0-9]?', time): #xx case
        temp = 12 + int(time)
        time = str(temp)
        time = time + '00'
        print('xx case')
    elif re.search(':', time):
        temps = time[len(time)-2:]
        temp = 12 + int(time[:2])
        time = str(temp) + temps
        print('xx:xx case')
        
    print('after: ', time)

    h, m = divmod(int(time), 100)
    return datetime.time(hour=h, minute=m)

def add_time(time) -> str:
    #take current time and add specified amount of time 
    #this will be a later implementation
    #will be quite complicated
    pass
    