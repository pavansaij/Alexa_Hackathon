from __future__ import print_function
import copy
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr


WELCOME_MESSAGE = ("Hi there welcome to ecom you can search a product here")
END_MESSAGE = ("Good Bye Have a great time")
HELP_MESSAGE = "This skill is used to search electroinic"
mobile = [[10000,"oppo","realme","amazon",4.8],[12000,"honor","7x","flipkart",4.7],[9500,"Mi","note5","flipkart",4.5],[45000,"samsung","galaxyS8","flipkart",4.4],[98000,"iphone","x","amazon",4.8]]
laptop = [[30000,"hp","pavilion5","amazon",4.1],[65000,"hp","omen","flipkart",4.2],[54500,"lenovo","thinkpad2","amazon",4.5],[47000,"acer","aspire5","amazon",3.4]]
tv = [[21000,"mi","smarttv","flipkart",4.1],[65000,"sony","bravia","flipkart",4.9],[54500,"samsung","series6","amazon",4.5],[47000,"panasonic","p5","amazon",3.4],[25000,"onida","o6","flipkart",4.1]]
ERROR = "Sorry i coudnt find anything with that tag"
global MSG1
MSG1 = "i've found some top picks for you"

products = ["mobile","smartphone","phone","laptop","television","tv","TV"]
site = ["flipkart","amazon"]

def on_session_started():
    """" called when the session starts  """
    #print("on_session_started")
    
def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']
    

    # process the intents
    if intent_name == "SearchProduct":
        return get_search_product(request)
    elif intent_name == "SearchProductSite":
        return get_search_prodsite(request)
    elif intent_name == "SearchProductPriceRange":
        return get_search_prodprice(request)
    elif intent_name == "SearchProductSitePriceRange":
        return get_search_prodpricesite(request)
    elif intent_name == "wishlist":
        return response(response_mul_text(get_wishlist(), False))
    elif intent_name == "getorder":
        return response(response_mul_text(get_order(), False))
    elif intent_name == "addtowishlist":
        return response(response_plain_text(add_to_wish_list(request), False))
    elif intent_name == "orderprod":
        return response(response_plain_text(add_to_order(request), False))
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_stop_response()
    else:
        print("invalid Intent reply with help")
        return get_help_response()

def response(speech_message):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'response': speech_message
    }

