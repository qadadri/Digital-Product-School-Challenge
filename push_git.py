import pyotp

totp = pyotp.TOTP({
  'key': "q.haytam@gmail.comDPSCHALLENGE",
  'T0': '0',
  'X': '120',
  'algorithm': 'HMAC-SHA-512',
  'digits':'100'
})

print(totp)