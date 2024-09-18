
<div id = "introducao"> 
  <h1>Introdução</h1>
  <p> 
  Redes de computadores são essenciais para a comunicação e o compartilhamento de informações em um mundo digitalizado, e sua aplicação permite que serviços e pessoas se conectem o tempo inteiro. Nesse contexto, foi solicitado aos alunos de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS) o desenvolvimento de um sistema para uma companhia aérea brasileira de baixo custo, que pretende permitir que seus clientes adquiram passagens online, oferecendo a capacidade de selecionar e reservar trechos de forma exclusiva. Este relatório detalha o desenvolvimento de um sistema de compras de passagens aéreas, onde o cliente pode selecionar seu percurso de viagem, visualizar trechos disponíveis e consultar suas disponibilidades. Para garantir uma comunicação eficaz entre clientes e o servidor, será utilizado o protocolo TCP/IP, que proporciona uma troca de dados segura e eficiente. A solução incluirá o desenvolvimento de uma API em Python, compatível com a API Socket TCP/IP, assegurando a confiabilidade e o desempenho do sistema de compras.
  </p>
</div>

<h2>Equipe</h2>
<uL>
  <li><a href="https://github.com/DiogoDSJ">Diogo dos Santos de Jesus</a></li>
  <li><a href="https://github.com/eugabrielbr">Gabriel Silva dos Santos</a></li>
</ul>

<h2>Tutor</h2>
<uL>
  <li>Prof. Me. Antonio Augusto Teixeira Ribeiro Coutinho (UEFS)</li>
</ul>

<h2>Sumário</h2>
<div id="sumario">
<ul>
</ul>
</div>

<h2>Metodologia</h2>
<div id="metodologia">

  <p>Nesta seção será apresentado todo o conjunto de métodos utilizados e o caminho percorrido desde o início até a conclusão da solução do problema</p>
  
  <h3>Arquitetura da solução</h3>

  <p>
    Primeiro, antes de explicar diretamente qual é a arquitetura da solução, é preciso destacar qual foi o planejamento inicial de comunicação entre um cliente que deseja comprar a passagem e o servidor que recebe a solicitação de compra. Segue na Figura 1 o diagrama que descreve a ideia do fluxo que serviu como base para o início do desenvolvimento. 
  </p>

  <div align="center"> 
  <img src = "https://github.com/user-attachments/assets/6f2c023e-cdae-4927-b50a-e3ec1c5e9c05" width="450px" />
</div>
<p align="center"><strong>Figura 1. Fluxograma de comunicação</strong></p>

<p>
A solução desenvolvida segue o modelo clássico de comunicação cliente-servidor, onde o cliente faz login na aplicação e solicita uma ou mais compras de passagens. De forma assíncrona, o servidor processa a compra e retorna o status ao cliente. A seguir, é apresentada uma explicação mais detalhada dos componentes implementados e como está funcionando para atingir o seu papel na solução.
</p>

  <h3>Componentes principais</h3>
  <h3>Cliente:</h3>
  <p>Responsável por interagir com o usuário, enviando para o servidor suas solicitações.</p>
  <p><strong>Criação do socket:</strong> Inicializa e estabelece uma conexão com o servidor utilizando um socket TCP, configurado com o IP e a porta especificados. Isso cria o ponto de comunicação necessário para a troca de dados entre o cliente e o servidor.</p>
  <p><strong>Login:</strong> Após conectar-se ao servidor, o cliente realiza a autenticação enviando um CPF. O servidor verifica se o CPF já está logado e responde de acordo.</p>
  <p><strong>Menu de opções:</strong> Exibe um menu principal ao cliente com opções para visualizar trechos disponíveis, comprar passagens ou encerrar a conexão. O menu permite ao usuário escolher a ação desejada e interage com o servidor conforme a escolha.</p>
  <p><strong>Envio e recebimento de mensagens:</strong> Dependendo da seleção do menu, o cliente envia comandos ao servidor e recebe respostas. Para visualizar trechos, o cliente solicita e exibe a lista de trechos. Para a compra de passagens, o cliente envia dados sobre a origem e o destino, recebendo opções de trechos e preços disponíveis.</p>
  <p><strong>Serialização de Dados com pickle:</strong> Utiliza o módulo pickle para converter objetos Python em uma forma que pode ser transmitida pela rede e para reconstruí-los ao serem recebidos. Isso assegura a integridade dos dados trocados entre cliente e servidor.</p>
  <p><strong>Tratamento de Erros e Conexão:</strong> Inclui mecanismos para tratar erros de conexão e comunicação, garantindo que problemas durante o envio e recebimento de dados sejam adequadamente gerenciados. Isso melhora a robustez e a confiabilidade da comunicação entre cliente e servidor.</p>

  <h3>Servidor:</h3>
  <p>Responsável por aceitar conexões, processar compras e efetuar a persistência de dados.</p>
  <p><strong>Criação do socket:</strong> O servidor inicia um socket TCP para escutar conexões dos clientes em um IP e porta específicos.</p>
  <p><strong>Processo de login:</strong> Após receber uma solicitação de login, o servidor verifica se o cliente já está conectado. Se não estiver, permite a conexão; caso contrário, rejeita.</p>
  <p><strong>Gerenciamento de Trechos e Clientes:</strong> Os dados de clientes e trechos são armazenados em um arquivo JSON. O servidor carrega e manipula essas informações, permitindo que os clientes vejam trechos disponíveis e façam compras.</p>
  <p><strong>Tratamento de requisições:</strong> O servidor processa pedidos como visualização de trechos, busca de rotas e compras, e responde conforme os dados do sistema.</p>
  <p><strong>Encerramento de conexões:</strong>Ao finalizar a interação, o servidor remove o cliente da lista de conectados e fecha a conexão.</p>
  <p><strong>Uso de grafo:</strong> O grafo é usado para representar as cidades e os trechos entre elas. Cada cidade é um nó, e as arestas conectando as cidades têm informações sobre o trecho, como preço, distância e vagas. O programa faz uma busca em profundidade (DFS) no grafo, explorando todas as rotas possíveis entre a origem e o destino. Para cada rota, o servidor calcula o preço total e retorna todas as opções de viagem disponíveis. Quando um cliente compra um trecho, o servidor diminui o número de vagas disponíveis no grafo, atualizando assim a disponibilidade de passagens em tempo real.</p>
  <p><strong>Gerenciamento do arquivo JSON:</strong> O servidor carrega e salva os dados de trechos e clientes no formato JSON, garantindo que as informações persistam e sejam atualizadas de forma segura.</p>
  <p><strong>Serialização de Dados com pickle:</strong> Para enviar e receber os dados complexos de clientes e trechos, o servidor utiliza a biblioteca pickle, facilitando a comunicação eficiente entre o servidor e os clientes.
</p>

</div>

