#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import time, cPickle, sys, os

#someday-maybe.py is used to be reminded of actions on a set interval. On each run
#it will ask for each item that has passed it's deadline if it shall be postponed
#or deleted. This is useful for the GTDs weekly review. So you don't have to go
#through all someday-maybe-items each time.

#quit the program with 'QUIT'
#show each entry with 'SHOW_ALL'

userhome = os.path.expanduser('~')
path = userhome + '/Dropbox/Projektmaterial/someday'
DBFile = path+ '/someday.pkl'
backupfile = path+'/somedaybackup.pkl'
INBOXPATH = userhome+'/Desktop/INBOX/'


#def input_complete(input_list):
#if ";" in input_list[-1]:
#return True
#else:
#return False
# 
#def get_input(prompt1, prompt2):
#L = list()
#prompt = prompt1
#while True:
#L.append(raw_input(prompt))
#if input_complete(L):
# return "\n".join(L)
# prompt = prompt2




class UI(object):
  def __init__(self, entrylist):
    self.entrylist = entrylist
  
  def quit(self):
    self.entrylist.save()
    sys.exit()
    
  def show_all(self):
    self.entrylist.show_all()
    
  #def reprocess_all(self):
    #for entry in entrylist.entries:
      #entry.process()
    
#get_date_input asks the user for a date and returns it as a time tuple.

  def decode_timestring(self, string):
    
    if string == '':
      day_code = 7
    else:
      last_character = string[len(string) - 1]
      if last_character == 'd':
	day_code = 1
      elif last_character == 'm':
	day_code = 30
      elif last_character == 'y':
	day_code = 365
      else:
	return string
      
    if len(string) > 1:
      counts = ''
      for i in range(len(string) - 1):
	counts += string[i]
      count = int(counts)
    else:
      count = 1

      
    now = time.mktime(time.localtime())
    day_seconds = 60*60*24
    day_count = day_code * count

    return time.strftime("%d.%m.%y", time.localtime(now + day_seconds * day_count))
      

  def get_date_input(self):
    stop = False
    while not stop:
      try:
	stop = True
	queryline1 = 'Choose Date\nFormat "[x][d/m/y]" for (m=30d, y=365d)*x\n'
	queryline2 = 'days from now or format like 31.12.99 (""=7d): '
	date_string = self.get_string_input(queryline1 + queryline2)
	date = self.decode_timestring(date_string)
	date = time.strptime(date, "%d.%m.%y")
      except ValueError:
	stop = False
	print 'Invalid input'
    return date
  
  def get_string_input(self, query, accepted_inputs = []):
    choice = raw_input(query)
    if choice == 'QUIT':
      self.quit()
    elif choice == 'SHOW_ALL':
      self.show_all()
      choice = self.get_string_input(query)
    if accepted_inputs != []:
      while choice not in accepted_inputs:
	choice = raw_input(query)
	if choice == 'quit':
          self.quit()

    return choice
    
    
    
class EntryList(object):
  def __init__(self):
    
    self.UI = UI(self)
    self.entries = []
    
  def create_new_entry(self, description = '', date = '', category = None, notes = None):
    print ''
    print 'Add new entry'
    print '#####'
    
    if description == '':
      description = self.UI.get_string_input('Description: ')
    if date == '':
      date = self.UI.get_date_input()
    if category is None:
      category = self.UI.get_string_input('Category: ')
    if notes is None:
      notes = self.UI.get_string_input('Notes: ')
    entry = Entry(self, description, date, category, notes)
    self.add_entry(entry)
    
    print 'Entry added'
    print '#####'
    print ''


    
  def import_list(self, filename):
    FILE = open(filename, 'r')
    for line in FILE.readlines():
      if '<CATEGORY>' in line:
        splitline = line.split("<CATEGORY>")
        category = splitline[1].split("</CATEGORY>")[0]
      else:
	date = time.strptime('09.09.10', "%d.%m.%y")
	entry = Entry(self, line, date, category, '')
	self.add_entry(entry)
  
  def export_txt(self, filename):
    pass
  
  def move_to_inbox(self, entry):
    inboxfile = open(INBOXPATH+entry.description, 'w')
    inboxfile.write(entry.notes)
    inboxfile.close()
    self.del_entry(entry)
    
  def add_entry(self, entry):
    self.entries.append(entry)
    
  def del_entry(self, entry):
    self.entries.remove(entry)
    
  def clear_list(self):
    self.entries = []
  
  def show_all(self):    
    count = 0
    for entry in self.entries:
      print entry
      if count % 50 == 49:
	raw_input()
      count += 1
      
