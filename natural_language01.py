try:
    f = open("nihongo3.txt", "rb")
except IOError:
    print("404 Not Found.")
    exit()

f.seek(0, 2)
length = f.tell()
f.seek(0)
print(length)

buf = f.read(length)
f.close()

# ISO-2022-JPの判定
is_iso_2022_jp = False
for i in range(length):
    if buf[i] == 0x1b:
        print("It's ISO-2022-JP.")
        is_iso_2022_jp = True
        break  # ISO-2022-JPが見つかったらループを終了

# 以下追記

if not is_iso_2022_jp:  # ISO-2022-JPでなかった場合のみ次の処理を行う
  
    # Shift-JISの判定
    def is_shift_jis(buf, length):
        i = 0
        while i < length:
            byte = buf[i]
            if (0x81 <= byte <= 0x9F) or (0xE0 <= byte <= 0xEF):  # JIS X 0208範囲
                if i + 1 >= length or not ((0x40 <= buf[i + 1] <= 0x7E) or (0x80 <= buf[i + 1] <= 0xFC)):
                    return False
                i += 2
            elif byte < 0x80:  # ASCII範囲
                i += 1
            else:
                return False
        return True
    # EUC-JPの判定
    def is_euc_jp(buf, length):
        i = 0
        while i < length:
            byte = buf[i]
            if 0xA1 <= byte <= 0xFE:  # JIS X 0208範囲
                if i + 1 >= length or not (0xA1 <= buf[i + 1] <= 0xFE):
                    return False
                i += 2
            elif byte < 0x80:  # ASCII範囲
                i += 1
            else:
                return False
        return True

    # 文字コードの判定
    if is_euc_jp(buf, length):
        print("It's EUC-JP.")
    elif is_shift_jis(buf, length):
        print("It's Shift_JIS.")
    else:
        print("It's unknown.")
