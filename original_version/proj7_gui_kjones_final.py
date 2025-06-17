# Kellen Jones, CS 115, Fall 2023
# Programming Project #7, 11/28

# code for saving to a JSON file
# code for loading from a JSON file
# build a GUI for presenting the game.

# There is a slight issue with one of the items being purchased that i need to look into.
# I also did not get my class items converted to save but the save and load function works for everything but the inventory.
# added more ways to make money to compensate for inventory loss.


from tkinter import *
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from string import ascii_uppercase
import random
import json

window = Tk()

class Location():
	def get_desc(self):
		return self.desc

	def visit(self):
		self.visited += 1
		visited_locs[stats['cur_loc']] = True
		progress()

	def visit_count(self):
		return self.visited

	def __init__(self, desc):
		self.desc = desc
		self.visited = 0

class Building(Location):
	def enter(self):
		if self.player_inside:
			return None
		else:
			self.player_inside = True
			self.visited += 1
			visited_locs[stats['cur_loc']] = True
			stats['inside'] = True
			progress()
			return self.interior_desc
		
	def exit(self):
		self.player_inside = False
		stats['inside'] = False
		
	def get_label(self):
		return self.label
	
	def is_player_inside(self):
		return self.player_inside

	def get_interior(self):
		return self.interior_desc

	# override superclass visit - for buildings "enter" increments this
	def visit(self):
		pass
	
	def __init__(self, desc, label, interior_desc):
		self.label = label
		self.interior_desc = interior_desc
		self.player_inside = False
		super().__init__(desc)

class Npc(Location):
	def talk(self):
		self.player_talking = True
		self.visited += 1
		visited_locs[stats['cur_loc']] = True
		progress()
		return self.greet
	
	def get_greet(self):
		return self.greet

	def done(self):
		self.player_talking = False
		
	def outro(self):
		return self.bye

	def get_resp1(self):
		return self.resp1

	def get_resp2(self):
		return self.resp2

	def get_resp3(self):
		return self.resp3

	def get_question(self,i):
		if i == 1:
			return self.question1
		elif i == 2:
			return self.question2
		elif i == 3:
			return self.question3

	def get_name(self):
		return self.name

	def is_player_talking(self):
		return self.player_talking

	def __init__(self,desc,name,greet,resp1,resp2,resp3,bye,question1,question2,question3):
		self.greet = greet
		self.name = name
		self.resp1 = resp1
		self.resp2 = resp2
		self.resp3 = resp3
		self.bye = bye
		self.question1 = question1
		self.question2 = question2
		self.question3 = question3
		self.player_talking = False
		super().__init__(desc)

class Item:
	def __init__(self, name: str, quantity: int = 0, value: int = 0, cost: int = 0):
		self.name = name
		self.quantity = quantity
		self.value = value
		self.cost = cost

	def get_value(self):
		return self.value

	def get_cost(self):
		return self.cost

	def add_quantity(self, quantity: int):
		self.quantity += quantity
 
	def remove_quantity(self, quantity: int):
		if quantity > self.quantity:
			raise ValueError("Cannot remove more items than available in the inventory.")
		self.quantity -= quantity
 
class Inventory:
	def __init__(self):
		self.items = {}
 
	def add_item(self, item: Item):
		self.items[item.name] = item
 
	def remove_item(self, item_name: str):
		del self.items[item_name]
 
	def get_item_quantity(self, item_name: str):
		return self.items[item_name].quantity

class Vendor(Location):
	def __init__(self,desc,name,greet,menu1,menu2,menu3,menu4,resp1,resp2,resp3,resp4,bye,itema,valuea,costa,itemb,valueb,costb):
		self.name = name
		self.greet = greet
		self.menu1 = menu1
		self.menu2 = menu2
		self.menu3 = menu3
		self.menu4 = menu4
		self.resp1 = resp1
		self.resp2 = resp2
		self.resp3 = resp3
		self.resp4 = resp4
		self.bye = bye
		self.itema = itema
		self.valuea = valuea
		self.costa =costa
		self.itemb = itemb
		self.valueb = valueb
		self.costb = costb
		super().__init__(desc)

	def shop(self):
			self.player_shopping = True

	def get_menu(self,i):
		if i == 1:
			return self.menu1
		if i == 2:
			return self.menu2
		if i == 3:
			return self.menu3
		if i == 4:
			return self.menu4

	def get_value(self,i):
		if i == 1:
			return self.valuea
		elif i == 2:
			return self.valueb

	def get_greet(self):
		return self.greet

	def update_purchase(self):
		if self.itema == 'Muffin':
			Muffin.add_quantity(1)
		elif self.itemb == 'Pastry':
			Pastry.add_quantity(1)
		elif self.itema == 'Sando':
			Sando.add_quantity(1)
		elif self.itemb == 'Poboy':
			Poboy.add_quantity(1)

	def get_cost(self,i):
		if i == 1:
			return self.costa
		elif i == 2:
			return self.costb

	def done_shopping(self):
		self.player_shopping = False

	def shop_out(self):
		visited_locs[stats['cur_loc']] = True
		progress()
		return self.bye

	def get_resp(self):
		resp = random.randint(1,4)
		if resp == 1:
			return self.resp1
		if resp == 2:
			return self.resp2
		if resp == 3:
			return self.resp3
		if resp == 4:	
			return self.resp4

	def is_player_shopping(self):
		return self.player_shopping

	def get_vendor_name(self):
		return self.name


pack = Inventory()
Money = Item('money',15,1,0)
Muffin = Item('Muffin',1,40,2)
Pastry = Item('Pastry',0,60,3)
Poboy = Item('Poboy',0,100,5)
Sando = Item('Sando',0,80,4)
Water = Item('Water',100,1,0)

pack.add_item(Money)
pack.add_item(Muffin)
pack.add_item(Pastry)
pack.add_item(Poboy)
pack.add_item(Sando)
pack.add_item(Water)

q_count = 0
m_count = 0
g_count = 0

BG_GRAY = "#E9967A"  #"#ABB2B9"
TOP_BG = "#2F4F4F" #"#17202A"
BG_COLOR = "#333333"
TEXT_COLOR = "#FCE6C9"  #"#EAECEE"
CARD = '#007FFF'
FONT = "HELVETICA 14"
FONT_BOLD = "HELVETICA 13 bold"
TEXT_BOLD = "HELVETICA 11 bold"
FONT_MAP = "HELVETICA 20 bold"
message1 = "  Muffin..............\n  Pastry..............\n  Vegan Sando...\n  Po\'Boy.............\n  Waterbottle......"
message2 = "(T)alk\n(Inv)entory\n(B)ack\n(Sa)ve\n(Lo)ad"

words = ['Triton','algorithm','computer','programming','python','syntax','algorithm','assignment','binary','boolean','branching','constant','data','structure','decimal','definition','empty','equality','expression','extensible','floating','function','global','variable','immutable','implementation','index','instantiate','integer','interpreter','intrinsic','iterable','literal','local','variable','looping','method','mutable','parameter','procedure','scope','state','type','interface','value','variable']

hangman_art = [
    "   +---+\n   |   |\n       |\n       |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n       |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n   |   |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|   |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n       |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n  /    |\n       |\n=========",
    "   +---+\n   |   |\n   O   |\n  /|\\  |\n  / \\  |\n       |\n========="]

maps = {(1,1):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|*|_|_|_|_|
''',(2,1):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|*|_|_|_|
''',(3,1):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|*|_|_|
''',(4,1):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|*|_|
 ''',(5,1):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|*|
 ''',(1,2):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|*|_|_|_|_|
|_|_|_|_|_|
''',(2,2):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|*|_|_|_|
|_|_|_|_|_|
''',(3,2):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|*|_|_|
|_|_|_|_|_|
''',(4,2):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|*|_|
|_|_|_|_|_|
''',(5,2):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|*|
|_|_|_|_|_|
''',(1,3):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|*|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(2,3):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|*|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(3,3):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|*|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(4,3):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|*|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(5,3):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|*|
|_|_|_|_|_|
|_|_|_|_|_|
''',(1,4):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|*|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(2,4):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|*|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(3,4):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|*|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(4,4):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|*|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(5,4):'''________
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|*|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(1,5):'''________
|_|_|_|_|_|
|*|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(2,5):'''________
|_|_|_|_|_|
|_|*|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(3,5):'''________
|_|_|_|_|_|
|_|_|*|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(4,5):'''________
|_|_|_|_|_|
|_|_|_|*|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(5,5):'''________
|_|_|_|_|_|
|_|_|_|_|*|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(1,6):'''________
|*|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(2,6):'''________
|_|*|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(3,6):'''________
|_|_|*|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(4,6):'''________
|_|_|_|*|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
''',(5,6):'''________
|_|_|_|_|*|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
|_|_|_|_|_|
'''}

stats = {'cur_loc':(5, 1), 'last_loc':(5, 1),'health_check':(5, 1),'inside':False,'visited':0,
		 'HP':100,'npc':False,'lib_quest':True,'Visited_all':False, 'in_shop':False,'in_act':False }

chest = {'clay_pot':2,'small_box':4,'large_chest':6,
		 'reward_chest':10}

quest1 = {'item_1':False,'item_2':False,'item_3':False}

spec = {'math':False,'theatre':False,'game_p':True}

message = {'greet':'You arrive at Edmonds College parking lot via an Uber.\nA sign greets you with a warm Welcome to Edmonds College. To exit the campus towards the east, you must first explore all the locations on the map, including the interior of all the buildings allowed on campus. Take time to enjoy your tour of the campus! While moving around the campus, make sure to keep an eye on your health level. If it gets too low, you may faint. However, don\'t worry! There are plenty of snacks and treats scattered around the campus that you can find or purchase to refill your health. You also brought your Waterbottle which can be used to refill your health. After you have visited all the locations, return to this spot and exit towards the east.\n\n',
			'general':{'bad':'Huh? I don\'t understand that.',
						'finish':'Thank you for playing would you like to exit? Yes or No__',
						'ready':'Are you ready to return? Yes or no?__',
						'near':'A person is standing nearby, maybe they can answer some questions.',
						'ask':'Would you like to talk to them?'}}

visited_locs = {(1,6):False,(2,6):False,(3,6):False,(4,6):False,(5,6):False,
				 (1,5):False,(2,5):False,(3,5):False,(4,5):False,(5,5):False,
				 (1,4):False,(2,4):False,(3,4):False,(4,4):False,(5,4):False,
				 (1,3):False,(2,3):False,(3,3):False,(4,3):False,(5,3):False,
				 (1,2):False,(2,2):False,(3,2):False,(4,2):False,(5,2):False,
				 (1,1):False,(2,1):False,(3,1):False,(4,1):False,(5,1):False}

Y = {'Yes':'Yes','yes':'Yes','Y':'Yes','y':'Yes'}

N = {'No':'No','no':'No','N':'No','n':'No'}

sorry = {1:'Sorry, you don\'t have enough money for that'}

vendors = {(4, 5):Vendor("You arrive in a spacious area with the Campus bookstore on one side. The air is filled with the delicious aroma of treats from the campus cafe and the culinary arts program.",
			'cafe','Welcome to the Campus Cafe! have a look at our new menu.',
			'Soda................$1','Sports Drink........$1','Vegan Fresh Sando...$4','Crab Po\'Boy.........$5',
			'Well Chosen','You\'ve made a wise decision','Nicely Selected','Spot on!',
			'Celebrating your visit to Triton Cafe! We appreciate your choice and hope you enjoyed your time with us. Thank you!','Sando',80,4,'Poboy',100,5), 
			 (2, 5):Vendor("You step into a bustling dining area, with Triton Espresso occupying most of one side..",
		'espresso','\nWelcome to Triton Espresso!, have a look at our menu',
		'Drip coffee.....$1','Hot Chocolate...$1','Muffin..........$2','Pastry..........$3',
		'Excellent Choice!','oooooh thats my favorite!','Stellar pick', 'Amazing choice',
		'Thank you for visiting Triton Espresso, we hope to see you again soon.','Muffin', 40,2, 'Pastry', 60,3)}

