# Игра Виселица

Данный проект представляет собой реализацию игры в [виселицу](https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D1%81%D0%B5%D0%BB%D0%B8%D1%86%D0%B0_(%D0%B8%D0%B3%D1%80%D0%B0)) на базе blockchain.

# Что нужно для игры

- Python 3.6+

- Solidity compiler
```sh
$ sudo add-apt-repository ppa:ethereum/ethereum
$ sudo apt-get update
$ sudo apt-get install solc
```
- py-solc
```sh
$ pip install py-solc
```
- Ganache CLI
```sh
$ npm install -g ganache-cli
```
- Web3.py
```sh
$ pip install web3
```

# Как запускать
- В отдельном окне терминала запустить сервер ganache-cli
```sh
$ ganache-cli --accounts=1
```
- В новом окне терминала
```sh
$ python hangman.py
```

# Как играть
- Запустить
- Подождать пока список слов будет загружен в blockchain
- Играть
