import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('1')
    f.add_state('1a')
    f.add_state('1b')
    f.add_state('1c')
    f.add_state('1d')
    f.add_state('1e')
    f.add_state('1b1')
    f.add_state('1b7')
    f.add_state('1be')
    f.add_state('1be0')
    f.add_state('1be8')
    f.add_state('2')
    f.add_state('2a')
    f.add_state('2b')
    f.add_state('2c')
    f.add_state('2d')
    f.add_state('2e')
    f.add_state('2f')
    f.add_state('2g')
    f.add_state('2h')
    f.add_state('2i')
    f.add_state('2j')
    f.add_state('2k')
    f.add_state('2l')
    f.add_state('3')
    f.add_state('4')

    
    f.initial_state = '1'
    
    f.set_final('4')
    f.set_final('1a')
    f.set_final('1b')
    
    f.set_final('1c')
    f.set_final('1d')
    f.set_final('1e')
    f.set_final('2b')
    f.set_final('2d')
    f.set_final('2c')
    f.set_final('2e')
    f.set_final('2f')
    f.set_final('2g')
    f.set_final('2h') 
    f.set_final('2i') 
    f.set_final('2j') 
    f.set_final('2k') 
    f.set_final('2l') 
# If 000     
    for ii in xrange(10):
        if ii == 0: #if 000 
            f.add_arc('1', '2', [str(ii)], [])
            f.add_arc('2', '3', [str(ii)], []) 
            f.add_arc('2d', '2d', [str(ii)], [])
      
#Handle 00(0-9)         
        if ii in xrange(10): #Handle 00(0-9)
            f.add_arc('3', '4', [str(ii)], [kFRENCH_TRANS[ii]])

#Handle 0(1-9)(0-9)
# 2 Digit starting with 1
        if ii == 1: #Handle ex: 01(0-9)
            f.add_arc('2', '2a', [str(ii)], [])  
        if ii in xrange(7): #Handle ex: 01(0-6)
            f.add_arc('2a', '2b', [str(ii)], [kFRENCH_TRANS[10+ii]])
        if ii == 7 or ii == 8 or ii ==9: #Handle ex: 01(7-9)
            f.add_arc('2a', '2c', [str(ii)], [kFRENCH_TRANS[10]+" "+kFRENCH_TRANS[ii]])

# 2 Digit starting with 2-6
        if ii == 2 or ii == 3 or ii == 4 or ii == 5 or ii == 6: #Handle ex: 02(0-9)
            f.add_arc('2', '2d', [str(ii)], [kFRENCH_TRANS[10*ii]])
        if ii == 1: #Handle ex: 0(2-6)1
            f.add_arc('2d', '2e', [str(ii)], [kFRENCH_AND+" "+kFRENCH_TRANS[1]])
        if ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6 or ii == 7 or ii == 8 or ii == 9: #Handle ex: 0(2-6)(2-9)
            f.add_arc('2d', '2f', [str(ii)], [kFRENCH_TRANS[ii]])

# 2 Digit starting with 7
        if ii == 7: # For Hadling 7
            f.add_arc('2', '2g', [str(ii)], [kFRENCH_TRANS[60]])
        if ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6: # For Hadling 72,3,4,5,6 [only 16 in dictionary]
            f.add_arc('2g', '2h', [str(ii)], [kFRENCH_TRANS[10+ ii]])
        if ii == 7 or ii == 8  or ii == 9: # For Hadling 77,8,9[its prounced as 60 + 10 + 7/8/9]
            f.add_arc('2g', '2h', [str(ii)], [kFRENCH_TRANS[10]+" "+kFRENCH_TRANS[ii]])  
        if ii == 0: # For Hadling 70
            f.add_arc('2g', '2h', [str(ii)], [kFRENCH_TRANS[10]]) 
        if ii == 1: # For Hadling 71
            f.add_arc('2g', '2h', [str(ii)], [kFRENCH_AND+ " " + kFRENCH_TRANS[11]]) 

