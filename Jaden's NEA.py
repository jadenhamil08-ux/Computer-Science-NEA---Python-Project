#importing libraries
from dotenv import load_dotenv, find_dotenv
import os
import pygame
import random
import smtplib
import string
import sqlite3

#initialising pygame
pygame.init()

# screen creation
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w,info.current_h), pygame.FULLSCREEN | pygame.SCALED)

#get screen size
title_w, title_h = screen.get_size()

#load original image / scale page
bg = pygame.image.load("Frontpage.png").convert()
bg = pygame.transform.smoothscale(bg, (title_w, title_h))

#title class
class Title:
    def __init__(self,text,font,colour,x,y):
        self.text = font.render(text,True,colour)
        self.rect = self.text.get_rect(center=(x,y))

    def draw(self, surface):
        surface.blit(self.text,self.rect)

#title font
title_font = pygame.font.Font("Jomhuria-Regular.ttf", 300)

#main label font
normal_font = pygame.font.Font("Jomhuria-Regular.ttf", 100)

#input font
input_font = pygame.font.Font("Jomhuria-Regular.ttf", 80)

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

#render text over multiple lines
def render_multi_lines(surface,text,x,y,font,colour):
    lines = text.splitlines()
    line_height = font.get_linesize()
    for index,line in enumerate(lines):
        surface.blit(font.render(line,True,colour),(x,y + (index * line_height)))

#button font and position (when width == 300)
button_x = title_w // 2 - 150
button_y = title_h // 2
button_font = pygame.font.Font("Jomhuria-Regular.ttf", 80)

#class for input boxes
class InputBox:
    def __init__(self,x,y,w,h,text_colour,font):
        self.rect = pygame.Rect(x,y,w,h)
        self.font = font
        self.text_colour = text_colour
        self.text = ""
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
            self.active = self.rect.collidepoint(event.pos)
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
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_colour, self.rect)
        else:
            pygame.draw.rect(surface, self.colour, self.rect)
        textsurface = self.font.render(self.text, True, self.text_colour)
        width = max(self.rect.w,textsurface.get_width()+10)
        self.rect.w = width
        surface.blit(textsurface,(self.rect.x+5,self.rect.y))
        pygame.draw.rect(surface, self.border_colour, self.rect, width=self.border_width)

#===================#
# CREATING DATABASE #
#===================#