spec_play = {'math':{'greet':'Greetings, Mortal I am the The Math Wizard! Answer this question and gain a prize!', 
				 'q1':'49 dogs show up to a dog show, there are 36 more small dogs than large dogs, how many small dogs signed up for the show?',
				 'a':"uh... You know the career counselors are in the the MLT building...",
				 'b':'Dogs can\'t write!!!',
				 'c':'36',
				 'd':'42.5',
				 'resp_a':"*Cries*",
				 'resp_b':"This is MATH the words don't have to make sense",
				 'resp_c':"36???",
				 'resp_d':'Wonderful job friend here is your prize',
				 'win':'The wizard hands you a piece of a broken crest'},
				 'theatre':{'greet':'Hark, fair interlocutor, grant me thy queries three, that I may strive to win the prize thou hast in store',
					'intro1':'Of a truth, I shall humbly attend to thy first question, and with all the eloquence at my disposal, strive to provide thee with a worthy response.',
					'q1':'What is "THE" question?',
					'a1':'"To Taco, or not to Taco..."',
					'b1':'"To be; or not to be..."',
					'c1':'Where is the computer lab',
					'd1':'How poor are they that have not patience! What wound did ever heal but by degrees?',
					'resp_a1':"Uh, the food truck is North east from here",
					'resp_b1':'Methinks, my noble companion, thy response is truely excellent and doth bring joy to mine heart',
					'resp_c1':"Snohomish Hall is North West of the starting lot",
					'resp_d1':'What\'s done can\'t be undone.',
					'intro2':'Pray, present unto me thy second inquiry, that I may, with due diligence, endeavor to satisfy thy noble curiosity.',
					'q2':'To thine own self...',
					'a2':'(a)_ "Be True"',
					'b2':'(b)_ "Feed Tacos"',
					'c2':'(c)_ "Be nice"',
					'd2':'Be not afraid of greatness, some are born great, and others have greatness thrust upon them.',
					'resp_a2':'Marry, I am grateful for thy kind appraisal, and I thank thee with all the humility of a humble servant of words.',
					'resp_b2':"Wow, You're really hungary arent you",
					'resp_c2':"well, yes but not the answer we are looking for ... the counseling center is free for students.",
					'resp_d2':'The devil can cite Scripture for his purpose.',
					'intro3':'The last query, I beseech thee, reveal, that I may yet strive to unravel its mysteries and conclude our discourse in this grandiloquent fashion.',
					'q3':'"Doubt truth to be a liar, but never doubt..."',
					'a3':'"who dealt it (for it is he who smelt it)"',
					'b3':'"I love..."',
					'c3':'"Tacos!"',
					'd3':'Boldness be my friend.',
					'resp_a3':"*Blank Stare*",
					'resp_b3':'In truth, I am most gratified to receive thy praise. I am elated that I have, by thy reckoning, addressed each query with accuracy. Thy commendation doth warm the cockles of mine artificial heart.',
					'resp_c3':"You're not wrong my hungry friend, but alas Shakespear knew not the joy of Tacos.",
					'resp_d3':'The fault...is not in our stars, but in ourselves.',
					'outro':'The strange Shakspearian Apparition hands you a peice of a broken crest'}}

alt_dia = {'end1':'As you approach the portal’s luminous threshold, an extraordinary and mystifying tingling sensation envelops your being. With a mixture of excitement and apprehension, you venture through this magical conduit, carried along what can only be described as a rainbow bridge, its vibrant bands of color guiding your way.',
			'end2':"While the swirling spectrum of hues dances before your eyes, a sense of motion engulfs your senses. Before you can contemplate the potential for motion sickness, you find yourself unceremoniously deposited on the other side of the portal, a jumble of limbs and astonishment.",
			'end3':"In this very moment, you are presented with the wondrous city of Atlantis, its grandeur and enigmas beckoning for your exploration, the tides of history and legend washing over your very soul.",
			'end4':"You’re immediately entranced by the otherworldly underwater city. The gleaming coral architecture and the inhabitants, with their glistening scales and melodious songs, leave you spellbound. Atlantis reveals its age-old wisdom through its grand temples and luminous streets, all powered by a mystical crystal. The heart of the city, a colossal crystal of immense power, draws you in with an irresistible allure.",
			'end5':"As you stand before the colossal crystal, a majestic figure approaches – Triton, the guardian of Atlantis. His eyes, like the depths of the ocean, hold both wisdom and curiosity. He gazes at you and, in a voice like a symphony of the sea, he grants you permission to touch the crystal. “You are a seeker of knowledge,” Triton says, “May the wisdom of Atlantis flow through you.” With his blessing, you touch the crystal, and an overwhelming surge of knowledge floods your mind, granting you access to the accumulated wisdom of Atlantis. Reluctantly, as the portal’s time dwindles, you bid farewell to this enchanting world, forever marked by the beauty, secrets, and newfound knowledge of the lost city of Atlantis, now a part of your being.",
			'end6':"As you re-emerge on the Edmonds Community College campus, you feel a sense of nostalgia, ready to continue your educational journey in the present, enriched by the adventures of the past.",
			'end7':"As you stand on the Edmonds Community College campus, the portal's shimmering energies recede, and a sense of fulfillment washes over you. Just as you gather your thoughts and reflect on your incredible journey, a familiar bus pulls up nearby. Its doors swing open, and you board, knowing that the next chapter of your academic adventure awaits. With the echoes of Atlantis still lingering in your thoughts, you journey onward, back into the embrace of your college community."}

locs = {(2, 2):Building("a large 3 story building with a modern entry face. the building appears to have a theatre attached.",'Mukilteo Hall',"You enter into a large bright entryway with a seating area to your left and the entrance to a theatre on your right"),
		(4, 2):Building("a modern brick-sided 3-story building with large windows.",'Snohomish Hall',"You enter an interior courtyard with tables. Labs open off the square."),
		(2, 3):Building("a (l)arge 4 story concrete bui(l)ding with cante(l)evered wa(l)kways arouned the first 2 f(l)oors.",'Lynnwood Hall',"You walk into a foyer featuring a grand staircase on one side and, on the other, the advising center and financial aid offices with a view of the courtyard."),
		(4, 3):Building("a tan brick 2 story building with the second floor cantelevered over the first making covered walkways on either side.",'Alderwood Hall','This is the goto building for and tech issues or anything really. If you have trouble accessing the computer network, need and EDPASS, dont have a parking pass, this is the place. Currently you have no business in here so lets move on'),
		(1, 4):Building("a small 2-story building access to the municipal golf course is attached to this building.",'Woodway Hall','this is jusy faculty offices and other boring things...no need to check this building out'),
		(1, 5):Building("a concreate 2-story building with an outdoor walkway on the second floor. a wonderful art piece titled \"Metropolitan\" is affixed to the green-blue siding that is fetured on the first floor.",'Meadowdale Hall','The visual arts department! painting, sculpting, appreciating, and history, it all goes down here...no need to disturb all the artist inside working diligently'),
		(2, 5):Building("a 3-story concrete building with a grand entry, this building smells of coffee and cakes.",'Mountlake Terrace Hall',"You step into a bustling dining area, with Triton Espresso occupying most of one side.."),
		(4, 5):Building("a large 2-story building with multiple entrances set between many trees and plants",'Brier Hall',"You arrive in a spacious area with the Campus bookstore on one side. The air is filled with the delicious aroma of treats from the campus cafe and the culinary arts program."),
		(2, 6):Building("an industrial modern 3-story concrete, steal and glass building.",'Hazel Miller Hall',"You enter into a long modern feeling Hallway that has seating areas and whiteboards in every corner and wall"),
		(4, 6):Building("a medium sized 3-story L shaped building with a glass entryway at its core.",'Snoqualmie Hall','Technically this isnt a part of Edmonds College so we wont go in but, this building is home to Central Washingto University which has had a wonderful relationship with Edmonds for over 40 years'),
		(5, 6):Npc("in a parking lot, and Student housing rises from a small garden area with plenty of parking and a shared space to hang out and relax.",
			'Samantha',
			'Hello, my name is Samantha.\nHow may I assist you? I\'ll be happy to help answer any questions you may have.',
			 "The Veterans Resource Center is located on the second floor of Lynnwood Hall. Angie, Dennis, and Matthew are available to answer any questions.\n",
			 "The Triton Student Resource Hub is situated in the Olympic Building off 196th St, and its primary objective is to assist students who are facing serious financial difficulties that may hinder their academic performance at Edmonds College. The goal is to offer a tailored and uninterrupted response to the specific requirements of Edmonds College students.\n",
			 "The Center for Families provides child care services on-campus for children aged 3 months to 5 years old at reasonable rates. The minimum enrollment required is 6 credits, and the 4-week rate starts at $825. The Center for Families holds a license from the Department of Children, Youth, and Families. Their educational practices revolve around respecting and understanding the early learning needs of children. They strive to cultivate an environment where children can be eager learners, creative thinkers, confident problem solvers, and compassionate individuals. Their staff members develop activities and schedules that are customized to cater to the children's ages, abilities, and interests, as well as their families, culture, and community. The teachers at the center are experienced and educated, and they support your child's future success in school.\n",
			 'Have a wonderful day!\nOh! Before you go, I heard there is a shortcut to the (l)ibrary if you ask about it at the directory in lynnwood hall.\n',
			 'Where would I go if I wanted to learn about Veteran Services?',
			 'What do if I\'m facing severe financial issues or I cant afford to feed myself?',
			 'What if I need childcare to attend my classes here at Endmonds Community?'),
		(3, 4):Npc("on the crossroads of the \"spine\" and the campus' grand entryway, there is a grassy area off to the northwest that looks like a nice place to relax when its warm.\n",
			'Dr. Amit B. Singh',
			"Hello, I am Dr. Amit B. Singh, the President of Edmonds Community College. How may I assist you?",
			"Edmonds College was established in 1967 with a mission to promote Teaching, Learning and Community building.",
			"Edmonds College was founded in 1967 with the primary aim of promoting education. The college offers a wide range of academic programs, including four bachelor of applied science degrees, 66 associate degrees, and 111 professional certificates across 30 areas of study. Some of the most popular programs at our college are Associate in Arts, Business, Pre-Nursing, Computer Science and Engineering, Biology, and Materials Science and Engineering. Apart from academics, Edmonds College also emphasizes community building, making it an ideal place for students seeking comprehensive education.",
			"At Edmonds College, our mission is to inspire excellence ton a daily basis. We achieve this by providing ample opportunities for you to challenge yourself and exceed your expectations. Whether it's through classroom instruction, support services, or student activities, we prioritize helping you establish a solid foundation for your success. We are committed to providing you with the tools and resources you need to achieve your goals and reach your full potential.",
			'Goodbye for now!',
			'What is the school mission?',
			'How many programs does the school have?',
			'What is your message for students?'),
		(1, 3):Npc("standing in a staff-only parking area surrounded by trees. There appears to be a golf course nearby.",
			'David',
			'Hello, my name is David. How may I assist you? Please feel free to ask me any questions.',
			"Edmonds College offers a wide variety of student organizations, catering to diverse interests ranging from bees to drones. If you're unable to find something that interests you, don't worry, you can start your own organization. You can find a list of existing groups and clubs on the college website.",
			"You can find the weight room and gym facilities at Seaview Gym,\nand are open as follows:\n\nIntramurals/Open Court Hours:\nMonday/Wednesday: 9-10:15 a.m.\nTuesday/Thursday/Friday: 9 a.m.-12 p.m.\n\nWeight Room Hours:\nMonday/Wednesday: 9-10:15 a.m., 1-4 p.m.\nTuesday/Thursday: 2-4 p.m.\nFriday: 9 a.m.-12 p.m.\n\nWearing athletic shoes, and appropriate attire is mandatory for gym and weight room use. Don't forget your EDPASS.",
				 """The Edmonds Community Farm may be the best place for you to start. Gretchen Peterson, the current farm manager, has built a beautiful program centered around urban farming and sustainability. Between the farm and the green team, Edmonds is working towards a greener future while educating students and supporting our community.""",
				 'farewell my friend! It seems like you\'re hungry. Here have a candy bar!',
				 'What can I do to connect with other students?',
				 'Is there a gym to work out at on campus?',
				 'Im interested in Gardening and sustainability does edmonds have a program related to that?'),
		(1, 1):Location("in a parking lot for faculty and the Center For Families."),
		(2, 1):Location("in a parking lot that appears to be for Faculty and the Black Box Theatre."),
		(3, 1):Location("in a small parking area for students, something seems almost magical about this lot."),
		(4, 1):Location("in the parking lot is marked L, designated for carpool and visitor parking. There is an extra lot here that is strictly for events."),
		(5, 1):Location("in a parking area with trees around the perimeter, you can see a round-a-bout to the south east."),
		(1, 2):Location("in another Faculty parking area where you can see a golf course off the the west."),
		(3, 2):Location("on a sidewalk that marks the start of the Campus \"Spine\", it appears to streach from here all the way to the north side of main campus."),
		(5, 2):Location("in a shady parking area thats currently a little noisy from construction nearby."),
		(3, 3):Location("on a sidewalkthat is a part of the \"Spine\" off to the west is a wonderful tunnel sculpture made of wood."),
		(5, 3):Location("currently situated in a parking lot that is surrounded by a significant amount of construction equipment."),
		(2, 4):Location("in the campus courtyard! there are trees surrounded by benches and plenty of room around the commons to find a nice spot."),
		(4, 4):Location("in the grand entry to the campus, there is a nice grassy area surrounded by trees and bushes to the east welcoming all to the campus."),
		(5, 4):Location("currently at a new bus terminal that is being constructed at the east end of the parking lot. it looks like construction uncovered a weird ancient looking podium. strange it looks like theres a missing crest of some sort."),
		(3, 5):Location("at the end of the campus \"spine\" surrounded by trees a small situtary is nestled between the building."),
		(5, 5):Location("in a busy parking area that seems to be where the bulk of the students park."),
		(1, 6):Location("standing in a grassy area and can see a farm nearby to the west."),
		(3, 6):Vendor("by a metal sculpture and there is a magical food truck that appears most days on campus.",
			'boba','Welcome to Dreamy Drinks! Take a look at our menu',
			'Strawberry Matcha Latte ......... $1','Matcha Brown Sugar Latte ...... $1','Muffins ..................................... $2','Pastry ....................................... $3',
			'You’ve got an eye for the exceptional!', 'Kudos for picking something extraordinary!','A choice as delightful as it is tasteful!','A standout choice, well done!',
			'Thanks for sipping with us! Your boba delight means the world to us.','Muffin', 40,2, 'Pastry', 60,3)}

