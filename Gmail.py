"""
    RFC822 es un protocolo de acceso a mensajes de internet

    Posiciones de interes del array "original":
        Delivered-To
        Received
        Message-ID
        Date
        Subject
        From
        To
        Content-Type
"""
import imaplib
import email

def read_email_from_gmail(user,password,n):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        mail.login(user,password)
    except:
        print("""
        Ha ocurrido un error de autenticación. Verifique que su correo admita accesos a aplicaciones externas
        o ingrese nuevamente sus datos""")
        return 1
    mail.list() #Listo todas las casillas
    mail.select('inbox') #Selecciono el inbox
    retcode, messages = mail.search(None,'ALL') #Recolecto todos los mensajes sin leer
    if(retcode == 'OK'):
        id_list = messages[0].split() #IDs encontrados, son bytes literales (ej. b'1')
        latest_emails = id_list[-n:]
        for num in latest_emails: 
            typ, data = mail.fetch(num, '(RFC822)') #Recupero el mensaje completo con formato RFC822 pasando los IDs
            for response_part in data: #Bucle que entra en la primera posicion de data
                if isinstance(response_part,tuple):
                    original = email.message_from_bytes(response_part[1]) #Parseo la respuesta en bytes a 'email.message.Message'
                    print(f"\t{original['Date']}")
    mail.close()
    mail.logout()
    return 0

def set_unseen_email_from_gmail(user,password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    try:
        mail.login(user,password)
    except:
        print("""
        Ha ocurrido un error de autenticación. Verifique que su correo admita accesos a aplicaciones externas
        o ingrese nuevamente sus datos""")
        return 1
    mail.list() #Listo todas las casillas
    mail.select('inbox') #Selecciono el inbox
    retcode, messages = mail.search(None,'(UNSEEN)') #Recolecto todos los mensajes sin leer
    if(retcode == 'OK'):
        count = 0
        id_list = messages[0].split() #IDs encontrados, son bytes literales (ej. b'1')
        for num in id_list: 
            typ, data = mail.fetch(num, '(RFC822)') #Recupero el mensaje completo con formato RFC822 pasando los IDs
            for response_part in data: #Bucle que entra en la primera posicion de data
                if isinstance(response_part,tuple):
                    original = email.message_from_bytes(response_part[1]) #Parseo la respuesta en bytes a 'email.message.Message'
                    mail.store(num,'+FLAGS','\\Seen') #Marco como leidos todos los mensajes que cumplan el condicional
                    print("\n\tMarcado como LEIDO")
                    count += 1
    print(f"\n\t{count} correos fueron marcados como 'LEIDO'")

    mail.close()
    mail.logout()
    return 0

error = 1
while( True ):
    if error:
        user = input("Correo electronico: ")
        passwd = input("Password: ")
    opc = int(input("""
        Que desea realizar?:
        1. Mostrar la fecha de los ultimos (n) correos
        2. Marcar todos los correos como leidos
        3. Salir
        
        Opcion: """))
    if opc == 1:
        n = int(input("\n\tCuantos correos desea visualizar?: "))
        error = read_email_from_gmail(user,passwd,n)
    elif opc == 2:
        error = set_unseen_email_from_gmail(user,passwd)
    elif opc == 3:
        break
    else:
        continue