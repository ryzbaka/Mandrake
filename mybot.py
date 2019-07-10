import re
import sys
import datetime as dt
import time
import discord
import pandas as pd
import random
import nltk
c1 = ['artless', 'bawdy', 'beslubbering', 'bootless', 'churlish', 'cockered',
'clouted', 'craven', 'currish', 'dankish', 'dissembling', 'droning', 'errant',
'fawning', 'fobbing', 'froward', 'frothy', 'gleeking', 'goatish', 'gorbellied',
'impertinent', 'infectious', 'jarring', 'loggerheaded', 'lumpish', 'mammering',
'mangled', 'mewling', 'paunchy', 'pribbling', 'puking', 'puny', 'qualling', 
'rank', 'reeky', 'rogueish', 'ruttish', 'saucy', 'spleeny', 'spongy', 'surly', 
'tottering', 'unmuzzled', 'vain', 'venomed', 'villainous', 'warped', 'wayward', 
'weedy', 'yeastly'] # first column...

c2 = ['base-court', 'bat-fowling', 'beef-witted', 'beetle-headed', 'boil-brained',
'clapper-clawed', 'clay-brained', 'common-kissing', 'crook-pated', 'dismal-dreaming',
'dizzy-eyed', 'doghearted', 'dread-bolted', 'earth-vexing', 'elf-skinned', 'fat-kidneyed',
'fen-sucked', 'flap-mouthed', 'fly-bitten', 'folly-fallen', 'fool-born', 'full-gorged',
'guts-griping', 'half-faced', 'hasty-witted', 'hedge-born', 'hell-hated', 'idle-headed',
'ill-breeding', 'ill-nurtured', 'knotty-pated', 'milk-livered', 'motley-minded', 'onion-eyed',
'plume-plucked', 'pottle-deep', 'pox-marked', 'reeling-ripe', 'rough-hewn', 'rude-growing',
'rump-fed', 'shard-borne', 'sheep-biting', 'spur-galled', 'swag-bellied', 'tardy-gaited',
'tickle-brained', 'toad-spotted', 'unchin-snouted', 'weather-bitten'] # second column...

c3 = ['apple-john', 'baggage', 'barnacle', 'bladder', 'boar-pig', 'bugbear', 'bum-bailey',
'canker-blossom', 'clack-dish', 'clotpole', 'coxcomb', 'codpiece', 'death-token', 'dewberry',
'flap-dragon', 'flax-wench', 'flirt-gill', 'foot-licker', 'fustilarian', 'giglet', 'gudgeon',
'haggard', 'harpy', 'hedge-pig', 'horn-beast', 'hugger-mugger', 'joithead', 'lewdster', 'lout',
'maggot-pie', 'malt-worm', 'mammet', 'measle', 'minnow', 'miscreant', 'moldwarp', 'mumble-news',
'nut-hook', 'pidgeon-egg', 'pignut', 'puttock', 'pumpion', 'ratsbane', 'scut', 'skainsmate',
'strumpet', 'varlot', 'vassal', 'whey-face', 'wagtail']
oo=pd.read_csv('shortjokes.csv')
oo.drop(labels='ID',axis=1,inplace=True)
jokes=list(oo.Joke)
length=len(jokes)
oo=pd.read_csv('jokes.csv')
questions=list(oo.Question)
answers=list(oo.Answer)
prof=pd.read_json('profane-words/words.json')
profanity=list(prof.iloc[:,0])

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}! I am Mandrake.'.format(member, guild)
            await guild.system_channel.send(to_send)

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if 'goodnight' in message.content.lower():
            await message.channel.send('Goodnight{0.author.mention}'.format(message))
        if message.content.lower().startswith('!savedlinks'):
            await message.channel.send('Showing saved links:')
            reader=open('links.txt','r')
            links=reader.readlines()[0].rstrip().split(' ')
            if len(links)>0:
                for link in links:
                    await message.channel.send(link)
        if len(re.findall(r'http[s]://[\w./+?=@]+',message.content))>0:
            await message.channel.send('saving link(s)')
            for link in re.findall(r'http[s]://[\w./+?=@-]+',message.content):
                await message.channel.send(link)
                writer=open('links.txt','a')
                writer.write(link+' ')
        if message.content.lower().startswith('gaydar'):
            mems=[]
            #print(self.guilds)
            for chan in self.guilds:
                #await message.channel.send(chan)
                for mem in chan.members:
                    mems.append(mem)
                break
            await message.channel.send('The gaydar is at {}'.format(random.choice(mems)))
        if message.content.lower()=="shoo mandrake shoo":
            sentient=random.randint(1,3)
            if sentient==1:
                await message.channel.send("If that's what you want {0.author.mention}, I am but a servant and you are the master.".format(message))
                time.sleep(2)
                await message.channel.send('Farewell all!')
                time.sleep(3)
                sys.exit()
            elif sentient==2:
                await message.channel.send("Actually, I don't think I'll leave just yet. Don't test me.")
                time.sleep(2)
                await message.channel.send("{0.author.mention}, I'll be watching you closesly.".format(message))
            else:
                await message.channel.send("Cool. Not leaving though.")
        if message.content.lower().startswith('diss'):
            await message.channel.send(f'thou {random.choice(c1)} {random.choice(c2)} {random.choice(c3)}!')
        if 'mandrake' in message.content.lower() and 'shoo' not in message.content.lower():
            choices=random.randint(1,3)
            if choices==1:
                await message.channel.send('Someone call my name?')
            if choices==2:
                await message.channel.send('Yes?')
            if choices==3:
                await message.channel.send("I'm here")
        if message.content.startswith('!hello mandrake'):
            await message.channel.send('Grrreetings! {0.author.mention}'.format(message))
        if message.content.lower().startswith('plis joke'):
            random_choice=random.randint(1,2)
            if random_choice==1:
                await message.channel.send(jokes[random.randint(0,len(jokes))])
            else:
                randomq=random.randint(0,len(questions))
                await message.channel.send(questions[randomq])
                await message.channel.send("(Take a guess, I'm waiting..)")
                time.sleep(5)
                await message.channel.send(answers[randomq])

        if message.content.startswith('Its alive!'):
            await message.channel.send('Yes, I am{0.author.mention}'.format(message))
        if message.content.startswith('!gamertime'):
            await message.channel.send("{0.author.mention},I'm still learning what that means".format(message))
        for word in nltk.word_tokenize(message.content):
            if word.lower() in profanity:
                scold=random.randint(1,4)
                if scold==1:
                    await message.channel.send("Language!{0.author.mention}".format(message))
                    break
                elif scold==2:
                    await message.channel.send("Mind your language{0.author.mention}".format(message))
                elif scold==3:
                    await message.channel.send("{0.author.mention},You kiss your mother with that mouth?".format(message))
                else:    
                    await message.channel.send("Good golly,{0.author.mention},that's a naughty word".format(message))
client = MyClient()
client.run('NTk4MjUyOTMyODAyMTUwNDA3.XSUAEg.77s2MABsdJzClcFMUeJHQiLsIKY')
