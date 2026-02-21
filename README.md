# Сокет-сервер

Сервер принимает данные о геолокации и качестве мобильной сети от Android приложения через ZeroMQ, сохроняет в PostgresSQL и строит температурную карту RSRP.

## Архитектура 

Android App (LocationService) → ZMQ (tcp://*:5500) → Python Server → PostgreSQL (telephony)
                                                                  ↓
                                                           Matplotlib Карта RSRP

## Старт

1. Создаем таблицу в PostgresSQL 
```
CREATE DATABASE telephony;
\c telephony;

CREATE TABLE telephony (
    id SERIAL PRIMARY KEY,
    Lat DOUBLE PRECISION,
    Lon DOUBLE PRECISION,
    Alt DOUBLE PRECISION,
    Speed DOUBLE PRECISION,
    Accuracy DOUBLE PRECISION,
    Timestamp BIGINT,
    Time TEXT,
    Operator TEXT,
    NetworkType INTEGER,
    SignalLevel INTEGER,
    CellClass TEXT,
    NetworkTypeName TEXT,
    IsWifi BOOLEAN,
    IsMobile BOOLEAN,
    IsConnected BOOLEAN,
    Cells TEXT,
    RSRP INTEGER
);
```
2. Устнавливаем нужные зависимости через терминал
```
pip install pyzmq psycopg2-binary matplotlib numpy
```
3. Запуск
```
python server.py

#Визуализаци
python graph.py
```
## Android-клиент данные

Данные от Android клиента приходят в формате JSON.

## Визуализация

- RdYlGn цветовая схема (красный=плохо, зелёный=отлично)

- Размер точки ∝ качество сигнала

- Colorbar с RSRP в дБм (-140..-80)


