#importing libraries
import pygame
import string
import sqlite3

#initialising pygame
pygame.init()

#find pygame resolution
info = pygame.display.Info()
title_w, title_h = info.current_w, info.current_h

#title page creation
title_page = pygame.display.set_mode((title_w,title_h), pygame.FULLSCREEN | pygame.SCALED)

#load original image for title
titlebg = pygame.image.load("Frontpage.png").convert()
#scale to full screen
title_w, title_h = title_page.get_size()
titlebg = pygame.transform.smoothscale(titlebg, (title_w, title_h))

#title class
class Title:
    def __init__(self,text,font,colour,x,y):
        self.text = font.render(text,True,colour)
        self.rect = self.text.get_rect(center=(x,y))

    def draw(self, surface):
        surface.blit(self.text,self.rect)

#title font
title_font = pygame.font.Font("Jomhuria-Regular.ttf", 300)

#title creation(main)
title_main = Title("CINCO!",title_font,"white",title_w//2,title_h * 0.3)

#button class
class Button:
    def __init__(self,x,y,w,h,text,font,colour,hover_colour,text_colour,border_colour,border_width):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = font.render(text,True,text_colour)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.colour = colour
        self.hover_colour = hover_colour
        self.border_colour = border_colour
        self.border_width = border_width
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface,self.hover_colour,self.rect)
        else:
            pygame.draw.rect(surface,self.colour,self.rect)
        surface.blit(self.text, self.text_rect)
        pygame.draw.rect(surface,self.border_colour,self.rect,width=self.border_width)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False
#button font and position (when width == 300)
button_x = title_w // 2 - 150
button_y = title_h // 2
button_font = pygame.font.Font("Jomhuria-Regular.ttf", 80)

