import requests
import json
from config import SETUP_KEY, CHAT_KEY



def writer(confi):
    url = "https://api.openai.com/v1/chat/completions"
    key = SETUP_KEY+CHAT_KEY

    payload = json.dumps({
    "model": "gpt-4-turbo",
    "messages": [
        {
        "role": "user",
        "content": "My company builds the following meeting room pods with the following max occupancies:\nBOW One	1\nBOW Two	1\nBOW Four	4\nBOW Six	6\nBOW Nine	6\nBOW Twelve	8\nWe have built a program that suggests changes to their configuration. When I send you the changes we suggest, write a 1 paragraph explanation for why we suggest this. Be definite."
        },
        {
        "role": "assistant",
        "content": "Of course! Whenever you're ready, just send me the details of the suggested changes, and I'll provide you with a concise explanation tailored to those specific suggestions."
        },
        {
        "role": "user",
        "content": "('BowTwo', -2)\n('BowFour', -1)\n('BowSix', +1)"
        },
        {
        "role": "assistant",
        "content": "Based on the suggested changes to the meeting room pods configuration, it seems the recommendation is to reduce two 'BOW Two' pods and one 'BOW Four' pod while adding an additional 'BOW Six' pod. This adjustment could be driven by the observed demand and usage patterns, indicating a higher need for medium-sized meeting spaces compared to smaller ones. By reducing the number of 'BOW Two' and 'BOW Four' pods, which cater to individuals or smaller groups, and increasing the 'BOW Six' pods, the configuration better aligns with the requirement for spaces that accommodate larger groups or teams. This reconfiguration optimizes the use of available space, catering to the evolving needs of the workspace and ensuring that the facilities are more effectively utilized to meet group meeting demands."
        },
        {
        "role": "user",
        "content": "Not bad, but I said be definite. So no 'seems', 'could' etc. Also, never use the word pods, only spaces. Try again."
        },
        {
        "role": "assistant",
        "content": "The suggested changes to the spaces configuration, specifically decreasing the number of 'BOW Two' spaces by two and 'BOW Four' spaces by one while increasing the 'BOW Six' spaces by one, are a strategic response to the clear demand for larger meeting spaces. By reallocating resources from smaller spaces designed for individuals or small groups to a larger 'BOW Six' space, the adjustment directly addresses the need for spaces that accommodate medium-sized teams. This decision ensures that the workspace is more effectively utilized, enhancing collaboration and efficiency by providing adequately sized meeting environments that match the current utilization trends and requirements of the users."
        },
        {
        "role": "user",
        "content": confi
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '+key
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return response.json()
