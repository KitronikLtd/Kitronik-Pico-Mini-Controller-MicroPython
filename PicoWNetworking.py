import network
import socket

class KitronikPicoWClient:
    
    # Client - Connect to soft AP setup by the server
    def __init__(self, ssid, password):
        # Create WiFi object of network type STA for station (client)
        self.wlan = network.WLAN(network.STA_IF)
        # Turn on the WiFi
        self.wlan.active(True)
        # Connect to the network setup by the server
        self.wlan.connect(ssid, password)
        # Create the socket to communicate with the server
        self.server = socket.socket()

    # While not connected, waiting for connection
    # while client.isWifiConnected() == False:
    #     sleep(0.5)
    def isWifiConnected(self):
        return self.wlan.isconnected()

    # Surround with try catch
    def connectToServer(self):
        # Get the gateway address for the network
        address = socket.getaddrinfo(self.wlan.ifconfig()[2], 80)[0][-1]
        # Connect to the socket using the network gateway address
        self.server.connect(address)

    # Surround with try catch
    def sendToServer(self, message):
        # Send message to server
        self.server.send(message)
    
    # Surround with try catch
    def receiveFromServer(self):
        # Receive message from server
        return self.server.recv(1024).decode()
    
    def disconnect(self):
        # Close connection
        self.server.close()
        # Disconnect from WiFi
        self.wlan.disconnect()

class KitronikPicoWServer:

    # Server - Start soft AP for client to connect to
    def __init__(self, ssid, password, ip = "10.0.0.4", gateway = "10.0.0.1"):
        # Create WiFi object of network type AP for access point (server)
        self.ap = network.WLAN(network.AP_IF)
        # Setup the network name as ssid with password as password
        self.ap.config(essid = ssid, password = password)
        # Setup the networks IP address, subnet mask, gateway address, DNS server
        self.ap.ifconfig((ip, "255.255.255.0", gateway, "8.8.8.8"))
        # Turn on the WiFi
        self.ap.active(True)
        # Create the socket to communicate with the client
        self.s = socket.socket()
        # Setup empty client
        self.client = None

    # While not turned on, waiting for access point
    # while ap.active() == False:
    #     pass
    def isAPConnected(self):
        return self.ap.active()

    # Surround with try catch
    def listenForClient(self):
        # Get the gateway address for the network
        address = socket.getaddrinfo(self.ap.ifconfig()[2], 80)[0][-1]
        # Bind the socket to the gateway address
        # Server will listen for clients on this address
        self.s.bind(address)
        # Start socket for client to connect to
        self.s.listen(1)
        # Accept a connection from a client
        self.client, _ = self.s.accept()
        
    # Surround with try catch
    def sendToClient(self, message):
        # Send message to server
        self.client.send(message)
    
    # Surround with try catch
    def receiveFromClient(self):
        # Receive message from client
        return self.client.recv(1024).decode()
    
    def disconnect(self):
        # Close connection
        self.client.close()
        # Disconnect from WiFi
        self.ap.disconnect()

