# word_bank

User interface: command line based
commands available:

>>add
'To add a word into your customized work bank'

vocabulary:
definition:
usage:
reference:
affiliation:


>>edit <word> -v/-d/-u/-r/-a
'Edit your word in your word bank'

-v "edit vocab of chosen word"
-d "edit definition of chosen word"
-u "edit usage of chosen word"
-a "edit affiliation of chosen word"

>>delete <word>
'delete a word from your word bank'

>>daily -A
'retrieve all word newly added for today'

-A 'with complete definition and usage'

>>weekly -A
'retrieve all word added for this week'

-A 'with complete definition and usage'

>>monthly -A
'retrieve all word added for this month'

-A 'with complete definition and usage'

>>yearly -A
'retrieve all word added for this month'

-A 'with complete definition and usage'

>>review -D/-W/-M -1
'enter review mode and self-check whether you remember a word'

-D 'review today's word'
-W 'review this week's word'
-M 'review this month's word'
-1 'previous day,previous month or previoys year'

-- enter y to confirm you know this word
-- enter n to show its definition and add it to the review list
-- enter the <word> to confirm you know this word's definition and in addition to reinforce the spelling
  
 
>>clear
'similar to bash command 'clear', clears the command window'

>>quit
'closed database and quit this word bank'


