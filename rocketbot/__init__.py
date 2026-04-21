# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"

    pip install <package> -t .

"""

import os
import sys
import json

base_path = tmp_global_obj["basepath"]
cur_path = base_path + 'modules' + os.sep + 'BotMonitor' + os.sep + 'libs' + os.sep
if cur_path not in sys.path:
    sys.path.append(cur_path)

from botmonitorObject import BotMonitorObject

global botmonitor_I

module = GetParams("module")

try:

    if (module == "connectToMonitor"):

        api_url = GetParams("api_url")
        api_key = GetParams("api_key")
        bot_id = GetParams("bot_id")

        botmonitor_I = BotMonitorObject(api_url, api_key, bot_id)

        resultConnection = False

        if botmonitor_I.connected:
            resultConnection = True

        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, resultConnection)

    if (module == "sendLog"):

        level = GetParams("level")
        message = GetParams("message")
        payload = GetParams("payload")
        durationMs = GetParams("durationMs")

        if payload:
            payload = json.loads(payload)
        if durationMs:
            durationMs = int(durationMs)

        result = botmonitor_I.sendLog(level, message, payload, durationMs)

        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, result)

    if (module == "sendData"):

        table = GetParams("table")
        row = GetParams("row")
        columns = GetParams("columns")

        if row:
            row = json.loads(row)
        if columns:
            columns = json.loads(columns)

        result = botmonitor_I.sendData(table, row, columns)

        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, result)

    if (module == "uploadDatabase"):

        # Connection overrides: si se proveen api_url + api_key + bot_id en el
        # form, se crea una instancia nueva para esta ejecucion. Si alguno esta
        # vacio, se reutiliza botmonitor_I creado por un connectToMonitor previo.
        api_url = GetParams("api_url")
        api_key = GetParams("api_key")
        bot_id = GetParams("bot_id")
        if api_url and api_key and bot_id:
            botmonitor_I = BotMonitorObject(api_url, api_key, bot_id)

        db_path = GetParams("dbPath")
        primary_keys_raw = GetParams("primaryKeys")
        batch_size_raw = GetParams("batchSize")

        # Parse PK list: soporta "id,tenant" o '["id","tenant"]'
        primary_keys = []
        if primary_keys_raw:
            s = primary_keys_raw.strip()
            if s.startswith("["):
                primary_keys = json.loads(s)
            else:
                primary_keys = [c.strip() for c in s.split(",") if c.strip()]

        batch_size = int(batch_size_raw) if batch_size_raw else 500

        result = botmonitor_I.uploadDatabase(db_path, primary_keys, batch_size)

        whereToStore = GetParams("whereToStore")
        SetVar(whereToStore, result)

except Exception as e:
    print("\x1B[" + "31;40mAn error occurred\x1B[" + "0m")
    PrintException()
    raise e
