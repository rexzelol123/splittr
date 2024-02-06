from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Participant, ValuedItems, Bidding, ResultAuction
from django.core.mail import send_mail

def index(request):
        
    return render(request,'index.html')
    
def create(request):
    
    if request.method =='POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        IDparticipant = request.POST['IDpart']
        item_id = request.POST['item_id']
        new_profile = Participant(firstName= firstName, lastName= lastName, email=email,IDparticipant=IDparticipant, item_id = item_id )
        new_profile.save()
        send_mail('splltr', f'this is your link for the sealed bidding: http://127.0.0.1:8000/{IDparticipant}', 'sealedbidmethod@gmail.com', [email], fail_silently=False)

        success = 'Participants and Items Created Successfully: Check the Email for the Link of Your Bid'
        
        return HttpResponse(success)
    
def items(request):
    if request.method=='POST':
        valItems = request.POST['valItems']
        IDitems = request.POST['IDitems']
        new_item = ValuedItems(valItems= valItems, IDitems=IDitems)
        new_item.save()
        
        success = ''
        
        return HttpResponse(success)
    
def display(request, participant_id):
    participant_check = Participant.objects.filter(IDparticipant = participant_id)
    if participant_check.exists():
        participant = Participant.objects.get(IDparticipant=participant_id)
        myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id))
        participantID = participant_id
        i=0
        for myItem in myItems:
            i+=1
            
        return render(request, 'display.html', {'participant': participant, 'myItems': myItems, 'i':i, 'participantID': participantID})
    else:
        participant_check2 = ResultAuction.objects.filter(link = participant_id)
        
        if participant_check2.exists():
            participant = ResultAuction.objects.get(link=participant_id)
    
            return render(request, 'result.html', {'participant': participant})
        else:
            return HttpResponse("DID NOT EXIST")
    
#SAVE PARTICIPANT ID

def compute2(request):
    #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2,total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
               
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)

#SAVE PARTICIPANT ID

def compute3(request):
    #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            item3 = request.POST['item3']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2, item3=item3,total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)
        
def compute4(request):
    #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        print(IDparticipant)
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            item3 = request.POST['item3']
            item4 = request.POST['item4']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2, item3=item3, item4=item4,total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)
        
def compute5(request):
    #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            item3 = request.POST['item3']
            item4 = request.POST['item4']
            item5 = request.POST['item5']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2, item3=item3, item4=item4,item5=item5, total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)
        
def compute6(request):
    #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            item3 = request.POST['item3']
            item4 = request.POST['item4']
            item5 = request.POST['item5']
            item6 = request.POST['item6']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2, item3=item3, item4=item4, item5=item5, item6=item6,total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)
        
def compute7(request):
    #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            item3 = request.POST['item3']
            item4 = request.POST['item4']
            item5 = request.POST['item5']
            item6 = request.POST['item6']
            item7 = request.POST['item7']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2, item3=item3, item4=item4,item5=item5, item6=item6, item7 = item7,total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)
        
def compute8(request):
    #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            item3 = request.POST['item3']
            item4 = request.POST['item4']
            item5 = request.POST['item5']
            item6 = request.POST['item6']
            item7 = request.POST['item7']
            item8 = request.POST['item8']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2, item3=item3, item4=item4, item5 = item5, item6=item6, item7=item7, item8=item8, total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)
        
def compute9(request):
   #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            item3 = request.POST['item3']
            item4 = request.POST['item4']
            item5 = request.POST['item5']
            item6 = request.POST['item6']
            item7 = request.POST['item7']
            item8 = request.POST['item8']
            item9 = request.POST['item9']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2, item3=item3, item4=item4, item5 = item5, item6=item6, item7=item7, item8=item8, item9=item9, total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)
        
