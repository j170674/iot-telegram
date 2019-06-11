# IOT - TELEGRAM
Este projeto tem como o objetivo unir um Telegram bot com um dispositivo IoT.

## Circuito
![Circuito](/imgs/circuit.jpg)

## Esquemático
![Esquemático](/imgs/final_project_sketch.jpg)

## Resumo
A solução, como um todo, permite que o usuário tenha acesso a temperatura, umidade, luminosidade do ambiente e cardápio do restaurante universitário da Unicamp através do seu celular. Além disso é possivel mandar mensagens para o dispositivo.

## Componentes
- NodeMCU board
- DHT11 (sensor de temperatura de umidade)
- LDR 
- Nokia 5110 LCD display

## Execução
Após montar o esquemático e carregar o código .ino no NodeMCU, execute o bot.py caso queira subir o servidor.
No aplicativo do Telegram, pesquise "MC853_bot".
Uma vez na conversa com o bot, digite o comando desejado, caso não seja um comando, a informação será exibida no display.
### Comandos
- /temp - Retorna a temperatura e exibe no display.
- /hum - Retorna a umidade e exibe no display.
- /light - Retorna a % de Luminosidade e exibe no display.
- /sensors - Escolha um sensor graficamente!
- /cardapio - Descubra o Cardapio do dia e exiba no display.


