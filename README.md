# Pototipo de Reconhecimento de Movimentos de Braço - TCC

Projeto de Visão Computacional desenvolvido em Python utilizando **OpenCV** e **MediaPipe**. Este protótipo faz parte do desenvolvimento de um sistema interativo voltado para a reabilitação motora de crianças com paralisia cerebral, combinando o rastreio de amplitude de movimento (ROM) dos membros superiores com uma interface simples para testar a responsividade entre câmera e jogo.

---

## 🎯 Sobre o Projeto

* **O que é?**  
   Um sistema de rastreio de movimento por vídeo que utiliza inteligência artificial do MediaPipe para detectar e usa NumPy para calcular ângulos articulares do ombro, aproveitando os pontos ombro, pulso e quadril para criar um triângulo.

* **Por que foi construído assim?**  
   Este projeto foi desenvolvido por **Lucas Teixeira da Silva** como um *primeiro contato* prático com Visão Computacional, contando com o apoio de ferramentas de IA, como Gemini para codificar e ChatGPT/Perplexity para ajudar a planejar e estruturar a lógica de programação. O objetivo acadêmico é compreender como posso utilizar as ferramentas OpenCV, MediaPipe e Python no desenvolvimento de um projeto e, futuramente, aplicar em um possível TCC.

* **Como funciona (Estado Atual):**  
   1. O sistema lê um vídeo de entrada (ou webcam).  
   2. O MediaPipe detecta os marcos corporais (pose landmarks).  
   3. O código calcula de forma bilateral a triangulação do braço para medir a amplitude de movimento, registrando sessões automatizadas.  
   4. Futuramente, criar um layout com 5 seções: inferior esquerda e direita, superior esquerda e direita, e topo. Esse layout terá interação com a câmera e, através dela, identificará em qual seção o jogador está.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.11**  
* **OpenCV** (Processamento de imagem e vídeo)  
* **MediaPipe Pose Landmarker** (Extração de marcos corporais)  

---

## 🐞 Problemas Identificados

### **Problemas de Código:**
1. Dificuldade em manter a precisão do rastreio em diferentes ângulos, podendo modificar a informação real do ângulo se o braço estiver mais para frente, já que a câmera não identifica corretamente a profundidade.  
    *(Nota: Acredito que exista uma forma de usar o sistema de coordenadas cartesianas (\(x, y, z\)) para reduzir distorções por profundidade. Contudo, como o exercício necessário é previsível e regido, basta instruir as crianças a ficarem no ângulo específico para jogar o jogo.)*

2. Possíveis falhas na detecção de marcos corporais devido a roupas largas ou obstruções.  

3. Necessidade de calibração para diferentes alturas e distâncias da câmera.  

### **Problemas Físicos:**
1. Processadores da escola não conseguem usar as versões mais recentes de NumPy, forçando o uso de versões antigas incompatíveis com o Python atual, criando uma cadeia de dependências desatualizadas.  

2. Falta de compreensão sobre o próprio código: Apesar de usar IA para desenvolver, o baixo conhecimento sobre o código dificulta a resolução de problemas sem assistência.  

3. Incapacidade de testar a webcam: A webcam, essencial para o projeto, não é acessível nos computadores da instituição, limitando os testes a vídeos e prejudicando a eficiência no desenvolvimento.  

---

## 🚀 Guia de Instalação e Testes (Para Avaliação)

### 1. Clonar o Repositório
```bash
git clone https://github.com/Lukai-14/TCC-Prototipo-VisaoComputacional.git
cd TCC-Prototipo-VisaoComputacional
```

### 2. Criar e Ativar o Ambiente Virtual (venv)
No Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(Caso o PowerShell bloqueie a execução de scripts por políticas de segurança, use o Prompt de Comando `cmd` e execute `venv\Scripts\activate.bat`.)*

### 3. Instalar as Dependências
Com o ambiente virtual ativo, atualize o gestor de pacotes e instale os componentes necessários:
```powershell
python -m pip install --upgrade pip
pip install opencv-python mediapipe
```
Ou, se preferir usar o arquivo de configuração padrão:
```powershell
pip install -r requirements.txt
```

### 4. Executar os Testes do Sistema
Para verificar se o ambiente e as bibliotecas estão configurados corretamente:
```powershell
python src/teste.py
```
Para testar o pipeline de vídeo e a extração do protótipo:
```powershell
python src/testar_video.py
```

---

### Como Atualizar o `README.md` no VS Code:
1. Clique no arquivo `README.md` na barra lateral esquerda do projeto.  
2. Apague todo o conteúdo antigo e cole este texto novo.  
3. Salve o arquivo (`Ctrl + S`).  
4. Para enviar ao GitHub, abra o terminal e execute:  
    ```powershell
    git add .
    git commit -m ""
    git push
    ```