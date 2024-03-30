import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate(r"E:\OtherStuff\University\SeriousMDProject\simple-firebase-project-ca464-firebase-adminsdk-l7ls2-055ab19f91.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

response = requests.get('https://edition.cnn.com/')
if response.status_code == 200:
    cnn_web_content = response.text
    print("Works")
    
    soup = BeautifulSoup(cnn_web_content, 'html.parser')
    stack_condensed_items = soup.find("div", class_="stack_condensed__items")
    headline_texts = stack_condensed_items.find_all("span", class_="container__headline-text")

    for idx, headline_text in enumerate(headline_texts):
        doc_ref = db.collection('headlines').document(f'headline_{idx}')
        doc_ref.set({
            'headline': headline_text.text.strip()
        })

else:
    print("Failed")

#Print Headlines that has the word Ukraine    
ukraine_headlines = db.collection('headlines').where('headline', '>=', 'Ukraine').get()
    
for doc in ukraine_headlines:
    print(doc.id, doc.to_dict()['headline'])
    
print("\n")

#Print everything inside the headline collection instead
all_headlines = db.collection('headlines').get()
for doc in all_headlines:
    print(doc.id, doc.to_dict()['headline'])