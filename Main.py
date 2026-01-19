from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.uix.stacklayout import StackLayout
from kivy.properties import BooleanProperty, StringProperty, NumericProperty
import random

class Manager(ScreenManager):
    pass

class HomePage(Screen):
    pass

class Profile(Screen):
    pass

class Help(Screen):
    pass

class Setting(Screen):
    pass

class Stats(Screen):
    pass

# basic games main class
class Basic_Games(Screen):
    def difficult(self,_diff,_screen):
        games_class=self.manager.get_screen(_screen)
        games_class.difficulty=_diff

# games inside basic games
class Basic_Math_Game_1(Screen):
    difficulty=StringProperty("Easy")
    points=NumericProperty(0)
    prod_1,div_1,sum_1,sub_1= 1, 10, 1, 1
    prod_2,div_2,sum_2,sub_2= 10, 100, 100, 100
    # for increasing points for every correct answer
    inc_point=NumericProperty(0)
    # accuracy
    total_ques=0

    # this function will run as soon as screen opens
    def on_enter(self, *args):
        if self.difficulty=="Hard":
            pass
        elif self.difficulty=="Medium":
            pass
        else:
            self.prod_1,self.div_1,self.sum_1,self.sub_1= 1, 10, 1, 1
            self.prod_2,self.div_2,self.sum_2,self.sub_2= 10, 100, 100, 100
            self.inc_point=1  # for easy just 1 point
        self.rand_ques(self.prod_1,self.div_1,self.sum_1,self.sub_1,self.prod_2,self.div_2,self.sum_2,self.sub_2)
    
    ques_text=StringProperty("0")
    question=NumericProperty(1)
    # function to choose a random question
    def rand_ques(self,prod_1,div_1,sum_1,sub_1,prod_2,div_2,sum_2,sub_2):
        operator=random.choice(["X", "÷", "+", "-"])
        if operator=="X":
            operand_1, operand_2 = random.randint( prod_1, prod_2), random.randint( prod_1, prod_2)
            self.ques_text= f"{operand_1} {operator} {operand_2}"
            self.question= operand_1*operand_2
        elif operator=="÷":
            operand_1, operand_2 = random.randint( div_1, div_2), random.randint(div_1//10, div_2//10)
            self.ques_text= f"{operand_1} {operator} {operand_2}"
            self.question= operand_1/operand_2
        elif operator=="+":
            operand_1, operand_2 = random.randint( sum_1, sum_2), random.randint(sum_1, sum_2//2)
            self.ques_text= f"{operand_1} {operator} {operand_2}"
            self.question= operand_1+operand_2
        elif operator=="-":
            operand_1, operand_2 = random.randint( sub_1, sub_2), random.randint(sub_1, sub_2//2)
            self.ques_text= f"{operand_1} {operator} {operand_2}"
            self.question= operand_1-operand_2
    
    ans_text=StringProperty("") 
    # input reflector for numbers       customise for multiple "."s
    def keypad(self,_id):
        self.ans_text+=_id
    def uni_opera(self):
        if self.ans_text=="":
            pass
        elif "." in self.ans_text:
            self.ans_text=str(-float(self.ans_text))
        else:
            self.ans_text=str(-int(self.ans_text))
    def delete(self):
        self.ans_text=self.ans_text[:-1]
    
    def enter(self):
        if self.question==float(self.ans_text):
            print("correct")
            self.ques_text="correct"
            self.points+=self.inc_point
        else:
            self.ques_text="wrong"
        self.total_ques+=1
        self.ans_text=""
        self.rand_ques(self.prod_1,self.div_1,self.sum_1,self.sub_1,self.prod_2,self.div_2,self.sum_2,self.sub_2)



class Lessons(Screen):
    pass





class GyanSetuApp(App):
    pass

GyanSetuApp().run()