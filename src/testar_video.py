import cv2

# Como o script está em 'src' e o vídeo está em 'data' na raiz,
# usamos '../data/' para voltar uma pasta e aceder ao vídeo.
caminho_video = "data/lateral.mp4"

cap = cv2.VideoCapture(caminho_video)

if not cap.isOpened():
  print(f"Erro: Não foi possível abrir o vídeo em {caminho_video}")
else:
  print("Vídeo aberto com sucesso! Pressione 'q' na janela do vídeo para fechar.")

while cap.isOpened():
  ret, frame = cap.read()
  if not ret:
    print("Fim do vídeo.")
    break

  # Mostra o frame do vídeo na tela
  cv2.imshow("Teste - Elevacao Lateral", frame)

  # Pressione a tecla 'q' para sair
  if cv2.waitKey(25) & 0xFF == ord("q"):
    break

cap.release()
cv2.destroyAllWindows()