# 2 Digit starting with 8
        if ii == 8: # For Hadling 8
            f.add_arc('2', '2i', [str(ii)], [])
        if ii == 0: # For Hadling 80 -> 4 20 [quatre-vingts]
            f.add_arc('2i', '2j', [str(ii)], [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]]) 
        # For Hadling 8(1-9) pronounced as 82 -> 4 20 2 [quatre-vingt-deux]
        if ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6 or ii == 7 or ii == 8  or ii == 9: 
            f.add_arc('2i', '2j', [str(ii)], [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]+" "+kFRENCH_TRANS[ii]])  
        if ii == 1 :
            f.add_arc('2i', '2j', [str(ii)], [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]+" "+kFRENCH_TRANS[ii]]) 

# 2 Digit starting with 9
        if ii == 9: # For Hadling 9
            f.add_arc('2', '2k', [str(ii)], [])
        if ii == 0: # For Hadling 90 -> 4 20 10  [quatre-vingt-dix]
            f.add_arc('2k', '2l', [str(ii)], [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]+" "+kFRENCH_TRANS[10]]) 
        # For Hadling 9(1-6) pronounced as 96 -> 4 20 [10+(1-6)] [quatre-vingt-seize]
        if ii == 1 or ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6: 
            f.add_arc('2k', '2l', [str(ii)], [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]+" "+kFRENCH_TRANS[10+ii]]) 
        if ii == 7 or ii == 8  or ii == 9: # For Hadling 9(7-9) pronounced as 98 -> 4 20 10 (7-9)] [quatre-vingt-dix-huit]
            f.add_arc('2k', '2l', [str(ii)], [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]+" "+kFRENCH_TRANS[10]+" "+kFRENCH_TRANS[ii]])   

#Handle (1-9)(0-9)(0-9)          
# 3 Digit starting with 1
        if ii == 1: #Handle 1(0-9)(0-9) ie., 100-> cent 
            f.add_arc('1', '1a', [str(ii)], [kFRENCH_TRANS[100]])
   
# 3 Digit starting with (2-9)(0-9)(0-9)
        #Handle (2-9)(0-9)(0-9) 200-> deux cents
        if ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6 or ii == 7 or ii == 8  or ii == 9: 
            f.add_arc('1', '1a', [str(ii)], [kFRENCH_TRANS[ii]+" "+kFRENCH_TRANS[100]])

# 3 Digit starting with (2-9)0(0-9)
        #Handle (1-9)0(0-9)         
        if ii == 0: #Handle (1-9)0(0-9)
            f.add_arc('1a', '1be0', [str(ii)], [])
# 3 Digit starting with (2-9)00
        if ii == 0: #Handle (1-9)00 ie., 200 -> deux cents
            f.add_arc('1b', '1c', [str(ii)], [])
            f.add_arc('1b7', '1c', [str(ii)], [kFRENCH_TRANS[10]])
            f.add_arc('1be', '1c', [str(ii)], [kFRENCH_TRANS[10]])
            f.add_arc('1be0', '1c', [str(ii)], [])
# 3 Digit starting with (2-9)0(1-9)
        #Handle (1-9)0(1-9) ie., 501 -> cinq cent un or 555,686etc., 3rd digit (1-9) to print 1/2/3/4/5/6/7/8/9 is done in this loop
        if ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6 or ii == 7 or ii == 8 or ii ==9:
            f.add_arc('1b', '1c', [str(ii)], [kFRENCH_TRANS[ii]])
            #f.add_arc('1be1', '1c', [str(ii)], [kFRENCH_TRANS[ii]])
            f.add_arc('1be0', '1c', [str(ii)], [kFRENCH_TRANS[ii]])
        if ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6 :
            f.add_arc('1b7', '1c', [str(ii)], [kFRENCH_TRANS[10+ii]])
        if ii == 7 or ii == 8  or ii == 9 :
            f.add_arc('1b7', '1c', [str(ii)], [kFRENCH_TRANS[10]+ " " + kFRENCH_TRANS[ii]])
        if ii == 1: #to Handle et
            f.add_arc('1b', '1c', [str(ii)], [kFRENCH_AND+" "+kFRENCH_TRANS[ii]])
            f.add_arc('1b7', '1c', [str(ii)], [kFRENCH_AND+" "+kFRENCH_TRANS[10+ii]])
            #f.add_arc('1be1', '1c', [str(ii)], [kFRENCH_TRANS[ii]])
            f.add_arc('1be0', '1c', [str(ii)], [kFRENCH_TRANS[ii]])
       
