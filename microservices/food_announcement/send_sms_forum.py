# only have $15.50 to spend :')
from twilio.rest import Client
import json
import requests
import os
import amqp_setup

monitor_binding_key = "#.sms.forum.#"
'''
Function: initiate the queue
'''
def receive_sms():
    amqp_setup.check_setup()
    queue_name = 'sms_forum'

    # set up queue and look for incoming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()
    # need to terminate using Ctrl+C

'''
Function: callback function when receiving a message
Input: Input: JSON object -> {
    "food" : JSON object,
    "user" : JSON object
}
'''
def callback(channel, method, properties, body):
    print("\nReceived an sms from " + __file__)
    sendClientUpdate(json.loads(body))
    print()

'''
Function: sending an SMS to related users
Input: JSON object -> {
    "food" : JSON object,
    "user" : JSON object
}
Output: SMS sent to users + a line printing the result of each SMS + success line when code completes
'''
def sendClientUpdate(body):
    comment = body['comment']
    post = body['post']
    user = body['user']

    # twilio account id
    account_sid = "ACa19a8bdec26a1726665512c7cdd46b8b"
    # twilio auth token
    auth_token = "ae4f1d734eaddf6693475b0acd224d2f"

    client = Client(account_sid, auth_token)
    # for sending to one person

    # user info
    recipient_number = user['number']
    recipient_name = user['name']

    # comment info
    commenter_name = comment['commentor_username']
    comment_content = comment['comment']
    comment_datetime = comment['datetime']

    # post info
    # poster_name = post["username"]
    post_title = post["title"]
    # post_description = post["description"]
    # post_datetime = post["datetime"]

    ## INCLUDE YOUR FORUM VARIABLES HERE ##
    
    ## write your message here ##
    msg = f'Dear {recipient_name},\n\nUser {commenter_name} has commented on your post: {post_title}!\n\n{commenter_name} commented:\n{comment_content}\n- {comment_datetime}.'

    # create your text message
    message = client.messages.create(
        to=recipient_number,
        from_="+15077075060",
        body=msg)
    print(f"SMS to {recipient_name} has been sent to the following number : {recipient_number}")

    # for sending to multiple people

    # for each_user in user:
    #     recipient_number = each_user['number']
    #     recipient_name = each_user['name']
    #     food_location = food['location']
    #     msg = f"Dear {recipient_name}, there is a buffet located at {food_location} that is within your travel appetite."
    #     # create your text message
    #     message = client.messages.create(
    #         to=recipient_number,
    #         from_="+15077075060",
    #         body=msg)
    #     print(f"SMS to {recipient_name} has been sent to the following number : {recipient_number}")
    # return "All messages sent!"

if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(f": monitoring routing key '{monitor_binding_key}' in exchange '{amqp_setup.exchangename}' ...".format(
        monitor_binding_key, amqp_setup.exchangename))
    receive_sms()

# twilio -- sending sms practice
# account_sid = "ACa19a8bdec26a1726665512c7cdd46b8b"
# auth_token = "129c79176dd301a34abc383562c80f5b"
# client = Client(account_sid, auth_token)
# message = client.messages.create(
#   body="Hello from Twilio, racacacacacacacaca!",
#   from_="+15077075060",
#   to="+6588180849"
# )
# print(message.sid)