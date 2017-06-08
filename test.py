# test send sms to customer
from twilio.rest import Client

client = Client('AC410132c8bd44ed00f7f4539559884283', '47bd5593b50b4a7a46aa164542238016')

client.messages.create(to='+380687130103',
                       from_='+18582958048',
                       body='Ticket №0000199223')