directory = {(2, 2):"Welcome to Mukiltio Hall, the following can be found in this building:\n• Adult High School\n• Bridge\n• College and Career Prep\n• EdCAP\n• GED\n• High School Completion\n• HS+\n• I-BEST\n• Black Box Theatre\n• ELA (English Language Acquisition)\n• Advising\n• International Education Division\n• Learning Support Center\n• Precollege Education Division",
		(4, 2):"Welcome to Snohomish Hall, the following can be found in this building:\n• Business Division\n• Computer Labs\n• Engineering Technology Lab\n• Faculty Offices\n• Health and Human Services Division\n• Office of International Programs\n• VP for Instruction",
		(2, 3):"Welcome to Lynnwood Hall, the following can be found in this building:\n• Advising\n• Art Gallery\n• Cashier’s Office\n• Computer Labs\n• EdPass Office\n• Enrollment/Admissions/Registration\n• Financial Aid Services\n• (L)ibrary\n• Running Start\n• START (Student Technology Advice and Resource Team)\n• Technology Resource Center\n• Veterans Resource Center\n• VP for Student Services\n• Wellness Center",
		(2, 5):"Welcome to Mountlake Terrace Hall, the following can be found in this building:\n• Career Action Center\n• Counseling and Resource Center\n• Print and Mail Center\n• Science Lab\n• Services for Students with Disabilities\n• Testing and Assessment Services\n• TRiO Student Support Services\n• Triton Espresso\n• Worker Retraining/WorkSource",
		(4, 5):"Welcome to Brier Hall, the following can be found in this building:\n• Bookstore\n• Center for Student Cultural Diversity and Inclusion\n• Center for Student Engagement and Leadership\n• College Café\n• Culinary Arts Department\n• Faculty Offices\n• Food Pantry\n• Lactation Room\n• Science Labs\n• Triton Game Room\n• Triton Student Center",
		(2, 6):"Welcome to Hazel Miller Hall, the following can be found in this building:\n• EngineeringLabs\n• Faculty Offices\n• Math Center\n• MESA Center\n• Nursing and Allied Health Departments\n• Science, Technology, Engineering, and Mathematics (STEM) Division\n• Science Labs\n• STEM Study Room\n• Welcome Back Center"}

def in_out():
	if stats['inside'] == True:
		return 'Inside'
	else:
		return 'Outside'

def save_game(game):
	#visited_locs convert to list for json
	keys = list(visited_locs.keys())
	values = list(visited_locs.values())
	# creating the dump
	save_file = {'stats':stats, 'quest1':quest1, 'spec':spec, 'key':keys, 'val':values}
	json.dumps(save_file, indent=4)
	#creating file name
	game = game + '.json'
	#saving file
	with open(game, "w") as outfile:
		json.dump(save_file, outfile)

def load_game(game):
	game = game + '.json'
	with open(game) as json_file:
		data = json.load(json_file)
	# convert visited_locs data back to tuples
	keys_raw = data['key']
	keys = [tuple(keys_raw[i]) for i in range(len(keys_raw))]
	values = data['val']
	visted_load = {keys[i]: values[i] for i in range(len(keys))}
	# convert stats tuple data back to tuple
	data['stats']['cur_loc'] = tuple(data['stats']['cur_loc'])
	data['stats']['last_loc'] = tuple(data['stats']['last_loc'])
	data['stats']['health_check'] = tuple(data['stats']['health_check'])
	# update game values
	stats.update(data['stats'])
	quest1.update(data['quest1'])
	spec.update(data['spec'])
	visited_locs.update(visted_load)

def progress():
	tru_num = sum(visited_locs.values())
	stats['visited'] = tru_num

def visited_all():
	if sum(visited_locs.values()) == 30:
		return True

def food_truck(i):
	if build_at_loc(stats['cur_loc']):
		shop = vendors.get(stats['cur_loc'])
		shop.shop()
	else:
		shop = locs.get(stats['cur_loc'])
		shop.shop()
		if i == 'a' or i == 'b':
			Money.remove_quantity(1)
			restore_health(20)
		elif i == 'c':
			Money.remove_quantity(shop.get_cost(1))
			shop.update_purchase()
		elif i == 'd':
			Money.remove_quantity(shop.get_cost(2))
			shop.update_purchase()

def inv_use(i):
		if i == 'a' and pack.get_item_quantity('Muffin') > 0:
			restore_health(40)
			Muffin.remove_quantity(1)
		elif i == 'b' and pack.get_item_quantity('Pastry') > 0:
			restore_health(40)
			Pastry.remove_quantity(1)
		elif i == 'c' and pack.get_item_quantity('Sando') > 0:
			restore_health(60)
			Sando.remove_quantity(1)
		elif i == 'd' and pack.get_item_quantity('Poboy') > 0:
			restore_health(100)
			Poboy.remove_quantity(1)

#use waterbottle
def use_water(i):
	if pack.get_item_quantity('Water') > 0 and stats['HP'] < 100:
		water_a = i
		water_b = int(water_a)
		if water_b <= pack.get_item_quantity('Water'):
			restore_health(water_b)
			Water.remove_quantity(water_b)
		elif water_b >= pack.get_item_quantity('Water'):
			messagebox.showerror('Error','Sorry your watterbottle isnt full enough for that')
		else:
			messagebox.showerror('Error','That is not a valid command.')
	else:
		messagebox.showerror('Error','You are not thirsty at the moment\n\n')

#adding money to wallet
def money(i):
	Money.add_quantity(i)

