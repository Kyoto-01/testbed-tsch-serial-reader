# Testbed TSCH USB Serial Reader

Aplicação que lê os dados enviados pelos motes através da porta serial, trata-os e grava em um banco de dados de séries temporais.

## Utilização

### Instalação de pacotes nescessários

```
sudo apt install python3-pip -y
```

### Criação e utilização de um ambiente virtual

```
pip install virtualenv
```

```
mkdir ~/venvs
```

```
cd ~/venvs
```

```
python3 -m virtualenv <nome_do_ambiente_virtual>
```

```
source ~/venvs/<nome_do_ambiente_virtual>/bin/activate
```

### Instalação de dependências

```
cd testbed-tsch-serial-reader
```

```
pip install -r requirements.txt
```

### Permissão para usuários acessarem portas USB sem sudo

```bash
sudo usermod -a -G plugdev $USER
```

```bash
sudo usermod -a -G dialout $USER
```

### Observações

* Certifique-se de ter o InfluxDB rodando na máquina local ou remota.
* Modifique o arquivo dbController.py de acordo com as configurações de seu InfluxDB.

### Execução

```
cd testbed-tsch-serial-reader
```

```
./main.py -p <usb_device_name>
```

Caso não tenham sido feitas as permissões de acesso as portas USB:

```
sudo -E env PATH=$PATH ./main.py -p <usb_device_name>
```
