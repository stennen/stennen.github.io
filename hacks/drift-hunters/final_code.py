#   This code was created by:
#
#   STENNEN (C), Copyright 2016.
#
#   This file might not be distributed in someone elses name!

import winreg

print("Info: This program was created by STENNEN.")
print("Warning: This program can run while Drift Hunters is still open!\n")

def collect_vals():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\studionum43\Drift Hunters', 0, winreg.KEY_READ)
    result = ""

    for i in range(0, winreg.QueryInfoKey(key)[1]):
        val = winreg.EnumValue(key, i)
        name, val, typ = val
        result += "%s %s\n" % (name, val)

    winreg.CloseKey(key)
    return result

def get_changed_keys():
    with open("before_run.txt", "r") as f:
        bef = f.readlines()
    with open("after_run.txt", "r") as f:
        after = f.readlines()

    bef_dc = {}
    after_dc = {}

    for b in bef:
        bef_dc[b.split()[0]] = b.split()[1]

    for b in after:
        after_dc[b.split()[0]] = b.split()[1]

    for key, val in after_dc.items():
        if key in bef_dc:
            if val != bef_dc[key]:
                print("Changed key", key, "from", bef_dc[key], "to", val)
        else:
            print("New key", key, "created with value", val)

encode_table = {
    'A': '(', 'B': 'w', 'C': 'u', 'D': 'a', 'E': 'p', 'F': 'o', 'G': 'z',
    'H': 'i', 'I': 'h', 'J': 's', 'K': 'e', 'L': 'n', 'M': 'l', 'N': 'd',
    'O': 'r', 'P': 't', 'Q': 'y', 'R': 'f', 'S': 'x', 'T': '4', 'U': 'q',
    'V': 'b', 'W': '{', 'X': '.', 'Y': ';', 'Z': ']', '0': '>', '1': 'm',
    '2': '?', '3': '0', '4': ':', '5': '}', '6': ',', '7': '+', '8': '-',
    '9': '<', ',': ')', '|': '[', '_': '=', '{': '1', '}': '7', '-': '*',
    '.': '^'
}

decode_table = {val: key for key,val in encode_table.items()}

def drifthunters_decrypt(s):
    res = ''
    for c in s:
        if c == '\x00':
            return res
        res += decode_table[c]
    return res

def drifthunters_encrypt(s):
    res = ''
    for c in s:
        res += encode_table[c]

    return res + '\x00'

def get_encrypted_valuekey(val):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\studionum43\Drift Hunters', 0, winreg.KEY_READ)
    enc_val = drifthunters_encrypt(val)[:-1] # exclude null terminator

    for i in range(0, winreg.QueryInfoKey(key)[1]):
        val = winreg.EnumValue(key, i)
        name, val, typ = val
        if name.startswith(enc_val + '_'):
            winreg.CloseKey(key)
            return drifthunters_decrypt(val.decode('ascii'))

    winreg.CloseKey(key)

def set_encrypted_valuekey_val(keyname, val):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\studionum43\Drift Hunters', 0, winreg.KEY_READ | winreg.KEY_WRITE)
    enc_val = drifthunters_encrypt(keyname)[:-1] # exclude null terminator

    for i in range(0, winreg.QueryInfoKey(key)[1]):
        v = winreg.EnumValue(key, i)
        name, _, typ = v
        if name.startswith(enc_val + '_'):
            winreg.SetValueEx(key, name, 0, typ, drifthunters_encrypt(str(val)).encode())
            winreg.CloseKey(key)
            return
            

    winreg.CloseKey(key)
    raise FileNotFoundError

money_cur = int(get_encrypted_valuekey("PLAYERMONEY"))

print("Current money count:", money_cur)
wanted_money = int(input("Wanted money: "))

set_encrypted_valuekey_val("PLAYERMONEY", wanted_money)

print("New money count:", wanted_money)
print("Verified new money count:", get_encrypted_valuekey("PLAYERMONEY"))