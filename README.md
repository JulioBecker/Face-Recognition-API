# API de reconhecimento facial e de gestos
> Essa API recebe duas fotos como parâmetros e faz reconhecimento facial entre as duas. Além de reconhecer gestos da segunda foto (piscadas, sorrisos e número de dedos levantados). 

Passando duas imagens para API é possível verificar se se trata da mesma pessoa nas fotos, além de verificar se ela está fazendo gestos específicos. O retorno da API é um JSON com os seguintes parâmetros:

"face_found_in_image" -> boolean: verifica se faces foram detectadas em ambas as fotos
"is_same"             -> boolean: verifica se é a mesma pessoa nas fotos
"score"               -> double: valor entre 0 e 1 da pontuação de reconhecimento
"is_blinking"         -> boolean: verifica se a pessoa está piscando na segunda foto
"has_smile"           -> boolean: verifica se a pessoa está sorrindo na segunda foto
"one_finger"          -> boolean: verifica se a pessoa está com um dedo levantado na segunda foto
"two_finger"          -> boolean: verifica se a pessoa está com dois dedos levantados na segunda foto
"three_finger"        -> boolean: verifica se a pessoa está com três dedos levantados na segunda foto
"four_finger"         -> boolean: verifica se a pessoa está com quatro dedos levantados na segunda foto
"five_finger"         -> boolean: verifica se a pessoa está com cinco dedos levantados na segunda foto

## Instalação

Linux:

Dependências Python3:

```sh
pip3 install opencv-python
pip3 install face_recognition
pip3 install tensorflow
pip3 install keras
pip3 install flask
pip3 install flask_cors

```

Copiar o script web_service_compare_novo.py para o diretório /bin/
Editar o arquivo crontab, para inicialização automática do script:

```sh
sudo crontab -e
```

adicionado o comando:
@reboot python3 /bin/web_service_compare_novo.py &
no final do arquivo (abaixo de todos os '#')

Reiniciar o sistema, assim a aplicação estará funcionando na porta 5001

```sh
sudo reboot
```

## Testes

Dentro da pasta teste há alguns scripts para testes unitários:

teste_facial.py -> passando um arquivo de imagem na linha 3 do script, é possível fazer a detecção de faces, olhos e sorrisos na mesma, retornando uma tela com as características detectadas

teste_facial_webcam.py -> mesma ideia do teste_facial.py, mas pegando as imagens de uma webcam

photo_finger.py -> passando um arquivo de imagem na linha 23 do script, é possível fazer a detecção de dedos levantados na mesma, retornando uma tela com o número de dedos reconhecido

webcam_finger.py -> mesma ideia do photo_finger.py, mas pegando as imagens de uma webcam


