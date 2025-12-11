import bcrypt

# 1. Scrivi qui le password dei tuoi amici
passwords_in_chiaro = ['passwordDiAlby', 'passwordDiEma', 'passwordDiVale', 'passwordDiAle', 'tuaPassword']

print("--- COPIA I CODICI QUI SOTTO NEL TUO FILE APP.PY ---")

for password in passwords_in_chiaro:
    # Trasforma la password in bit
    password_bytes = password.encode('utf-8')
    # Genera il "sale" (serve per la sicurezza)
    salt = bcrypt.gensalt()
    # Crea l'hash finale
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Stampa il risultato leggibile
    print(f"Password '{password}' diventa: {hashed.decode('utf-8')}")