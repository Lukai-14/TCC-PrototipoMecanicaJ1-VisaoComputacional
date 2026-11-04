import math
import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


def calcular_angulo(p_quadril, p_ombro, p_pulso):
  """Calcula o ângulo entre o quadril, o ombro e o pulso em graus."""
  radianos = math.atan2(p_pulso.y - p_ombro.y, p_pulso.x - p_ombro.x) - math.atan2(
      p_quadril.y - p_ombro.y, p_quadril.x - p_ombro.x
  )
  angulo = abs(radianos * 180.0 / math.pi)
  if angulo > 180.0:
    angulo = 360 - angulo
  return angulo


# Lê o modelo diretamente em binário para evitar problemas com acentos
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

# Variáveis para controlo de repetições e métricas da sessão
contador = 0
estagio = "baixo"
max_rom_dir = 0
max_rom_esq = 0

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

    alerta_compensacao = False

    if result.pose_landmarks:
      for landmarks in result.pose_landmarks:
        # Lado direito
        p_q_dir = landmarks[24]
        p_o_dir = landmarks[12]
        p_p_dir = landmarks[16]

        pt_q_dir = (int(p_q_dir.x * w), int(p_q_dir.y * h))
        pt_o_dir = (int(p_o_dir.x * w), int(p_o_dir.y * h))
        pt_p_dir = (int(p_p_dir.x * w), int(p_p_dir.y * h))

        # Lado esquerdo
        p_q_esq = landmarks[23]
        p_o_esq = landmarks[11]
        p_p_esq = landmarks[15]

        pt_q_esq = (int(p_q_esq.x * w), int(p_q_esq.y * h))
        pt_o_esq = (int(p_o_esq.x * w), int(p_o_esq.y * h))
        pt_p_esq = (int(p_p_esq.x * w), int(p_p_esq.y * h))

        # Calcular ângulos
        ang_dir = calcular_angulo(p_q_dir, p_o_dir, p_p_dir)
        ang_esq = calcular_angulo(p_q_esq, p_o_esq, p_p_esq)

        # Atualizar amplitude máxima atingida (ROM)
        if ang_dir > max_rom_dir:
          max_rom_dir = ang_dir
        if ang_esq > max_rom_esq:
          max_rom_esq = ang_esq

        # 1. Deteção de Compensação Postural (Inclinação lateral do tronco)
        cx_quadril = (p_q_dir.x + p_q_esq.x) / 2
        cx_ombro = (p_o_dir.x + p_o_esq.x) / 2
        desvio_horizontal = abs(cx_ombro - cx_quadril)

        if (
            desvio_horizontal > 0.045
        ):  # Limiar de desvio tolerável para o tronco
          alerta_compensacao = True

        # Lógica de contagem de repetições (baseada no braço direito)
        if ang_dir < 30:
          estagio = "baixo"
        if ang_dir > 75 and estagio == "baixo":
          estagio = "cima"
          contador += 1

        # Desenhar triângulos
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

        # Textos de ângulo individuais
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

    # Painel de Feedback Visual no Ecrã (Caixa superior)
    cv2.rectangle(frame, (0, 0), (320, 100), (245, 117, 16), -1)

    cv2.putText(
        frame,
        "REPETICOES",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 0),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        str(contador),
        (15, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (255, 255, 255),
        3,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        "ESTAGIO",
        (150, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 0, 0),
        1,
        cv2.LINE_AA,
    )
    cv2.putText(
        frame,
        str(estagio),
        (150, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    # Alerta visual de compensação postural em destaque na parte inferior
    if alerta_compensacao:
      cv2.rectangle(frame, (0, h - 50), (w, h), (0, 0, 255), -1)
      cv2.putText(
          frame,
          "ALERTA: TRONCO INCLINADO!",
          (20, h - 18),
          cv2.FONT_HERSHEY_SIMPLEX,
          0.8,
          (255, 255, 255),
          2,
          cv2.LINE_AA,
      )

    cv2.imshow("TCC - Deteccao de Pose", frame)
    if cv2.waitKey(25) & 0xFF == ord("q"):
      break

cap.release()
cv2.destroyAllWindows()

# Guardar o relatório de dados da sessão num ficheiro de texto ao terminar
with open("relatorio_sessao.txt", "w", encoding="utf-8") as f:
  f.write("=========================================\n")
  f.write("      RELATORIO DA SESSAO DE TERAPIA     \n")
  f.write("=========================================\n")
  f.write(f"Total de Repeticoes: {contador}\n")
  f.write(f"Amplitude Maxima (Lado Direito): {int(max_rom_dir)} deg\n")
  f.write(f"Amplitude Maxima (Lado Esquerdo): {int(max_rom_esq)} deg\n")
  f.write("=========================================\n")

print("Sessao terminada. Relatorio guardado em 'relatorio_sessao.txt'.")