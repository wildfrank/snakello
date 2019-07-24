# snakello.py
#
# Copyright (C) 2017-2019 Gianfranco Pampado
# All rights reserved.
#	
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#	
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import os
import os.path
import string
from trello import TrelloApi
import unidecode
import datetime
import sys

_RVU = '0.0.12'
_varsnakestatus = 0
_vtrello = 0
_vtrello_app_key =''
_vtrello_user_token = ''
_vdirtk = {}
_vcurboar_id = ''
_vcurboar_name = u''
_vcurboar_num = 0
_vfilename = 'snake.txt'
_vselected_list = []
_vmembers = []
_vexcluded_list = []
_vexcluded_card = []
_vserviceclass = {}
_vwicfile = ''
_vcumulative_wic_list = []
_vleadtime_startlist=-1
_vleadtime_endlist=-1
_vleadfile = ''
_vserviceclass_lead = ''

def fsnakestatus():
	global _varsnakestatus
	global _vtrello 
	global _vcurboar_id
	global _vcurboar_name
	global _vcurboar_num
	global _vdirtk
	cf = []
	lcf = 0
	cl = []
	lcl = 0
	s = ''
	vidMember = ''
	vboards = []
	aboard = ''
	i = 0
	ltot_ncard = 0
	ltot_ncard_noexcluded = 0
		
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.')
	else :
		print('You\'re connnected.')
		print("Trello Application Key: % s" % _vtrello_app_key)
		print("User Token: % s" % _vtrello_user_token)
		
		if _vcurboar_id != '' and _vcurboar_name != '':
			s = 'print'
		elif _vcurboar_id != '' and _vcurboar_name == '':
			
			vidMember = _vdirtk[u'idMember']
			vboards = _vtrello.members.get_board(vidMember)
			
			for i in range(len(vboards)):
				aboard = vboards[i]
				if _vcurboar_id == aboard[u'id']:
					_vcurboar_name = aboard[u'name']
					_vcurboar_num = i
					break
					
			s = 'print'
		
		if s == 'print':

			cf = _vtrello.boards.get_card(_vcurboar_id)
			lcf = len(cf)
			#cl = _vtrello.boards.get_list(_vcurboar_id)
			ltot_ncard, ltot_ncard_noexcluded, cl = fgetcardtoconsider(ltot_ncard, ltot_ncard_noexcluded, cl)
			lcl = len(cl)
			print "* Current selected board is: \"", _vcurboar_name , "\"", "-", _vcurboar_id, "with", lcl, "lists."
			print "The selected lists are:", _vselected_list, "and they contain", ltot_ncard, "cards."
			print "The excluded lists are:", _vexcluded_list
			print "The board contains", lcf, "cards but actually you should consider", ltot_ncard_noexcluded, "cards."
			fcountserviceclass(False)
			


def fgetcardtoconsider(tot_ncard, tot_ncard_noexcluded, cl):
	tot_ncard = 0
	tot_ncard_noexcluded = 0
	cl = []
	global _vselected_list
	global _vexcluded_list
	global _vexcluded_card

	i = 0
	alist = ''
	ncard = 0
	cardsinthelist = []

	
	cl = _vtrello.boards.get_list(_vcurboar_id)
	for i in range(len(cl)):
		alist = cl[i]
		
		cardsinthelist = _vtrello.lists.get_card(alist[u'id'])
		
		ncard = len(cardsinthelist)
		
		# Exclude the cards in _vexcluded_card	
		for y in range(ncard):
			if cardsinthelist[y][u'id'] in _vexcluded_card:
				ncard = ncard - 1
		
		# print i, alist[u'name'], alist[u'id'], "- with", ncard, "cards."
		if i in _vselected_list:
			tot_ncard = tot_ncard + ncard
		if i not in _vexcluded_list:
			tot_ncard_noexcluded = tot_ncard_noexcluded + ncard
		# print tot_ncard
		# print tot_ncard_noexcluded
		
	return tot_ncard, tot_ncard_noexcluded, cl
	

		
		
def fsnakeconnect():

	global _varsnakestatus
	global _vtrello 
	global _vtrello_app_key
	global _vtrello_user_token
	global _vdirtk

	s = ''
	a = False
	
	
	if _varsnakestatus == 0:
	
		if _vtrello_app_key == '':
			print('Insert your own Trello Application Key. It is a 32 digits hex string')
			s = raw_input('--: ')
		else:
			s = _vtrello_app_key
				
		if len(s) != 32 :
			print ("Error: \"%s\" is has a wrong lenght" % s)
			_vtrello = 0
		else:
			_vtrello_app_key = s
			_vtrello = TrelloApi(_vtrello_app_key)
			
		if _vtrello :
			
			if _vtrello_user_token == '':
				print('Insert your own User Token. It is a 64 digits hex string')
				s = raw_input('--: ')
			else:
				s = _vtrello_user_token
			
			if len(s) != 64 :
				print ("Error: \"%s\" is has a wrong lenght" % s)
				_vtrello = 0
			else :
				_vtrello_user_token = s
				_vtrello.set_token(_vtrello_user_token)
				_vdirtk = _vtrello.tokens.get(_vtrello_user_token)
				_varsnakestatus = 1
				a = True
	else :
		print('You\'re already connected to Trello')
		a = True
		
	if a:
		print('Some info on your connection:')
		print("- User Token: % s" % _vtrello_user_token)
		print("- dateExpires: % s" % _vdirtk[u'dateExpires'])
		print("- dateCreated: % s" % _vdirtk[u'dateCreated'])
		print("- idMember: % s\n" % _vdirtk[u'idMember'])
			

def fsnakelistboard():
	global _varsnakestatus
	global _vtrello 
	global _vcurboar_id
	global _vcurboar_name
	global _vcurboar_num
	global _vdirtk
	vidMember = ''
	vboards = []
	aboard = ''
	i = 0

	
	
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.')
	else:
		vidMember = _vdirtk[u'idMember']
		vboards = _vtrello.members.get_board(vidMember)
		
		for i in range(len(vboards)):
			aboard = vboards[i]
			print i, unidecode.unidecode(aboard[u'name']), aboard[u'id'], aboard[u'url']
			
		if _vcurboar_id != '':
			print "* Current selected board is: ", unidecode.unidecode(_vcurboar_name)
		
