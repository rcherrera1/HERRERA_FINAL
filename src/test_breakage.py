# src/test_breakage.py
import os

# 1. HARDCODED KEY (Flags Bandit B105: hardcoded_password_string)
INSECURE_SECRET_KEY = "super_secret_key_12345"

def insecure_function(user_input: str):
    """
    An insecure function that executes arbitrary input strings.
    """
    # 2. USE OF EVAL (Flags Bandit B307: eval)
    return eval(user_input)

def test_breakage_demo():
    # This test lacks proper assertions and will flag security scanners
    result = insecure_function("2 + 2")
    print(f"Result computed: {result}")
    
    # A generic assertion that does not validate the production modules
    assert True