# creating table of data
with sqlite3.connect("credentials.db") as connect:
    cursor = connect.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_credentials (
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )""")
connect.commit()

# adding users to the database
def addUser(username,email,password):
    with sqlite3.connect("credentials.db") as connect:
        cur = connect.cursor()
        cur.execute("INSERT INTO user_credentials (username, email, password) VALUES (?,?,?)",
        (username,email,password))
        connect.commit()

# change password in the database
def changePassword(email,password):
    with sqlite3.connect("credentials.db") as connect:
        cur = connect.cursor()
        cur.execute("UPDATE user_credentials SET password=? WHERE email=?",(password,email))
        connect.commit()

#===================================#
# DATA VALIDATIONS FOR LOGIN SYSTEM #
#===================================#

#presence check function
def presence_check(text):
    return text.strip() != ""

presence_check_text = Title("Not all fields are filled in - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#length check function for login system username
def length_check_user(text):
    if len(text) < 4:
        return 1
    elif len(text) > 16:
        return 2
    return None

#length check function for password:
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

#format check function for password
def has_special_char(text):
    special_characters = string.punctuation
    return any(char in special_characters for char in text)
format_check_text = Title("Password must contain a special character - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#format check for email
def email_format(text):
    if "@" not in text:
        return False
    if text.count("@") != 1:
        return False
    local, domain = text.split("@")
    if not local or not domain:
        return False
    elif "." not in domain:
        return False
    else:
        return True
format_email_check_text = Title("Invalid email format - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#match check for password/confirm in register
def check_match(text1,text2):
    if text1 != text2:
        return False
    else:
        return True
match_password_error_text = Title("Passwords do not match - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#lookup check function for login system
def check_User(text1,text2):
    with sqlite3.connect("credentials.db") as connect:
        cur = connect.cursor()
        cur.execute("SELECT * FROM user_credentials WHERE username = ? AND password = ?",(text1,text2))
        result = cur.fetchone()
    if result:
        return True
    else:
        return False
lookup_check_text = Title("Credentials not found - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#lookup user check for registration
def lookup_user(text):
    with sqlite3.connect("credentials.db") as connect:
        cur = connect.cursor()
        cur.execute("SELECT * FROM user_credentials WHERE username = ?", (text,))
        result = cur.fetchone()
    if result:
        return True
    else:
        return False
user_exists_text = Title("Username already exists - Please enter an alternative.",normal_font,"white",title_w//2, title_h * 0.95)

#lookup email check for registration
def lookup_email(text):
    with sqlite3.connect("credentials.db") as connect:
        cur = connect.cursor()
        cur.execute("SELECT * FROM user_credentials WHERE email = ?", (text,))
        result = cur.fetchone()
    if result:
        return True
    else:
        return False
email_exists_text = Title("Email already exists - Please enter an alternative.",normal_font,"white",title_w//2, title_h * 0.95)
email_not_exists_text = Title("Email not found - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#code check for password reset
match_code_error_text = Title("Code does not match - Please try again.",normal_font,"white",title_w//2, title_h * 0.95)

#successful login/register message
login_successful_text = Title("Login Successful!",normal_font,"white",title_w//2, title_h * 0.95)
create_account_successful_text = Title("Account created successfully!",normal_font,"white",title_w//2, title_h * 0.95)
reset_pass_successful_text = Title("Password reset successfully!",normal_font,"white",title_w//2, title_h * 0.95)

#MAIN VALIDATION FUNCTION FOR LOGIN
def validate_login(username,password):
    #presence check
    if not presence_check(username) or not presence_check(password):
        return False, presence_check_text

    #lookup check username
    if not check_User(username,password):
        return False, lookup_check_text

    return True, login_successful_text

#MAIN VALIDATION FUNCTION FOR REGISTRATION
def validate_registration(username, email, password, conpassword):
    #presence check
    if not presence_check(username) or not presence_check(email) or not presence_check(password) or not presence_check(conpassword):
        return False, presence_check_text

    #username length
    userlen = length_check_user(username)
    if userlen == 1:
        return False, length_check_text_user_short
    if userlen == 2:
        return False, length_check_text_user_long

    #email format
    if not email_format(email):
        return False, format_email_check_text

    #password length
    passlen = length_check_pass(password)
    if passlen == 1:
        return False, length_check_text_pass_short
    elif passlen == 2:
        return False, length_check_text_pass_long

    #password special character
    if not has_special_char(password):
        return False, format_check_text

    #matching passwords
    if not check_match(password, conpassword):
        return False, match_password_error_text

    #username exists
    if lookup_user(username):
        return False, user_exists_text

    #email exists
    if lookup_email(email):
        return False, email_exists_text

    return True, None

#MAIN VALIDATION FUNCTION FOR RESET PASSWORD
def validate_reset_password(email, password, conpassword):
    #presence check
    if not presence_check(email) or not presence_check(password) or not presence_check(conpassword):
        return False, presence_check_text

    #email format
    if not email_format(email):
        return False, format_email_check_text

    #lookup email
    if not lookup_email(email):
        return False, email_not_exists_text

    #password length
    passlen = length_check_pass(password)
    if passlen == 1:
        return False, length_check_text_pass_short
    elif passlen == 2:
        return False, length_check_text_pass_long

    #password special character
    if not has_special_char(password):
        return False, format_check_text

    #matching passwords
    if not check_match(password, conpassword):
        return False, match_password_error_text

    return True, None

#VALIDATION FUNCTION FOR PASSWORD RESET:
def validate_reset_pass_verify(code,sent_code):
    #presence check
    if not presence_check(code):
        return False, presence_check_text
    if not check_match(code,sent_code):
        return False, match_code_error_text

    return True, None

#generate code
def generate_code():
    return random.randint(100000,999999)

#verification email
def send_email(email,code):
    sender = "cincoofficialgame@gmail.com"
    receiver = email
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    password = os.getenv("APP_PASSWORD")
    subject = "Email Verification to Reset Password"
    body = f"Here is your code, please enter it in the text box within the game: \n {code}"
    message = f"""From: {sender}
To: {receiver}
Subject: {subject}