def fsnakesetboard():
	global _varsnakestatus
	global _vtrello
	global _vcurboar_id
	global _vcurboar_name
	global _vcurboar_num
	global _vdirtk
	global _vselected_list
	global _vexcluded_list
	global _vserviceclass
	
	vidMember = ''
	vboards = []
	aboard = ''
	i = 0
	s = ''
	nb = 0
	
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.')
	else:
		vidMember = _vdirtk[u'idMember']
		vboards = _vtrello.members.get_board(vidMember)
		
		for i in range(len(vboards)):
			aboard = vboards[i]
			print i, aboard[u'name'], aboard[u'id'], aboard[u'url']
			
		if _vcurboar_id != '':
			print("* Current selected board is: % s" % _vcurboar_name)
	
		while 1:
			print('Insert the number of the board you want to select.')
			s = raw_input('--: ')
			
			if s == '':
				print('No selection.')
				break
			else:
				i = int(s)
				nb = len(vboards)
			
				if i < nb or i == 0:
					aboard = vboards[i]
					print i, aboard[u'name'], aboard[u'id'], aboard[u'url']
					_vcurboar_id = aboard[u'id']
					_vcurboar_name = aboard[u'name']
					_vcurboar_num = i
					print("* Current selected board is: % s" % _vcurboar_name)
					_vselected_list = []
					_vexcluded_list = []
					_vserviceclass.clear()
					break
				else:
					print('Wrong selection.')

					
def fsnakelistlists(pflag):
	global _varsnakestatus
	global _vtrello
	global _vcurboar_id
	global _vcurboar_name
	global _vcurboar_num
	global _vselected_list
	global _vexcluded_list
	global _vdirtk
	global _vexcluded_card
	
	cl = []
	alist = ''
	ncard = 0
	tot_ncard = 0
	i = 0
	s = ''
	vidMember = ''
	vboards = []
	aboard = ''
		
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.')
	elif _vcurboar_id == '':
		print('No board selected. ')
		print('Use "setboard" to select a board.')
	else:
		
		if pflag == 0:

			if _vcurboar_id != '' and _vcurboar_name == '':
				vidMember = _vdirtk[u'idMember']
				vboards = _vtrello.members.get_board(vidMember)
			
				for i in range(len(vboards)):
					aboard = vboards[i]
					if _vcurboar_id == aboard[u'id']:
						_vcurboar_name = aboard[u'name']
						_vcurboar_num = i
						break	
		
		if pflag == 0:
			print("* Current selected board is: % s" % _vcurboar_name)
		
		print("* These are the lists in the board:")
		
		cl = _vtrello.boards.get_list(_vcurboar_id)
		for i in range(len(cl)):
			
			alist = cl[i]
			cardsinthelist = _vtrello.lists.get_card(alist[u'id'])

			ncard = len(cardsinthelist)

			for x in range(len(_vselected_list)):
				if _vselected_list[x] == i:
					# Exclude the cards in _vexcluded_card			
					for y in range(ncard):
						if cardsinthelist[y][u'id'] in _vexcluded_card:
							ncard = ncard - 1
					tot_ncard = tot_ncard + ncard
					s = 'print'
			if s == 'print' or pflag == 0:
				if i in _vexcluded_list:
					print i, alist[u'name'], alist[u'id'], "- with", ncard, "cards, is **EXCLUDED**"
				else:
					print i, alist[u'name'], alist[u'id'], "- with", ncard, "cards."
				s = ''
		if pflag == 1:
			print "The selected lists contain", tot_ncard, "cards"
		else:
			print "The selected lists are:", _vselected_list
			print "The excluded lists are:", _vexcluded_list	
			
def fsnakesetlists():
	global _varsnakestatus
	global _vselected_list
	global _vtrello
	s = ''
	i = 0
	cl = []
	x = 0
	
	
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.\n')
	else:
		fsnakelistlists(0)
		cl = _vtrello.boards.get_list(_vcurboar_id)

		while 1:
			_vselected_list.sort()
			
			if x != 0:
				print _vselected_list
			else:
				x = x+1
				
			print "Enter the index number of the list you want to select"
			s = raw_input('--: ')
    	    
			if s == '-':
				if len(_vselected_list) > 0:
					_vselected_list.pop()
			elif s == '--':
				_vselected_list = []
			elif s == '++':
				_vselected_list = []
				for i in range(len(cl)):
					_vselected_list.append(i)
			elif s != '':
				if s.isdigit():
					i = int(s)
					if i+1 > len(cl):
						print ("\nError: \"%s\" is a wrong value." % s)
						print ("You should type a valid integer number.\n")
					else:
						if _vselected_list.count(i) == 0:
							_vselected_list.append(i)
				else:
					print ("\nError: \"%s\" is non recognised." % s)
					print ("You should type a valid integer number.\n")
			else:
				print "The selected list are:", _vselected_list
				break			

def fexcludelist():
	global _varsnakestatus
	global _vexcluded_list
	global _vtrello
	cl = []
	s = ''
	i = 0
	x = 0
	
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.\n')
	else:
		fsnakelistlists(0)
		cl = _vtrello.boards.get_list(_vcurboar_id)
		while 1:
			_vexcluded_list.sort()

			if x != 0:
				print _vexcluded_list
			else:
				x = x+1

			print "Enter the index number of the list you want to exclude"
			s = raw_input('snakello.excludelist --: ')
    	    
			if s == '-':
				if len(_vselected_list) > 0:
					_vexcluded_list.pop()
			elif s == '--':
				_vexcluded_list = []
			elif s == '++':
				_vexcluded_list = []
				for i in range(len(cl)):
					_vexcluded_list.append(i)
			elif s != '':
				if s.isdigit():
					i = int(s)
					if i+1 > len(cl):
						print ("\nError: \"%s\" is a wrong value." % s)
						print ("You should type a valid integer number.\n")
					else:
						if _vexcluded_list.count(i) == 0:
							_vexcluded_list.append(i)
				else:
					print ("\nError: \"%s\" is non recognised." % s)
					print ("You should type a valid integer number.\n")
			else:
				print "The exluded lists are:", _vexcluded_list
				break			
		
