# Testbed TSCH Serial Reader

Módulo do testbed TSCH que coleta os dados enviados pelos motes através da porta serial, decodifica-os de acordo com o formato do protocolo do testbed (definido [aqui](https://github.com/Kyoto-01/testbed-tsch-firmware#2-protocolo)), imprime-os na tela e, opcionalmente, grava-os em um banco de dados de séries temporais (InfluxDB).

## 1. Preparação do ambiente

### 1.1 Instalação do InfluxDB 
Caso deseje persistir os dados coletados, siga os tutoriais abaixo para instalar e realizar as configurações iniciais do InfluxDB:
* [Instalação do InfluxDB](https://github.com/Kyoto-01/testbed-tsch/blob/main/doc/howto/influxdb/start/install-influxdb.md)
* [Configuração do InfluxDB](https://github.com/Kyoto-01/testbed-tsch/blob/main/doc/howto/influxdb/start/setup-influxdb.md)

### 1.2 Clonagem do repositório

```
git clone https://github.com/Kyoto-01/testbed-tsch-serial-reader.git
```

### 1.3 Setup da ferramenta

```
cd testbed-tsch-serial-reader/
```

```
chmod +x setup.sh && ./setup.sh
```

### 1.4 Arquivo de configuração

Se ainda não existir, crie um arquivo de configuração chamado ```config.ini``` em ```testbed-tsch-serial-reader``` e preencha-o seguindo o modelo disponibilizado em ```testbed-tsch-serial-reader/config.example.ini```.

#### 1.4.1 InfluxDB
Caso deseje persistir os dados coletados, vá até a seção *\[influx2\]* do arquivo de configuração ```config.ini``` e atribua os valores de *url*, *org* e *token* de acordo com as configurações de seu InfluxDB. Para visualizar essas configurações siga o tutorial disponível [aqui](https://github.com/Kyoto-01/testbed-tsch/blob/main/doc/howto/influxdb/start/setup-influxdb.md).

## 2. Utilização da ferramenta

Em ```testbed-tsch-serial-reader/src``` execute:

```
./main.py [-p | --ports <device_name_1>[,...,<device_name_n>]] [-b | --baudrate <baudrate>] [-n | --nopersist]
```

---
**_OBS.:_** Caso obtenha algum erro relacionado a permissões de acesso a alguma porta serial, tente a seguinte abordagem:

```
sudo -E env PATH=$PATH ./main.py [-p | --ports <device_name_1>[,...,<device_name_n>]] [-b | --baudrate <baudrate>] [-n | --nopersist]
```
---

* **-p | --ports**: Lista de portas seriais que serão lidas pela ferramenta.

* **-b | --baudrate**: Inteiro que indica a taxa de atualização da porta serial.

* **-n | --nopersist**: Flag que indica para a ferramenta que ela não deve persistir os dados coletados. Esta flag deve ser usada se o InfluxDB não estiver instalado/configurado ou se o usuário deseja simplesmente visualizar as informações coletadas.
