import time
import frida
import json
enc_cipher_hashcodes = [] #cipher objects with Cipher.ENCRYPT_MODE will be stored here
dec_cipher_hashcodes = [] #cipher objects with Cipher.ENCRYPT_MODE will be stored here


def my_message_handler(message, payload):
    #mainly printing the data sent from the js code, and managing the cipher objects according to their operation mode
    if message["type"] == "send":
        # print message["payload"]
        my_json = json.loads(message["payload"].encode("utf-8"))
        if my_json["my_type"] == "KEY":
            if str(payload.decode("utf-8"))  != 'sunlinecimbagent':
                file = open("key.txt","w")
                key = file.write(str(payload.decode("utf-8")))
                print ("\r\n[+] Current SecretKey: %s" % str(payload.decode("utf-8")))
        elif my_json["my_type"] == "IV":
            if str(payload.decode("utf-8")) != '0123456789123456':
                print ("[+] Curent IV: %s" % str(payload.decode("utf-8")))
    else:
        print (message)
        print ('*' * 16)
        print (payload)


#device = frida.get_usb_device()
#pid = device.spawn(["com.sunline.sinarmas"])
#device.resume(pid)
#time.sleep(1)  # Without it Java.perform silently fails
#session = device.attach(pid)
process = frida.get_usb_device(1).attach('app')

with open("s5.js") as f:
    script = process.create_script(f.read())
script.on("message", my_message_handler)  # register the message handler
script.load()

input("")

