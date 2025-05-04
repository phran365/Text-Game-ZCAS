# 'A simple example game using the text adventure engine.'
from idlelib.configdialog import changes
from random import randint
from time import sleep
import time
import sys
from tkinter.messagebox import QUESTION

from engine.activity import Activity
from engine.game import Game
from engine.inventory_item import InventoryItem
from engine.place import Place
from engine.event import Event
from engine.transition import Transition

class Simple(Game):
    def __init__(self):
        super(Simple, self).__init__('Happiness')
        self.did_rest = False
        self.solved_math = False
        self.watched_tv = False
        self.ate_meal = False
        self.successful_exit = False
        self.introduction = 'Welcome Home'
        self.character = input('ENTER YOUR NAME-->')
        home = Place ('Home', 'Welcome home '+self.character+ ' unwind and relax')
        welcome_event = Event(1, 'Music is playing in the background, it relaxes you.',10)
        home.add_events(welcome_event)

        #Room 2 BEDROOM
        bedroom = Place('Bedroom','Room to sleep in.')
        bedroom.add_activities(Activity('Rest', self.relax))
        rest_event = Event(2, 'You have rested', 10)
        bedroom.add_events(rest_event)
        bedroom.add_activities(Activity("Pick up item", self.relax))
        remote = InventoryItem('TV Remote', 7)
        bedroom.add_items(remote)

        # Room LIVING_ROOM
        living_room = Place('Living Room',
                            'The Living is where you can enjoy yourself and relax \n\nTo watch TV, item Required:\nTV Remote *Look for it*')
        living_room.add_activities(
            Activity('Watch TV', self.watch_tv, remote)
        )
        pen = InventoryItem('Pen', 1)
        notepad = InventoryItem('Notepad', 1)
        calculator = InventoryItem('Calculator', 0.9)
        living_room.add_items(calculator, pen, notepad)

        #FRIDGE
        fridge = Place('Fridge')
        fruit_juice = InventoryItem('Fruiticana' ,1)
        mineral_water = InventoryItem('Vatra')
        fruit = InventoryItem('Apple')
        fridge.add_transitions(home)
        fridge.add_items(fruit_juice,mineral_water,fruit)

        #OVEN
        oven = Place('Oven')
        pancakes = InventoryItem('Pancakes',1)
        oven.add_items(pancakes)
        oven_event = Event(1,'You eat some pancake.', 25, max_occurrences=10)
        oven.add_events(oven_event)

        # KITCHEN
        kitchen = Place('Kitchen', 'A happy place for you to enjoy a meal, \nItem Required:\nFridge Key *Look for it*')

        #STUDY ROOM
        study_room = Place('Study Room','Place for you to study and research \nTo solve a math question item Required:\nCalculator *Look For it*')
        study_room.add_activities(Activity('Solve a Match Problem',self.solve_math_problem, calculator))
        study_room.add_events = Event(2,'You have done a math exercise',10,0.5)

        #DINING ROOM
        dining = Place('Dining','A very comfortable for you to have a meal, drink, smoke and chat')
        dining.add_activities(Activity('Enjoy meal',self.food_choice,pancakes,mineral_water,fruit_juice))
        key_to_the_fridge = InventoryItem('Key To The Fridge',10)
        car_key = InventoryItem('Car key')
        dining.add_items(key_to_the_fridge,car_key)


        #EXIT
        leave_home = Place('Leave the house and go to the mall','\nTo leave the house item required:\nCar Key *Look For it*')
        leave_home.add_activities(Activity('Leave home and get some fresh air',self.exit_game,car_key))

        #TRANSITIONS
        sleep(3)
        home.add_transitions(living_room,bedroom,kitchen, study_room,dining,leave_home)
        living_room.add_transitions(home, Transition(dining))
        bedroom.add_transitions(home)
        kitchen.add_transitions(oven, Transition(fridge,key_to_the_fridge),Transition(home))
        oven.add_transitions(home)
        study_room.add_transitions(home)
        dining.add_transitions(living_room, Transition(home))
        leave_home.add_transitions(home)

        # STARTING PLACE
        self.location = home

#ACTIVITY FUNCTIONS

# SOLVING A MATH QUESTION
    def solve_math_problem(self) -> int:
        self.solved_math =True
        m1 = randint(2, 5)
        m2 = randint(11, 19)
        product = m1 * m2
        answer = int(input(f'Please solve this problem: {m1} * {m2} = ? '))
        change = 10
        while True:
            try:
                answer = int(input(f'Please solve this problem: {m1}*{m2} = ? '))
                if answer == product:
                    print ("Correct! Well done.")
                    break
                else:
                    print("Incorrect. Try again.")
            except ValueError:
                print ("Please enter a valid number")

# CHOOSING WHAT TO WATCH
    def watch_tv(self) -> str:
        self.watched_tv = True
        while True:
            print("\nChoose what you want to do:")
            print("1. Watch Football")
            print("2. Watch Movies")
            print("3. Play Video Games")

            act_1 = input("Enter your choice (1-4): ")

            if act_1 == "1":
                print("You chose Football! Time to hit the field.\nWATCHING TV.....")
                loading_dots()
            elif act_1 == "2":
                print("You chose Movies! Grab some popcorn.")
            elif act_1 == "3":
                print("You chose Video Game! Let’s play.")
            elif act_1 == "4":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 4.")

# CHOOSING THE HOURS TO REST
    def relax(self) -> int:
        self.did_rest = True
        while True:
            try:
                num = int(input("How many hours do you want to rest for\nChoose 2-6 hours?\n"))
                if num in range(2, 6):
                    # time.sleep(3)
                    print("You have rested for:",num,"hours")
                    break
                else:
                    print('Hours out of range of the sleeping time. \nEnter number of hours between 2 and 6')
            except ValueError:
                print("Invalid Input. Please enter a valid number")

# CHOOSING FOOD ITEMS
    def food_choice(self) -> str:
        while True:
            print("\nChoose what you want to eat:")
            print("1. Pancakes")
            print("2. Fruiticana")
            print("3. Apples")
            print("4. Vatra")
            print("5. Exit")

            act_1 = int(string("Enter your choice (1-5): "))
            self.ate_meal = True
            if act_1 == "1":
                print("You chose Pancakes! Fluffy and warm.")
            elif act_1 == "2":
                print("You chose Fruiticana! A tropical treat.")
            elif act_1 == "3":
                print("You chose Apples! Crunchy and fresh.")
            elif act_1 == "4":
                print("You chose Vatra! Enjoy the traditional flavor.")
            elif act_1 == "5":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 5.")


# EXITING THE GAME AND SHOWING GAME STATS
    def exit_game(self="Do you want to leave the house and get some fresh air?"):
        self.successful_exit = True
        print(self)
        print("\n--- GAME SUMMARY ---")
        print(f"Player: {self.character}")
        print(f"Rested: {'Yes' if self.did_rest else 'No'}")
        print(f"Solved Math Problem: {'Yes' if self.solved_math else 'No'}")
        print(f"Watched TV: {'Yes' if self.watched_tv else 'No'}")
        print(f"Ate or Drank Something: {'Yes' if self.ate_meal else 'No'}")
        print(f"Successfully Left the House: {'Yes' if self.successful_exit else 'No'}")
        print("Thanks for playing! \n\nSee you next time.")
        print("\nInventory Collected:")
        if self.inventory:
            for item in self.inventory:
                print(f"- {item.name}")
        else:
            print("No items collected.")
        sys.exit()

if __name__ == '__main__':
    game = Simple()
    game.play()