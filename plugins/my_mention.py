#coding: utf-8

import detectMotion
import requests
from slackbot.bot import respond_to     # Decorders that respond to @botname:
from slackbot.bot import listen_to      # Decorders responding with in-channel statements
# from slackbot.bot import default_reply  # Decorders that react when there is no corrsponding response

# @respond_to('string')   message to bot
#                         string can be a regular expression "r'string'"
# @listen_to('string')    posts  on the channel that are not addressed to the bot
#                         Note that @botname: does not respond to @botname
#                         mentions to other people do respond
#                         regex possible
# @default_reply()        if you specify a regular expression that works the sama as
#                         DEFAULT_REPLY, no other decoder will hit it, and it will
#                         respond when it matches the regular expression
# message.reply('string')      @speaker name: send message with string
# message.send('string')        send a string
# message.react('icon_emoji')   react (stamp) to the speaker's message
#                               no need for ":" in the string
@respond_to('fried rice') 
def mention_function(message):
    message.reply('I love fried rice so much!')     # mention

@respond_to('Good morning')
def goodMorning(message):
    message.reply('Good morning!')

@listen_to('fried rice')
def listen_function(message):
    message.send('It seems that someone mentioned fried rice.')
    message.reply('Do you want to talk about fried rice?') #mention

detectMotion.motionDetection()