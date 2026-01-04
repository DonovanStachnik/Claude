"""
Setup Kalshi Credentials
Stores Key ID and RSA Private Key
"""

import os

# Your Kalshi credentials
KEY_ID = "c76cce95-da33-424c-835b-f2f838c92217"

PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAre/vypVeHx+AOQI+daXX8XNr3KkTeecLg+jzO45UBEWau4Gx
XXA9t5Pp2ZmLeE1NQ6LJ941Ycl+qz6TzuztMM4Hh/ZeluPRXRjyTyfmRW+Oys2sQ
lVcu1HVTgIbxGAfju/qxGzBaGACG7cL2ka4cBMtjYV/Fuo2ztQV+hCJDSXTbIZxS
4ef4AZhSHMB18JJICx0Z0EOBv85hkYC5Z/3GiVg47kcBIGIdIBsA4DwaQ/5f1sMB
msR5doUYa/gPM+weWRWeGNMq2Ng5qpgfCz6H8vNfJ2NdpgnWycuAFfUQBLBks3X5
mO+8pyOcgPuSlgvGiwN2PFNiMfWl0YWX0vingQIDAQABAoIBAFKDM7RdNli6V1fz
/hBOe8nhUMZNeN1H4xkQ/a3/f1DFejlANZUXZVe8dd+RrO2FckVHKNtkNJSRWJUH
cc4cu7HliAEGmwnJ88rwesWCPFgkhMYDYMsPoDoObG3Y1e9p8rlem/zDa8HeIiQR
bGnAeC84Eu2DAuhUR29060cgf94Mpoov7pcXnIAFBV0+ZgBMMGUsO4dDFbbpch4d
gcenBy+ADLZgAIzLR+m2E7Z+ftZmYX6kAQbeKcqGpb+vH99AFGty29FGCqxRZMUX
Hge1PuzkQcpdw/EePO/lci9M0Wmco5N3kCJY2Q5jnYMWT2logxELaVcL75v4c8zv
yk9OQKcCgYEAzOiEQH38nOWBJErbw5j1Ji7V9EqUiynNuXD6nZFAeOCKSz/ogQ7H
PZMqAb7pWaNi6OlZJJkoxacdByiaGEfddH9ymm929GfrZjFYUpy3VHHK0GEgTOQv
Cnedscy9cEgjybVUCcVeQqMuWe4p+CnZqQuZIC5In6FfpjGfnj1Fz9cCgYEA2U6C
+8yhCmiSCii78GLRsK5nVCHoWSNZ4RERK5og4LtZp4V/GKj8TtMgX4t+ls5nlMbK
ZHxzLhzQP+IK+ph6yE3vhFRayu1YPd55asIN9Er4nssTD6WF6ylUXtU1XKXxCqpQ
h5wgfqUyR/UCkYUCq2DSMB+6Hb973FRIN1uNOGcCgYEAx0L5kQmzRRP94MAXM/+j
rgzvrM914lq1nzbZz653ptScR48PV6l6YUuiFu6DV9MGFX8OXAPA3WykUtjN+Pyx
w19IoBvy7ru787XasQOLWEgMNVWuJnfjsucdZ9C1C+JrQvTdk17mSiELqxJqp9Ry
wOvxbZT0tJ8mN6ScFzJ4mCMCgYEAkfNydA5HJ0d+tsYPHHAyqDkq+03e0We16T1e
S+u0I1yR5br61yRAeezBdIqrVjyBQ2KU8xLHBXSixhVbDF63MKtvsHA7nsn0l3FC
GVsGpkpoW7bHMZ4ZqQ1UNnF66qQlleU4Oyy4gncPo1bDB9vPJC3eXiYhCfPfC+er
rUqXOgcCgYBDuDu1Kp5su9BpHFXKSFloigWabM/JCD6NB15jMzrKeN+ZLLqxKqyx
in4IegvHj+HkqoYMivLGOhBP1ULLgLQxgLWRCKiJjOpSwV2/kvjRxZ8P3ilj1NeC
+Pccc9pQJ5uSjJBrndY7wLQPrEM+7sIygLIssu22DqBgL1RZTAFhEg==
-----END RSA PRIVATE KEY-----"""

def setup():
    """Create .env file with credentials"""

    # Format private key for .env (keep original newlines)
    private_key_formatted = PRIVATE_KEY.strip()

    env_content = f"""# Kalshi API Credentials (RSA Authentication)
KALSHI_KEY_ID={KEY_ID}
KALSHI_PRIVATE_KEY={private_key_formatted}

# Analysis Settings
MIN_EDGE_PERCENTAGE=5.0
MIN_LIQUIDITY=1000
MAX_POSITIONS=10
"""

    # Write .env
    with open('.env', 'w') as f:
        f.write(env_content)

    print("=" * 60)
    print("✓ Kalshi credentials configured!")
    print("=" * 60)
    print()
    print("Key ID:", KEY_ID)
    print("Private Key: [STORED SECURELY]")
    print()
    print("Next steps:")
    print("  1. pip install -r requirements.txt cryptography")
    print("  2. ./start.sh  (or start.bat on Windows)")
    print()
    print("Dashboard: http://localhost:5000")
    print("=" * 60)

if __name__ == "__main__":
    setup()
