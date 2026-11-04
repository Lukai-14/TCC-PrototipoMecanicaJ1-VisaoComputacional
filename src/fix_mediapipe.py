import os
import urllib.request

# Garante que a pasta models existe no diretório correto
os.makedirs("models", exist_ok=True)

url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
destino = "models/pose_landmarker.task"

print("A descarregar o modelo leve...")
urllib.request.urlretrieve(url, destino)
print("Sucesso! Ficheiro guardado em:", os.path.abspath(destino))