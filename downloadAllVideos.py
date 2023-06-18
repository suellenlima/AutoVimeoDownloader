#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import base64
import os
import re
import requests
import subprocess
import urllib.parse
import xmltojson
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
import re

# Sample URL to fetch the html page
url = "https://alunos.aprendavfx.com/area/produto/item/885648"

urlDefault = "https://alunos.aprendavfx.com/area/produto/item/"

urlVimeo = "https://player.vimeo.com/video/"
  
# Headers to mimic the browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': 'https://alunos.aprendavfx.com/auth/login?redirect=/area/produto/item/885648',
    'Cookie': '_ga=GA1.1.1431774022.1686544285; laravel_session=8jOAvN8odpy5Go2oCqrHWZA8SEBQmjPTzXBtmnk8; __cflb=02DiuH5Ncy7aKdUJtG1UW5cn2bVRqKEmSfXCQzeRkEMbA; _ga_37GXT4VGQK=GS1.1.1687060365.27.1.1687060366.0.0.0; XSRF-TOKEN=eyJpdiI6Ii9iZG8wMkdWSEhjcHlmaDRzS05ENXc9PSIsInZhbHVlIjoiMHREcXg4WGQ0VENkc1dxUHJFRWZkYlN6WHg4TUFLK3NJeXB2eWNHUjYrTW9pVnIyOVpiNUoyNC85dzFvUERaaDhKbjJyQWhKcmowUitaOXgzZWc1cHpGZllyUVRmeUxONktHSDFEbVVPSkFkelZvaWU5WHVMWUZ3U29vRFBmZDYiLCJtYWMiOiI3ZWRhZmNkYmU5OTM1MzZjZDcxNjEzYmJhY2YxZDc2Nzg1OTc2Mjc0ODJiZjBiOGEyYmQ1MmIyZDIyMTE1ZjVkIn0%3D'
}
  
# Get the page through get() method
html_response = requests.get(url=url, headers=headers)
  
# Save the page content as sample.html
with open("sample.html", "w", encoding='utf-8') as html_file:
    html_file.write(html_response.text)
      
with open("sample.html", "r", encoding='utf-8') as html_file:
     html = html_file.read()   

# Analisar o HTML usando BeautifulSoup
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')

# Buscar os valores da propriedade data-item-id
ids = [div['data-item-id'] for div in soup.find_all('div', {'data-item-id': True})]
testids = [ids[4], ids[5], ids[6], ids[7]]
# Imprimir a lista de valores
print(ids)

# Buscar os valores dentro das divs com a classe "item-titulo" e aplicar substituições e tratamentos
valores = []
for div in soup.find_all('div', class_='item-titulo'):
    texto = div.text
    texto = re.sub(r'\n|\.', '', texto)  # Remover quebras de linha (\n) ou pontos (.)
    texto = re.sub(r'\n|\,', '', texto)  # Remover quebras de linha (\n) ou pontos (.)
    texto = texto.rsplit(' ', 1)[0] + '.mp4'  # Substituir o último espaço por ".mp4"
    texto = texto.replace(' ', '-')  # Substituir espaços por traços
    valores.append(texto)

# Salvar a lista de valores em um arquivo em UTF-8
with open('valores.txt', 'w', encoding='utf-8') as arquivo:
    for valor in valores:
        arquivo.write(valor + '\n')

# Imprimir a lista de valores
print(valores)
testvalores = [valores[4], valores[5], valores[6], valores[7]]

int = 0

