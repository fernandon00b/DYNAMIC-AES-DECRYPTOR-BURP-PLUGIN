from burp import IBurpExtender, ITab
from javax import swing
from java.awt import BorderLayout
from hashlib import md5
from base64 import b64decode
from base64 import b64encode
import base64
from Crypto import Random
from Crypto.Cipher import AES
import sys
import string
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
try:
    from exceptions_fix import FixBurpExceptions
except ImportError:
    pass


class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        # Required for easier debugging:
        # https://github.com/securityMB/burp-exceptions
        sys.stdout = callbacks.getStdout()

        # Keep a reference to our callbacks object
        self.callbacks = callbacks

        # Set our extension name
        self.callbacks.setExtensionName("AES Plugin by XzC")

        # Create the tab
        self.tab = swing.JPanel(BorderLayout())

        # Create the text area at the top of the tab
        textPanel = swing.JPanel()

        # Create the label for the text area
        boxVertical = swing.Box.createVerticalBox()
        boxHorizontal = swing.Box.createHorizontalBox()
        textLabel = swing.JLabel("Text to be encoded/decoded/hashed")
        boxHorizontal.add(textLabel)
        boxVertical.add(boxHorizontal)

        # Create the text area itself
        boxHorizontal = swing.Box.createHorizontalBox()
        self.textArea = swing.JTextArea('', 6, 100)
        self.textArea.setLineWrap(True)
        boxHorizontal.add(self.textArea)
        boxVertical.add(boxHorizontal)

        # Add the text label and area to the text panel
        textPanel.add(boxVertical)

        # Add the text panel to the top of the main tab
        self.tab.add(textPanel, BorderLayout.NORTH)

        # Created a tabbed pane to go in the center of the
        # main tab, below the text area
        tabbedPane = swing.JTabbedPane()
        self.tab.add("Center", tabbedPane);

        # First tab
        firstTab = swing.JPanel()
        firstTab.layout = BorderLayout()
        tabbedPane.addTab("Encode", firstTab)

        # Button for first tab
        buttonPanel = swing.JPanel()
        buttonPanel.add(swing.JButton('Encode', actionPerformed=self.encrypt))
        firstTab.add(buttonPanel, "North")



        # Panel for the encoders. Each label and text field
        # will go in horizontal boxes which will then go in
        # a vertical box
        encPanel = swing.JPanel()
        boxVertical = swing.Box.createVerticalBox()

        boxHorizontal = swing.Box.createHorizontalBox()
        self.b74EncField = swing.JTextField('', 75)
        boxHorizontal.add(swing.JLabel("  Encode   :"))
        boxHorizontal.add(self.b74EncField)
        boxVertical.add(boxHorizontal)

        # Add the vertical box to the Encode tab
        firstTab.add(boxVertical, "Center")
        #
        #
        #
        # Second tab
        secondTab = swing.JPanel()
        secondTab.layout = BorderLayout()
        tabbedPane.addTab("Decode", secondTab)
        # Button for first tab
        buttonPanel = swing.JPanel()
        buttonPanel.add(swing.JButton('Decode', actionPerformed=self.decrypt))
        secondTab.add(buttonPanel, "North")

        # Panel for the encoders. Each label and text field
        # will go in horizontal boxes which will then go in
        # a vertical box
        encPanel = swing.JPanel()
        boxVertical = swing.Box.createVerticalBox()

        boxHorizontal = swing.Box.createHorizontalBox()
        self.b64EncField = swing.JTextField('', 75)
        boxHorizontal.add(swing.JLabel("  Decode   :"))
        boxHorizontal.add(self.b64EncField)
        boxVertical.add(boxHorizontal)

        # Add the vertical box to the Encode tab
        secondTab.add(boxVertical, "Center")


        # Add the custom tab to Burp's UI
        callbacks.addSuiteTab(self)
        return

    # Implement ITab
    def decrypt(self, event):
        file = open("key.txt")
        key = file.read()
        ciphered_data = base64.b64decode(str(self.textArea.text))
        iv = "0123456789123456"
        cipher = AES.new(str.encode(key), AES.MODE_CBC,iv)
        original_data = unpad(cipher.decrypt(ciphered_data), AES.block_size)
        self.b64EncField.text = original_data

    def encrypt(self,event):
        file = open("key.txt")
        key = file.read()
        # key="heo!oc~n477817fb"
        # any = 'x' * 16
        any = 'x' * 16
        data = str.encode(any + str(self.textArea.text))
        seckey = str.encode(key)
        iv = "0123456789123456"
        cipher = AES.new(seckey, AES.MODE_CBC,iv)
        ciphered_data = cipher.encrypt(pad(data, AES.block_size))
        result = base64.b64encode(ciphered_data)
        print(result.decode("ISO-8859-1"))
        self.b74EncField.text = result.decode("ISO-8859-1")

    # def encode(self, event):
    #     """Encodes the user input and writes the encoded
    #     value to text fields.
    #     """
    #     text=self.textArea.text
    #     self.b64EncField.text = self.encrypt(text)

    def getTabCaption(self):
        """Return the text to be displayed on the tab"""
        return "AES Plugin by XzC"

    def getUiComponent(self):
        """Passes the UI to burp"""
        return self.tab


try:
    FixBurpExceptions()
except:
    pass