def fsnakesave():
	global _varsnakestatus
	global _vtrello 
	global _vtrello_app_key
	global _vtrello_user_token
	global _vcurboar_id
	global _vcurboar_name
	global _vselected_list
	global _vexcluded_list
	global _vexcluded_card
	global _vserviceclass
	global _vwicfile
	global _vcumulative_wic_list
	global _vleadtime_startlist
	global _vleadtime_endlist
	global _vleadfile
	global _vserviceclass_lead
	
		
	s = ''
	
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.')
	else :
		print('You\'re connnected.')
			
	print("Trello Application Key: % s" % _vtrello_app_key)
	print("User Token: % s" % _vtrello_user_token)
	print("Current Board: % s\n" %_vcurboar_name)
		
	while 1:
			print('Are you sure you wanna save? (Y/N)')
			s = raw_input('--: ')
			
			if s == '':
				print('')
			elif s == 'N' or s == 'n':
				break
			elif s == 'Y' or s == 'y':
				_vfilenum = open(_vfilename, 'w')
				_vfilenum.write("_vtrello_app_key"+"="+_vtrello_app_key+"\n")
				_vfilenum.write("_vtrello_user_token"+"="+_vtrello_user_token+"\n")	
				_vfilenum.write("_vcurboar_id"+"="+_vcurboar_id+"\n")

				s = ''
				for i in range(len(_vselected_list)):
						s = s + str(_vselected_list[i]) + ","
				_vfilenum.write("_vselected_list" + "=" + s + "\n")

				s = ''
				for i in range(len(_vexcluded_list)):
						s = s + str(_vexcluded_list[i]) + ","
				_vfilenum.write("_vexcluded_list" + "=" + s + "\n")
				
				s = ''
				for i in range(len(_vexcluded_card)):
						s = s + str(_vexcluded_card[i]) + ","
				_vfilenum.write("_vexcluded_card" + "=" + s + "\n")
				# Save _vserviceclass = {}
		
				s = ''
				keys = list(_vserviceclass.viewkeys())
				values = list(_vserviceclass.viewvalues())
							
				for i in range(len(keys)):
					s = s + keys[i] + ':' + str(values[i]) + ","
					
				_vfilenum.write("_vserviceclass" + "=" + s + "\n")


				if len(_vwicfile) > 0:
					s = "_vwicfile=" + str(_vwicfile)
					_vfilenum.write(s + "\n")					
				
				if len(_vcumulative_wic_list) > 0:
					s = ''
					for i in range(len(_vcumulative_wic_list)):
						s = s + str(_vcumulative_wic_list[i]) + ","
					_vfilenum.write("_vcumulative_wic_list" + "=" + s + "\n")
					
				if _vleadtime_startlist > -1:
					s = "_vleadtime_startlist=" + str(_vleadtime_startlist)
					_vfilenum.write(s + "\n")
				
				if _vleadtime_endlist > -1:
					s = "_vleadtime_endlist=" + str(_vleadtime_endlist)
					_vfilenum.write(s + "\n")
					
				if len(_vleadfile) > 0:
					s = "_vleadfile=" + str(_vleadfile)
					_vfilenum.write(s + "\n")					

				
				if len(_vserviceclass_lead) > 0:
					s = "_vserviceclass_lead=" + str(_vserviceclass_lead)
					_vfilenum.write(s + "\n")					
				
				_vfilenum.close()
				break
				
				
				
			else:
				print('Wrong selection.')
				
def fsnakeload():
		
	global _vtrello_app_key
	global _vtrello_user_token
	global _vcurboar_id
	global _vselected_list
	global _vexcluded_list
	global _vexcluded_card
	global _vcurboar_id
	global _vserviceclass
	global _vwicfile
	global _vcumulative_wic_list
	global _vleadtime_startlist
	global _vleadtime_endlist
	global _vleadfile
	global _vserviceclass_lead
	
	array = []
	i = 0

	if not os.path.exists(_vfilename):
		print _vfilename, "doesn't exist."
	else:
		_vfilenum = open(_vfilename, 'r')
		while 1:
			in_line = _vfilenum.readline()
			if len(in_line) == 0:
				break
			in_line = in_line[:-1] 						#skip \n
			[name,value] = string.split(in_line,"=")
			if name == '_vtrello_app_key':
				_vtrello_app_key = value
				print "loaded", in_line
			elif name == '_vtrello_user_token':
				_vtrello_user_token = value
				print "loaded", in_line
			elif name == '_vcurboar_id':
				_vcurboar_id = value
				print "loaded", in_line
			elif name == "_vselected_list":
				array = []
				_vselected_list = []
				if value != '':
					array=string.split(value, ",")
					for i in range(len(array)):
						if array[i].isdigit():
							_vselected_list.append(int(array[i]))
					_vselected_list.sort()
				print "loaded", "_vselected_list=", _vselected_list
			elif name == "_vexcluded_list":
				array = []
				_vexcluded_list = []
				if value != '':
					array=string.split(value, ",")
					for i in range(len(array)):
						if array[i].isdigit():
							_vexcluded_list.append(int(array[i]))
					_vexcluded_list.sort()
				print "loaded", "_vexcluded_list=", _vexcluded_list
			elif name == "_vexcluded_card":
				array = []
				_vexcluded_card = []
				if value != '':
					array=string.split(value, ",")
					for i in range(len(array)):
						if len(array[i]) == 24:
							_vexcluded_card.append(array[i])
				print "loaded", "_vexcluded_card=", _vexcluded_card
				
			elif name == "_vserviceclass":
				_vserviceclass.clear()
				if value != '':
					array=string.split(value, ",")
					# print array
					for i in range(len(array)):
						if array[i] != '':
							coppia = string.split(array[i], ":")
							key_x = coppia[0]
							val_x = int(coppia[1])
							_vserviceclass[key_x] = val_x
					print "loaded", "_vserviceclass", _vserviceclass
			elif name == "_vwicfile":
				if value != '':
					if not os.path.exists(value):
						print "Warning:", value, "doesn't exist."

					_vwicfile = value
					print "loaded", "_vwicfile=", _vwicfile
			elif name == "_vcumulative_wic_list":
				array = []
				_vcumulative_wic_list = []
				if value != '':
					array=string.split(value, ",")
					for i in range(len(array)):
						if array[i].isdigit():
							_vcumulative_wic_list.append(int(array[i]))
					_vcumulative_wic_list.sort()
				print "loaded", "_vcumulative_wic_list=", _vcumulative_wic_list
			elif name == '_vleadtime_startlist':
				_vleadtime_startlist = int(value)
				print "loaded", "_vleadtime_startlist=", _vleadtime_startlist
			elif name == '_vleadtime_endlist':
				_vleadtime_endlist = int(value)
				print "loaded", "_vleadtime_endlist=", _vleadtime_endlist
			
			elif name == "_vleadfile":
				if value != '':
					if not os.path.exists(value):
						print "Warning:", value, "doesn't exist."
					_vleadfile = value
					print "loaded", "_vleadfile=", _vleadfile

			elif name == '_vserviceclass_lead':
				_vserviceclass_lead = value
				print "loaded", in_line					
		
			else:
				print "this is a wrong line: ", "\'", in_line, "\'"
						
		_vfilenum.close()

		
		
