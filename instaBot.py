import instagrapi, time, random, os, wget,json, logging
from instagrapi import Client
from instagrapi.types import DirectThread, DirectMessage, DirectResponse
from datetime import datetime
import chatbot

user_name=''
password=''
hashtags=[]
comments=[u"Wow 😍😍",u"😍😍"]
path_file = 'cookie_thumper'
api=None

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

with open("config.json") as f:
    data = json.loads(f.read())
    user_name = data["user_name"]
    password = data["password"]
    hashtags = data["hashtags"]


### LOGIN ###

def savecookie(data):
    with open(path_file, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=True)#, default=default)

def readcookie(data):
    with open(data, 'r', encoding='utf8') as json_file:
        return json.load(json_file)#, object_hook=object_hook)

def blogin():
    global api
    print("Login con",user_name)
    if os.path.exists(path_file):
        api = Client(readcookie(path_file))
    else:
        api = Client()
        api.uuid="99f90278-174d-420c-9b07-47677e09ab20"
        api.phone_id="51224ec5-943d-4ea8-b71d-bd3249c0d588"
        api.device_id="android-ef688bb0d352317c"
        api.user_agent="Instagram 135.0.0.1.1 Android (28/9.0; 420dpi; 1080x1920; OnePlus; ONEPLUS A3003; OnePlus3; qcom; en_US; 180322800)"
        api.client_session_id="dfc8810b-633d-4048-b396-e170f2037832"
        api.login(user_name, password,relogin=True)
        savecookie(api.get_settings())

### CORE ###

def manage_followers():
    followers=api.user_followers(api.user_id_from_username(user_name))
    following=api.user_following(api.user_id_from_username(user_name))
    for f in followers: 
        if f not in following: api.user_follow(f)
    return followers

def unfollow_infami():
    followers=api.user_followers(api.user_id_from_username(user_name))
    following=api.user_following(api.user_id_from_username(user_name))
    for f in following: 
        if f not in followers: api.user_unfollow(f)
        time.sleep(random.randint(1,39)/10)
        print("Removed ",api.username_from_user_id(f))

def like_inquietanti(user):
    lista=api.user_medias(user,amount=40)
    if len(lista)==0: lista=api.user_medias_v1(user,amount=40)
    print("Processing ",api.username_from_user_id(user))
    print("Found ",len(lista)," medias")
    for l in lista: 
        print('Media liked\n',l.id)
        time.sleep(random.randint(1,39)/10)
        api.media_like(l.id)
    print("ho messo like ai post di ",api.username_from_user_id(user))

def upload_foto(url='https://i.pinimg.com/originals/79/1f/ca/791fca6132c5c51e1bac62a78dfac848.jpg',frase=''):
    path='./cat/'
    foto=path+'cat.jpg'
    try:os.remove(foto)
    except:pass
    time.sleep(2)
    wget.download(url,foto)
    api.photo_upload(foto,caption=frase)

def upload_storia(url='https://i.pinimg.com/originals/79/1f/ca/791fca6132c5c51e1bac62a78dfac848.jpg',frase=''):
    path='./cat/'
    foto=path+'cat.jpg'
    try:os.remove(foto)
    except:pass
    time.sleep(2)
    wget.download(url,foto)
    api.photo_upload_to_story(foto,'')

def interagisci_hashtag(nome):
    print("Interagendo con hashtag: ",nome)
    medias=api.hashtag_medias_recent(nome,amount=15)
    print("Found ",len(medias)," medias")
    for m in medias:
        print("Liked hashpost ",m.id)
        api.media_like(m.id)
        time.sleep(random.randint(1,39)/10)
        api.media_comment(m.id,text=random.choice(comments))
        time.sleep(random.randint(10,90)/10)
    print("YAY!")

def manage_direct():
    threads=api.direct_threads(amount=99)
    for t in threads:
        message=(api.direct_messages(t.id,1))[0]
        userid=message.user_id
        if userid != api.user_id_from_username(user_name):
            print(api.username_from_user_id(userid)," says ",message.text)
            api.direct_answer(t.id,answer(message.text)) #"non so ancora risponderti, sono solo un gatto!"
    return

def answer(messaggio):
    return str(chatbot.pio.get_response(messaggio)).lower()


if __name__ == '__main__':
    blogin()
    time.sleep(10)
    print("loop start")
    while True:
        try:
            ### manage direct ###
            manage_direct()
            ### manage followers ###
            if (datetime.now().hour)%4==0 and datetime.now().minute==00:
                followers=manage_followers()
            ### like followers ###
                for f in followers: like_inquietanti(f)
            ### scheduled ###
            if datetime.now().hour==18 and datetime.now().minute==00:
                upload_foto('https://i.pinimg.com/originals/79/1f/ca/791fca6132c5c51e1bac62a78dfac848.jpg','miao')
                upload_storia('https://i.pinimg.com/originals/79/1f/ca/791fca6132c5c51e1bac62a78dfac848.jpg')
                interagisci_hashtag(random.choice(hashtags))
            if datetime.now().hour==23 and datetime.now().minute==00:
                unfollow_infami()
            time.sleep(1)
        except Exception as e: 
            print(e)
            os.remove(path_file)
            time.sleep(2)
            blogin()
            continue
