import requests
API_KEY_GOOGLE = 'AIzaSyCYK8VNsmIZQ2vcOieEVc4pm0AjS9k0GYQ'
SERCH_ENGINE_ID = '31a7b0acb015c4a18'
query ="python"
page =1
language = 'lang_es'

#construct the URL for the search
URL=f"https://www.googleapis.com/customsearch/v1?key={API_KEY_GOOGLE}&cx={SERCH_ENGINE_ID}&q={query}$start={page}&lr={language}"

data=requests.get(URL).json()
results = data.get('items')

for r in results:
    print('-----NUEVO RESULTADO-----')
    print(r.get('title'))
    print(r.get('link'))
    print(r.get('snippet'))
    print('-------------------')
    print('\n\n')