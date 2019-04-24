# የሚያስፈልጉ ፓይተን ጥቅሎች 
# ከድረ-ገጽ የንባብ ጥያቄ ለማቅረብ የሚጠቅም ጥቅል
# pip install requests 
import requests
#ከድረ-ገጽ ተነቦ የመጣውን ለመተንተን የሚረዳ ጥቅል
# apt-get install python3-bs4 (sudo)
from bs4 import BeautifulSoup
#በመጨረሻ የተገኘውን በኮማ በተነጣጠለ ፋይል ለማስቀመጥ የሚረዳ ጥቅል   
import csv
#ቀኑን ሰዓቱን እና ዓመተምህረቱን ከፋይል ስማችን ጋር ለማያያዝ የሚጠቅም ጥቅል። 
import time
# የምንጽፈው ፋይል ስም ላይ ተቀጣይ ጊዜ ለማስገባት 
ጊዜ=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())

# ጠያቂ ተግባር 
def ጥያቄ_አቅርብ(አድራሻ):
    """ የመጣለትን አድራሻ ተቀብሎ ጥያቄ የሚያቀርብ ነው። የሚመልሰውም ለትንተና የተዘጋጀ ጽሑፍ ነው"""
    return ለትንተና_አዘጋጅ(requests.get(አድራሻ).text)

def ለትንተና_አዘጋጅ(አድራሻ):
    """ ከጥያቄ_አቅርብ ጋር በቅንጅት የሚሰራ ተግባር"""
    return BeautifulSoup(አድራሻ, 'lxml')

# ርዕስ የሚፈልግ ተግባር 
def ርዕስ_ፈልግ(ጽሑፍ):
    """ ከጽሑፉ ውስት ርዕስ የሚፈልግ ተግባር"""
    return ጽሑፍ.find('span', class_='most-popular-list-item__headline').text

# ደረጃ የሚፈልግ ተግባር 
def ደረጃ_ፈልግ(ዜና):
    """ደረጃ የሚፈልግ ተግባር"""
    return ዜና.find('span', class_='most-popular-list-item__rank').text

# አድራሻ ፈላጊ ተግባር 
def አድራሻ_ፈልግ(ዜና):
    """ አድራሻ ፈልጎ ተደራሽ በሆነ መልኩ የሚመልስ ተግባር """
    የዜና_አድራሻ = ዜና.find('a', class_='most-popular-list-item__link')['href']
    return f'https://www.bbc.com{የዜና_አድራሻ}'

# ቀን የሚፈልግ ተግባር 
def ቀን_ፈልግ(ዜና):
    """ቀን ፈልጎ የሚያመጣ ተግባር"""
    return ዜና.find('div', class_='date').text

# የዜናውን ጽሑፍ የሚፈልግ ተግባር 
def ዜና_ጽሑፍ(ዜና):
    """ የዜና ጽሑፉን የሚያሳይ ተግባር"""
    return ዜና.find('div', class_='story-body__inner').text


ብዙ_የተነበቡ_10 = open('./ዜና/ዜና_'+ጊዜ+'.csv', 'w')
ሲኤስቪ_ጸሐፊ = csv.writer(ብዙ_የተነበቡ_10)
ሲኤስቪ_ጸሐፊ.writerow(['ደረጃ', 'ርዕስ', 'ቀን', 'ዜና','ድረ-ገጽ'])

#፲ በጣም የተነበቡ ዜናዎች የሚገኙበት የድረ-ገጽ ጠቋሚ አድራሻ 
አድራሻ = "https://www.bbc.com/amharic/popular/read"

#ጥያቄ_አቅርብ ለሚለው ተግባር አድራሻ እንላክለት 
የተዘጋጀ_ዜና =ጥያቄ_አቅርብ(አድራሻ)
for ተነባቢ in የተዘጋጀ_ዜና.find_all('li', class_='most-popular-list-item'):
    try:
        ርዕስ=ርዕስ_ፈልግ(ተነባቢ)
        ደረጃ = ደረጃ_ፈልግ(ተነባቢ)
        ማግኛ_አድራሻ = አድራሻ_ፈልግ(ተነባቢ)
        # በማግኛ አድራሻ ላይ ያገኘነውን በመጠቀም ዜናውን እንፈልግ 
        የዜና_መነሻ = ጥያቄ_አቅርብ(ማግኛ_አድራሻ)
        ዜናው = የዜና_መነሻ.find('div', class_='story-body')
        የዜናው_ቀን = ቀን_ፈልግ(ዜናው)
        ጽሑፉ = ዜና_ጽሑፍ(ዜናው)
        #print(ርዕስ, ደረጃ, ማግኛ_አድራሻ, የዜናው_ቀን, ጽሑፉ, sep='\n')
        #print()
        ሲኤስቪ_ጸሐፊ.writerow([ደረጃ, ርዕስ, የዜናው_ቀን, ጽሑፉ, ማግኛ_አድራሻ])
    # ይሔ የሚጠቅመው ድንገት ለሚፈጠር ሳንካ ተለዋዋጮቹ እሴት እንዲያገኙ ያደርጋል። 
    except Exception as e:
        ርዕስ = None
        ደረጃ = None
        ማግኛ_አድራሻ=None
        የዜናው_ቀን=None
        ጽሑፉ=None
# ፋይሉን መዝጋት 
ብዙ_የተነበቡ_10.close() 
