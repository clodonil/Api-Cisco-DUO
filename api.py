import duo_client
import pprint


def connect(ikey, skey, host):
  try:
    print("############## CONECTANDO NO DUO ###############")
    admin_api = duo_client.Admin(ikey=ikey, skey=skey , host=host)
    return admin_api
  except error:
    print("############# ERROR NA CONEXAO")
    print(error)
    return False

def create_user(admin_api,username, realname):
  try:
    print("############## CRIANDO USUARIO ###############")  
    user = admin_api.add_user(
        username=username, 
        realname=realname,        
        alias1=f'itau\{username}',
        status = 'active'
        )
    #pprint.pprint(user)
    return user
  except RuntimeError as e:
    print("############# ERROR NA CRIACAO DO USUARIO")  
    print(e)
    return False

def create_phone(admin_api, number):
  try:
    print("############## CRIANDO PHONE ###############")    
    phone = admin_api.add_phone(number=number,type='mobile',platform='generic smartphone')
    #pprint.pprint(phone)
    return phone
  except RuntimeError as e:
    print("############# ERROR NA CRIACAO DO PHONE #############")    
    print(e)  

def add_user_phone(admin_api, user, phone):
  try:
    print("############## ADD USER NO PHONE ##########")
    admin_api.add_user_phone(user_id=user['user_id'],phone_id=phone['phone_id']) 
    return True
  except RuntimeError as e:
    print("############# ERROR ADD USER NO PHONE #############")      
    print(e)
    return False

def add_user_group(admin_api,user, group_id):
    try:
      print("############# ADICINANDO O USUARIO NO GROUP ################")
      admin_api.add_user_group(user['user_id'], group_id)
      return True
    except RuntimeError as e:
      print("############# ERRO AO ADICIONAR USUARIO NO GROUP #############")        
      print(e)
      return False
      
    

def send_sms(admin_api, phone):
  try:
    print("############# SEND SMS ################")      
    act_sent = admin_api.send_sms_activation_to_phone(phone_id=phone['phone_id'],install='1')
    print('SMS activation sent to', phone['number'] + ':')
    return True
  except RuntimeError as e:
    print("############# ERRO NO SEND SMS #############")        
    print(e)
    return False


ikey=""
skey=""
host=""
GROUP_ID = ''


for users in lista:
    username = users[0].lower()
    nome = users[1].title()
    phone = users[2]
    print("########## CRIANDO MFA: {0}".format(nome))
    conn = connect(ikey, skey, host)
    try:
      if conn:
         user =  create_user(conn,username, nome)     
         if user:
            group = add_user_group(conn, user, GROUP_ID) 
            obj_phone = create_phone(conn, phone)
            if obj_phone:
               if add_user_phone(conn,user,obj_phone):
                  send_sms(conn,obj_phone) 
    except RuntimeError as e:
      print("############# ERRO NO MFA #############")        
      print(e)
        
   

