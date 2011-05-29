# -*- coding: utf-8 -*-
#!/usr/bin/env python2

import somedaymaybe, unittest, time, os.path, os

DBFile = 'someday.pkl'
userhome = os.path.expanduser('~')
INBOXPATH = userhome+'/Desktop/INBOX/'

class CreatingTest(unittest.TestCase):
  def setUp(self):
    pass

  #def TestCreating(self):
    #pass
    
class MoveToInbox(unittest.TestCase):
  def setUp(self):
    self.entrylist = somedaymaybe.EntryList()
    date = time.strptime('09.09.10', "%d.%m.%y")
    self.entry = somedaymaybe.Entry(self, 'TestDescription', date, 'TestCategory', '')
    self.entrylist.add_entry(self.entry)
    
  def testmovetoinbox(self):
    self.entrylist.move_to_inbox(self.entry)
    self.assert_(not self.entry in self.entrylist.entries)
    self.assert_(os.path.isfile(INBOXPATH+'TestDescription'))
    
  def tearDown(self):
    os.system('rm ' + INBOXPATH + 'TestDescription')


##useful assert Expressions
#self.assertEqual(self.seq, range(10))
#self.assertEqual(numeral, result)
#self.assertRaises(ValueError, random.sample, self.seq, 20)
#self.assert_( CONDITION )



if __name__ == '__main__':
  unittest.main()