{body}
"""
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    try:
        server.login(sender,password)
        server.sendmail(sender, receiver, message)
        server.quit()
        print("Code sent successfully")
    except Exception as e:
        print(e)

#=============#
#DRAWING PAGES#
#=============#

# Page Parent Class
class Page:
    def draw_page(self,surface):
        surface.blit(bg,(0,0))

    def handle_event(self,event):
        pass

# Title Page Class
class TitlePage(Page):
    def __init__(self):
        # title creation(main)
        self.title_main = Title("CINCO!", title_font, "white", title_w // 2, title_h * 0.3)

        # title page buttons
        self.login_button = Button(x=button_x, y=button_y, w=300, h=120, text="LOGIN",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)

        self.reg_button = Button(x=button_x, y=button_y * 1.4, w=300, h=120, text="REGISTER",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)

        self.exit_button = Button(x=button_x * 0.15, y=button_y * 1.55, w=150, h=100, text="EXIT",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)

    def handle_event(self,event):
        global current_page
        if self.login_button.is_clicked(event):
            current_page = LoginPage()
        if self.reg_button.is_clicked(event):
            current_page = RegisterPage()
        if self.exit_button.is_clicked(event):
            pygame.quit()

    def draw_page(self,surface):
        super().draw_page(surface)
        self.title_main.draw(surface)
        self.login_button.draw(surface)
        self.reg_button.draw(surface)
        self.exit_button.draw(surface)

# Login Page Class
class LoginPage(Page):
    def __init__(self):
        # login page title
        self.login_username_input = InputBox(title_w * 0.4,title_h * 0.51,600,70,"#000000",input_font)
        self.login_password_input = InputBox(title_w * 0.4,title_h * 0.61,600,70,"#000000",input_font)
        self.login_title = Title("LOGIN", title_font, "white", title_w // 2, title_h * 0.3)

        # login labels
        self.login_username_label = Title("Username:", normal_font, "white", title_w * 0.3, title_h * 0.55)
        self.login_password_label = Title("Password:", normal_font, "white", title_w * 0.3, title_h * 0.65)

        # login page buttons
        self.login_page_button = Button(x=button_x * 0.6, y=button_y * 1.5, w=300, h=120, text="Login",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF",border_colour="#000000", border_width=5)
        self.forgot_password_button = Button(x=button_x * 1.3, y=button_y * 1.5, w=400, h=120, text="Forgot Password",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF",border_colour="#000000", border_width=5)
        self.back_button = Button(x=button_x * 0.15, y=button_y * 1.55, w=150, h=100, text="BACK",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)

    def handle_event(self,event):
        global current_page,current_error_message
        self.login_username_input.do_event(event)
        self.login_password_input.do_event(event)

        # data validation for login
        if self.login_page_button.is_clicked(event):
            username = self.login_username_input.text.strip()
            password = self.login_password_input.text.strip()
            is_valid, message = validate_login(username, password)

            # error message to print/success
            if not is_valid:
                current_error_message = message
            else:
                current_error_message = None
                current_page = MenuPage()

        elif self.forgot_password_button.is_clicked(event):
            current_page = ResetPassPage()
        elif self.back_button.is_clicked(event):
            current_page = TitlePage()

    def draw_page(self,surface):
        super().draw_page(surface)
        self.login_title.draw(surface)
        self.login_username_label.draw(surface)
        self.login_password_label.draw(surface)
        self.login_username_input.draw(surface)
        self.login_password_input.draw(surface)
        self.login_page_button.draw(surface)
        self.forgot_password_button.draw(surface)
        self.back_button.draw(surface)

# Register Page Class
class RegisterPage(Page):
    def __init__(self):
        # register page title
        self.register_title = Title("REGISTER", title_font, "white", title_w // 2, title_h * 0.25)

        # register page labels and inputs
        self.reg_username_label = Title("Username:", normal_font, "white", title_w * 0.3, title_h * 0.4)
        self.reg_username_input = InputBox(title_w * 0.4, title_h * 0.36, 600, 75, "#000000", input_font)
        self.reg_email_label = Title("Email Address:", normal_font, "white", title_w * 0.27, title_h * 0.5)
        self.reg_email_input = InputBox(title_w * 0.4, title_h * 0.46, 600, 75, "#000000", input_font)
        self.reg_password_label = Title("Password:", normal_font, "white", title_w * 0.3, title_h * 0.6)
        self.reg_password_input = InputBox(title_w * 0.4, title_h * 0.56, 600, 75, "#000000", input_font)
        self.reg_confirm_label = Title("Confirm Password:", normal_font, "white", title_w * 0.24, title_h * 0.7)
        self.reg_confirm_input = InputBox(title_w * 0.4, title_h * 0.66, 600, 75, "#000000", input_font)

        # register page buttons
        self.create_account_button = Button(x=(title_w - 400) // 2, y=button_y * 1.55, w=400, h=120, text="Create Account",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000", border_width=5)
        self.back_button = Button(x=button_x * 0.15, y=button_y * 1.55, w=150, h=100, text="BACK",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)

    def handle_event(self,event):
        global current_page,current_error_message
        # register input text
        self.reg_username_input.do_event(event)
        self.reg_email_input.do_event(event)
        self.reg_password_input.do_event(event)
        self.reg_confirm_input.do_event(event)

        # register page validations
        if self.create_account_button.is_clicked(event):
            username = self.reg_username_input.text.strip()
            email = self.reg_email_input.text.strip()
            password = self.reg_password_input.text.strip()
            conpassword = self.reg_confirm_input.text.strip()

            is_valid, message = validate_registration(username, email, password, conpassword)

            # error message to print/success
            if not is_valid:
                current_error_message = message
            else:
                addUser(username,email,password)
                current_error_message = None
                current_page = LoginPage()
        elif self.back_button.is_clicked(event):
            current_page = TitlePage()

    def draw_page(self,surface):
        super().draw_page(surface)
        self.register_title.draw(surface)
        self.reg_username_label.draw(surface)
        self.reg_username_input.draw(surface)
        self.reg_email_label.draw(surface)
        self.reg_email_input.draw(surface)
        self.reg_password_label.draw(surface)
        self.reg_password_input.draw(surface)
        self.reg_confirm_label.draw(surface)
        self.reg_confirm_input.draw(surface)
        self.create_account_button.draw(surface)
        self.back_button.draw(surface)

# Reset Password Page
class ResetPassPage(Page):
    def __init__(self):
        # reset page title
        self.reset_title = Title("RESET PASSWORD", title_font, "white", title_w // 2, title_h * 0.3)

        # reset page labels and inputs
        self.reset_email_label = Title("Email Address:", normal_font, "white", title_w * 0.27, title_h * 0.45)
        self.reset_email_input = InputBox(title_w * 0.4, title_h * 0.41, 600, 75, "#000000", input_font)
        self.reset_password_label = Title("Password:", normal_font, "white", title_w * 0.3, title_h * 0.55)
        self.reset_password_input = InputBox(title_w * 0.4, title_h * 0.51, 600, 75, "#000000", input_font)
        self.reset_confirm_label = Title("Confirm Password:", normal_font, "white", title_w * 0.24, title_h * 0.65)
        self.reset_confirm_input = InputBox(title_w * 0.4, title_h * 0.61, 600, 75, "#000000", input_font)

        # reset page buttons
        self.reset_button = Button(x=(title_w - 400) // 2, y=button_y * 1.5, w=400, h=120, text="Reset Password",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)
        self.back_button = Button(x=button_x * 0.15, y=button_y * 1.55, w=150, h=100, text="BACK",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)

    def handle_event(self,event):
        global current_page,current_error_message,current_email,current_password
        # reset input text
        self.reset_email_input.do_event(event)
        self.reset_password_input.do_event(event)
        self.reset_confirm_input.do_event(event)

        if self.reset_button.is_clicked(event):
            email = self.reset_email_input.text.strip()
            password = self.reset_password_input.text.strip()
            conpassword = self.reset_confirm_input.text.strip()

            is_valid, message = validate_reset_password(email, password, conpassword)

            if not is_valid:
                current_error_message = message
            else:
                current_password = password
                current_error_message = None
                current_email = email
                current_page = EmailVeriPage()
        elif self.back_button.is_clicked(event):
            current_page = LoginPage()

    def draw_page(self,surface):
        # drawing reset password page screen/labels/buttons
        super().draw_page(surface)
        self.reset_title.draw(surface)
        self.reset_email_label.draw(surface)
        self.reset_email_input.draw(surface)
        self.reset_password_label.draw(surface)
        self.reset_password_input.draw(surface)
        self.reset_confirm_label.draw(surface)
        self.reset_confirm_input.draw(surface)
        self.reset_button.draw(surface)
        self.back_button.draw(surface)

# Email Verification Page (To reset password)
class EmailVeriPage(Page):
    def __init__(self):
        # email verification page title
        self.email_veri_page_title = Title("EMAIL VERIFICATION", title_font, "white", title_w // 2, title_h * 0.15)

        # email verification page label and input
        self.code_sent_message = """