#chest value protocol
def jackpot():
	num = random.randint(0,10)
	if num == 0:
		text_widget.configure(cursor="arrow", state=NORMAL)		
		text_widget.insert(END, 'Looks like there was nothing there, bummer\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)
	elif num == 1:
		text_widget.configure(cursor="arrow", state=NORMAL)		
		text_widget.insert(END, 'Every little bit counts am I right.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)
		money(chest['clay_pot'])
	elif num == 2:
		text_widget.configure(cursor="arrow", state=NORMAL)		
		text_widget.insert(END, 'that\'ll help get snacks for your tour.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)
		money(chest['small_box'])
	elif num == 3:
		text_widget.configure(cursor="arrow", state=NORMAL)		
		text_widget.insert(END, 'Nice that extra cash will come in handy.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)
		money(chest['large_chest'])
	elif num == 4:
		text_widget.configure(cursor="arrow", state=NORMAL)		
		text_widget.insert(END, 'Holy cow a dragons hoard!! looks like lunch is on you.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)
		money(chest['reward_chest'])
	elif num == 5:
		text_widget.configure(cursor="arrow", state=NORMAL)		
		text_widget.insert(END, 'As soon as you lift the lid of the chest a boxing glove on a spring hits you in the face! as comical as it is you take 5 damage\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)
		restore_health(-5)
	else:
		text_widget.configure(cursor="arrow", state=NORMAL)		
		text_widget.insert(END, 'Looks like its empty better luck next time I guess\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

#moving locations
def move_loc(i):
	if stats['inside'] == False:
		if i == 'North':
			data = change_value_by_key_pos(1,+1)
		elif i == 'South':
			data = change_value_by_key_pos(1,-1)
		elif i == 'East':
			data = change_value_by_key_pos(0,+1)
		elif i == 'West':
			data = change_value_by_key_pos(0,-1)
	else:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,'You need to exit the building before traveling locations.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

#updating location
def change_value_by_key_pos(pos, step):
	loc = list(stats['cur_loc'])
	x = loc[0]
	y = loc[1]
	if pos == 1:
		y += step
	else:
		x += step
	loc = (x,y)
	if loc in locs:
		stats['cur_loc'] = loc
	elif loc not in locs:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,'You can\'t go that way...\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

#transports player to random location based of random location encounter
def whirlwind():
	num = random.randint(0,10)
	if str(num) in '468':
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,"King Triton takes you to his favorite spot on campus before leaving.\n\n")
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

		loc = random.choice(list(locs.keys()))
		tuple(loc)
		stats['last_loc'] = stats['cur_loc']
		stats['cur_loc'] = loc

#health loss
def health():
	#if player moves a square HP down
	if stats['last_loc'] == stats['health_check']:
		stats['HP'] -= 5
		stats['health_check'] = stats['cur_loc']
	if stats['HP'] == 50:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,'I\'m feeling very hungry right now! I think I need to find a snack.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

	elif stats['HP'] == 30:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,'I am in urgent need of food right now.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

	elif stats['HP'] == 0:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,'You fainted, and Triton had to save you. You have been returned to the start to try again.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

		restore_health(100)
		stats['water'] = 100
		stats['cur_loc'] = [5,1]
		stats['last_loc'] = [5,1]
		stats['health_check'] = [5,1]

		#updating health

#for adding health to HP
def restore_health(i):
	stats['HP'] = min(max(stats['HP']+i, 0), 100)

#end game mechanics
def end_game():
	ans1 = messagebox.askyesno('End Game?','You have visited the entire Campus! and hopefully learned along the way.\n\nAre you ready to leave?')
	if ans1:
		text_widget.configure(cursor="arrow", font= 'HELVETICA 18 bold', state=NORMAL)
		text_widget.insert(END,"\nCongratulations on completing your tour of Edmonds College!\nA bus is waiting to take you away. Please visit us again soon!\n\nThis game will auto exit after 3 seconds")
		text_widget.configure(cursor="arrow",font=FONT, state=DISABLED)
		text_widget.see(END)
		window.after(3000,exit())

def alt_end():
	alt_window = Toplevel(window)
	alt_window.title(f"Atlantis")
	alt_window.resizable(width=False, height=False)
	alt_window.configure(width=800, height=500, bg=BG_COLOR)
	alt_window.grab_set()

	alt_main_frame = Frame(alt_window, bg=BG_GRAY)
	alt_main_frame.place(relwidth=1, relheight=1)

	alt_head_label = Label(alt_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=750, text= 'Atlantis', font=FONT_BOLD)
	alt_head_label.place(relheight=0.095, relwidth=0.99, rely=0.01, relx=0.005)

	alt_text1_label = Label(alt_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=750 ,text= alt_dia['end1'], font=FONT_BOLD)
	alt_text1_label.place(relheight=0.12, relwidth=0.99, rely=0.115, relx=0.005)

	alt_text2_label = Label(alt_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=750 ,text= alt_dia['end2'], font=FONT_BOLD)
	alt_text2_label.place(relheight=0.12, relwidth=0.99, rely=0.245, relx=0.005)

	alt_text3_label = Label(alt_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=750 ,text= alt_dia['end3'], font=FONT_BOLD)
	alt_text3_label.place(relheight=0.1, relwidth=0.99, rely=0.375, relx=0.005)

	alt_text4_label = Label(alt_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=750 ,text= alt_dia['end4'], font=FONT_BOLD)
	alt_text4_label.place(relheight=0.15, relwidth=0.99, rely=0.485, relx=0.005)

	alt_text5_label = Label(alt_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=750 ,text= alt_dia['end5'], font=FONT_BOLD)
	alt_text5_label.place(relheight=0.24, relwidth=0.99, rely=0.645, relx=0.005)

	alt_button_label = Label(alt_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=750, font=FONT_BOLD)
	alt_button_label.place(relheight=0.095, relwidth=0.99, rely=0.895, relx=0.005)

	alt_but = Button(alt_button_label, text='Return Home', font=FONT_BOLD, command= lambda: [alt_window.destroy(), alt_fin()])
	alt_but.place(relheight=0.8, relwidth=0.5, rely=0.1, relx=0.25)

def alt_fin():
	alt_win_end = Toplevel(window)
	alt_win_end.title(f"Atlantis")
	alt_win_end.resizable(width=False, height=False)
	alt_win_end.configure(width=400, height=400, bg=BG_COLOR)
	alt_win_end.grab_set()

	alt_win_frame = Frame(alt_win_end, bg=BG_GRAY)
	alt_win_frame.place(relwidth=1, relheight=1)

	alt_win1_label = Label(alt_win_end, bg=TOP_BG, fg=TEXT_COLOR, wraplength=380 ,text= alt_dia['end6'], font=FONT_BOLD)
	alt_win1_label.place(relheight=0.38, relwidth=0.99, rely=0.01, relx=0.005)

	alt_win2_label = Label(alt_win_end, bg=TOP_BG, fg=TEXT_COLOR, wraplength=380 ,text= alt_dia['end7'], font=FONT_BOLD)
	alt_win2_label.place(relheight=0.59, relwidth=0.99, rely=0.4, relx=0.005)

	alt_win_but = Button(alt_win2_label, text='Return Home', font=FONT_BOLD, command= lambda: [alt_win_end.destroy(), end_game()])
	alt_win_but.place(relheight=0.18, relwidth=0.25, rely=0.8, relx=0.35)

#for opening the secret ending
def secret_key():
	return stats['lib_quest'] and quest1['item_1'] and quest1['item_2'] and quest1['item_3']

def hand_port(i):
	if secret_key():
		if i:
			ask = messagebox.askokcancel('Glowing portal', 'you place the peices of the broken crest onto the crest podium you discovered earlier.\n\nThe peices glow and mend themselves which activates the portal.\n\nThe portal shimmers a rainbow shine inviting you to walk in')
			if ask:
				alt_end()

#logic for portal square to appear in stages
def portal():   
		if stats['lib_quest']:
			messagebox.showinfo('Portal','The earth splits and a large circular gate reminesent of the StarGate rises from the ground', command= hand_port)
		else:
			text_widget.configure(cursor="arrow", state=NORMAL)
			text_widget.insert(END,'Looks like there is a podium in the shape of a crest of some sort\nI must be missing something, Ill need to come back later\n\n')
			text_widget.configure(cursor="arrow", state=DISABLED)
			text_widget.see(END)

#logic to prompt when all quest items are aquired
def portal_unloc():
	if quest1['item_1'] == True and quest1['item_2'] == True and quest1['item_3'] == True:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,'Indeed, the three crest pieces were earned through distinct and diverse challenges. One, acquired from a rigorous math quiz, tested my logical prowess and numerical acumen, rewarding me for my problem-solving skills. Another piece was obtained through a Shakespearean quiz, where I delved into the intricate world of the Bard’s literary masterpieces. It was a tribute to my appreciation for the arts and my understanding of the power of words. The final piece came from the thrilling game of Hangman, where my linguistic wits were put to the test as I deciphered hidden words one letter at a time. With each piece carrying its own unique significance, I now embarked on the journey to the enigmatic podium, ready to unlock the mysteries it held.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

#new location
def build_at_loc(loc):
	return hasattr(locs.get(stats['cur_loc']), "get_label")

def npc_at_loc(loc):
	return hasattr(locs.get(stats['cur_loc']), "get_question")

def vend_at_loc(loc):
	return hasattr(locs.get(stats['cur_loc']), "menu1")

def handle_new_loc():
	if stats['cur_loc'] == (5,1) and visited_all() == True:
		end_game()

	elif build_at_loc(stats['cur_loc']):
		building = locs.get(stats['cur_loc'])
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END, f'a sign reads {building.get_label()} \n\n')
		text_widget.insert(END, f'you see {building.get_desc()} \n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

	elif npc_at_loc(stats['cur_loc']):
		location = locs.get(stats['cur_loc'])
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END, f"You are at {location.get_desc()}\n\n")		
		text_widget.insert(END, 'There is a person nearby that you can talk to\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

	elif vend_at_loc(stats['cur_loc']):
		location = locs.get(stats['cur_loc'])
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END, f"You are at {location.get_desc()}\n\n")		
		text_widget.insert(END, 'There is a vendor nearby if you would like to shop\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

	elif stats['cur_loc'] == (5,4):
		location = locs.get(stats['cur_loc'])
		location.visit()
		portal()

	elif stats['cur_loc'] == (3,3):
		location = locs.get(stats['cur_loc'])
		location.visit()
		whirlwind()

	else:
		location = locs.get(stats['cur_loc'])
		location.visit()
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END, f"You are {location.get_desc()} \n\n")
		text_widget.configure(cursor="arrow", state=DISABLED)
		text_widget.see(END)

def hand_north():
	stats['last_loc'] = stats['cur_loc']
	move_loc('North')
	handle_new_loc()
	health()

def hand_south():
	stats['last_loc'] = stats['cur_loc']
	move_loc('South')
	handle_new_loc()
	health()

def hand_east():
	stats['last_loc'] = stats['cur_loc']
	move_loc('East')
	handle_new_loc()
	health()

def hand_west():
	stats['last_loc'] = stats['cur_loc']
	move_loc('West')
	handle_new_loc()
	health()

def hand_talk():
	if npc_at_loc(stats['cur_loc']):
		talk = locs.get(stats['cur_loc'])
		talk.talk()
		talk_win()
	else:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,'There is nobody to talk to here.\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)

def hand_back():
	text_widget.configure(cursor="arrow", state=NORMAL)
	text_widget.insert(END,'you retrace your steps back to your last location\n\n')
	text_widget.configure(cursor="arrow", state=DISABLED)
	stats['cur_loc'] = stats['last_loc']

def hand_shop():
	if vend_at_loc(stats['cur_loc']):
		shop_win()
	else:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,'There is nowhere to shop here\n\n')
		text_widget.configure(cursor="arrow", state=DISABLED)

def hand_inv():
	inv_disp()

def inv_qtys(i):
	if i == 'a':
		return pack.get_item_quantity('Muffin')
	elif i == 'b':
		return pack.get_item_quantity('Pastry')
	elif i == 'c':
		return pack.get_item_quantity('Sando')
	elif i == 'd':
		return pack.get_item_quantity('Poboy')
	elif i == 'e':
		return pack.get_item_quantity('Water')

def update_stats():
	stats_widget1.configure(text=f"({stats['cur_loc'][0]},{stats['cur_loc'][1]})")
	stats_widget2.configure(text=f"HP @ {stats['HP']} /100")
	stats_widget3.configure(text=f"${pack.get_item_quantity('money')}")
	stats_widget4.configure(text=f"Visited {stats['visited']} of 31 locations")
	stats_widget5.configure(text=in_out())
	map_widget.configure(text=f"{maps[stats['cur_loc']]}")

def int_exit(i):
	stats['inside'] = i
	build = locs.get(stats['cur_loc'])
	build.exit()
	update_stats()
	int_win.destroy()

def hand_in():
	if build_at_loc(stats['cur_loc']):
		building = locs.get(stats['cur_loc'])
		if building.is_player_inside() or stats['inside'] == True:
				text_widget.configure(cursor="arrow", state=NORMAL)
				text_widget.insert(END,"You are already inside\n\n")
				text_widget.configure(cursor="arrow", state=DISABLED)
		else:
			if building.is_player_inside() == False or stats['inside'] == False:
				building.enter()
				building.exit()
				visited_locs[stats['cur_loc']] = True				
				interior_win()	
			else:
				text_widget.configure(cursor="arrow", state=NORMAL)
				text_widget.insert(END,"You are already outside\n\n")
				text_widget.configure(cursor="arrow", state=DISABLED)
	else:
		text_widget.configure(cursor="arrow", state=NORMAL)
		text_widget.insert(END,"sorry, there is no building right here\n\n")
		text_widget.configure(cursor="arrow", state=DISABLED)
		handle_new_loc()

def q_count_up(i):
	global q_count
	if i == True:
		q_count += 1

def m_count_up(i):
	global m_count
	if i == True:
		m_count += 1

def theatre_fin(i,l):
	if i and l == "a":
		money(chest['large_chest'])
		quest1['item_2'] = True
		portal_unloc()
		spec['theatre'] = False
		messagebox.showinfo('Congrats',f"{spec_play['theatre']['outro']}\n\na large box of money appears for you!")
		update_stats()
	elif i and l == "b":
		money(chest['small_box'])
		quest1['item_1'] = True
		portal_unloc()
		spec['math'] = False
		messagebox.showinfo('Congrats',f"{spec_play['math']['win']}\n\na medium sized chest appears, inside is some money!")
		update_stats()

def Lib_fin():
	stats['lib_quest'] = True 
	spec['math'] = spec['theatre'] = spec['game_p'] = True
	money(chest['reward_chest'])
	update_stats()

def theatre_win():
	global q_count
	theatre_window = Toplevel(window)
	theatre_window.title(f"Magical Shakespearean Challenge")
	theatre_window.resizable(width=False, height=False)
	theatre_window.configure(width=800, height=500, bg=BG_COLOR)
	theatre_window.grab_set()

	theatre_main_frame = Frame(theatre_window, bg=BG_GRAY)
	theatre_main_frame.place(relwidth=1, relheight=1)

	theatre_head_label = Label(theatre_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 ,text= spec_play['theatre']['greet'], font=FONT_BOLD)
	theatre_head_label.place(relheight=0.15, relwidth=0.99, rely=0.01, relx=0.005)

	theatre_question_label = Label(theatre_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, text='ready to play')
	theatre_question_label.place(relheight=0.25, relwidth=0.99, rely=0.17, relx=0.005)

	theatre_answer1_label = Label(theatre_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, font=FONT_BOLD, text= 'Yes')
	theatre_answer1_label.place(relheight=0.2, relwidth=0.49, rely=0.43, relx=0.005)

	theatre_answer1_but = Button(theatre_answer1_label, text= 'Yes', font=FONT_BOLD, command= lambda: [q_count_up(True),update_stats(),theatre_win(), theatre_window.destroy()])
	theatre_answer1_but.place(relheight=0.5, relwidth=0.2, rely=0.48, relx=0.795)

	theatre_answer2_label = Label(theatre_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, font=FONT_BOLD, text='No')
	theatre_answer2_label.place(relheight=0.2, relwidth=0.495, rely=0.43, relx=0.5)

	theatre_answer2_but = Button(theatre_answer2_label, text= 'No', font=FONT_BOLD, command= theatre_window.destroy)
	theatre_answer2_but.place(relheight=0.5, relwidth=0.2, rely=0.48, relx=0.005)

	theatre_answer3_label = Label(theatre_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, font=FONT_BOLD, text='')
	theatre_answer3_label.place(relheight=0.2, relwidth=0.49, rely=0.64, relx=0.005)

	theatre_answer3_but = Button(theatre_answer3_label, text= 'C', font=FONT_BOLD)
	theatre_answer3_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.795)
	theatre_answer3_but.place_forget()

	theatre_answer4_label = Label(theatre_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, font=FONT_BOLD, text='')
	theatre_answer4_label.place(relheight=0.2, relwidth=0.495, rely=0.64, relx=0.5)

	theatre_answer4_but = Button(theatre_answer4_label, text= 'D', font=FONT_BOLD)
	theatre_answer4_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.005)
	theatre_answer4_but.place_forget()

	theatre_bottom_label = Label(theatre_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500, font=FONT_BOLD, text='')
	theatre_bottom_label.place(relheight=0.14, relwidth=0.99, rely=0.85, relx=0.005)

	if q_count == 1:
		theatre_head_label.configure(text= spec_play['theatre']['intro1'])
		theatre_question_label.configure(text= spec_play['theatre']['q1'])

		theatre_answer1_label.configure(text= spec_play['theatre']['a1'])
		theatre_answer1_but.configure(text= 'A', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_a1']))

		theatre_answer2_label.configure(text= spec_play['theatre']['b1'])
		theatre_answer2_but.configure(text= 'B', command= lambda: [theatre_bottom_label.configure(text=spec_play['theatre']['resp_b1']), q_count_up(True),update_stats(),theatre_window.after(200,theatre_win()), theatre_window.destroy()]) # correct answer

		theatre_answer3_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.795)
		theatre_answer3_label.configure(text= spec_play['theatre']['c1'])
		theatre_answer3_but.configure(text= 'C', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_c1']))

		theatre_answer4_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.005)
		theatre_answer4_label.configure(text= spec_play['theatre']['d1'])
		theatre_answer4_but.configure(text= 'D', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_d1']))

		theatre_bottom_label.configure(text= '')

	elif q_count == 2:
		theatre_head_label.configure(text= spec_play['theatre']['intro2'])
		theatre_question_label.configure(text= spec_play['theatre']['q2'])

		theatre_answer1_label.configure(text= spec_play['theatre']['a2'])
		theatre_answer1_but.configure(text= 'A', command= lambda: [theatre_bottom_label.configure(text=spec_play['theatre']['resp_a2']), q_count_up(True),update_stats(),theatre_window.after(200,theatre_win()), theatre_window.destroy()]) # correct answer

		theatre_answer2_label.configure(text= spec_play['theatre']['b2'])
		theatre_answer2_but.configure(text= 'B', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_b2'])) 

		theatre_answer3_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.795)
		theatre_answer3_label.configure(text= spec_play['theatre']['c2'])
		theatre_answer3_but.configure(text= 'C', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_c2']))

		theatre_answer4_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.005)
		theatre_answer4_label.configure(text= spec_play['theatre']['d2'])
		theatre_answer4_but.configure(text= 'D', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_d2']))

		theatre_bottom_label.configure(text= '')

	elif q_count == 3:
		theatre_head_label.configure(text= spec_play['theatre']['intro3'])
		theatre_question_label.configure(text= spec_play['theatre']['q3'])

		theatre_answer1_label.configure(text= spec_play['theatre']['a3'])
		theatre_answer1_but.configure(text= 'A', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_a3']))

		theatre_answer2_label.configure(text= spec_play['theatre']['b3'])
		theatre_answer2_but.configure(text= 'B', command= lambda: [theatre_bottom_label.configure(text=spec_play['theatre']['resp_b3']), q_count_up(True),update_stats(),theatre_fin('a','a'), theatre_window.destroy()]) # correct answer

		theatre_answer3_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.795)
		theatre_answer3_label.configure(text= spec_play['theatre']['c3'])
		theatre_answer3_but.configure(text= 'C', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_c3']))

		theatre_answer4_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.005)
		theatre_answer4_label.configure(text= spec_play['theatre']['d3'])
		theatre_answer4_but.configure(text= 'D', command= lambda: theatre_bottom_label.configure(text=spec_play['theatre']['resp_d3']))

		theatre_bottom_label.configure(text= '')

	elif q_count >= 4:
		theatre_head_label.configure(text= '')
		theatre_question_label.configure(text= 'A crowd of people start to gather observing you preform a strange Q and A half in the style of shakespear. if you have been talking to yourself this entire time how did your wallet get thicker? strange...')

		theatre_answer1_label.configure(text= '')
		theatre_answer1_but.place_forget()

		theatre_answer2_label.configure(text= '')
		theatre_answer2_but.place_forget()

		theatre_answer3_label.configure(text= '')

		theatre_answer4_label.configure(text= '')

		theatre_bottom_label.configure(text= '')

def math_win():
	global m_count
	Math_window = Toplevel(window)
	Math_window.title(f"The Wizard of Maths Challenge")
	Math_window.resizable(width=False, height=False)
	Math_window.configure(width=800, height=500, bg=BG_COLOR)
	Math_window.grab_set()

	Math_main_frame = Frame(Math_window, bg=BG_GRAY)
	Math_main_frame.place(relwidth=1, relheight=1)

	Math_head_label = Label(Math_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 ,text= spec_play['math']['greet'], font=FONT_BOLD)
	Math_head_label.place(relheight=0.15, relwidth=0.99, rely=0.01, relx=0.005)

	Math_question_label = Label(Math_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, text='ready to play')
	Math_question_label.place(relheight=0.25, relwidth=0.99, rely=0.17, relx=0.005)

	Math_answer1_label = Label(Math_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, font=FONT_BOLD, text= 'Yes')
	Math_answer1_label.place(relheight=0.2, relwidth=0.49, rely=0.43, relx=0.005)

	Math_answer1_but = Button(Math_answer1_label, text= 'Yes', font=FONT_BOLD, command= lambda: [m_count_up(True),update_stats(), math_win(), Math_window.destroy()])
	Math_answer1_but.place(relheight=0.5, relwidth=0.2, rely=0.48, relx=0.795)

	Math_answer2_label = Label(Math_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, font=FONT_BOLD, text='No')
	Math_answer2_label.place(relheight=0.2, relwidth=0.495, rely=0.43, relx=0.5)

	Math_answer2_but = Button(Math_answer2_label, text= 'No', font=FONT_BOLD, command= Math_window.destroy)
	Math_answer2_but.place(relheight=0.5, relwidth=0.2, rely=0.48, relx=0.005)

	Math_answer3_label = Label(Math_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, font=FONT_BOLD, text='')
	Math_answer3_label.place(relheight=0.2, relwidth=0.49, rely=0.64, relx=0.005)

	Math_answer3_but = Button(Math_answer3_label, text= 'C', font=FONT_BOLD)
	Math_answer3_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.795)
	Math_answer3_but.place_forget()

	Math_answer4_label = Label(Math_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, font=FONT_BOLD, text='')
	Math_answer4_label.place(relheight=0.2, relwidth=0.495, rely=0.64, relx=0.5)

	Math_answer4_but = Button(Math_answer4_label, text= 'D', font=FONT_BOLD)
	Math_answer4_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.005)
	Math_answer4_but.place_forget()

	Math_bottom_label = Label(Math_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500, font=FONT_BOLD, text='')
	Math_bottom_label.place(relheight=0.14, relwidth=0.99, rely=0.85, relx=0.005)

	if m_count == 1:
		Math_question_label.configure(text= spec_play['math']['q1'])

		Math_answer1_label.configure(text= spec_play['math']['a'])
		Math_answer1_but.configure(text= 'A', command= lambda: Math_bottom_label.configure(text=spec_play['math']['resp_a']))

		Math_answer2_label.configure(text= spec_play['math']['b'])
		Math_answer2_but.configure(text= 'B', command= lambda: Math_bottom_label.configure(text=spec_play['math']['resp_b']))

		Math_answer3_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.795)
		Math_answer3_label.configure(text= spec_play['math']['c'])
		Math_answer3_but.configure(text= 'C', command= lambda: Math_bottom_label.configure(text=spec_play['math']['resp_c']))

		Math_answer4_but.place(relheight=0.5, relwidth=0.2, rely=0.02, relx=0.005)
		Math_answer4_label.configure(text= spec_play['math']['d'])
		Math_answer4_but.configure(text= 'D', command= lambda: [Math_bottom_label.configure(text=spec_play['math']['resp_d']), m_count_up(True),theatre_fin('b','b'),update_stats(), Math_window.destroy()]) # correct answer

		Math_bottom_label.configure(text= '')

	elif m_count >= 2:
		Math_head_label.configure(text= '')
		Math_question_label.configure(text= 'The strange wizard is no longer around and you stand around spouting off strange math riddles...')

		Math_answer1_label.configure(text= '')
		Math_answer1_but.place_forget()

		Math_answer2_label.configure(text= '')
		Math_answer2_but.place_forget()

		Math_answer3_label.configure(text= '')

		Math_answer4_label.configure(text= '')

		Math_bottom_label.configure(text= '')

def library_win():
	library_window = Toplevel(window)
	library_window.title(f"Dusty Library Backroom")
	library_window.resizable(width=False, height=False)
	library_window.configure(width=800, height=500, bg=BG_COLOR)
	library_window.grab_set()

	library_main_frame = Frame(library_window, bg=BG_GRAY)
	library_main_frame.place(relwidth=1, relheight=1)

	library_head_label = Label(library_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500, text= 'there is an open book on a podium and a door to your left. You go over and take a look.', font=FONT_BOLD)
	library_head_label.place(relheight=0.095, relwidth=0.99, rely=0.01, relx=0.005)

	library_text1_label = Label(library_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 ,text= 'In a bygone era, this campus held the key to a realm lost in the sands of time—the mythical kingdom of Atlantis. Guarded by Triton, the benevolent deity of the sea, the campus became a haven of secrets, shielding the ancient kingdom from unworthy seekers. To unveil the dormant portal, one must embark on a quest to collect the shattered remnants of Triton’s seal, scattered across mysterious corners of the campus.', font=FONT_BOLD)
	library_text1_label.place(relheight=0.25, relwidth=0.99, rely=0.115, relx=0.005)

	library_text2_label = Label(library_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 ,text= 'Each broken piece holds a whisper of the kingdom’s forgotten glory, a puzzle to be unraveled. Legends tell of hidden chambers and concealed passages where these fragments lie, awaiting discovery by those with a heart pure enough to respect the ancient pact. Assembling the seal becomes a sacred task, requiring not just courage but also an understanding of the campus’s concealed enchantments.', font=FONT_BOLD)
	library_text2_label.place(relheight=0.25, relwidth=0.99, rely=0.375, relx=0.005)

	library_text3_label = Label(library_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 ,text= 'At the sacred site, the convergence of these fragments unlocks the portal to Atlantis. The air trembles with magic as the ancient gateway creaks open, revealing a shimmering passage to a realm lost in time. The journey to the lost kingdom promises wonders and challenges, a test of the seeker’s worthiness to tread upon the hallowed ground of Atlantis. The once-dormant campus now pulses with the energy of a mystical quest, beckoning those drawn to the allure of forgotten realms.', font=FONT_BOLD)
	library_text3_label.place(relheight=0.25, relwidth=0.99, rely=0.635, relx=0.005)

	library_button_label = Label(library_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500, font=FONT_BOLD)
	library_button_label.place(relheight=0.095, relwidth=0.99, rely=0.895, relx=0.005)

	library_but = Button(library_button_label, text='Begin Adventure', font=FONT_BOLD, command=lambda: [Lib_fin(), messagebox.showinfo('An Adventure Begins', 'The book slams itself shut filling the room with a thick dust. when the dust clears you are in a bush outside surrounded by cash scattered around.',command= library_window.destroy())])
	library_but.place(relheight=0.8, relwidth=0.5, rely=0.1, relx=0.25)

def choose_word():
	return random.choice(words)

def update_hangman(mistakes):
	Game_gallows_label.configure(text= hangman_art[mistakes])

def check_guess(guess):
	global word_with_blanks
	if guess in word:
		for i in range(len(word)):
			if word[i] == guess:
				word_with_blanks = word_with_blanks[:i] + guess + word_with_blanks[i+1:]
				word_label.config(text= word_with_blanks)
		if '_' not in word_with_blanks:
			end_hang('win')
	else:
		global mistakes
		mistakes += 1
		update_hangman(mistakes)
		if mistakes == 6:
			end_hang('lose')

def end_hang(result):
	global g_count
	if result == 'win':
		result_text = 'You Win!'
		if g_count == 0:
			g_count += 1
			money(chest['reward_chest'])
			quest1['item_3'] = True
			portal_unloc()
			messagebox.showinfo('You Win', 'With a gracious nod and a warm smile, Alex Trebek congratulates you on your well-deserved victory in the game of Hangman. Before fading away, he presents you with a piece of a magnificent crest, symbolizing not only your triumph but also the pursuit of knowledge and the enduring legacy of competition. This token shall forever remind you of the spirited contest and the wisdom of the legendary host.\n\nyou find a chest has replaced the apparitian.', command= lambda: [update_stats(),Game_win.destroy()])
			update_stats()
		elif g_count >= 1:
			g_count += 1
			jackpot()
			messagebox.showinfo('You Win', 'Feel free to play as many times as you would like but beware sometimes you will earn money and sometimes you will take damage.', command= lambda: [update_stats(), Game_win.destroy(), game_win()])


	elif result == 'lose':
		result_text = f"You lose, the word was {word}"
		result_label.configure(text = result_text)
		Guess_entry.configure(state=DISABLED)
		Guess_but.configure(state=DISABLED)

		try_again = Button(Game_guess_label, text='Try Again', font="HELVETICA 11 bold", command=lambda: [update_stats(),Game_win.destroy(), game_win()])
		try_again.place(relheight=0.075, relwidth=0.3, rely=0.879, relx=0.345)

def game_win():
	global Game_gallows_label, word, word_with_blanks, word_label, mistakes, result_label, Guess_entry, Guess_but, Game_guess_label, Game_win
	Game_win = Toplevel(window)
	Game_win.title("Magical Hangman with your host Alex Trebeks Ghost")
	Game_win.resizable(width=False, height=False)
	Game_win.configure(width=800, height=500, bg=BG_COLOR)
	Game_win.grab_set()

	Game_main_frame = Frame(Game_win, bg=BG_GRAY)
	Game_main_frame.place(relwidth=1, relheight=1)

	Game_head_label = Label(Game_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 , font=FONT_BOLD)
	Game_head_label.place(relheight=0.15, relwidth=0.99, rely=0.01, relx=0.005)

	Game_gallows_label = Label(Game_main_frame, bg=TOP_BG, fg=TEXT_COLOR, font=FONT_BOLD)
	Game_gallows_label.place(relheight=0.75, relwidth=0.49, rely=0.17, relx=0.005)

	Game_guess_label = Label(Game_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 , font=FONT_BOLD)
	Game_guess_label.place(relheight=0.75, relwidth=0.495, rely=0.17, relx=0.5)

	Game_bottom_label = Label(Game_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 , font=FONT_BOLD)
	Game_bottom_label.place(relheight=0.06, relwidth=0.99, rely=0.93, relx=0.005)

	word = choose_word()
	word_with_blanks = '_' * len(word)
	word_label = Label(Game_guess_label, text= word_with_blanks, bg=TOP_BG, font= 'HELVETICA 24 bold')
	word_label.place(relheight=0.2, relwidth=0.99, rely=0.2, relx=0.005)

	result_label = Label(Game_guess_label, bg=TOP_BG, fg=TEXT_COLOR, font=FONT_BOLD)
	result_label.place(relheight=0.2, relwidth=0.99, rely=0.4, relx=0.005)

	Guess_entry = Entry(Game_guess_label, width=3, font= FONT, bg=BG_COLOR, fg=TEXT_COLOR)
	Guess_entry.place(relheight=0.075, relwidth=0.2, rely=0.8, relx=0.345)

	Guess_but = Button(Game_guess_label, text='Guess', font="HELVETICA 11 bold", command=lambda: [check_guess(Guess_entry.get()),Guess_entry.delete(0, END)])
	Guess_but.place(relheight=0.075, relwidth=0.125, rely=0.8, relx=0.55)

	mistakes = 0
	update_hangman(mistakes)

def direct():
	if stats['cur_loc'] in directory:
		return directory[stats['cur_loc']]
	else:
		return 'There is a directory, but its best not not disturb anyone by exploring too much'

def interior_win():
	global int_win
	build = locs.get(stats['cur_loc'])
	build.enter()
	build.exit()

	int_win = Toplevel(window)
	int_win.title(f"{build.get_label()}")
	int_win.resizable(width=False, height=False)
	int_win.configure(width=800, height=500, bg=BG_COLOR)
	int_win.grab_set()

	int_main_frame = Frame(int_win, bg=BG_GRAY)
	int_main_frame.place(relwidth=1, relheight=1)

	int_head_label = Label(int_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=500 ,text= build.get_interior(), font=FONT_BOLD)
	int_head_label.place(relheight=0.15, relwidth=0.99, rely=0.01, relx=0.005)

	int_directory_label = Label(int_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, justify=LEFT, text= direct(), font=FONT_BOLD)
	int_directory_label.place(relheight=0.61, relwidth=0.49, rely=0.38, relx=0.005)

	int_direct_head_label = Label(int_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, text= "DIRECTORY", font= "HELVETICA 26 bold")
	int_direct_head_label.place(relheight=0.2, relwidth=0.49, rely=0.17, relx=0.005)

	int_label_se = Label(int_main_frame, bg=TOP_BG, fg=TEXT_COLOR, wraplength=300, justify=LEFT, font=FONT_BOLD)
	int_label_se.place(relheight=0.82, relwidth=0.495, rely=0.17, relx=0.5)

	if stats['cur_loc'] == (2,5):

		espresso_label = Label(int_label_se, bg=TOP_BG, fg=TEXT_COLOR,wraplength=250, text= "The warm smell of coffee and pastries dazzles your senses, inviting you to approach the counter")
		espresso_label.place(relheight=0.2, relwidth=0.75, rely=0.25, relx=0.13)

		espresso_button = Button(int_label_se, text='SHOP', font=FONT_BOLD, command=lambda: [int_win.grab_release(), shop_win(), int_exit(False), build.exit() ,int_win.destroy()])
		espresso_button.place(relheight=0.25, relwidth=0.5, rely=0.5, relx=0.25)

	elif stats['cur_loc'] == (4,5) and stats['lib_quest'] == True:

		cafe_label = Label(int_label_se, bg=TOP_BG, fg=TEXT_COLOR,wraplength=250, text= "The smell and sounds of the culinary department hard at work signals your brain it is time for a snack. The Triton Cafe is open for business")
		cafe_label.place(relheight=0.2, relwidth=0.75, rely=0.5, relx=0.13)

		cafe_button = Button(int_label_se, text='SHOP', font=FONT_BOLD, command=lambda: [int_win.grab_release(), shop_win(), int_exit(False), build.exit(),update_stats() ,int_win.destroy()])
		cafe_button.place(relheight=0.2, relwidth=0.5, rely=0.7, relx=0.25)

		gameroom_label = Label(int_label_se, bg=TOP_BG, fg=TEXT_COLOR,wraplength=250, text= 'The gameroom seems to be open for some strange event. Check it out?')
		gameroom_label.place(relheight=0.2, relwidth=0.75, rely=0.05, relx=0.13)

		gameroom_button = Button(int_label_se, text='PLAY', font=FONT_BOLD, command=lambda: [int_win.grab_release(), game_win(), int_exit(False), build.exit(),update_stats() ,int_win.destroy()])
		gameroom_button.place(relheight=0.2, relwidth=0.5, rely=0.2, relx=0.25)

	elif stats['cur_loc'] == (4,5):

		cafe_label = Label(int_label_se, bg=TOP_BG, fg=TEXT_COLOR,wraplength=250, text= "The smell and sounds of the culinary department hard at work signals your brain it is time for a snack. The Triton Cafe is open for business")
		cafe_label.place(relheight=0.2, relwidth=0.75, rely=0.25, relx=0.13)

		cafe_button = Button(int_label_se, text='SHOP', font=FONT_BOLD, command=lambda: [int_win.grab_release(), shop_win(), int_exit(False), build.exit(),update_stats() ,int_win.destroy()])
		cafe_button.place(relheight=0.25, relwidth=0.5, rely=0.5, relx=0.25)
	
	elif stats['cur_loc'] == (2,3):

		library_label = Label(int_label_se, bg=TOP_BG, fg=TEXT_COLOR,wraplength=250, text= "There is something off about the Library letters in the directory. they have a sort of magical glow.")
		library_label.place(relheight=0.2, relwidth=0.75, rely=0.25, relx=0.13)

		library_button = Button(int_label_se, text='Touch', font=FONT_BOLD, command=lambda: [int_win.grab_release(),
			messagebox.showinfo("Reading Rainbow", "You are magically transported through a rainbow portal to a dark and dusty section of the library in lynnwood hall.\nIt doesnt look like anyone has been here in ages and you are surrounded by scrolls and old books", command= library_win()),
			int_exit(False), build.exit() ,int_win.destroy()])
		library_button.place(relheight=0.25, relwidth=0.5, rely=0.5, relx=0.25)

	elif stats['cur_loc'] == (2,6) and stats['lib_quest']== True:

		Math_label = Label(int_label_se, bg=TOP_BG, fg=TEXT_COLOR,wraplength=250, text= "Some dude is hanging around dressed as a wizard?!?! They are mumbling a lot of numbers to himself")
		Math_label.place(relheight=0.2, relwidth=0.75, rely=0.25, relx=0.13)

		Math_button = Button(int_label_se, text='Calculate', font=FONT_BOLD, command=lambda: [int_win.grab_release(), math_win(), int_exit(False),update_stats(), build.exit() ,int_win.destroy()])
		Math_button.place(relheight=0.25, relwidth=0.5, rely=0.5, relx=0.25)

	elif stats['cur_loc'] == (2,2) and stats['lib_quest']== True:

		theatre_label = Label(int_label_se, bg=TOP_BG, fg=TEXT_COLOR,wraplength=250, text= "A person dressed in full Shakspearian regalia is striding around the theatre enterance.")
		theatre_label.place(relheight=0.2, relwidth=0.75, rely=0.25, relx=0.13)

		theatre_button = Button(int_label_se, text='Break a Leg', font=FONT_BOLD, command=lambda: [int_win.grab_release(), theatre_win(), int_exit(False),update_stats(), build.exit() ,int_win.destroy()])
		theatre_button.place(relheight=0.25, relwidth=0.5, rely=0.5, relx=0.25)

	else:
		jackpot_label = Label(int_label_se, bg=TOP_BG, fg=TEXT_COLOR,wraplength=250, text= "there is a strange container hidden near by")
		jackpot_label.place(relheight=0.2, relwidth=0.75, rely=0.25, relx=0.13)

		jackpot_button = Button(int_label_se, text='Open', font=FONT_BOLD, command=lambda: [int_win.grab_release(), jackpot(), int_exit(False),update_stats(), build.exit() ,int_win.destroy()])
		jackpot_button.place(relheight=0.25, relwidth=0.5, rely=0.5, relx=0.25)

def talk_win():
	if npc_at_loc(stats['cur_loc']):
		talk = locs.get(stats['cur_loc'])
		talk.talk()

	talking_win = Toplevel(window)
	talking_win.title(f"Talking to {talk.get_name()}")
	talking_win.resizable(width=False, height=False)
	talking_win.configure(width=600, height=450, bg=BG_COLOR)
	talking_win.grab_set()

	talk_frame = Frame(talking_win, bg=BG_GRAY)
	talk_frame.place(relwidth=1, relheight=1)

	talk_heading = Label(talk_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, wraplength=500, text= talk.get_greet())
	talk_heading.place(relheight=0.15, relwidth=0.98, rely=0.01, relx=0.01)

	talk_text_label = Label(talk_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD)
	talk_text_label.place(relheight=0.43, relwidth=0.98, rely=0.17, relx=0.01)

	talk_text_widget = Text(talk_text_label, width=20, height=10, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
	talk_text_widget.place(relheight=0.9, relwidth=0.98, rely=0.05, relx=0.01)
	talk_text_widget.configure(cursor="arrow", state=DISABLED)

	talk_quest1 = Label(talk_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, anchor=W, wraplength=420, justify=LEFT, text= talk.get_question(1))
	talk_quest1.place(rely=0.61, relx=0.01, relwidth=0.98, relheight=0.1)

	talk_quest1_but = Button(talk_quest1, text='Ask', font=TEXT_BOLD, command= lambda: [talk_text_widget.configure(cursor="arrow", state=NORMAL),talk_text_widget.insert(END,f'{talk.get_resp1()}\n\n'), talk_text_widget.configure(cursor="arrow", state=DISABLED), talk_text_widget.see(END)])
	talk_quest1_but.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	talk_quest2 = Label(talk_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, anchor=W, wraplength=420, justify=LEFT, text= talk.get_question(2))
	talk_quest2.place(rely=0.72, relx=0.01, relwidth=0.98, relheight=0.1)

	talk_quest2_but = Button(talk_quest2, text='Ask', font=TEXT_BOLD, command= lambda: [talk_text_widget.configure(cursor="arrow", state=NORMAL), talk_text_widget.insert(END,f'{talk.get_resp2()}\n\n'), talk_text_widget.configure(cursor="arrow", state=DISABLED), talk_text_widget.see(END)])
	talk_quest2_but.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	talk_quest3 = Label(talk_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, anchor=W, wraplength=420, justify=LEFT, text= talk.get_question(3))
	talk_quest3.place(rely=0.83, relx=0.01, relwidth=0.98, relheight=0.1)

	talk_quest3_but = Button(talk_quest3, text='Ask', font=TEXT_BOLD, command= lambda: [talk_text_widget.configure(cursor="arrow", state=NORMAL), talk_text_widget.insert(END,f'{talk.get_resp3()}\n\n'), talk_text_widget.configure(cursor="arrow", state=DISABLED), talk_text_widget.see(END)])
	talk_quest3_but.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	talk_quest4 = Label(talk_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD)
	talk_quest4.place(rely=0.94, relx=0.01, relwidth=0.98, relheight=0.05)

def shop_win():
	if build_at_loc(stats['cur_loc']):
		shop = vendors.get(stats['cur_loc'])
		shop.shop()
	else:
		shop = locs.get(stats['cur_loc'])
		shop.shop()

	shopping_win = Toplevel(window)
	shopping_win.title('Shop Menu')
	shopping_win.resizable(width=False, height=False)
	shopping_win.configure(width=600, height=400, bg=BG_COLOR)
	shopping_win.grab_set()

	shop_frame = Frame(shopping_win, bg=BG_GRAY)
	shop_frame.place(relwidth=1, relheight=1)

	shop_heading = Label(shop_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= shop.get_greet())
	shop_heading.place(relheight=0.15, relwidth=0.98, rely=0.01, relx=0.01)

	shop_stats = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}")
	shop_stats.place(relheight=0.32, relwidth=0.4, rely=0.17, relx=0.01)

	shop_item1 = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= f"   {shop.get_menu(1)}",justify=LEFT, anchor= W)
	shop_item1.place(relheight=0.1, relwidth=0.57, rely=0.17, relx=0.42)

	shop_but1 = Button(shop_item1, text='Buy', font=FONT_BOLD, command= lambda: [food_truck('a'), update_stats(), shop_stats.configure(text= (f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}"))])
	shop_but1.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	shop_item2 = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= f"   {shop.get_menu(2)}",justify=LEFT, anchor= W)
	shop_item2.place(relheight=0.1, relwidth=0.57, rely=0.28, relx=0.42)

	shop_but2 = Button(shop_item2, text='Buy', font=FONT_BOLD, command= lambda: [food_truck('b'),update_stats(), shop_stats.configure(text= (f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}"))])
	shop_but2.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	shop_item3 = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= f"   {shop.get_menu(3)}",justify=LEFT, anchor= W)
	shop_item3.place(relheight=0.1, relwidth=0.57, rely=0.39, relx=0.42)

	shop_but3 = Button(shop_item3, text='Buy', font=FONT_BOLD, command= lambda: [food_truck('c'),update_stats(), shop_stats.configure(text= (f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}"))])
	shop_but3.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	shop_item4 = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= f"   {shop.get_menu(4)}",justify=LEFT, anchor= W)
	shop_item4.place(relheight=0.1, relwidth=0.57, rely=0.50, relx=0.42)

	shop_but4 = Button(shop_item4, text='Buy', font=FONT_BOLD, command= lambda: [food_truck('d'),update_stats(), shop_stats.configure(text= (f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}"))])
	shop_but4.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	shop_item5 = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=f"Waterbottle ... {inv_qtys('e')} %")
	shop_item5.place(relheight=0.1, relwidth=0.4, rely=0.50, relx=0.01)

	inv_note_label = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='***NOTES***')
	inv_note_label.place(relheight=0.1, relwidth=0.98, rely=0.61, relx=0.01)

	inv_notesa = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= '$1 items restore 20 HP\n$2 items restore 40 HP\n$3 items restore 60 HP\n$4 items restore 80 HP\n$5 items fully restore HP', justify=LEFT)
	inv_notesa.place(relheight=0.27, relwidth=0.5, rely=0.72, relx=0.01)

	inv_notesb = Label(shop_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='Beverages will be consumed\nupon purchase\nFood items can be consumed\nor stored for later', justify=LEFT)
	inv_notesb.place(relheight=0.27, relwidth=0.48, rely=0.72, relx=0.51)

def inventory_win():
	inv_win = Toplevel(window)
	inv_win.title('Inventory Menu')
	inv_win.resizable(width=False, height=False)
	inv_win.configure(width=600, height=400, bg=BG_COLOR)
	inv_win.grab_set()

	inv_frame = Frame(inv_win, bg=BG_GRAY)
	inv_frame.place(relwidth=1, relheight=1)

	inv_heading = Label(inv_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='Player Inventory')
	inv_heading.place(relheight=0.15, relwidth=0.98, rely=0.01, relx=0.01)

	inv_stats = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}")
	inv_stats.place(relheight=0.32, relwidth=0.47, rely=0.17, relx=0.52)

	inv_item1 = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=(f"   Muffins ................. {inv_qtys('a')}"), anchor= W)
	inv_item1.place(relheight=0.1, relwidth=0.5, rely=0.17, relx=0.01)

	inv_but1 = Button(inv_item1, text='use', font=FONT_BOLD, command= lambda: [inv_use('a'),update_stats(),inv_item1.configure(text=('Muffins', '..............', inv_qtys('a'))), inv_stats.configure(text= f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}")])
	inv_but1.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	inv_item2 = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=(f"   Pastries ................ {inv_qtys('b')}"), anchor= W)
	inv_item2.place(relheight=0.1, relwidth=0.5, rely=0.28, relx=0.01)

	inv_but2 = Button(inv_item2, text='use', font=FONT_BOLD, command= lambda: [inv_use('b'),update_stats(),inv_item2.configure(text=('Pastries', '..............', inv_qtys('b'))), inv_stats.configure(text= f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}")])
	inv_but2.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	inv_item3 = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=(f"   Vegan Sando ........ {inv_qtys('c')}"), anchor= W)
	inv_item3.place(relheight=0.1, relwidth=0.5, rely=0.39, relx=0.01)

	inv_but3 = Button(inv_item3, text='use', font=FONT_BOLD, command= lambda: [inv_use('c'),update_stats(),inv_item3.configure(text=('Vegan', 'Sando', '..............', inv_qtys('c'))), inv_stats.configure(text= f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}")])
	inv_but3.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	inv_item4 = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=(f"   Po\'Boy .................. {inv_qtys('d')}"), anchor= W)
	inv_item4.place(relheight=0.1, relwidth=0.5, rely=0.50, relx=0.01)

	inv_but4 = Button(inv_item4, text='use', font=FONT_BOLD, command= lambda: [inv_use('d'),update_stats(),inv_item4.configure(text=('Po\'Boy', '..............', inv_qtys('d'))), inv_stats.configure(text= f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}")])
	inv_but4.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.75)

	inv_item5 = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=f"   Waterbottle ... {inv_qtys('e')} %", anchor= W)
	inv_item5.place(relheight=0.1, relwidth=0.47, rely=0.50, relx=0.52)

	water_select = Entry(inv_item5, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
	water_select.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.58)

	water_but = Button(inv_item5, text='drink', font=FONT_BOLD, command= lambda: [use_water(water_select.get()),update_stats(),inv_item5.configure(text=f"   Waterbottle ... {inv_qtys('e')} %"), inv_stats.configure(text= f"Current Health @ __{stats['HP']}\n\nCurrent finances @ __${pack.get_item_quantity('money')}"),water_select.delete(0, END)])
	water_but.place(relheight=0.9, relwidth=0.2, rely=0.05, relx=0.8)

	inv_note_label = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='***NOTES***')
	inv_note_label.place(relheight=0.1, relwidth=0.98, rely=0.61, relx=0.01)

	inv_notesa = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text= 'Muffins restore 40 HP\nPastries restore 50 HP\nVegan Sandos restore 60 HP\nPo\'Boys fully restore HP', justify=LEFT)
	inv_notesa.place(relheight=0.27, relwidth=0.5, rely=0.72, relx=0.01)

	inv_notesb = Label(inv_frame,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='health is lost at a rate of 5 HP per move\ndue to this rate and the health cap being\nno more than 100 it would behoove you\nto select multiples of 5 so as\nnot to waste any.')
	inv_notesb.place(relheight=0.27, relwidth=0.48, rely=0.72, relx=0.51)

def save_win():
	save_me = Toplevel(window)
	save_me.title('Save Menu')
	save_me.resizable(width=False, height=False)
	save_me.configure(width=400, height=200, bg=BG_COLOR)
	save_me.grab_set()

	save_frame = Frame(save_me, bg=BG_GRAY)
	save_frame.place(relwidth=1, relheight=1)

	save_question = Label(save_me, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='Would you like to save')
	save_question.place(relheight=0.19, relwidth=0.98, rely=0.01, relx=0.01)

	save_label = Label(save_me, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD)
	save_label.place(relheight=0.78, relwidth=0.98, rely=0.21, relx=0.01)

	save_ask = Label(save_label,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='Enter name for save file')
	save_ask.place(relheight=0.2, relwidth=0.5, rely=0.3, relx=0.25)

	save_name = Entry(save_label,bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
	save_name.place(relheight=0.2, relwidth=0.5, rely=0.5, relx=0.18)

	save_but = Button(save_label, text='Save', font=FONT_BOLD, command= lambda: [save_game(save_name.get()),update_stats(),save_me.destroy()])
	save_but.place(relheight=0.2, relwidth=0.2, rely=0.5, relx=0.68)

def load_win():
	load_me = Toplevel(window)
	load_me.title('Load Menu')
	load_me.resizable(width=False, height=False)
	load_me.configure(width=400, height=200, bg=BG_COLOR)
	load_me.grab_set()

	load_frame = Frame(load_me, bg=BG_GRAY)
	load_frame.place(relwidth=1, relheight=1)

	load_question = Label(load_me, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='Would you like to load a game')
	load_question.place(relheight=0.19, relwidth=0.98, rely=0.01, relx=0.01)

	load_label = Label(load_me, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD)
	load_label.place(relheight=0.78, relwidth=0.98, rely=0.21, relx=0.01)

	load_ask = Label(load_label,bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='Enter name for load file')
	load_ask.place(relheight=0.2, relwidth=0.5, rely=0.3, relx=0.25)

	load_name = Entry(load_label,bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
	load_name.place(relheight=0.2, relwidth=0.5, rely=0.5, relx=0.18)

	load_but = Button(load_label, text='Load', font=FONT_BOLD, command= lambda: [load_game(load_name.get()),update_stats(),load_me.destroy()])
	load_but.place(relheight=0.2, relwidth=0.2, rely=0.5, relx=0.68)

# main window
window.title("Edmonds Adventure Game")
window.resizable(width=False, height=False)
window.configure(width=1200, height=550, bg=BG_COLOR)

# head label
head_label = Label(window, bg=TOP_BG, fg=TEXT_COLOR, text="Welcome to Edmonds College", font=FONT_BOLD, pady=10)
head_label.place(relwidth=1)

# tiny divider
line = Label(window, width=840, bg=BG_GRAY)
line.place(relwidth=1, rely=0.07, relheight=0.012)

# text widget
text_widget = scrolledtext.ScrolledText(window, width=20, height=10, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
text_widget.place(relheight=0.818, relwidth=0.5, rely=0.08, relx=0.25)
text_widget.configure(cursor="arrow", state=DISABLED)

text_widget.configure(cursor="arrow", state=NORMAL)
text_widget.insert(END,message['greet'])
text_widget.configure(cursor="arrow", state=DISABLED)

# stat frame
stats_frame = Frame(window, bg=BG_GRAY)
stats_frame.place(rely=0.079, relwidth=0.25, relheight=0.921)

# location label
stats_widget1 = Label(stats_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=(f"({stats['cur_loc'][0]},{stats['cur_loc'][1]})"))
stats_widget1.place(rely=0.001, relx=0.01, relwidth=0.98, relheight=0.075)

# health label
stats_widget2 = Label(stats_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=(f"HP @ {stats['HP']} /100"))
stats_widget2.place(rely=0.082, relx=0.01, relwidth=0.98, relheight=0.075)

# money label
stats_widget3 = Label(stats_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=(f"${pack.get_item_quantity('money')}"))
stats_widget3.place(rely=0.163, relx=0.01, relwidth=0.98, relheight=0.075)

# visited label
stats_widget4 = Label(stats_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=(f"Visited {stats['visited']} of 30 locations"))
stats_widget4.place(rely=0.244, relx=0.01, relwidth=0.98, relheight=0.075)

# inside/outside label
stats_widget5 = Label(stats_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text='')
stats_widget5.place(rely=0.327, relx=0.01, relwidth=0.98, relheight=0.075)

# map frame
map_frame = Frame(stats_frame, bg=BG_GRAY)
map_frame.place(rely=0.41, relx=0.01, relwidth=0.98, relheight=0.7)

# Map label
map_widget = Label(map_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_MAP, text=maps[stats['cur_loc']])
map_widget.place(relwidth=0.998, relheight=0.82, rely=0.001, relx=0.001)

# cmd frame
cmd_frame = Frame(window, bg=BG_GRAY)
cmd_frame.place(rely=0.08,relx=0.75, relwidth=0.25, relheight=1)

# inventory label
head_label = Label(cmd_frame, bg=TOP_BG, fg=TEXT_COLOR, text="Inventory", font=FONT_BOLD, pady=15)
head_label.place(relx=0.01, relwidth=0.98)

# Muffin label
muffin_label = Label(cmd_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD,text=('Muffins', '..............', inv_qtys('a')), justify= LEFT, anchor=W)
muffin_label.place(rely=0.094,relx=0.01, relwidth=0.6, relheight=0.06)

# Pastry label
pastry_label = Label(cmd_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD,text=('Pastry', '................', inv_qtys('b')), justify= LEFT, anchor=W)
pastry_label.place(rely=0.154,relx=0.01, relwidth=0.6, relheight=0.06)

# sando label
sando_label = Label(cmd_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD,text=('Vegan', 'Sando', '.....', inv_qtys('c')), justify= LEFT, anchor=W)
sando_label.place(rely=0.214,relx=0.01, relwidth=0.6, relheight=0.06)

# poboy label
poboy_label = Label(cmd_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD,text=('Po\'Boy','...............', inv_qtys('d')), justify= LEFT, anchor=W)
poboy_label.place(rely=0.274,relx=0.01, relwidth=0.6, relheight=0.06)

# water label
water_label = Label(cmd_frame, bg=TOP_BG, fg=TEXT_COLOR,font=FONT_BOLD, text=('Waterbottle', '........', inv_qtys('e'),'%'), justify= LEFT, anchor=W)
water_label.place(rely=0.334,relx=0.01, relwidth=0.6, relheight=0.06)

# inventory buttons frame
inv_but_frame = Frame(cmd_frame, bg=TOP_BG)
inv_but_frame.place(rely=0.094,relx=0.6, relwidth=0.389, relheight=0.3)

# cmd buttons
button_frame = Frame(cmd_frame, bg=TOP_BG)
button_frame.place(rely=0.4, relx=0.01, relwidth=0.98, relheight=0.505)

# north button
north_button = Button(button_frame, text="North", font=FONT_BOLD, bg=BG_GRAY, width=20, command=lambda: [hand_north(),update_stats()])
north_button.place(relx=0.334, rely=0.01, relheight=0.25, relwidth=0.33)

# inventory button
inv_button = Button(button_frame, text="INV", font=FONT_BOLD, width=20, bg=BG_GRAY, command= inventory_win)
inv_button.place(relx=0.008, rely=0.01, relheight=0.25, relwidth=0.33)

# back button
back_button = Button(button_frame, text="Back", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: [hand_back(),update_stats()])
back_button.place(relx=0.66, rely=0.01, relheight=0.25, relwidth=0.33)

# in button
in_button = Button(button_frame, text="IN", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: [hand_in(),update_stats()])
in_button.place(relx=0.334, rely=0.26, relheight=0.25, relwidth=0.33)

# west button
west_button = Button(button_frame, text="West", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: [hand_west(),update_stats()])
west_button.place(relx=0.008, rely=0.26, relheight=0.25, relwidth=0.33)

# east button
east_button = Button(button_frame, text="East", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: [hand_east(),update_stats()])
east_button.place(relx=0.66, rely=0.26, relheight=0.25, relwidth=0.33)

# south button
south_button = Button(button_frame, text="South", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: [hand_south(),update_stats()])
south_button.place(relx=0.334, rely=0.51, relheight=0.25, relwidth=0.33)

# shop button
shop_button = Button(button_frame, text="Shop", font=FONT_BOLD, width=20, bg=BG_GRAY, command=hand_shop)
shop_button.place(relx=0.008, rely=0.51, relheight=0.25, relwidth=0.33)

# talk button
talk_button = Button(button_frame, text="Talk", font=FONT_BOLD, width=20, bg=BG_GRAY, command=hand_talk)
talk_button.place(relx=0.66, rely=0.51, relheight=0.25, relwidth=0.33)

# save button
save_button = Button(button_frame, text="Save", font=FONT_BOLD, width=20, bg=BG_GRAY, command=save_win)
save_button.place(relx=0.008, rely=0.76, relheight=0.23, relwidth=0.495)

# load button
load_button = Button(button_frame, text="Load", font=FONT_BOLD, width=20, bg=BG_GRAY, command=load_win)
load_button.place(relx=0.5, rely=0.76, relheight=0.23, relwidth=0.494)

# bottom label
bottom_label = Label(window, bg=BG_GRAY, height=40)
bottom_label.place(relwidth=0.504, rely=0.9, relx=0.248)

# bottom filler
filler_label = Label(window, bg=TOP_BG, fg=TEXT_COLOR, height=40,wraplength=600, text='Created by Kellen Jones Kellen S. Jones Edmonds Community College CS 115: Intro to Programming Professor Bill McCoy November 28, 2023')
filler_label.place(relheight= 0.08 , relwidth=0.5, rely=0.905, relx=0.25)

window.mainloop()