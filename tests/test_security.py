from app.security import create_access_token, decode_access_token, hash_password, verify_password

def test_password_hashing():
    hashed = hash_password("correct-horse-battery")
    assert hashed != "correct-horse-battery"
    assert verify_password("correct-horse-battery", hashed)
    assert not verify_password("wrong-password", hashed)

def test_jwt_round_trip():
    token = create_access_token("42")
    assert decode_access_token(token)["sub"] == "42"