#title page buttons
login_button = Button(x=button_x,y=button_y,w=300,h=120,text="LOGIN",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

reg_button = Button(x=button_x,y=button_y * 1.4,w=300,h=120,text="REGISTER",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

exit_button = Button(x=button_x * 0.2,y=button_y * 0.2,w=150,h=100,text="EXIT",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

#login page creation
login_page = pygame.display.set_mode((title_w,title_h), pygame.FULLSCREEN | pygame.SCALED)
loginbg = pygame.transform.smoothscale(titlebg, (title_w, title_h))

#login page title
login_title = Title("LOGIN",title_font,"white",title_w//2,title_h * 0.3)

#login label font
normal_font = pygame.font.Font("Jomhuria-Regular.ttf", 100)

#inputs font
input_font = pygame.font.Font("Jomhuria-Regular.ttf",80)

#login labels
login_username_label = Title("Username:",normal_font,"white",title_w * 0.3,title_h * 0.55)
login_password_label = Title("Password:",normal_font,"white",title_w * 0.3,title_h * 0.65)

#class for input boxes
class InputBox:
    def __init__(self,x,y,w,h,text_colour,font):
        self.rect = pygame.Rect(x,y,w,h)
        self.font = font
        self.text_colour = text_colour
        self.inputBox = pygame.Rect(x,y,w,h)
        self.text = " "
        self.colourInactive = "#FFFFFF"
        self.colourActive = "#808080"
        self.colour = self.colourInactive
        self.hover_colour = "#5F5F5F"
        self.border_colour = "#000000"
        self.border_width = 5
        self.active = False
        self.inactive = True

    def do_event(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.inputBox.collidepoint(event.pos)
            if self.active:
                self.colour = self.colourActive
            else:
                self.colour = self.colourInactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.inputBox.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_colour, self.inputBox)
        else:
            pygame.draw.rect(surface, self.colour, self.inputBox)
        textsurface = self.font.render(self.text, True, self.text_colour)
        width = max(600,textsurface.get_width()+10)
        self.inputBox.w = width
        surface.blit(textsurface,(self.inputBox.x+5,self.inputBox.y+5))
        pygame.draw.rect(surface, self.border_colour, self.inputBox, width=self.border_width)

#login input boxes
login_username_input = InputBox(title_w * 0.4,title_h * 0.51,300,75,"#000000",normal_font)
login_password_input = InputBox(title_w * 0.4,title_h * 0.61,300,75,"#000000",normal_font)

#login page buttons
login_page_button = Button(x=button_x * 0.6,y=button_y * 1.5,w=300,h=120,text="Login",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)
forgot_password_button = Button(x=button_x * 1.3,y=button_y * 1.5,w=400,h=120,text="Forgot Password",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

#register page creation
register_page = pygame.display.set_mode((title_w,title_h), pygame.FULLSCREEN | pygame.SCALED)
registerbg = pygame.transform.smoothscale(titlebg, (title_w,title_h))

#register page title
register_title = Title("REGISTER",title_font,"white",title_w//2,title_h * 0.3)

#register page labels and inputs
reg_username_label = Title("Username:",normal_font,"white",title_w * 0.3,title_h * 0.45)
reg_username_input = InputBox(title_w * 0.4,title_h * 0.41,300,75,"#000000",normal_font)
reg_email_label = Title("Email Address:",normal_font,"white",title_w * 0.27,title_h * 0.55)
reg_email_input = InputBox(title_w * 0.4,title_h * 0.51,300,75,"#000000",normal_font)
reg_password_label = Title("Password:",normal_font,"white",title_w * 0.3,title_h * 0.65)
reg_password_input = InputBox(title_w * 0.4,title_h * 0.61,300,75,"#000000",normal_font)
reg_confirm_label = Title("Confirm Password:",normal_font,"white",title_w * 0.24,title_h * 0.75)
reg_confirm_input = InputBox(title_w * 0.4,title_h * 0.71,300,75,"#000000",normal_font)

#create account button
create_account_button = Button(x=(title_w - 400) // 2,y=button_y * 1.65,w=400,h=120,text="Create Account",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

#reset page creation
reset_page = pygame.display.set_mode((title_w,title_h), pygame.FULLSCREEN | pygame.SCALED)
resetbg = pygame.transform.smoothscale(titlebg, (title_w,title_h))

#reset page title
reset_title = Title("RESET PASSWORD",title_font,"white",title_w//2,title_h * 0.3)

#reset page labels and inputs
reset_email_label = Title("Email Address:",normal_font,"white",title_w * 0.27,title_h * 0.45)
reset_email_input = InputBox(title_w * 0.4,title_h * 0.41,300,75,"#000000",input_font)
reset_password_label = Title("Password:",normal_font,"white",title_w * 0.3,title_h * 0.55)
reset_password_input = InputBox(title_w * 0.4,title_h * 0.51,300,75,"#000000",input_font)
reset_confirm_label = Title("Confirm Password:",normal_font,"white",title_w * 0.24,title_h * 0.65)
reset_confirm_input = InputBox(title_w * 0.4,title_h * 0.61,300,75,"#000000",input_font)

#reset password button
reset_button = Button(x=(title_w - 400) // 2,y=button_y * 1.5,w=400,h=120,text="Reset Password",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

#menu page creation
menu_page = pygame.display.set_mode((title_w,title_h), pygame.FULLSCREEN | pygame.SCALED)
menubg = pygame.transform.smoothscale(titlebg, (title_w,title_h))

#menu page title
menu_title = Title("MAIN MENU",title_font,"white",title_w//2,title_h * 0.2)

#menu page buttons
menu_play_button = Button(x=(title_w - 400) // 2,y=button_y * 0.7,w=400,h=120,text="PLAY",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

menu_leaderboard_button = Button(x=(title_w - 400) // 2,y=button_y * 1,w=400,h=120,text="Leaderboard",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

menu_rules_button = Button(x=(title_w - 400) // 2,y=button_y * 1.3,w=400,h=120,text="Rules/Tutorial",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

menu_settings_button = Button(x=(title_w - 400) // 2,y=button_y * 1.6,w=400,h=120,text="Settings",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

menu_exit_button = Button(x=button_x * 0.2,y=button_y * 0.2,w=150,h=100,text="EXIT",font=button_font,
    colour="#CD2626",hover_colour="#8B0000",text_colour="#FFFFFF",border_colour="#000000",border_width=5)

#creating database

#connecting to database file
credentials_db = sqlite3.connect("credentials.db")

#creating cursor, to send commands to the database
cursor = credentials_db.cursor()

#creating table of data
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_credentials (
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )""")

#adding users to the database
def addUser(username,email,password):
    connect = sqlite3.connect("credentials.db")
    cur = connect.cursor()
    cur.execute("INSERT INTO user_credentials (username, email, password) VALUES (?,?,?)",
    (username,email,password))
    connect.commit()
    connect.close()

#data checks for validation

#presence check function
def presence_check(text):
    return text.strip()

presence_check_text = Title("Not all fields are filled in - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#length check function for login system username
def length_check_user(text):
    if len(text) < 4:
        return 1
    elif len(text) > 16:
        return 2
    return None

#length check function for login system password:
def length_check_pass(text):
    if len(text) < 8:
        return 1
    elif len(text) > 16:
        return 2
    return None

length_check_text_user_short  = Title("Username is too short - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)
length_check_text_user_long  = Title("Username is too long - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)
length_check_text_pass_short = Title("Password is too short - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)
length_check_text_pass_long  = Title("Password is too long - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#format check function for login system password
def has_special_char(text):
    special_characters = string.punctuation
    return any(char in special_characters for char in text)

format_check_text = Title("Password must contain a special character - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#lookup check function for login system
def check_User(text1,text2):
    connect = sqlite3.connect("credentials.db")
    cur = connect.cursor()
    cur.execute("SELECT * FROM user_credentials WHERE username = ? AND password = ?",(text1,text2))
    result = cur.fetchone()
    connect.close()
    if result:
        return True
    else:
        return False
lookup_check_text = Title("Credentials not found - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#successful login
login_successful_text = Title("Login Successful!",normal_font,"white",title_w//2, title_h * 0.95)

#creating validation variables
show_presence_check_error = False
show_length_check_error_user_short = False
show_length_check_error_user_long = False
show_length_check_error_pass_short = False
show_length_check_error_pass_long = False
show_format_check_error_pass = False
show_lookup_error = False
show_login_successful = False

#gameloop
runtime = True
while runtime:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()

       #login input text
       login_username_input.do_event(event)
       login_password_input.do_event(event)

       #data validation
       if login_page_button.is_clicked(event):
           username = login_username_input.text.strip()
           password = login_password_input.text.strip()

           #presence check
           if not presence_check(username) or not presence_check(password):
               show_presence_check_error = True
               show_length_check_error_user_short = False
               show_length_check_error_user_long = False
               show_length_check_error_pass_short = False
               show_length_check_error_pass_long = False
               show_format_check_error_pass = False
               show_lookup_error = False

           #length check for username
           elif length_check_user(username) == 1:
               show_presence_check_error = False
               show_length_check_error_user_short = True
               show_length_check_error_user_long = False
               show_length_check_error_pass_short = False
               show_length_check_error_pass_long = False
               show_format_check_error_pass = False
               show_lookup_error = False

           elif length_check_user(username) == 2:
               show_presence_check_error = False
               show_length_check_error_user_short = False
               show_length_check_error_user_long = True
               show_length_check_error_pass_short = False
               show_length_check_error_pass_long = False
               show_format_check_error_pass = False
               show_lookup_error = False

           #length check for password
           elif length_check_pass(password) == 1:
               show_presence_check_error = False
               show_length_check_error_user_short = False
               show_length_check_error_user_long = False
               show_length_check_error_pass_short = True
               show_length_check_error_pass_long = False
               show_format_check_error_pass = False
               show_lookup_error = False

           elif length_check_pass(password) == 2:
               show_presence_check_error = False
               show_length_check_error_user_short = False
               show_length_check_error_user_long = False
               show_length_check_error_pass_short = False
               show_length_check_error_pass_long = True
               show_format_check_error_pass = False
               show_lookup_error = False

           #format check for password
           elif not has_special_char(password):
               show_presence_check_error = False
               show_length_check_error_user_short = False
               show_length_check_error_user_long = False
               show_length_check_error_pass_short = False
               show_length_check_error_pass_long = False
               show_format_check_error_pass = True
               show_lookup_error = False

           elif not check_User(username,password):
               show_presence_check_error = False
               show_length_check_error_user_short = False
               show_length_check_error_user_long = False
               show_length_check_error_pass_short = False
               show_length_check_error_pass_long = False
               show_format_check_error_pass = False
               show_lookup_error = True
           elif check_User(username,password):
               show_presence_check_error = False
               show_length_check_error_user_short = False
               show_length_check_error_user_long = False
               show_length_check_error_pass_short = False
               show_length_check_error_pass_long = False
               show_format_check_error_pass = True
               show_lookup_error = False
               show_login_successful = True

       #register input text
       reg_username_input.do_event(event)
       reg_email_input.do_event(event)
       reg_password_input.do_event(event)
       reg_confirm_input.do_event(event)

       #reset input text
       reset_email_input.do_event(event)
       reset_password_input.do_event(event)
       reset_confirm_input.do_event(event)

   #drawing title page screen/labels/buttons
   title_page.blit(titlebg, (0,0))
   title_main.draw(title_page)
   login_button.draw(title_page)
   reg_button.draw(title_page)
   exit_button.draw(title_page)

   #drawing login page screen/labels/buttons
   login_page.blit(loginbg, (0,0))
   login_title.draw(login_page)
   login_username_label.draw(login_page)
   login_password_label.draw(login_page)
   login_username_input.draw(login_page)
   login_password_input.draw(login_page)
   login_page_button.draw(login_page)
   forgot_password_button.draw(login_page)

   #login validation variables/ printing error messages
   if show_presence_check_error:
       presence_check_text.draw(login_page)
   elif show_length_check_error_user_short:
       length_check_text_user_short.draw(login_page)
   elif show_length_check_error_user_long:
       length_check_text_user_long.draw(login_page)
   elif show_length_check_error_pass_short:
       length_check_text_pass_short.draw(login_page)
   elif show_length_check_error_pass_long:
       length_check_text_pass_long.draw(login_page)
   elif show_format_check_error_pass:
       format_check_text.draw(login_page)
   elif show_lookup_error:
       lookup_check_text.draw(login_page)
   elif show_login_successful:
       login_successful_text.draw(login_page)


   pygame.display.flip()