def fsetserviceclass():
	global _vserviceclass
	labels = []
	s = ''
	while 1:
		print "\n"
		if len(_vserviceclass) > 0:
			labels = _vserviceclass.keys()
			print "Current labels for Service Classes are:", _vserviceclass
		print "Enter a Service Classe name that is valid in your Kanban board to insert it."
		s = raw_input('snakello.card.serviceclass.set --: ')
		if s == '--':
			labels = []
		elif s == '':
			break
		else:
			if s not in labels:
				labels.append(s)
			else:
				print s, 'already inserted'
		_vserviceclass.clear()
		_vserviceclass = dict.fromkeys(labels, 0)
	print _vserviceclass
			
		
def fcountserviceclass(pflag):
	
	global _vserviceclass
	global _vcurboar_id
	cards = []
	lists = []
	excludedlist_ids = []
	i = 0
	j = 0
	labels = []
	k = False
	
	cards = _vtrello.boards.get_card(_vcurboar_id)
	lists = _vtrello.boards.get_list(_vcurboar_id)
	
	for i in range(len(lists)):
		if i in _vexcluded_list:
			excludedlist_ids.append(lists[i][u'id'])
		
	labels = _vserviceclass.keys()
	#print _vserviceclass
	#print labels
	#raw_input('press enter to continue')
	for i in range(len(labels)):
		_vserviceclass[labels[i]] = 0
	
	for i in range(len(cards)):
		#cards[i][u'labels'][0][u'name']
		
		#print unidecode.unidecode(cards[i][u'name']), cards[i][u'id'], cards[i][u'idList']
		#raw_input('press enter to continue')
				
		if cards[i][u'id'] not in _vexcluded_card and cards[i][u'idList'] not in excludedlist_ids:
			k = False
			for j in range(len (cards[i][u'labels'])):
				if cards[i][u'labels'][j][u'name'] in _vserviceclass:
					_vserviceclass[cards[i][u'labels'][j][u'name']] += 1
					k = True
					#print _vserviceclass
					#raw_input('press enter to continue')
			if not k and pflag:
				print "This card has not any Service Class:", unidecode.unidecode(cards[i][u'name']), cards[i][u'id'], cards[i][u'idList']
		
	print "The Service Classes are:", _vserviceclass
	
def fserviceclass():
	
	print('\nYou are in "serviceclass" function. Type "set", or "count", or "return".')
	s = ''
	while 1:
		s = raw_input('snakello.card.serviceclass --: ')
		if s == 'return' or s == 'ret':
			break
		elif s == 'set':
			fsetserviceclass()
		elif s == 'count':
			fcountserviceclass(True)
		elif s == '':
			pass
		else:
			print "I can't quit you baby"
		
		
def fsnakelabels():
	
	global _vcurboar_id
	cl = []
	i = 0
	alist = ''
	cards_inlist = []
	x = 0
	the_card = {}
	the_labels = []
	k = 0
	j = 0
	
	valid_labels = dict()
		
	cl = _vtrello.boards.get_list(_vcurboar_id)

	for i in range(len(cl)):
				
		for x in range(len(_vselected_list)):	
			
		#	if _vselected_list[x] == i: # if i not in _vexcluded_list:
			if _vselected_list[x] == i and i not in _vexcluded_list:
			
				for x in range(len(_vselected_list)):
			
					if _vselected_list[x] == i:
					
						alist = cl[i]
					
						print "*L[", alist[u'name'],"]"
						cards_inlist = _vtrello.lists.get_card(alist[u'id'])
				
						for k in range(len(cards_inlist)):
							the_card = cards_inlist[k]
						
							print "  c(", unidecode.unidecode(the_card[u'name']), ")"
						
							the_labels = the_card[u'labels']
												
							for j in range (len(the_labels)):
								cur_label = the_labels[j]
							
								print "     |", unidecode.unidecode(cur_label[u'name']), "|"

								if cur_label[u'name'] not in valid_labels:
									valid_labels[cur_label[u'name']] = 1
								else:
									valid_labels[cur_label[u'name']] = valid_labels[cur_label[u'name']] + 1
						
						

	s = "The labels used in the selected lists of this board are:"
	for i in range(len(valid_labels)):
		s = s + '\n-' + valid_labels.keys()[i] + ':' +  str(valid_labels[valid_labels.keys()[i]])
		
	print "\n", s, "\n" 
	
						
def fsnakeoldestcard():
	
	global _vcurboar_id
	global _vselected_list
	global _vexcluded_list
	global _vexcluded_card
	cl = []
	i = 0
	j = 0
	cards = []
	date = ''
	cardname = ''
	cardid = ''
	listname = ''
	
	cl = _vtrello.boards.get_list(_vcurboar_id)
	
	for i in range(len(cl)):
		if i in _vselected_list and i not in _vexcluded_list:
		
			cards = _vtrello.lists.get_card(cl[i][u'id'])
			
			for j in range( len(cards) ):
				
				# Don't consider cards in _vexcluded_card
				if cards[j][u'id'] not in _vexcluded_card:
				
					if date == '':
						date = cards[j][u'dateLastActivity']
						cardname = cards[j][u'name']
						cardid = cards[j][u'id']
						listname = cl[i][u'name']
						# print date, cardname, listname
					else:
						if cards[j][u'dateLastActivity'] < date:
							date = cards[j][u'dateLastActivity']
							cardname = cards[j][u'name']
							cardid = cards[j][u'id']
							listname = cl[i][u'name']

	print "Oldest action was done on the card", "[", cardname, "]", "that is in the list", "[", listname, "]", "on", "[", date, "]"
	