# 3 Digit starting with (1-9)(1-6)(1-9) ex: 119, 269 -> 2 100 60 9 (deux cent soixante-neuf)
        if ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6:
            f.add_arc('1a', '1b', [str(ii)], [kFRENCH_TRANS[10*ii]]) 
        if ii == 1: #Handle 111,216
            f.add_arc('1a', '1be', [str(ii)], []) 
        if ii == 1 or ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6 : 
            f.add_arc('1be', '1b', [str(ii)], [kFRENCH_TRANS[10+ii]]) 
            f.add_arc('1be8', '1b', [str(ii)], [kFRENCH_TRANS[ii]]) 
        if ii == 7: 
            f.add_arc('1be', '1b', [str(ii)], [kFRENCH_TRANS[10]+" "+kFRENCH_TRANS[ii]]) 
        if ii == 7 or ii == 8 or ii == 9:
            f.add_arc('1b1', '1b', [str(ii)], [kFRENCH_TRANS[10]+" "+kFRENCH_TRANS[ii]]) 
            f.add_arc('1be8', '1b', [str(ii)], [kFRENCH_TRANS[ii]]) 
        if ii == 8 or ii == 9:
            f.add_arc('1be', '1b', [str(ii)], [kFRENCH_TRANS[10]+" "+kFRENCH_TRANS[ii]]) 
        if ii == 0:
            f.add_arc('1b1', '1b', [str(ii)], [kFRENCH_TRANS[10]]) 
            f.add_arc('1be8', '1b', [str(ii)], [])
# 3 Digit starting with (1-9)7(1-9) ex: 719, 769 -> 7 100 60 10 9 (sept cent soixante-neuf)
        if ii == 7:
            f.add_arc('1a', '1b7', [str(ii)], [kFRENCH_TRANS[60]])
   
# 3 Digit starting with (1-9)8(1-9) ex: 885 -> 8 100 4 20 5 (huit cent quatre-vingt-cinq)
        if ii == 8:
            f.add_arc('1a', '1be8', [str(ii)], [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]])   

# 3 Digit starting with (1-9)9(1-9) ex: 995 -> 9 100 4 20 15 (neuf cent quatre-vingt-quinze)
        if ii == 9:
            f.add_arc('1a', '1d', [str(ii)], [kFRENCH_TRANS[4]+" "+kFRENCH_TRANS[20]])
        if ii == 0: # Handle (1-9)9(1-6) ex: 900
            f.add_arc('1d', '1e', [str(ii)], [kFRENCH_TRANS[10]]) 
        # Handle (1-9)9(1-6) ex: 995 -> 9 100 4 20 15 (neuf cent quatre-vingt-quinze)
        if ii == 1 or ii == 2 or ii == 3  or ii == 4 or ii == 5 or ii == 6: 
            f.add_arc('1d', '1e', [str(ii)], [kFRENCH_TRANS[10+ii]]) 
        if ii == 7 or ii == 8 or ii == 9: # Handle (1-9)9(7-9) ex: 998 -> 9 100 4 20 10 8(neuf cent quatre-vingt-dix-huit)
            f.add_arc('1d', '1e', [str(ii)], [kFRENCH_TRANS[10]+" "+kFRENCH_TRANS[ii]])
    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