def response_mul_text(output, endsession):
    """ create a simple json plain text response  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'shouldEndSession': endsession
    }

def response_plain_text(output, endsession):
    """ create a simple json plain text response  """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def get_welcome_message():
    """ return a welcome message """
    return response(response_plain_text(WELCOME_MESSAGE, False))

def get_stop_response():
    return response(response_plain_text(END_MESSAGE, True))

def on_launch(request):
    """ called on Launch, we reply with a launch message  """
    return get_welcome_message()

def send_response(msg):
    """ return a welcome message """
    return response(response_plain_text(msg, False))

def speech_to_alexa(sub_set):
    if len(sub_set) <= 0:
        return response(response_plain_text(ERROR, False))
    msg = MSG1 + "<break time = '1s'/>"
    for ss in sub_set:
        stn = str(ss[1] + " " + ss[2] + " from" +  " " + ss[3] + " costs" + " " + str(ss[0]) + " rupees" + " and rated" + " " + str(ss[4]) + " out of 5")
        stn = stn + "<break time = '0.5s'/>"
        msg = (msg + "," + stn)
    msg = "<speak>" + msg + "</speak>"
    return response(response_mul_text(msg, False))
            
def search_prod(sub_set):
    return speech_to_alexa(sub_set)
    
def get_search_product(request):
    try:    
        prod_val = request["intent"]["slots"]["product"]["value"]
    except:
        return response(response_mul_text("<speak>please try again with another utterance</speak>", False))
        
    if prod_val not in products:
        return response(response_plain_text(ERROR, False))
    else: 
        if prod_val in products[0:3]:
            sub_set = copy.deepcopy(mobile)
            return search_prod(sub_set)
        elif prod_val == "laptop":
            sub_set = copy.deepcopy(laptop)
            return search_prod(sub_set)
        elif prod_val == "tv" or "television":
            sub_set = copy.deepcopy(tv)
            return search_prod(sub_set)

def get_search_prodsite(request):
    try:    
        prod_val = request["intent"]["slots"]["product"]["value"]
    except:
        return response(response_mul_text("<speak>please try agin with another utterance</speak>", False))
        
    try:    
        site_val = request["intent"]["slots"]["site"]["value"]
    except:
        return response(response_mul_text("<speak>please try agin with another utterance</speak>", False))
        
    if prod_val not in products or site_val not in site:
        return response(response_plain_text(ERROR, False))
    else: 
        if prod_val in products[0:3]:
            sub_set = copy.deepcopy(mobile)
            sub_set = [elem for elem in sub_set if elem[3] == site_val]
            return search_prod(sub_set)
        elif prod_val == "laptop":
            sub_set = copy.deepcopy(laptop)
            sub_set = [elem for elem in sub_set if elem[3] == site_val]
            return search_prod(sub_set)
        elif prod_val == "tv" or "television":
            sub_set = copy.deepcopy(tv)
            sub_set = [elem for elem in sub_set if elem[3] == site_val]
            return search_prod(sub_set)

def get_search_prodprice(request):
    try:    
        prod_val = request["intent"]["slots"]["product"]["value"]
    except:
        return response(response_mul_text("<speak>please try agin with another utterance</speak>", False))

    try:
        pric_val = int(request["intent"]["slots"]["pricerange"]["value"])
    except KeyError:
        return response(response_mul_text("<speak>please try agin with another utterance</speak>", False))
        
    if prod_val not in products:
        return response(response_plain_text(ERROR, False))
    else: 
        if prod_val in products[0:3]:
            sub_set = copy.deepcopy(mobile)
            sub_set = [elem for elem in sub_set if elem[0] <= int(pric_val)]
            return search_prod(sub_set)
        elif prod_val == "laptop":
            sub_set = copy.deepcopy(laptop)
            sub_set = [elem for elem in sub_set if elem[0] <= int(pric_val)]
            return search_prod(sub_set)
        elif prod_val == "tv" or "television":
            sub_set = copy.deepcopy(tv)
            sub_set = [elem for elem in sub_set if elem[0] <= int(pric_val)]
            return search_prod(sub_set)

def get_search_prodpricesite(request):
    try:    
        prod_val = request["intent"]["slots"]["product"]["value"]
    except:
        return response(response_mul_text("<speak>please try agin with another utterance</speak>", False))

    try:
        pric_val = int(request["intent"]["slots"]["pricerange"]["value"])
    except KeyError:
        return response(response_mul_text("<speak>please try agin with another utterance</speak>", False))
    
    try:    
        site_val = request["intent"]["slots"]["site"]["value"]
    except:
        return response(response_mul_text("<speak>please try agin with another utterance</speak>", False))
        
    if prod_val not in products or site_val not in site:
        return response(response_plain_text(ERROR, False))
    else: 
        if prod_val in products[0:3]:
            sub_set = copy.deepcopy(mobile)
            sub_set = [elem for elem in sub_set if elem[3] == site_val]
            sub_set = [elem for elem in sub_set if elem[0] <= int(pric_val)]
            return search_prod(sub_set)
        elif prod_val == "laptop":
            sub_set = copy.deepcopy(laptop)
            sub_set = [elem for elem in sub_set if elem[3] == site_val]
            sub_set = [elem for elem in sub_set if elem[0] <= pric_val]
            return search_prod(sub_set)
        elif prod_val == "tv" or "television":
            sub_set = copy.deepcopy(tv)
            sub_set = [elem for elem in sub_set if elem[3] == site_val]
            sub_set = [elem for elem in sub_set if elem[0] <= pric_val]
            return search_prod(sub_set)
            
def add_to_wish_list(request):
    try:    
        prodn_val = request["intent"]["slots"]["prodn"]["value"]
    except:
        return response(response_mul_text("<speak>please try again with another utterance</speak>", False))
    
    try:    
        brd_val = request["intent"]["slots"]["brd"]["value"]
    except:
        return response(response_mul_text("<speak>please try again with another utterance</speak>", False))
    
    try:    
        sit_val = request["intent"]["slots"]["site"]["value"]
    except:
        return response(response_mul_text("<speak>please try again with another utterance</speak>", False))
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('wishlist')
    response = table.put_item(
   Item={
        'productname': prodn_val,
        'brand':brd_val,
        'site':sit_val,
        'product':"product"
        
        }
    )
    return ("Added your item to respective wishlist")

def add_to_order(request):
    try:    
        prodnm_val = request["intent"]["slots"]["prodnam"]["value"]
    except:
        return response(response_mul_text("<speak>please try again with another utterance</speak>", False))
    
    try:    
        sitn_val = request["intent"]["slots"]["site"]["value"]
    except:
        return response(response_mul_text("<speak>please try again with another utterance</speak>", False))
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('orders')
    response = table.put_item(
    Item={
        'prodname': prodnm_val,
        'site':sitn_val
        
        }
    )
    return ("Added your item to respective cart")

def get_wishlist():
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table('wishlist')
    response = table.scan()
    nameCount = len(response['Items'])
    nmd = "Following are the items from your wish list<break time = '1s'/>"
    nme = ""
    for itm in response["Items"]:
        prd = str(itm["productname"])
        brd = str(itm["brand"])
        ste = str(itm["site"])
        nme = nme + brd + " branded " + prd + " from " + ste + "<break time = '0.5s'/>" 
    return "<speak>" + nmd + nme + "</speak>"

def get_order():
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table('orders')
    response = table.scan()
    nameCount = len(response['Items'])
    nmd = "Following are the items from your order list<break time = '1s'/>"
    nme = ""
    for itm in response["Items"]:
        prd = str(itm["prodname"])
        ste = str(itm["site"])
        nme = nme + prd + " from " + ste + "<break time = '0.5s'/>" 
    return "<speak>" + nmd + nme + "</speak>"

def lambda_handler(event, context):
    """  App entry point  """
    #print(event)

    if event['session']['new']:
        on_session_started()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()
