from twitter import Twitter, OAuth, TwitterHTTPError
import csv, sqlite3
import random, string

OAUTH_TOKEN = ''
OAUTH_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

t = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET))

db = sqlite3.connect("dotatips.sqlite")
c = db.cursor()

heroes = ['Skeleton King', 'Drow Ranger', 'Disruptor', 'Clinkz', 'Pugna']
nouns = ['a local dota player', 'a 100 year old dota player', 'a brazilian dota player', 'a 12 year old dota player']
verbs = ['HATE', 'despise', 'love']
reaction_adjectives = ['furious', 'confused', 'crying', 'complaining', 'shocked', 'scared', 'mad', 'upset', 'raging']
trick_adjectives = ['weird', 'strange', 'simple', 'clever', 'hilarious', 'embarassing', 'secret']
player_types = ['carries', 'supports', 'initiators', 'feeders']
items = ['aegis', 'blink dagger']
teams = ['the Dire', 'the Radiant']
locations = ['fountain', 'jungle', 'lane', 'high ground']
actions = ['pushing', 'ganking', 'jungling', 'denying', 'last hitting']
goals = ['plays', 'kills', 'assists', 'items', 'farm', 'kill steals']

subjects = [heroes, player_types, teams, nouns]

message_templates = ['#SUBJECT# discovers #NUMBER# #T_ADJ# tricks that has #OBJECT# #R_ADJ#',
"Get the #GOAL# you deserve, what #SUBJECT# doesn't want you to know",
"Attacking #SUBJECT# in their #LOCATION#, these #NUMBER# #T_ADJ# tips will have them #R_ADJ#",
"#NUMBER# #T_ADJ# tricks that will have #SUBJECT# afraid to leave their #LOCATION#",
"#SUBJECT# and #ITEM#, what you need to know"]

def post_new_message():
	c.execute('select * from messages where used = 0')

	message = c.fetchone()
	
	print(message[0])

	t.statuses.update(status=message[0])
	
	c.execute("update messages set used = 1 where message = '%s'" % message[0])

def generate_message_component(list):
	temp = list[random.randint(1,len(list)) - 1]
	
	if not isinstance(temp, str):
		temp2 = temp[random.randint(1,len(temp)) - 1]
		
		return temp2
	else:
		return temp
	
def create_new_message():
	template = generate_message_component(message_templates)
	subject = generate_message_component([heroes, player_types, teams, nouns])

	t_adj = generate_message_component(trick_adjectives)
	object = generate_message_component([heroes, player_types, teams, nouns])
	r_adj = generate_message_component(reaction_adjectives)
	action = generate_message_component(actions)
	goal = generate_message_component(goals)
	location = generate_message_component(locations)
	item = generate_message_component(items)
	
	number = random.randint(2, 6)
	
	
	template = str.replace(template, '#SUBJECT#', subject)
	template = str.replace(template, '#NUMBER#', str(number))
	template = str.replace(template, '#T_ADJ#', t_adj)
	template = str.replace(template, '#OBJECT#', object)
	template = str.replace(template, '#R_ADJ#', r_adj)
	template = str.replace(template, '#ACTION#', action)
	template = str.replace(template, '#GOAL#', goal)
	template = str.replace(template, '#LOCATION#', location)
	template = str.replace(template, '#ITEM#', item)
	
	print(template)
	
	