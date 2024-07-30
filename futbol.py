import random

# dışarıdan sağlanan verilerdir
# her iki takımın da aynı strateji ve mevkiler ile oynadığını varsayalım
ortak_mevkiler = ["Kaleci", "Defans", "Sağ Bek", "Stoper", "Sol Bek", "Orta Saha", "Defansif", "Ofansif", "Forvet", "Forvet", "Forvet"]
oyuncular_FB = ["Bedirhan", "Selim", "Sukru", "Mehmet", "Selçuk", "Ahmet", "Veli", "Kağan", "Oğuzhan", "Mert", "Sitki"]
oyuncular_GS = ["Muhammed", "İcardi", "İsa", "Deniz", "Melis", "Merkez", "İbrahim", "Cevat", "Simge", "Ebru", "Sena"]
tum_oyuncu_isimleri = [oyuncular_FB, oyuncular_GS]
tum_takim_isimleri = ["İngiltere","Hollanda"]
normal_devre_suresi = 45
uzatma_devre_suresi = 15
olaylar = ["Yok","Sarı Kart", "Kırmızı Kart", "Gol"]
olay_agirliklari = [10, 0, 0, 0] 
penalti_olaylari = ["Gol","Gol Değil"]  

class Takim:
    def __init__(self, id, isim, oyuncular):
        self.id = id
        self.isim = isim
        self.oyuncular = oyuncular
        self.kalan_oyuncu_sayisi = 11
        self.atilan_gol = 0
    
    def oyuncu_cikar(self, oyuncu):
        self.oyuncular.remove(oyuncu)
        
class Oyuncu:
    def __init__(self, id, isim, mevki):
        self.id = id
        self.isim = isim
        self.mevki = mevki
        self.cezalar = [] # sarı kart veya kırmızı kart, bir sonraki aşamada kaçıncı dakikada aldığını da tutabiliriz
        self.atilan_gol = 0
        
