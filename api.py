import duo_client
import pprint


def connect(ikey, skey, host):
  try:
    print(" CONECTANDO NO DUO ".center(50, '#'))
    admin_api = duo_client.Admin(ikey=ikey, skey=skey , host=host)
    return admin_api
  except error:
    print(" ERRO NA CONEXAO ".center(50, '#'))
    print(error)
    return False

def pesquisa_user(admin_api, username):
  try:
    print(" PESQUISANDO USUARIO ".center(50, "#"))
    s_user = admin_api.get_users_by_name(username)
    user = s_user[0]
    if user:
       username  = user['username']
       print(f' USUARIO: {username} JA EXISTE'.center(50, "#"))
       return user
    else:
       print(f' USUARIO: {username} NAO EXISTE'.center(50, "#"))  
       return False
  except RuntimeError as e:
    print(" ERRO NA PESQUISA DO USUARIO ".center(50, '#'))  
    raise


def create_user(admin_api,username, realname):
  try:
    print(" CRIANDO USUARIO ".center(50, '#'))  
    user = admin_api.add_user(
        username=username, 
        realname=realname,        
        alias1=username,
        status = 'active'
        )

    return user
  except RuntimeError as e:
    print(" ERRO NA CRIACAO DO USUARIO ".center(50, '#'))  
    raise

def create_phone(admin_api, number):
  try:
    print(" CRIANDO PHONE ".center(50, '#'))    
    phone = admin_api.add_phone(number=number,type='mobile',platform='generic smartphone')
    return phone
  except RuntimeError as e:
    print(" ERRO NA CRIACAO DO PHONE ".center(50, '#'))    
    raise  
     
def add_user_phone(admin_api, user, phone):
  try:
    print(" ADD USER NO PHONE ".center(50, '#'))
    admin_api.add_user_phone(user_id=user['user_id'],phone_id=phone['phone_id']) 
    return True
  except RuntimeError as e:
    print(" ERRO ADD USER NO PHONE ".center(50, '#'))      
    raise

def add_user_group(admin_api,user, group_id):
    try:
      print(" ADICINANDO O USUARIO NO GROUP ".center(50, '#'))
      admin_api.add_user_group(user['user_id'], group_id)
      return True
    except RuntimeError as e:
      print(" ERRO AO ADICIONAR USUARIO NO GROUP ".center(50, '#'))        
      raise      
    
def send_sms(admin_api, phone):
  try:
    print(" SEND SMS ".center(50, '#'))      
    act_sent = admin_api.send_sms_activation_to_phone(phone_id=phone['phone_id'],install='1')
    print('SMS activation sent to', phone['number'] + ':')
    return True
  except RuntimeError as e:
    print(" ERRO NO SEND SMS ".center(50, '#'))        
    raise


ikey=""
skey=""
host="
GROUP_ID = ''


lista = [
          ['clodonil','Clodonil Honorio Trigo', '+55-11-xxxxxxx']
        ]


for users in lista:
    username = users[0].lower()
    nome = users[1].title()
    phone = users[2]
    banner = " CRIANDO MFA: {0} ".format(nome)
    print(banner.center(50,"#"))
    conn = connect(ikey, skey, host)
    try:
      if conn:
         user = pesquisa_user(conn, username)
         if not user:
            user =  create_user(conn,username, nome)     
            if user:
              group = add_user_group(conn, user, GROUP_ID) 
              obj_phone = create_phone(conn, phone)
              if obj_phone:
                 if add_user_phone(conn,user,obj_phone):
                    send_sms(conn,obj_phone)
         else:
           obj_phone = user['phones'][0]
           send_sms(conn,obj_phone)           
    except RuntimeError as e:
      print(" ERRO NO MFA ".center(50,'#'))        
      print(e)