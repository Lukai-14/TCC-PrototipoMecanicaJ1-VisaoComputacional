# Pototipo de Reconhecimento de Movimentos de Braço - TCC

Projeto de Visão Computacional desenvolvido em Python utilizando **OpenCV** e **MediaPipe**. Este protótipo faz parte do desenvolvimento de um sistema interativo voltado para a reabilitação motora de crianças com paralisia cerebral, combinando o rastreio de amplitude de movimento (ROM) dos membros superiores com uma interface simples para testar a responsabilidade entre camera-jogo.

---

## 🎯 Sobre o Projeto e Propósito

* **O que é?** Um sistema de rastreio de movimento por vídeo que utiliza inteligência artificial do mediapipe para detetar e usa numpy para calcular ângulos articular do ombro, se aproveitando dos pontos ombro, pulso e quadril, para criação de um triangulo.
* **Por que foi construído assim?** Este projeto foi desenvolvido por **Lucas Teixeira da Silva** como um primeiro contato prático com Visão Computacional, contando com o apoio de ferramentas de IA, como gemini para codificar e chatgpt para ajudar a planejar para desenhar e estruturar a lógica de programação. O objetivo acadêmico é tentar compreender como as ferramentas de openCV, Mediapie e python são utilizadas no desenvolvimento de um projeto, e futuramente aplicar num possivel TCC.
* **Como funciona (Estado Atual):**
  1. O sistema lê um vídeo de entrada (ou webcam).
  2. O MediaPipe deteta os marcos corporais (pose landmarks).
  3. O código calcula de forma bilateral a triangulação do braço para medir a amplitude de movimento, registrando sessões automatizadas.
  4. # futuramente criar um layout com 5 seções: inferior esq. e dir. , superior esq. e dir. e topo; e esse layoit ter contato com a acmera e atraves da camera indentificar em qual seção ele esta

---

## 🛠️ Tecnologias Utilizadas
* **Python 3.11**
* **OpenCV** (Processamento de imagem e vídeo)
* **MediaPipe Pose Landmarker** (Extração de marcos corporais)

---
## Problemas identificados
* **problemas fisicos**
```markdown
* **Problemas de codigo identificados:**
   1. Dificuldade em manter a precisão do rastreio em diferentes angulos, podendo modificar a informaçõa real do angulo se o braço estiver mais para frente, ja que a camera não identificar direito profundidade
   (Nota: Eu acredito que exista uma forma de ).
   2. Possíveis falhas na detecção de marcos corporais devido a roupas largas ou obstruções.
   3. Necessidade de calibração para diferentes alturas e distâncias da câmera.
(nota: acredito que mediapipe use plano cartesiano, então se tiver uma forma de usar Sistema de Coordenadas Cartesianas (\(x, y, z\)): Que usa eixos ortogonais para definir a posição exata de algo no espaço 3D ou no plano 2D. talbez seja possivel ignorar/reduzir os dados por causa de distorções por profundidade;
contudo, não vejo necessidade disso, o exercico que as crianças vão realizar no jogo é a elevação lateral dos braços, posso simplesmente instruir que as crianças fique no angulo especifico para jogar o jogo, afinal, o movimento necessario é extremamente previsivel e regido a propria exiostencia )
   **Problemas fisicos**
   1. Processador da escola não consegue usar as versões mais recentes de numpy, isso força a usar uma versão antiga do mesmo, que por sua vez, é incompativel com a versão atual do python, que me força a utilizar uma versão antiga do mesmo e assim progressivamente com todas as tecnologias usadas
   2. Falta de compreensão sobre o proprio codigo: Mesmo que usando ia seja bem tranquilo de realizar esse teste inicial, e memso que eu tenh pensando em tudo antes de pedi ajuda para codificar, inegavelmnete eu tenho baixissimo conhecimento sobre meu proprio codigo, o que significa que se ele quebrar e eu não tiver a IA disponivel, pode ser dificil concertar o mesmo
   3. Incapacidade de testar a webcam. A webcam, sendo a protagonsta principal de 2 jogos do meu tcc, infelismente não é acessivel utilizando os computadores da instituição. ao menos, não é acessivel usando o computador da escola. Como não tenho outras tecnologias disponiveis, isso acaba por atrapalhar na dinamica de construção do projeto, nos testes efetivos (sendo reduzidos a testa somente com videos) e a ter eficiencia em terminar o projeto

```

---
## 🚀 Guia de Instalação e Testes (Para Avaliação)

Se estás a clonar este repositório para testar o código (seja em ambiente de laboratório ou em casa), segue os passos abaixo:

### 1. Clonar o repositório
```bash
git clone [https://github.com/Lukai-14/TCC-Prototipo-VisaoComputacional.git](https://github.com/Lukai-14/TCC-Prototipo-VisaoComputacional.git)
cd TCC-Prototipo-VisaoComputacional

2. Criar e ativar o ambiente virtual (venv)
No Windows (PowerShell):

PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
(Caso o PowerShell bloqueie a execução de scripts por políticas de segurança, podes usar o Prompt de Comando cmd e executar venv\Scripts\activate.bat).

3. Instalar as dependências
Com o ambiente virtual ativo, atualiza o gestor de pacotes e instala os componentes necessários:

PowerShell
python -m pip install --upgrade pip
pip install opencv-python mediapipe
(Ou, se preferires usar o ficheiro de configuração padrão):

PowerShell
pip install -r requirements.txt
4. Executar os testes do sistema
Para verificar se o ambiente e as bibliotecas estão configuradas corretamente:

PowerShell
python src/teste.py
Para testar o pipeline de vídeo e a extração do protótipo:

PowerShell
python src/testar_video.py

---

### Como atualizar o `README.md` no teu VS Code agora:
1. Clica no ficheiro `README.md` na barra lateral esquerda do teu projeto[cite: 1].
2. Apaga todo o conteúdo antigo e cola este texto novo.
3. Salva o arquivo (`Ctrl + S`).
4. Se quiseres enviar já para o GitHub para ficar atualizado na nuvem, abre o terminal e envia:
   ```powershell
   git add README.md
   git commit -m "Atualiza README com documentacao completa do TCC"
   git push