def compute10(request):
    #getting the information in the javascript
   if request.method=='POST':
        IDparticipant = request.POST['partId']
        participant_check = Bidding.objects.filter(IDparticipant=IDparticipant)
        
        #check if the participant bid if exist the participant already bid
        if participant_check.exists():
            success = ' You Already Bid Please Wait for the Result in Your Email'
            return HttpResponse(success)
        #if not exist it will get all the information then save it to the database with 'Bidding' table
        else:
            item1 = request.POST['item1']
            item2 = request.POST['item2']
            item3 = request.POST['item3']
            item4 = request.POST['item4']
            item5 = request.POST['item5']
            item6 = request.POST['item6']
            item7 = request.POST['item7']
            item8 = request.POST['item8']
            item9 = request.POST['item9']
            item10 = request.POST['item10']
            total = request.POST['total']
            participant_auction = Bidding(IDparticipant=IDparticipant,item1=item1, item2=item2, item3=item3, item4=item4, item5 = item5, item6=item6, item7=item7, item8=item8, item9=item9, item10 = item10,total=total)
            participant_auction.save()
            
            participant = Participant.objects.get(IDparticipant=IDparticipant) # get all the participant with 'IDparticipant' 
            myItems = list(ValuedItems.objects.filter(IDitems = participant.item_id)) # the participant will now get its Item_ID 
            get_participants = list(Participant.objects.filter(item_id = participant.item_id)) # The Participant will store its participants information in an array get_participant
            value_items =[] #store all the values per item the participant have, it is a 2d array
            total_items = [] #store the total value they issue
           
            for get_participant in get_participants:
                participant_check2 = Bidding.objects.filter(IDparticipant=get_participant.IDparticipant) #checking if the participant exist in the bid or not
                value_items1 =[] # 1d array that collect all the declared value per item
                
                #if exist then will now process the getting the information inputted
                if participant_check2.exists():
                    participant1 = Bidding.objects.get(IDparticipant = get_participant.IDparticipant)             
                    total_items.append(participant1.total)
                    if participant1.item1 > 0:
                        value_items1.append(participant1.item1)
                    if participant1.item2 > 0:
                        value_items1.append(participant1.item2)
                    if participant1.item3 > 0:
                        value_items1.append(participant1.item3)
                    if participant1.item4 > 0:
                        value_items1.append(participant1.item4)
                    if participant1.item5 > 0:
                        value_items1.append(participant1.item5)
                    if participant1.item6 > 0:
                        value_items1.append(participant1.item6)
                    if participant1.item7 > 0:
                        value_items1.append(participant1.item7)
                    if participant1.item8 > 0:
                        value_items1.append(participant1.item8)
                    if participant1.item9 > 0:
                        value_items1.append(participant1.item9)
                    if participant1.item10 > 0:
                        value_items1.append(participant1.item10)
                    value_items.append(value_items1) # an array that will store in an array
                else:
                    success = 'You Successfully Bid and Please Wait the Result in Your Email: check it regularly'
                    return HttpResponse(success)
                
            total_value = [] # total value awarded
            amount = [] # amount they get or pay
            fair_share =[] # fair share
            final_amount =[] # amount minus the surplus
            participant_wonId =[] # participant id
            participant_wonFirstName = [] # participant first name
            participant_wonLastName = [] # participant last name
            participant_wonEmail=[] # participant last name
            item_won=[] # what items they won
            participant_link = [] # link they will get when send
            pay = []
            get = []
            largest = []
            
            # loop for storing the information in an array from get_participants
            for getParticipant in get_participants:
                participant_wonId.append(getParticipant.IDparticipant)
                participant_wonFirstName.append(getParticipant.firstName)
                participant_wonLastName.append(getParticipant.lastName)
                participant_wonEmail.append(getParticipant.email)
                participant_link.append(getParticipant.IDparticipant+getParticipant.item_id)
                
            # loop for just getting the length of an array the values will change in the process   
            for x in range(len(get_participants)):
                total_value.append(0)
                final_amount.append(0)
                amount.append(0)
                pay.append(0)
                get.append(0)
                item_won.append('')
                fairShare = total_items[x] / len(get_participants)
                rounded = round(fairShare, 2)
                fair_share.append(rounded)
            
            # loop for finding who had the highest bid
            count = 0  
            while count < len(myItems):
                values = [sublist[count] for sublist in value_items] # storing the sub array in an 2d array for example [[50, 150], [100, 200], [200, 300]] the values = [50, 100, 200]
                largest = max(values) #finding its highest value
                # loop for finding its position and declare it with that item
                for i in range(len(values)):
                    if values[i]==largest:
                        myItemm = myItems[count]
                        total_value[i] = total_value[i] + largest
                        item_won[i] = myItemm.valItems+' '+ item_won[i]
                count+=1                           
            for y in range(len(get_participants)):
                amount[y] = total_value[y] - fair_share[y] # total value awarded - fair share

            #finding its surplus by totaling its amount
            surplus = sum(amount)
            
            # will split the surplus depending on the participants
            surplus_split = surplus/len(get_participants)
            
            #rounding it off by 2 decimal places
            rounded_surplus = round(surplus_split, 2)
            
            # loop for the final amount they will pay - surplus
            for y in range(len(get_participants)):
                final_amount[y] = amount[y] - rounded_surplus
                if final_amount[y]>0:
                    pay[y] = round(final_amount[y], 2)
                else:
                    get[y] = round(abs(final_amount[y]), 2)
             
            #saving it to another table in the database the result of the auction       
            for y in range(len(get_participants)):
                auction_result = ResultAuction(firstName=participant_wonFirstName[y],
                                               lastName=participant_wonLastName[y], 
                                               email = participant_wonEmail[y],
                                               IDparticipant=participant_wonId[y],
                                               item=item_won[y],
                                               total_value = total_value[y],
                                               fair_share = fair_share[y],
                                               pay = pay[y],
                                               get = get[y],
                                               link = participant_link[y],
                                               )
                auction_result.save()
                send_mail('splltr', f'this is your link for the result of sealed bidding: http://127.0.0.1:8000/{participant_link[y]}', 'sealedbidmethod@gmail.com', [participant_wonEmail[y]], fail_silently=False)
            success = 'You Successfully Bid and the Link is Available in Your Email'
            return HttpResponse(success)