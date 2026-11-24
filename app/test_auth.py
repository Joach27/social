# test_auth.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.auth import get_password_hash, verify_password

password = "test123"
hashed = get_password_hash(password)
print(f"Mot de passe: {password}")
print(f"Hash: {hashed}")
print(f"Vérification réussie: {verify_password(password, hashed)}")
print(f"Vérification échouée: {verify_password('wrong', hashed)}")