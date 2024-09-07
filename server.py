import asyncio
import websockets
import json

# Dicionário para armazenar usuários conectados
conexoes = {}

async def tratar_conexao(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
            
            # Autenticação
            if data["type"] == "auth":
                username = data["username"]
                password = data["password"]
                
                # Simulação de autenticação
                if username and password == "1234":  # Exemplo: senha padrão "1234"
                    conexoes[username] = websocket
                    await websocket.send(json.dumps({"type": "auth", "status": "success"}))
                else:
                    await websocket.send(json.dumps({"type": "auth", "status": "fail"}))
                    return

            # Tratamento de mensagem
            elif data["type"] == "public":
                for user, ws in conexoes.items():
                    if ws != websocket:
                        await ws.send(json.dumps({"sender": data["username"], "message": data["message"]}))
            
            elif data["type"] == "private":
                destinatario = data["recipient"]
                if destinatario in conexoes:
                    await conexoes[destinatario].send(json.dumps({"sender": data["username"], "message": data["message"]}))
    except websockets.ConnectionClosed:
        print(f"Conexão fechada.")
        return

start_server = websockets.serve(tratar_conexao, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
print("Servidor WebSocket iniciado na porta 5000")
asyncio.get_event_loop().run_forever()
