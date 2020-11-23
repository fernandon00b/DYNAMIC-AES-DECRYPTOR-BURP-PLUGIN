This tool is used to decrypt Android applications that use dynamic AES encryption

To use this tool you must follow these steps:\n
1.install jython
2.install pycrypto
https://github.com/csm/jycrypto
3.start frida-server
4.open app
edit hook-aes.py
process = frida.get_usb_device (1) .attach ('app') change app with your app name
5.run hook-aes.py