Please click the send code button below to send a code 
to your email address. Enter the code in the text box 
below to verify your password:
        """
        self.code_input = InputBox(title_w * 0.4, title_h * 0.6, 300, 75, "#000000", input_font)

        # email verification page buttons
        self.send_code_button = Button(x=button_x * 0.6, y=button_y * 1.5, w=400, h=120, text="Send Code",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF",border_colour="#000000", border_width=5)

        self.verify_reset_button = Button(x=button_x * 1.3, y=button_y * 1.5, w=500, h=120, text="Verify Password Reset",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF",border_colour="#000000", border_width=5)
        self.back_button = Button(x=button_x * 0.15, y=button_y * 1.55, w=150, h=100, text="BACK",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)

    def handle_event(self,event):
        global current_page,current_error_message,current_code_sent
        self.code_input.do_event(event)

        if self.send_code_button.is_clicked(event):
            current_code_sent = str(generate_code())
            send_email(current_email,current_code_sent)

        elif self.verify_reset_button.is_clicked(event):
            code = self.code_input.text.strip()

            is_valid, message = validate_reset_pass_verify(code,current_code_sent)

            if not is_valid:
                current_error_message = message

            else:
                changePassword(current_email,current_password)
                current_error_message = None
                current_page = LoginPage()
        elif self.back_button.is_clicked(event):
            current_page = ResetPassPage()

    def draw_page(self,surface):
        # drawing verify email page labels/buttons/input
        super().draw_page(surface)
        self.email_veri_page_title.draw(surface)
        render_multi_lines(surface, self.code_sent_message, 100, title_h * 0.15, normal_font, "#FFFFFF")
        self.code_input.draw(surface)
        self.send_code_button.draw(surface)
        self.verify_reset_button.draw(surface)
        self.back_button.draw(surface)

class MenuPage(Page):
    def __init__(self):
        # menu page title
        self.menu_title = Title("MAIN MENU", title_font, "white", title_w // 2, title_h * 0.2)

        # menu page buttons
        self.menu_play_button = Button(x=(title_w - 400) // 2, y=button_y * 0.7, w=400, h=120, text="PLAY",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF",border_colour="#000000", border_width=5)

        self.menu_leaderboard_button = Button(x=(title_w - 400) // 2, y=button_y * 1, w=400, h=120, text="Leaderboard",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF",border_colour="#000000", border_width=5)

        self.menu_rules_button = Button(x=(title_w - 400) // 2, y=button_y * 1.3, w=400, h=120, text="Rules/Tutorial",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF",border_colour="#000000", border_width=5)

        self.menu_settings_button = Button(x=(title_w - 400) // 2, y=button_y * 1.6, w=400, h=120, text="Settings",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF",border_colour="#000000", border_width=5)

        self.exit_button = Button(x=button_x * 0.15, y=button_y * 1.55, w=150, h=100, text="EXIT",
            font=button_font,colour="#CD2626", hover_colour="#8B0000", text_colour="#FFFFFF", border_colour="#000000",border_width=5)

    def handle_event(self,event):
        if self.exit_button.is_clicked(event):
            pygame.quit()

    def draw_page(self,surface):
        # drawing menu page screen/labels/buttons
        super().draw_page(surface)
        self.menu_title.draw(surface)
        self.menu_play_button.draw(surface)
        self.menu_leaderboard_button.draw(surface)
        self.menu_rules_button.draw(surface)
        self.menu_settings_button.draw(surface)
        self.exit_button.draw(surface)

#==========#
# GAMELOOP #
#==========#

runtime = True
current_page = TitlePage()
current_email = " "
current_password = " "
current_code_sent = " "
current_error_message = None

while runtime:
   for event in pygame.event.get():
       current_page.handle_event(event)

   current_page.draw_page(screen)
   if current_error_message:
       current_error_message.draw(screen)
   pygame.display.flip()

