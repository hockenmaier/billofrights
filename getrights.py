#import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('bill_of_rights')

    #Finding the Intent and other parameters:
    try:
        intent = event['result']['metadata']['intentName']
        amendment = event['result']['parameters']['Amendments']
    except:
        print 'no intent or amendment found'
        return {"speech": 'I\'m sorry, There was a system error'}
   
    if(amendment == ""):
        return {"speech": 'I\'m sorry, I couldn\'t figure out what amendment you meant'}

   #Now we get the item in dynamo DB that represents the amendment the user asked about:
    rights = table.get_item(
        Key={
            'detail_ID': amendment,
        }
    )
    
    #This if tree goes through the intents and sends back the speech response.  If the give amendment's attribute is null, it returns a human-understandable error
    if(intent == 'Identify'):
        response = rights['Item']['Identify']
        return {"speech": "You are thinking of the " + response + "." + random_identify() + random_close()}
    elif(intent == 'Text') or (intent == 'Text-Context'):
        response = rights['Item']['Text']
        name = rights['Item']['Name']
        return {"speech": "The " + name + " reads: " + response + random_text() + random_close()}
    elif(intent == 'Origin') or (intent == 'Origin-Context'):
        response = rights['Item']['Origin']
        if response:
            return {"speech": response + random_close()}
        else:
            return {"speech": "I\'m not sure about the origin of that one yet. Please ask another question, or let me know if you\'re done."}
    elif(intent == 'Explanation') or (intent == 'Explanation-Context'):
        response = rights['Item']['Explanation']
        if response:
            return {"speech": response + random_close()}
        else:
            return {"speech": "I don\'t have an explanation for that one yet. Please ask another question, or let me know if you\'re done."}
    elif(intent == 'Status') or (intent == 'Status-Context'):
        response = rights['Item']['Status']
        if response:
            return {"speech": response + random_close()}
        else:
            return {"speech": "I am not sure how that one is doing yet. Please ask another question, or let me know if you\'re done."}

#These randomizer functions go after the text and identify responses to let the user know what else they can do, and keep it interesting
import random
def random_text():
    text = [' If that needs explanation, just ask!', ' Go ahead and ask about the history of that if you\'re curious!', ' Ask about how that\'s doing today!', ' Ask for an explanation if you\'d like', ' How about learning the history of that one?', ' Let\'s keep learning!', ' Still curious?  Ask away!', ' Now let\'s dig deeper about why that was written!', ' Want to know more? I sure love civil rights!', ' I sure love civil rights!', ' It\'s important to know your rights!', ' Ask about more facts about the Bill of rights!']
    return (random.choice(text))
    
def random_identify():
    text = [' You can ask me to read it to you, or about its history, meaning, or current status', ' Go ahead and ask about the history of that if you\'re curious!', ' Try asking about how that\'s doing today!', ' Ask for the full text if you want to hear it', ' Go ahead and ask me to read that to you.', ' Want to know anything else?  Just ask!',' If you need an explanation of that one, just ask!']
    return (random.choice(text))
    
def random_close():
    text = [' I\'m still listening, let me know if you\'re done.', ' When you\'re finished, ask to quit', ' I\'m ready for more questions, or would you like to finish for today?', ' If you\'re done, let me know!', ' If you\'ve hear enough, let me know!', ' Just tell me if you\'d like to exit now',' Remember to say goodbye when you\'re done.  Otherwise I\'m ready for more!']
    return (random.choice(text))
