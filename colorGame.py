import random
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
# Game: Color - game_on
# name: Rakefet Rosen


start_game  = False
hostName = "localhost"
serverPort = 9090
color_dict = dict()
counter = 0
html = ''
finsh_count = 21
row_column = 18


class MyServer(BaseHTTPRequestHandler):
   
    def do_GET(self):
        global start_game
        global color_dict
        global counter
        global html
        global finsh_count
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        color = 'color'
        old_color = 'rak'
        html_temp = ""
        color_dict_short = { 'r': "red",'y': "yellow",'b': "blue",'g': "green"               }
        if not start_game:
            my_url = self.start_the_game()
        elif counter < finsh_count:
            if not self.check_finish():
                my_url = self.path
                if 'color' in my_url:
                    color = self.color_old_color(my_url, old_color)
                    if color != '' and color in color_dict_short:
                        self.new_color_board(color_dict_short, color)
                    elif color not in color_dict_short:  
                        self.message_color(color)
                if counter == finsh_count:
                    self.counter21()
            self.finish_game()
                        
   
    def finish_game(self):
        global html
        global color_dict
        result = self.check_finish()
        if result:
            html += '''<p style = "font-size: 40px; color: red" >Success!!!!</p>'''
            self.wfile.write(bytes(html, "utf-8"))
    
    def counter21(self):
        global html
        global color_dict
        result = self.check_finish()
        if result:
            html += '''<p style = "font-size: 40px; color: red" >Success!!!!</p>'''
        else:
            html1 = ''
            html1 += '''<p style = "font-size: 40px; color: red" >Game Over</p>'''
            self.wfile.write(bytes(html1, "utf-8"))

    def start_the_game(self):
        global color_dict
        global counter
        global html
        global start_game
        global game_on
        global finsh_count
        color_dict = self.create_dict_color()
        start_game = True
        color_dict1 = dict()
        game_on = True
        my_url = ''
        html = self.bord(color_dict, html)
        if counter < finsh_count:
            html += self.input()
        self.wfile.write(bytes(html, "utf-8"))
        return my_url

    def color_old_color(self, my_url, old_color):
        color = self.find_color(my_url)
        if color == old_color:
                color = ''      
        else:
            old_color = str(color)
        return color

    def message_color(self, color):
        global html
        html1 = html
        html1 += '''<p style = "font-size: 20px; color: red" >''' +  color + ''' is not in the color list, please use r for red, g for green, b for blue, y for yellow</p>'''
        self.wfile.write(bytes(html1, "utf-8"))
        time.sleep(3)
        self.wfile.write(bytes(html, "utf-8"))

    def new_color_board(self, color_dict_short, color ):
        global counter
        global html
        global color_dict
        counter = counter + 1
        this_color = color_dict_short[color]
        if self.check_input_color(this_color):
            color_dict = self.change_color(color_dict, this_color)
            html = self.bord(color_dict, html)
            html += self.input()
            self.wfile.write(bytes(html, "utf-8"))
    
    def find_color(self, my_url):
        url_list = my_url.split('=')
        return url_list[1]

    def bord(self, color_dict, html):
        global counter
        if counter == 0:
            headline = 'Coloring Game'
        else:
            headline = 'Choose a color'    
        html1 = ""
        html += '''<html><body><h1>''' + headline + '''</h1>'''
        html1 = self.create_table(color_dict)
        html += html1
        html += ''' </body></html>'''
        return html

    def create_table(self, color_dict):
        global row_column
        id=0
        html = '''<head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        
        <title>Coloring game</title>
    </head>'''
        html += '''<table style="padding: 0;" > <tbody style="style="padding: 0; margin: 0;"'''
        all = row_column+1
        for i in range(1,all):
            html += '''<tr style="padding: 0; margin: 0;border:0px solid white;">'''
            for j in range(1,all):
                id = id+1
                html += '''<td  style="padding: 0; margin: 0;display: block; width:20px; height:20px; border:0px solid white; background-color:''' + color_dict[id] +''' "><td>'''
            html += '''</tr>'''
        html += '''</tbody></table>'''
        return html

    def change_color(self, color_dict, color):
        global row_column
        build_new_color_dict = dict()
        starting_cell = color_dict[1] 
        build_new_color_dict[1] = color
        same_color_list = [1]
        all = row_column*row_column +1
        for i in range(1, all):
            if i == all:
                build_new_color_dict[i] = color_dict[i]
                break; 
            if i in same_color_list and color_dict[i+1] == starting_cell:
                same_color_list.append(i+1)
                if i+1 not in build_new_color_dict: 
                    build_new_color_dict[i+1] = color
            if i+row_column<all and i in same_color_list and color_dict[i+row_column] == starting_cell:
                same_color_list.append(i+row_column)
                if i+row_column not in build_new_color_dict:
                    build_new_color_dict[i+row_column] = color
            
            if i not in build_new_color_dict:
                build_new_color_dict[i] = color_dict[i]
        return build_new_color_dict

    def check_finish(self):
        global color_dict
        color = color_dict[1]
        for key, value in color_dict.items():
            if value != color:
                return False
        return True

    def create_dict_color(self):
        global row_column
        color_dict = dict()
        color_list = ["blue", "red", "yellow", "green"]
        all =row_column*row_column +1
        for i in range(1,all):
            color_dict[i] = random.choice(color_list)
        return color_dict

    def check_input_color(self, color):
        color_list = ["blue", "red", "yellow", "green"]
        if color in color_list:
            return True
        return False

    def input(self):
        global counter
        html1 = ''
        html1 +=  '''<form name="color" action="" method="get">''' +  str(counter) + ''' moves: <input type = "text" maxlength="5" size="40" name="color"> 
                        <input value="Submit" type="submit">   
                        </form>'''
        return html1
   


   
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
    