def fsnakeoldestcardall():
	
	global _vcurboar_id
	global _vselected_list
	global _vexcluded_list
	global _vexcluded_card
	
	cl = []
	i = 0
	j = 0
	cards = []
	cardinfo = []
	listofcard = []
	sortedlistofcard = []
	
	cl = _vtrello.boards.get_list(_vcurboar_id)
	
	for i in range(len(cl)):
		if i in _vselected_list and i not in _vexcluded_list:
		
			cards = _vtrello.lists.get_card(cl[i][u'id'])
									
			for j in range( len(cards) ):
				
				# Don't consider cards in _vexcluded_card
				if cards[j][u'id'] not in _vexcluded_card:
				
					cardinfo.append(cards[j][u'dateLastActivity'])
					cardinfo.append(cards[j][u'name'])
					cardinfo.append(cl[i][u'name'])
					# print cardinfo
					listofcard.append(cardinfo)
					cardinfo = []
				
	
	# print "\n", listofcard, "\n"
	
	sortedlistofcard = sorted(listofcard,None,None,0)
	
	for i in range(len(sortedlistofcard)):
		print "Card [", unidecode.unidecode(sortedlistofcard[i][1]), "]", "in the list [", sortedlistofcard[i][2], "]", "on", "[", sortedlistofcard[i][0], "]"
	
def fsnakeprintid():
	global _vcurboar_id
	cl = []
	i = 0
	j = 0
	cards = []
	cardinfo = []
	listofcard = []
	sortedlistofcard = []
	
	cl = _vtrello.boards.get_list(_vcurboar_id)
	for i in range(len(cl)):
		if i in _vselected_list and i not in _vexcluded_list:
			cards = _vtrello.lists.get_card(cl[i][u'id'])
			
			for j in range( len(cards) ):
				if cards[j][u'id'] not in _vexcluded_card:
					cardinfo.append(cards[j][u'dateLastActivity'])
					cardinfo.append(cards[j][u'name'])
					cardinfo.append(cards[j][u'id'])
					cardinfo.append(cl[i][u'name'])
					# print cardinfo
					listofcard.append(cardinfo)
					cardinfo = []
				
	for i in range(len(listofcard)):
		print "Card [", unidecode.unidecode(listofcard[i][1]), "]", "in the list [", listofcard[i][3], "]", "has id", "[", listofcard[i][2], "]"
			
def fsnakeexcludecard():
	global _vtrello
	global _varsnakestatus
	global _vexcluded_card
	global _vcurboar_id
	s = ''
	i = 0
	x = 0
	
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.\n')
	else:
		
		x = len(_vexcluded_card)
		
		while 1:
		
			if x != 0:
				print "The excluded cards are:", _vexcluded_card
			else:
				x = x+1

			print "Enter the ID of the card you want to exclude"
			s = raw_input('--: ')
			
			if s == '-':
				if len(_vselected_card) > 0:
					_vexcluded_card.pop()
			elif s == '--':
				_vexcluded_card = []
			elif s != '':
				#the id must be 24 char length
				#must exist in the current boar
				#I should have to manage errors in https request but now I'm not able yet.
				if len(s) != 24:
					print ("\nError: \"%s\" is non recognised." % s)
				else:
					aboard = _vtrello.cards.get_board(s)
					if aboard[u'id'] == _vcurboar_id:
						if _vexcluded_card.count(s) == 0:
							_vexcluded_card.append(s)
					else:
						print ("\nError: \"%s\" is non recognised." % s)
			else:
				print "The exluded cards are:", _vexcluded_card
				break	
			
			
	
	
	
def fsnakecard():
	
	s = ''
	
	fsnakestatus()
	
	if _varsnakestatus == 0:
		return
	
	fsnakelistlists(1)
	
	print('\nYou are in "Card" function. Type "labels", or "oldest", or "oldest+", or "id", or "excludecard", or "serviceclass", or "return".')
	
	while 1:
		
		s = raw_input('snakello.card --: ')
		
		if s == 'labels':
			fsnakelabels()
		if s == 'serviceclass':
			fserviceclass()
		elif s == 'oldest':
			fsnakeoldestcard()
		elif s == 'oldest+':
			fsnakeoldestcardall()
		elif s == 'id':
			fsnakeprintid()
		elif s == 'excludecard':
			fsnakeexcludecard()
		elif s == 'return' or s == 'ret':
			print "\nBabe, baby, baby, I'm gonna leave you.", "I said baby, you know I'm gonna leave you.\n"
			break
		elif s == '':
			pass
		else:
			print "I can't quit you baby"
	

def fsnakemember():
	global _vcurboar_id
	cl = []
	i = 0
	j = 0
	k = 0
	mcard = []
	ncard = 0
	ncardtot = 0
	otherboard = 0
		
	fsnakestatus()
	
	if _varsnakestatus == 0:
		return
		
	cl = _vtrello.boards.get_list(_vcurboar_id)
		
	_vmembers = _vtrello.boards.get_member(_vcurboar_id)
	
	print "The members of the current board are:"
	
	for i in range(len(_vmembers)):
				
		mcard = _vtrello.members.get_card(_vmembers[i][u'id'])
		
		ncard = ncardtot= otherboard = 0
		
		for j in range(len(mcard)):
			if mcard[j][u'idBoard'] == _vcurboar_id:
				
				#check if the card is in one of the selected lists
				for k in range(len(cl)):
					if k in _vselected_list:
						if cl[k][u'id'] == mcard[j]['idList']:
							ncard = ncard + 1
							ncardtot = ncardtot + 1
							break
						else:
							ncardtot = ncardtot + 1
							
			else:
				otherboard = otherboard + 1
		
		# print _vmembers[i][u'fullName'], "has", str(ncard), "cards in the selected lists of the current board, and ", str(otherboard), "in other boards."
		print _vmembers[i][u'fullName'], "appears in", str(ncard), "cards in the selected lists and appears in the current board for a total of", str(ncardtot), "times"
				
				
