import math
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np


def calcular_angulo(p_quadril, p_ombro, p_pulso):
  """Calcula o ângulo entre o quadril, o ombro e o pulso em graus."""
  radianos = math.atan2(p_pulso.y - p_ombro.y, p_pulso.x - p_ombro.x) - math.atan2(
      p_quadril.y - p_ombro.y, p_quadril.x - p_ombro.x
  )
  angulo = abs(radianos * 180.0 / math.pi)
  if angulo > 180.0:
    angulo = 360 - angulo
  return angulo


def determinar_secoes_ativas(ang_esq, ang_dir):
  """Avalia o braço esquerdo e o direito de forma independente

  e retorna uma lista com todas as seções que devem acender.
  """
  secoes_ativas = []

  # --- Lógica do Lado Esquerdo ---
  if ang_esq > 115:
    secoes_ativas.append("Topo")
  elif ang_esq > 30:
    secoes_ativas.append("esq. superior")
  else:
    secoes_ativas.append("esq. inferior")

  # --- Lógica do Lado Direito ---
  if ang_dir > 115:
    if "Topo" not in secoes_ativas:
      secoes_ativas.append("Topo")
  elif ang_dir > 30:
    secoes_ativas.append("dir. superior")
  else:
    secoes_ativas.append("dir. inferior")

  return secoes_ativas


# Lê o modelo do MediaPipe
with open("models/pose_landmarker.task", "rb") as f:
  model_buffer = f.read()

base_options = python.BaseOptions(model_asset_buffer=model_buffer)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_poses=1,
)

PONTOS_INTERESSE = [11, 12, 15, 16, 23, 24]
cap = cv2.VideoCapture("data/lateral.mp4")

secoes_atuais = []
ang_esq = 0
ang_dir = 0

with vision.PoseLandmarker.create_from_options(options) as landmarker:
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break

    h, w, _ = frame.shape
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
    )
    result = landmarker.detect(mp_image)

    if result.pose_landmarks:
      for landmarks in result.pose_landmarks:
        # Lado Direito (ombro 12, quadril 24, pulso 16)
        p_q_dir = landmarks[24]
        p_o_dir = landmarks[12]
        p_p_dir = landmarks[16]

        pt_q_dir = (int(p_q_dir.x * w), int(p_q_dir.y * h))
        pt_o_dir = (int(p_o_dir.x * w), int(p_o_dir.y * h))
        pt_p_dir = (int(p_p_dir.x * w), int(p_p_dir.y * h))

        # Lado Esquerdo (ombro 11, quadril 23, pulso 15)
        p_q_esq = landmarks[23]
        p_o_esq = landmarks[11]
        p_p_esq = landmarks[15]

        pt_q_esq = (int(p_q_esq.x * w), int(p_q_esq.y * h))
        pt_o_esq = (int(p_o_esq.x * w), int(p_o_esq.y * h))
        pt_p_esq = (int(p_p_esq.x * w), int(p_p_esq.y * h))

        # Calcular ângulos de ambos os lados
        ang_dir = calcular_angulo(p_q_dir, p_o_dir, p_p_dir)
        ang_esq = calcular_angulo(p_q_esq, p_o_esq, p_p_esq)

        # Determinar quais seções devem acender simultaneamente
        secoes_atuais = determinar_secoes_ativas(ang_esq, ang_dir)

        # Desenhar triângulos e linhas de ambos os lados
        cv2.line(frame, pt_q_dir, pt_o_dir, (0, 255, 255), 2)
        cv2.line(frame, pt_o_dir, pt_p_dir, (0, 255, 255), 2)
        cv2.line(frame, pt_q_dir, pt_p_dir, (0, 255, 255), 2)

        cv2.line(frame, pt_q_esq, pt_o_esq, (255, 255, 0), 2)
        cv2.line(frame, pt_o_esq, pt_p_esq, (255, 255, 0), 2)
        cv2.line(frame, pt_q_esq, pt_p_esq, (255, 255, 0), 2)

        # Desenhar pontos de interesse
        for idx in PONTOS_INTERESSE:
          p = landmarks[idx]
          cv2.circle(frame, (int(p.x * w), int(p.y * h)), 6, (0, 255, 0), -1)

        # Textos de ângulo no vídeo
        cv2.putText(
            frame,
            f"Dir: {int(ang_dir)} deg",
            (pt_o_dir[0] - 80, pt_o_dir[1] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            f"Esq: {int(ang_esq)} deg",
            (pt_o_esq[0] + 10, pt_o_esq[1] - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            2,
            cv2.LINE_AA,
        )

    # --- TELA DIGITAL DO JOGO (Janela Separada) ---
    tela_jogo = np.zeros((250, 900, 3), dtype=np.uint8)

    blocos = [
        "esq. inferior",
        "esq. superior",
        "Topo",
        "dir. superior",
        "dir. inferior",
    ]
    largura_bloco = 160
    altura_bloco = 120
    inicio_y = 65

    for i, nome_bloco in enumerate(blocos):
      inicio_x = 30 + (i * 170)
      fim_x = inicio_x + largura_bloco
      fim_y = inicio_y + altura_bloco

      # Se o bloco estiver presente na lista de seções ativas, acende em verde
      if nome_bloco in secoes_atuais:
        cor_caixa = (0, 255, 0)  # Verde ativo
        cor_texto = (0, 0, 0)
        espessura_linha = -1
      else:
        cor_caixa = (50, 50, 50)  # Cinza inativo
        cor_texto = (200, 200, 200)
        espessura_linha = 2

      cv2.rectangle(
          tela_jogo,
          (inicio_x, inicio_y),
          (fim_x, fim_y),
          cor_caixa,
          espessura_linha,
      )
      if espessura_linha == -1:
        cv2.rectangle(
            tela_jogo, (inicio_x, inicio_y), (fim_x, fim_y), (255, 255, 255), 2
        )

      cv2.putText(
          tela_jogo,
          nome_bloco,
          (inicio_x + 15, inicio_y + 65),
          cv2.FONT_HERSHEY_SIMPLEX,
          0.55,
          cor_texto if espessura_linha == -1 else (255, 255, 255),
          2,
          cv2.LINE_AA,
      )

    # Informações extras na tela do jogo
    cv2.putText(
        tela_jogo,
        f"Dir: {int(ang_dir)} | Esq: {int(ang_esq)} | Ativos:"
        f" {', '.join(secoes_atuais)}",
        (30, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
        cv2.LINE_AA,
    )

    # Exibir as duas janelas separadas
    cv2.imshow("Visao Computacional - Bastidores (Camera/Video)", frame)
    cv2.imshow("Interface Digital - Jogo (5 Secoes)", tela_jogo)

    if cv2.waitKey(25) & 0xFF == ord("q"):
      break

cap.release()
cv2.destroyAllWindows()