for id in testids:
    html_response = requests.get(url=urlDefault+id, headers=headers)
    
    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html_response.text, 'html.parser')

    # Encontrar a div com a classe "video video-vimeo"
    div = soup.find('div', class_='video video-vimeo')

    # Acessar o valor da propriedade "data-id"
    data_id = div['data-id']

    # Imprimir o valor encontrado
    print(data_id)
    
    html_response = requests.get(url=urlVimeo+data_id+"?", headers=headers)
    
    # Save the page content as sample.html
    with open("video.html", "w", encoding='utf-8') as video_html_file:
        video_html_file.write(html_response.text)
        
    with open("video.html", "r", encoding='utf-8') as video_html_file:
        html = video_html_file.read()   
    
    # Analisar o HTML usando BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    
   # Encontrar a div com class="player" e id="player"
    div_player = soup.find('div', class_='player', id='player')

    # Encontrar o próximo elemento de script após a div
    script = div_player.find_next_sibling('script')

    # Extrair o conteúdo do JSON dentro do script
    json_content = script.string.strip()
    
    # Encontrar a substring correspondente ao JSON
    start_index = json_content.find('{')
    end_index = json_content.rfind('}') + 1
    json_content = json_content[start_index:end_index]

    # Extrair o valor do primeiro "avc_url" do JSON
    player_config = json.loads(json_content)
    progressive = player_config['request']['files']['progressive']
    hasProgressive = True if len(progressive) else False
    if hasProgressive:
        progressiveUrl = ''
        for objeto in progressive:
            # Verificar se o valor desejado está presente
            if objeto["width"] == 1280:
                progressiveUrl = objeto["url"]
                break
        if progressiveUrl == '':
            lastIndex = len(progressive)
            test = progressive[lastIndex]
            print(test)
            progressiveUrl = test["url"]
        print(progressiveUrl)
        url = progressiveUrl
        url = str(url)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(testvalores[int], 'wb') as arquivo:
                for chunk in response.iter_content(chunk_size=1024):
                    arquivo.write(chunk)
        int = int + 1
    else:
        avc_urls = player_config['request']['files']['dash']['cdns']['akfire_interconnect_quic']
        print(avc_urls)
        url = avc_urls['avc_url']
        url = str(url)
        # Imprimir o valor encontrado
        print(url)

        # Extract some stuff
        base_url = url[:url.rfind('/', 0, -26) + 1]
        resp = requests.get(url)
        content = resp.json()

        # Fix the base url
        base_url = urllib.parse.urljoin(base_url, content['base_url'])
        
        # Video download here
        heights = [(i, d['height']) for (i, d) in enumerate(content['video'])]
        idx = max(heights, key=lambda x: x[1])[0]
        video = content['video'][idx]
        video_base_url = base_url + video['base_url']
        print('Base url:', video_base_url)

        filenameVideo = 'video_%s.mp4' % video['id']
        print('Saving VIDEO to %s' % filenameVideo)

        video_file = open(filenameVideo, 'wb')

        init_segment = base64.b64decode(video['init_segment'])
        video_file.write(init_segment)
        
        if init_segment:
            for segment in tqdm(video['segments']):
                segment_url = video_base_url + segment['url']
                resp = requests.get(segment_url, stream=True)
                if resp.status_code != 200:
                    print('not 200!')
                    print(resp)
                    print(segment_url)
                    break
                for chunk in resp:
                    video_file.write(chunk)
        else:
            resp = requests.get(video_base_url, stream=True)
            if resp.status_code != 200:
                print('not 200!')
                print(resp)
                print(segment_url)
                break
            for chunk in resp:
                video_file.write(chunk)

        video_file.flush()
        video_file.close()

        # Audio download here
        bitrate = [(i, d['bitrate']) for (i, d) in enumerate(content['audio'])]

        print('Bitrate', bitrate)

        idx = max(bitrate, key=lambda x: x[1])[0]
        audio = content['audio'][idx]
        audio_base_url = base_url + audio['base_url']
        print('Base url:', audio_base_url)

        filenameAudio = 'audio_%s.mp4' % audio['id']
        print('Saving AUDIO to %s' % filenameAudio)

        audio_file = open(filenameAudio, 'wb')

        init_segment = base64.b64decode(audio['init_segment'])
        audio_file.write(init_segment)
        
        if init_segment:
            for segment in tqdm(audio['segments']):
                segment_url = audio_base_url + segment['url']
                segment_url = re.sub(r'/[a-zA-Z0-9_-]*/\.\./',r'/',segment_url.rstrip())
                resp = requests.get(segment_url, stream=True)
                if resp.status_code != 200:
                    print('not 200!')
                    print(resp)
                    print(segment_url)
                    break
                for chunk in resp:
                    audio_file.write(chunk)
        else:
            segment_url = audio_base_url
            segment_url = re.sub(r'/[a-zA-Z0-9_-]*/\.\./',r'/',segment_url.rstrip())
            resp = requests.get(segment_url, stream=True)
            if resp.status_code != 200:
                print('not 200!')
                print(resp)
                print(segment_url)
                break
            for chunk in resp:
                audio_file.write(chunk)

        audio_file.flush()
        audio_file.close()

        # Combine audio and video here
        print('Combining video and audio...')
        cmd = 'ffmpeg -y -i '
        cmd += filenameAudio
        cmd += ' -i '
        cmd += filenameVideo
        cmd += ' ' + valores[int]
        subprocess.call(cmd, shell=True)
        print('Mixing Done!')
        
        int = int + 1

        # Delete the remaining single audio and video files
        os.remove("video.html")
        os.remove(filenameAudio)
        os.remove(filenameVideo)
        print("Temporary files removed!")

    # Log the conclusion of the operations
    print("*** VIDEO DOWNLOADED SUCCESSFULLY ***")
    
os.remove("sample.html")
