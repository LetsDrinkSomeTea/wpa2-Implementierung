import wpa2lib


def hexdump_bytes(b):
    print("     " + " ".join("{:2x}".format(c)
                             for c in range(min(16, len(b)))))
    for i in range(0, len(b), 16):
        print("{:2x}x  ".format(int(i / 16)) + " ".join(
            "{:02x}".format(c) for c in b[i:i + 16]), end="")
        print("   " + "".join(chr(c) if 32 <= c <= 126 else "."
                              for c in b[i:i + 16]))
    print("                                 "
          "{:3} bytes {:4} bits".format(len(b), len(b) * 8))


def check():
    psk = "12345678"
    ssid = "Harkonen"
    a_nonce = b"\x22\x58\x54\xb0\x44\x4d\xe3\xaf\x06\xd1\x49\x2b\x85\x29\x84\xf0" \
              b"\x4c\xf6\x27\x4c\x0e\x32\x18\xb8\x68\x17\x56\x86\x4d\xb7\xa0\x55"
    s_nonce = b"\x59\x16\x8b\xc3\xa5\xdf\x18\xd7\x1e\xfb\x64\x23\xf3\x40\x08\x8d" \
              b"\xab\x9e\x1b\xa2\xbb\xc5\x86\x59\xe0\x7b\x37\x64\xb0\xde\x85\x70"
    a_mac = b"\x00\x14\x6c\x7e\x40\x80"
    s_mac = b"\x00\x13\x46\xfe\x32\x0c"
    mic = b"\xd5\x35\x53\x82\xb8\xa9\xb8\x06\xdc\xaf\x99\xcd\xaf\x56\x4e\xb6"
    data = b"\x01\x03\x00\x75\x02\x01\x0a\x00\x10\x00\x00\x00\x00\x00\x00\x00" \
           b"\x01\x59\x16\x8b\xc3\xa5\xdf\x18\xd7\x1e\xfb\x64\x23\xf3\x40\x08" \
           b"\x8d\xab\x9e\x1b\xa2\xbb\xc5\x86\x59\xe0\x7b\x37\x64\xb0\xde\x85" \
           b"\x70\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
           b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
           b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
           b"\x00\x00\x16\x30\x14\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac" \
           b"\x04\x01\x00\x00\x0f\xac\x02\x01\x00"

    psk = psk.encode("utf-8")
    ssid = ssid.encode("utf-8")

    pmk = wpa2lib.psk_to_pmk(psk, ssid)
    ptk = wpa2lib.prf_384(pmk, *wpa2lib.make_ab(a_nonce, s_nonce, a_mac, s_mac))
    print("PSK:")
    hexdump_bytes(psk)
    print("PMK:")
    hexdump_bytes(pmk)
    print("PTK:")
    hexdump_bytes(ptk)
    print("MIC:")
    hexdump_bytes(mic)
    calc_mic = wpa2lib.make_mic(ptk, data)
    print("CALC_MIC:")
    hexdump_bytes(calc_mic)
    print("Match" if mic == calc_mic else "Missmatch")


def main():
    passwords = ["Hallo123", "12345678", "Passwort", "1234567890"]

    ssid = "Harkonen".encode("utf-8")
    a_nonce = b"\x22\x58\x54\xb0\x44\x4d\xe3\xaf\x06\xd1\x49\x2b\x85\x29\x84\xf0" \
              b"\x4c\xf6\x27\x4c\x0e\x32\x18\xb8\x68\x17\x56\x86\x4d\xb7\xa0\x55"
    s_nonce = b"\x59\x16\x8b\xc3\xa5\xdf\x18\xd7\x1e\xfb\x64\x23\xf3\x40\x08\x8d" \
              b"\xab\x9e\x1b\xa2\xbb\xc5\x86\x59\xe0\x7b\x37\x64\xb0\xde\x85\x70"
    a_mac = b"\x00\x14\x6c\x7e\x40\x80"
    s_mac = b"\x00\x13\x46\xfe\x32\x0c"
    mic = b"\xd5\x35\x53\x82\xb8\xa9\xb8\x06\xdc\xaf\x99\xcd\xaf\x56\x4e\xb6"
    data = b"\x01\x03\x00\x75\x02\x01\x0a\x00\x10\x00\x00\x00\x00\x00\x00\x00" \
           b"\x01\x59\x16\x8b\xc3\xa5\xdf\x18\xd7\x1e\xfb\x64\x23\xf3\x40\x08" \
           b"\x8d\xab\x9e\x1b\xa2\xbb\xc5\x86\x59\xe0\x7b\x37\x64\xb0\xde\x85" \
           b"\x70\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
           b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
           b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
           b"\x00\x00\x16\x30\x14\x01\x00\x00\x0f\xac\x04\x01\x00\x00\x0f\xac" \
           b"\x04\x01\x00\x00\x0f\xac\x02\x01\x00"

    validator = wpa2lib.WPA2Validator(ssid, a_nonce, s_nonce, a_mac, s_mac, data, mic)
    for p in passwords:
        print("Testing password: " + p)
        print(validator.validate(p))


if __name__ == "__main__":
    main()
