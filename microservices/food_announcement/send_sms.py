# only have $15.50 to spend :')
from twilio.rest import Client
import json
import requests
import os
import amqp_setup

monitor_binding_key = "#.sms.#"
'''
Function: initiate the queue
'''
def receive_sms():
    amqp_setup.check_setup()
    queue_name = 'sms'

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
    food = body['food']
    user = body['user']
    # twilio account id
    account_sid = "ACa19a8bdec26a1726665512c7cdd46b8b"
    # twilio auth token
    auth_token = "63a81c646c25631dcb76152906362f2e"

    client = Client(account_sid, auth_token)
    # for sending to one person

    recipient_number = user['number']
    recipient_name = user['name']
    food_location = food['address']
    food_name = food['post_name']
    food_latitude = food['latitude']
    food_longitude = food['longitude']
    food_description = food['description']
    food_allergens = food['allergens']
    food_end_time = food['end_time']
    
    msg = f"Dear {recipient_name}, there's food nearby!\nBuffet name: {food_name}\nBuffet Address: {food_location}\nBuffet Lat, Long: {food_latitude}, {food_longitude}\nBuffet Description: {food_description}\nAllergens: {food_allergens}\nBuffet End Timing: {food_end_time}"
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