def fleadtime():
	global _vleadtime_startlist
	global _vleadtime_endlist
	global _vleadfile
	global _vserviceclass_lead
	date_done = ''
	date_start = ''
	date_start_ipo = ''
	listid_start_ipo = ''
	sx = 'return'
	recline1 = ''
	k1 = False
	k2 = 0
	array1 = []
	array2 = []
	datex = ''
	timex = ''

	if _vleadtime_startlist == -1 or _vleadtime_endlist == -1:
		print("_vleadtime_startlist and/or _vleadtime_endlist not initialized in % s" % _vfilename)
	else:
		
		if _vleadfile == '':
			print("_vwicfile not initialized in % s" % _vfilename)
			print("cannot save any data")
		else:
			while 1:
				print "\nYou are in snakello.metric.leadtime. Make your choice:"
				print "return - return to previous menu"
				print "write - extract and write data in the file in append mode"
				print "wlog - extract and write data in the file in append mode and log some output on stdout"
				print "write+ - extract and write data in the file. Overwrites the existing file if the file exists."
				print "wlog+ - extract and write data in the file and log some output on stdout. Overwrites the existing file if the file exists."
				
				sx = raw_input('snakello.metric.leadtime --: ')
				
				if sx == 'return' or sx == 'ret':
					print '\nSince my baby left me, I\'ve been losing, I\'ve been losing, I\'ve been losing my mind...'
					sx = 'return'
					break
				elif sx == 'write':
					break
				elif sx == 'wlog':
					break
				elif sx == 'write+':
					break
				elif sx == 'wlog+':
					break
				else:
					print('')
		
		if sx != 'return':
			
			if sx == 'write+' or 'wlog+':
				_vfilenum = open(_vleadfile, 'w+')
			elif sx == 'write' or 'wlog':
				_vfilenum = open(_vleadfile, 'a+')
			
			cl = _vtrello.boards.get_list(_vcurboar_id)
						
			cards = _vtrello.lists.get_card(cl[_vleadtime_endlist][u'id'])
			
			for i in range(len(cards)):
				card_actions = _vtrello.cards.get_action(cards[i][u'id'])
				
				if sx == 'wlog' or sx == 'wlog+':
					print card_actions
					print len(card_actions)
						
				if sx == 'wlog' or sx == 'wlog+':
					s = raw_input('snakello.metric.leadtime --: ')
					if s == "ret":
						break
			
				date_done = ''
				date_start = ''
				date_start_ipo = ''
			
				for j in range(len(card_actions)):
					
					if sx == 'wlog' or sx == 'wlog+':
						print card_actions[j][u'type'], card_actions[j][u'date']
					
					if date_done != '':		
						# If here we alreay have date_done the date-time of when the card entered in "DONE".
						if 	card_actions[j][u'type'] == u'updateCard':
							if sx == 'wlog' or sx == 'wlog+':
								print "######", card_actions[j][u'data'][u'listAfter']
											
							if card_actions[j][u'data'][u'listBefore'][u'id'] == cl[_vleadtime_startlist][u'id']:
								if sx == 'wlog' or sx == 'wlog+':
									print "Card was moved from", card_actions[j][u'data'][u'listBefore'], "to", card_actions[j][u'data'][u'listAfter'], "on", card_actions[j][u'date']
								
								date_start = card_actions[j][u'date']
								break
							else:
								date_start_ipo = card_actions[j][u'date']
								listid_start_ipo = card_actions[j][u'data'][u'listAfter'][u'id']
								
								if sx == 'wlog' or sx == 'wlog+':
									print "date_start_ipo=", date_start_ipo, "listAfter=", card_actions[j][u'data'][u'listAfter']
																				
						elif card_actions[j][u'type'] == u'commentCard':
							
							if sx == 'wlog' or sx == 'wlog+':
								print "Card was commented on", card_actions[j][u'data'][ u'list']
							
							if date_start_ipo == '':
								date_start_ipo = card_actions[j][u'date']
								listid_start_ipo = card_actions[j][u'data'][ u'list']['id']
								
								if sx == 'wlog' or sx == 'wlog+':
									print "date_start_ipo=", date_start_ipo, "list=", card_actions[j][u'data'][ u'list']
							else:
								for k in range(len(cl)):
									if cl[k][u'id'] == card_actions[j][u'data'][ u'list'][u'id']:
										if k > _vleadtime_startlist:
											date_start_ipo = card_actions[j][u'date']
											listid_start_ipo = card_actions[j][u'data'][ u'list']['id']
											
											if sx == 'wlog' or sx == 'wlog+':
												print "date_start_ipo=", date_start_ipo, "list=", card_actions[j][u'data'][ u'list']
																			
					else: 
					
						if card_actions[j][u'type'] == u'updateCard' and card_actions[j][u'data'][u'listAfter'][u'id'] == cl[_vleadtime_endlist][u'id']:
							
							if sx == 'wlog' or sx == 'wlog+':
								print "Card was moved from", card_actions[j][u'data'][u'listBefore'], "to", card_actions[j][u'data'][u'listAfter'], "on", card_actions[j][u'date']
							
							date_done = card_actions[j][u'date']
					
					
							
				if date_start == '' and date_start_ipo != '':
					for k in range(len(cl)):
						if cl[k][u'id'] == listid_start_ipo:
							if k > _vleadtime_startlist:
								date_start = date_start_ipo
				
		
				if sx == 'wlog' or sx == 'wlog+':
					print "For this card assume, start =", date_start, "end =", date_done
					
				if 	date_start != '' and date_done != '':
					thecard = _vtrello.cards.get(cards[i][u'id'])
					
					k1 = False
					for i1 in range(len (thecard[u'labels'])):
						if sx == 'wlog' or sx == 'wlog+':
							print "thecard[u'labels'][i1][u'name']=" + thecard[u'labels'][i1][u'name']
							print "_vserviceclass_lead=" + _vserviceclass_lead
						
						if thecard[u'labels'][i1][u'name'] == _vserviceclass_lead:
							k1 = True
							break
							
					if k1 == True:
						
						array1 = string.split(date_start, "T")
						datex = array1[0]
						array2 = string.split(array1[1], ".")
						timex = array2[0]
						
						recline1 = datex + "," + timex
						
						array1 = string.split(date_done, "T")
						datex = array1[0]
						array2 = string.split(array1[1], ".")
						timex = array2[0]
						
						recline1 = recline1 + "," + datex + "," + timex + "," + thecard[u'labels'][i1][u'name'] + "," + thecard[u'id'] + "," + thecard[u'shortUrl'] + "\n"
			
						if sx == 'wlog' or sx == 'wlog+':
							print date_start
							print date_done
							print thecard[u'labels'][i1][u'name']
							print thecard[u'id']
							print thecard[u'shortUrl']
								
							print recline1
						
						
						if k2 == 0:
							sys.stdout.write("\b")
							sys.stdout.write("-")
							k2 = k2 + 1
						elif k2 == 1:
							sys.stdout.write("\b")
							sys.stdout.write("\\")
							k2 = k2 + 1
						elif k2 == 2:
							sys.stdout.write("\b")
							sys.stdout.write("|")
							k2 = k2 + 1
						elif k2 == 3:
							sys.stdout.write("\b")
							sys.stdout.write("/")
							k2 = 0
									
						
						_vfilenum.write(recline1)
					
				recline1 = ''
					
				if sx == 'wlog' or sx == 'wlog+':					
					s = raw_input('snakello.metric.leadtime --: ')
					if s == "ret":
						break

		if sx != 'return':
			_vfilenum.close()
			
		sys.stdout.write("\b")
		
		
				