class Futbol_Maci:
    def TakimlariOlustur(self):
        self.takimlar = []
        for t in range(2): # t o anda oluşturulan takımın indeksini ifade eder 
            oyuncular = []
            for o in range(11): # o anda oluşturulan oyuncunun indeksini ifade eder
                oyuncu = Oyuncu(o, tum_oyuncu_isimleri[t][o],mevki = ortak_mevkiler[o])
                oyuncular.append(oyuncu)
            takim = Takim(t, tum_takim_isimleri[t], oyuncular)
            self.takimlar.append(takim)

    def takim_kadrosunu_goster(self, id): # id nolu takımın kadrosunu gösterir
        print("Takimin İsmi: ",self.takimlar[id].isim)
        for o in self.takimlar[id].oyuncular:
            print(f"oyuncu: {o.isim} (mevki: {o.mevki})")
        
    def tum_takim_kadrolarini_goster(self):
        for t in range(2):
            self.takim_kadrosunu_goster(t)
            
    def olay_olustur(self):
        self.olay = random.choices(olaylar, weights=olay_agirliklari)[0]
        takim = random.choice(self.takimlar) # iki takımdan birini seçeceğiz.
        oyuncu = random.choice(takim.oyuncular) # üst satırda seçilen takımdan oyuncularından birini seçtik.
        return takim, self.olay, oyuncu
    
    def gol_say(self,takim,oyuncu):
        takim.atilan_gol += 1
        oyuncu.atilan_gol += 1

    def penalti_atislari(self):
        for p in range(5): # p penaltı atışlarını simgeler en fazla 5 er tane penaltı atışı olacak
            # kalan penaltı sayısı takımların attıkları gol farklarına eşit veya büyükse ilk takım penaltı atabilir
            if self.penalti_at(p,0,[0,3]) == False:
                print(f"{self.takimlar[0].isim} takımının geriye kalan penaltıları atmasına gerek kalmadı", p)
                break
            if self.penalti_at(p,1,[0,6]) == False:
                print(f"{self.takimlar[1].isim} takımının geriye kalan penaltıları atmasına gerek kalmadı", p)
                break
            
    # penaltı_at fonksiyonu atma hakkım varsa penaltı attırıp True döndürür yoksa penaltı atılmadan False döndürür
    def penalti_at(self, p, t,penalti_olay_agirliklari):
        
        if 5 - p >= abs(self.takimlar[0].atilan_gol - self.takimlar[1].atilan_gol): 
            return self.tek_penalti_at(p, t, penalti_olay_agirliklari)
          #  return True
        else:
            return False
    # penaltı atma olayını simüle eder
    # p => kaçıncı penaltı atışı olduğunu ifade eder.
    # t => hangi takımın penaltı kullandıgını belirtir t 0 yada 1 olabilir
    # penalti_olay_agirliklari => bir takımın penaltıyı gole cevrilebilme yada kaçırma olasılıgıdır 2 elemanlı bir listedir
    # Penaltı atacak oyuncu kalmadığında maç bitmesi için fonksiyon false döner, oyuncu var ise, True döner.
    def tek_penalti_at(self, p, t, penalti_olay_agirliklari):
        penalti_olayi = random.choices(penalti_olaylari, weights=penalti_olay_agirliklari)[0]
        if len(self.takimlar[0].oyuncular) == 0 or len(self.takimlar[1].oyuncular) == 0:
            print("Penaltı atacak oyuncu kalmadığından maç berabere sonuçlandı.")
            return False
        secilen_oyuncu = random.choice(self.takimlar[t].oyuncular)
        if penalti_olayi == "Gol": 
            self.gol_say(self.takimlar[t],secilen_oyuncu)
            #self.takimlar[t].atilan_gol += 1
            print(f"{self.takimlar[t].isim} takımından {secilen_oyuncu.isim} penaltıyı {p + 1}. atışta  gole çevirdi.")
        else:
            print(f"{self.takimlar[t].isim} takımından {secilen_oyuncu.isim} {p + 1}. atışta penaltıyı kaçırdı.")
        self.skor_yaz()
        self.takimlar[t].oyuncu_cikar(secilen_oyuncu)   
        print(f"{self.takimlar[t].isim} takımında kalan oyuncu sayısı : {len(self.takimlar[t].oyuncular)}")     
        return True
    def skor_yaz(self):
        print(f"{self.takimlar[0].isim}: {self.takimlar[0].atilan_gol} - {self.takimlar[1].isim}: {self.takimlar[1].atilan_gol}")
    def maciSimuleEt(self):
        self.iki_devre_oynat(45)
        if self.takimlar[0].atilan_gol==self.takimlar[1].atilan_gol:
            print("Maç Berabere!")
            self.iki_devre_oynat(15) 
        if self.takimlar[0].atilan_gol==self.takimlar[1].atilan_gol:
            print("Uzatmalarda da berabere kalındı.")
            self.penalti_atislari()
        if self.takimlar[0].atilan_gol==self.takimlar[1].atilan_gol:
            print("Penaltı atışlarında da berabere kalındı.")
            self.seri_penalti_atislari()
        print("Maç Sonucu:")
        for t in self.takimlar:
            print(t.isim, t.atilan_gol)

    def seri_penalti_atislari(self):
        s = 0
        while self.takimlar[0].atilan_gol==self.takimlar[1].atilan_gol:
            if not (self.tek_penalti_at(s, 0, [0, 3]) and self.tek_penalti_at(s, 1, [0, 5])):
                break
            s += 1
            # if len(self.takimlar[0].oyuncular) == 0 or len(self.takimlar[1].oyuncular) == 0:
            #     print("Penaltı atacak oyuncu kalmadığından maç berabere sonuçlandı.")
            #     break
            # Kontrolü tek penaltı at içinde yapmak yerine, penaltıların akışını kontrol eden bu fonksiyonda yapmak daha okunur bir kod sağlar.
    def iki_devre_oynat(self, sure):
        for i in range(2): # iki devremiz var, ilk devrede i = 0, ikinci devrede i = 1
            if sure<45: # sure = 15, yani 45'ten küçükse bu devre uzatma devresidir.
                print(f"{i + 1}. Uzatma Devresi Başladı")  
            else: # sure = 45, yani 45'ten küçük değilse bu devre normal devredir...
                print(f"{i + 1}. Devre Başladı")
            for dakika in range(1, sure + 1):
                self.mac_olayi(i * sure + dakika)
            if sure < 45:
                print(f"{i + 1}. Uzatma Devresi Sonucu")  
            else: 
                print(f"{i + 1}. Devre Sonucu")
            for t in self.takimlar:
                print(t.isim, t.atilan_gol)
                    
    def mac_olayi(self,dakika):
        takim, olay, oyuncu = self.olay_olustur()   
        if olay == "Gol":
            self.gol_say(takim, oyuncu)
            print(f"{takim.isim} {dakika}. dakikada 1 gol attı.")
            print(f"{oyuncu.isim} {dakika}. dakikada 1 gol attı.")
        elif olay == "Kırmızı Kart":
            takim.oyuncu_cikar(oyuncu)
            print(oyuncu.isim, " doğrudan Kırmızı Kart gördü ve oyundan çıkartıldı.")
        elif olay == "Sarı Kart":
            oyuncu.cezalar.append("Sarı Kart")
            print(f"{dakika}. dakikada: {oyuncu.isim} ({takim.isim}) Sarı Kart gördü.")
            if len(oyuncu.cezalar) == 2: # ceza doğrudan kırmızı kart ise üst satırlarda oyuncu zaten hemen maçtan atılıyor 
                                         # kırmızı kart durumu yukarıda öndeden değerlendirildiğinden ikinci ceza alınmışsa
                                         # bu cezanın da sarı kart olması ve iki sarı kart ile oyuncunun atılması durumudur  
                takim.oyuncu_cikar(oyuncu)
                print(oyuncu.isim," ikinci Sarı Kart görerek oyundan çıkartıldı.")
        
mac = Futbol_Maci()
mac.TakimlariOlustur()
mac.tum_takim_kadrolarini_goster()
mac.maciSimuleEt()