#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gspread
import os
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2 import service_account
from bs4 import BeautifulSoup
from urllib.request import urlopen,Request


# In[2]:


signos = ['aries','touro','gemeos','cancer','leao','virgem','libra','escorpiao','sagitario','capricornio','aquario','peixes']


# In[3]:


url = 'https://joaobidu.com.br/horoscopo/signos/previsao-'


# In[4]:


url_imagem = 'https://joaobidu.com.br/static/img/'


# In[5]:


lista_texto = {}
lista_imagem = {}
for signo in signos:
    resposta = Request(url+signo,headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(resposta,timeout=10).read()
    conteudo = BeautifulSoup(html, 'html.parser')
    imagem = conteudo.p.img.get('src').replace('../static/img/','')
    texto = conteudo.p.get_text()
    lista_texto[signo] = texto.replace('\n','')
    lista_imagem[signo] = url_imagem+imagem


# In[6]:


df_signos_descricao = pd.DataFrame(list(lista_texto.items()),
                   columns=['Signos', 'Descrição'])


# In[7]:


df_signos_imagens = pd.DataFrame(list(lista_imagem.items()),
                   columns=['Signos', 'Imagem'])


# In[8]:


df_merge_signos = pd.merge(df_signos_descricao,df_signos_imagens, how='right', on = 'Signos')


# In[9]:


df_merge_signos


# In[10]:


scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]


# In[11]:


json_file = 'chave/' + str(os.listdir('chave/')[0])


# In[12]:


credentials = service_account.Credentials.from_service_account_file(json_file)
scoped_credentials = credentials.with_scopes(scopes)
gc = gspread.authorize(scoped_credentials)


# In[13]:


plan_aux = gc.open("BotTelegram")
aba_aux = plan_aux.worksheet("Teste")


# In[14]:


aba_aux.update([df_merge_signos.columns.values.tolist()] + df_merge_signos.values.tolist())