def fmetric():
	global _vwicfile
	global _vcumulative_wic_list
	global _vcurboar_id
	global _vexcluded_list
	global _vexcluded_card
	cl = []
	cards = []
	ncards = 0
	i = 0
	j = 0
	k = 0
	s = ''
	recline1 = ''
	recline2 = ''
	rechead1 = ''
	rechead2 = ''
	
	
	if _varsnakestatus == 0:
		print('Snakello is not connected to Trello.')
		print('Use "connect" to connect to Trello.\n')
	else:
	
		while 1:
			print('\nYou are in "metric" function. Type "wic", or "leadtime", or "return".')
			s = raw_input('snakello.metric --: ')
			
			if s == 'wic':
			
				recline1 = ''
				recline2 = ''
				rechead1 = ''
				rechead2 = ''
			
				if _vwicfile == '':
					print("_vwicfile not initialized in % s" % _vfilename)
					print("cannot save any data")
				else:
					_vfilenum = open(_vwicfile, 'a+')
					_vfinfo = os.stat(_vwicfile)
					
					cl = _vtrello.boards.get_list(_vcurboar_id)
					
					for i in range(len(cl)):
						if i in _vcumulative_wic_list:	
					
							#print cl[i][u'name']
							
							if _vfinfo.st_size == 0L:
								rechead2 = rechead2 + cl[i][u'name'] + ","
							
							cards = _vtrello.lists.get_card(cl[i][u'id'])
							ncards = 0
							
							for j in range( len(cards) ):
							
								# Don't consider cards in _vexcluded_card
								if cards[j][u'id'] not in _vexcluded_card:
									ncards = ncards + 1
									
									# sys.stdout.write(".")
									
									if k == 0:
										sys.stdout.write("\b")
										sys.stdout.write("-")
										k = k + 1
									elif k == 1:
										sys.stdout.write("\b")
										sys.stdout.write("\\")
										k = k + 1
									elif k == 2:
										sys.stdout.write("\b")
										sys.stdout.write("|")
										k = k + 1
									elif k == 3:
										sys.stdout.write("\b")
										sys.stdout.write("/")
										k = 0
									
							# print ncards
							
							recline2 = recline2 + str(ncards) + ","
							
					sys.stdout.write("\b")
					currentDT = datetime.datetime.now()
					recline1 = currentDT.strftime("%Y/%m/%d") + "," + currentDT.strftime("%H:%M:%S") + "," + recline2 + "\n"
					
					if _vfinfo.st_size == 0L:
						rechead1 = "Date,Time,"+rechead2+"\n"
						print rechead1
				
					print recline1
					
					while 1:
						print("Are you sure you wanna save the record in the file % s ? (Y/N)" % _vwicfile)
						s = raw_input('snakello.metric.wic --: ')
						if s == '':
							print('')
						elif s == 'N' or s == 'n':
							print("no data was written in the file %s \n" % _vwicfile)
							break
						elif s == 'Y' or s == 'y':
							if _vfinfo.st_size == 0L:
								_vfilenum.write(rechead1)
							_vfilenum.write(recline1)
							print("the record was written in the file %s \n" % _vwicfile)
							break
						else:
							print('')
					
					_vfilenum.close()
					s = ''
			
			if s == 'leadtime':
				fleadtime()
				
			elif s == 'return' or s == 'ret':
				print "\nBabe, baby, baby, I'm gonna leave you.", "I said baby, you know I'm gonna leave you.\n"
				break
			elif s == '':
				pass
			else:
				print "I can't quit you baby"		
			
		
		
		
		

		