#determines the triggered (reminder date is in the past) entries 
#end calls the process method of all those entries
      
  def process_entries(self):
    to_process = []
    for entry in self.entries:
      if type(entry.date) is time.struct_time:
	entry.date = Date(entry.date)
      if entry.date.difference_to_today() <= 0:
        to_process.append(entry)
    for entry in to_process:
      os.system('clear')
      print '#####'
      print 'Processing triggered entries'
      print '#####'
      print ''
      print '\n\nProcessing entry', str(to_process.index(entry)+1), 'of', str(len(to_process)), '\n'
      if entry.process() == 'delete':
      	self.del_entry(entry)
	
  
  def save(self):
    output = open(DBFile, 'wb')
    cPickle.dump(self.entries, output)
    output.close()
    output = open(backupfile, 'wb')
    cPickle.dump(self.entries, output)
    output.close()

  def load(self):
    try: 
      pkl_file = open(DBFile, 'rb')
      self.entries = (cPickle.load(pkl_file))
      pkl_file.close()
    except IOError:
      print 'FILE ERROR'
    

class Entry(object):
  def __init__(self, entrylist, description, date, category, notes):
    self.entrylist = entrylist
    self.description = description
    if category == '':
      category = 'No Category'
    self.category = Category(category)
    self.notes = notes
    self.date = Date(date)
    
  def __str__(self):
    return self.description + ' (' + self.category.name + ') ' + str(self.date) + ' ' + self.notes
      
#processing of triggered entries
  def process(self):
    print self
    query = '\nDelete(d), postpone(p), edit(e) or move to INBOX(i)? '
    choice = self.entrylist.UI.get_string_input(query, ['d' ,'p', 'e', 'i'])
    if choice == 'd':
      return 'delete'
    elif choice == 'p':
      self.date.set_date(self.entrylist.UI.get_date_input())
    elif choice == 'e':
      self.edit()
    elif choice == 'i':
      self.entrylist.move_to_inbox(self)
      
  def edit(self):
    description = self.entrylist.UI.get_string_input('New description ('' for no change): ')
    if description != '':
      self.description = description
    self.date = Date(self.entrylist.UI.get_date_input())
    category = self.entrylist.UI.get_string_input('New category: ')
    if category != '':
      self.category = category
    notes = self.entrylist.UI.get_string_input('New notes: ')
    if notes != '':
      self.notes = notes


class Date(object):
  def __init__(self, date):
    self.set_date(date)
    
  def difference_to_today(self):
    #Calculate difference between two days
    time_difference = time.mktime(self.date) - time.mktime(time.localtime())
    return time_difference
    
  #set the reminder date 
    
  def set_date(self, date):
    self.date = date
    
    #for Testing
    #print ''
    #print "Reminder set to", time.strftime("%d.%m.%Y", self.date)
    #time.sleep(2)
    
    
  def __str__(self):
    return time.strftime("%d.%m.%Y", self.date)


class Category(object):
  def __init__(self, name):
    self.name = name


def run():
  entrylist = EntryList()
  
  #entrylist.save()
  entrylist.load()
  #entrylist.clear_list()
  #entrylist.import_list('to_import.txt')
  query = 'View triggered entries (v) or add new entry (a): '
  
  while True:
    mode_choice = entrylist.UI.get_string_input(query, ['a', 'v'])
    if mode_choice == 'v':
      entrylist.process_entries()
      print 'Finished processing entries.'
    elif mode_choice == 'a':
      entrylist.create_new_entry()


if __name__ == "__main__":
  run()