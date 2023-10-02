#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

httpResponse = "HTTP/1.1 {} {}\r\nContent-Type: {}; charset=utf-8\r\n\r\n"

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        dataArray = self.data.decode().split(" ")    #split the request into an array

        if dataArray[0] == "GET":
            if "../" in dataArray[1]:
                self.request.sendall(bytearray(httpResponse.format(404, "Not Found", "text/html")+"Page Not Found",'utf-8'))
                return
            
            isDirectory = os.path.isdir("www" + dataArray[1]) #check if the path is a directory
            isFile = os.path.isfile("www" + dataArray[1]) #check if the path is a file

            if not isDirectory and not isFile: #if the path is neither a directory or a file, return 404
                self.request.sendall(bytearray(httpResponse.format(404, "Not Found", "text/html")+"Page Not Found",'utf-8'))
                return
            
            fileToRead = ""
            if isDirectory:
                if dataArray[1][-1] != "/":  
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: {}\nContent-Type: text/plain; charset=utf-8\r\n\r\n".format(dataArray[1]+"/"),'utf-8'))
                    return
                fileToRead = "www" + dataArray[1] + "index.html"
            else:
                fileToRead = "www" + dataArray[1]

            f = open(fileToRead, "r")
            file = f.read()

            if ".html" in fileToRead:  #if the file is an html file, return 200 OK with text/html
                self.request.sendall(bytearray(httpResponse.format(200, "OK", "text/html")+file,'utf-8'))
                return
            else: #if the file is a css file, return 200 OK with text/css
                self.request.sendall(bytearray(httpResponse.format(200, "OK", "text/css")+file,'utf-8'))
                return
                
        else:   
            self.request.sendall(bytearray(httpResponse.format(405, "Method Not Allowed", "text/html"),'utf-8'))
            return
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