def fsnakehelp():
	s = ''
	
	print('\nValid commands are:')
	#print('"quit" exits the snakello module.')
	#print('"status" tells you if snakello has a connection established with Trello, in such a case it tells you some information on the current selected board.')
	print('board')
	print('card')
	print('connect')
	print('copyright')
	print('credits')
	print('exludelist')
	print('license')
	print('list')
	print('load')
	print('member')
	print('save')
	print('setboard')	
	print('setlist')	
	print('status')
	print('quit')
	print('\nEnter the name of any command, to get help. To quit this help utility and return to the snakello command line, just press enter.\n')
	
	
	while 1:
		s = raw_input('snakello help> ')
		if s == 'board':
			print('\n"board" print the list of your boards and the name of selected board.')
			print('You should be connected to Trello before using this command.\n')
			print('\nSee also the command "connect".\n')
		elif s == 'card':
			print('\nwith the "card" command you enter an interactive submenu where you can use these commands:\n')
			print('"labels" --: gives you an highlight on all the Service Classes (i.e. labels) used in the current board.')
			print('"oldest" --: print the title card, in the selected lists, that has the oldest modification date (field "dateLastActivity").')
			print('"oldest+" --: prints the list of all the cards, in the selected lists, sorted in reverse order on the modification date (field "dateLastActivity").')
			print('"serviceclass" --: manage, set and count the labels that you assigned a Service Class meaning in your Kanban board.\n')
			print('\nBefore using the "card" command you should connect to Trello, select a board and select one ore more lists for that board.\n')
		elif s == 'connect':
			print('\n"connect" establishes a connection with Trello, via https, using two pieces of information you should own:')
			print('    your own "Trello Application Key". It is a 32 digits hex string')
			print('    your own "User Token". It is a 64 digits hex string.')
			print('\nPlease read the file "notes.txt" for more information on these two strings.')
			print('\n"connect" works in interactive way in case you haven\'t loaded the Application Key and the User token from file.')
			print('\nSee also the commands "load" and "save".\n')
		elif s == 'copyright':
			print('\n"copyright" prints the information of copyright of this software.\n')
		elif s == 'credits':
			print('\n"credits" prints the thanks the author wants to give to whom supportet him in developing this sofwtare program.\n')
		elif s == 'excludelist':
			print('\n"exludelist" lets you enter an interactive submenu where you can managage, add and delete the "Lists" and the relative cards you want to exclude in subsequent usage of data mining functions. \n')		
		elif s == 'load':
			print('\n"load" opens the file snake.txt, if it exists in the current directory, and it loads in memory the parameters that could be ')
			print('contained in it: "_vtrello_app_key" = "Trello Application Key"; "_vtrello_user_token" = "User Token"; "_vcurboar_id"; "_vselected_list"; "_vexcluded_list"; "_vexcluded_card"; "_vserviceclass".\n')
			print('\nSee also the commands "save" and "connect".\n')
		elif s == 'license':
			print('\n"license" prints the licence information of this sofwtare program.\n')
		elif s == 'list':
			print('\n"list" prints some summary information on all the "Lists" of the current Board; then prints the index of the "Selected Lists", the index of the "Excluded List" that both will be taken in account in subsequent usage of data mining functions.\n')
		elif s == 'member':
			print('\n"member" prints the names of board\'s member and for each of them it prints the number of the cards, in the selected lists, at which they belongs to.\n')
		elif s == 'metric':
			print('\n"metric" lets you manage some information for the Management Reporting.\n')
		elif s == 'quit':
			print('\n"quit" exits from Snakello.\n')
		elif s == 'save':
			print('\n"save" saves in the file snake.txt the current values of the memory global variables: "_vtrello_app_key" = "Trello Application Key"; "_vtrello_user_token" = "User Token"; "_vcurboar_id"; "_vselected_list"; "_vexcluded_list"; "_vexcluded_card"; "_vserviceclass".\n') 
		elif s == 'setboard': 
			print('\n"setboard" prints your boards and lets you select the one you want to work on.\n')
		elif s == 'setlist':
			print('\n"setlist" lets you enter an interactive submenu where you can managage, add and delete the "Lists" and the relative cards you want to consider in subsequent usage of data mining functions.\n')
		elif s == 'status':
			print('\n"status" if snakello is connected to Trello "status" prints some information: "Trello Application Key"; "User Token"; "Current selected board"; the index of "The selected lists"; the index of "The excluded lists"; the number of cards in the board.\n')
		elif s == '':
			print('\nYou are now leaving help and returning to the snakello command line.\n')
			break
		else :
			print ("Error: \"%s\" is non recognised." % s)
			print ('May be you\'re tired and you need some good snake stuff: https://youtu.be/L_rhl1IHxsQ')
	
# the main 
			
if __name__ == "__main__":
	import sys
	s = ''
	errtype = 0
	
	print "Snakello", _RVU
	
	if not (sys.version_info.major == 2 and sys.version_info.minor == 7):
		print ('Must use Python 2.7')
		exit()
			
	print('Play this: https://www.youtube.com/watch?v=diumeAfYULo, than make your choice or type "help", "copyright", "credits" or "license" for more information.')
		
	while 1: 
		s = raw_input('snakello-> ')
		if s == 'help':
			print('\nWelcome to Snakello %s. This is the online help utility.\n' % _RVU)
			print('If this is your first time using Snakello, you should definitely check out')
			print('the tutorial in the README file.\n')
			print('And don\'t forget my dog. \nFixed and consequent.\n')
			print('Type help() for interactive help.\n')
		elif s == 'help()':
			fsnakehelp()
		elif s == 'copyright':
			print('Copyright (c) 2017 2018 Gianfranco Pampado.\nAll Rights Reserved.')
		elif s == 'credits':
			print('Thanks to my family and my friends for supporting Snakello development.\n')
		elif s == 'license':
			print("Snakello % s" % _RVU)
			print('\nCopyright (C) 2017-2018 Gianfranco Pampado')
			print('All rights reserved.')
			print('\nRedistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:')
			print('\n1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.')
			print('\n2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.')
			print('\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.')
			print('\n')
		elif s == 'quit':
			print('\nLike lesser birds on the four winds, yeah')
			print('Like silver scrapes in May')
			print('Now the sands become a crust')
			print('And most of you have gone away (hm, yeah gone away)\n')
			break
		elif s == 'status':
			fsnakestatus()
		elif s == 'connect':
			fsnakeconnect()
		elif s == 'board':
			fsnakelistboard()
		elif s == 'setboard':
			fsnakesetboard()
		elif s == 'list':
			fsnakelistlists(0)
		elif s == 'setlist':
			fsnakesetlists()
		elif s == "save":
			fsnakesave()
		elif s == "load":
			fsnakeload()
		elif s == "card":
			fsnakecard()
		elif s == "member":
			fsnakemember()
		elif s == "excludelist":
			fexcludelist()
		elif s == "metric":
			fmetric()
		elif s != '':
			print ("Error: \"%s\" is non recognised." % s)
			errtype = errtype + 1
			if errtype == 3:
				print ('\n  So, hey mystery man\n  What\'s your plan\n  I\'ve got to tell the world\n  To beware you don\'t care.')
				print ('\n  Snake Charmer! - https://youtu.be/Tny7ZJAE0aM\n')
				errtype = 0
					
				
		
		
		


	
	
	
