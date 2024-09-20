<h1>Sobre o projeto</h1>
<p>Este projeto foi desenvolvido como parte da disciplina MI — Concorrência e Conectividade do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS). Ele representa um sistema de compra de passagens aéreas, criado para explorar conceitos de concorrência e conectividade em rede de computadores.</p>
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
  <p><strong>Encerramento de conexões:</strong> Ao finalizar a interação, o servidor remove o cliente da lista de conectados e fecha a conexão.</p>
  <p><strong>Uso de grafo:</strong> O grafo é usado para representar as cidades e os trechos entre elas. Cada cidade é um nó, e as arestas conectando as cidades têm informações sobre o trecho, como preço, distância e vagas. O programa faz uma busca em profundidade (DFS) no grafo, explorando todas as rotas possíveis entre a origem e o destino. Para cada rota, o servidor calcula o preço total e retorna todas as opções de viagem disponíveis. Quando um cliente compra um trecho, o servidor diminui o número de vagas disponíveis no grafo, atualizando assim a disponibilidade de passagens em tempo real.</p>
  <p><strong>Gerenciamento do arquivo JSON:</strong> O servidor carrega e salva os dados de trechos e clientes no formato JSON, garantindo que as informações persistam e sejam atualizadas de forma segura.</p>
  <p><strong>Serialização de Dados com pickle:</strong> Para enviar e receber os dados complexos de clientes e trechos, o servidor utiliza a biblioteca pickle, facilitando a comunicação eficiente entre o servidor e os clientes.

</p>


<h3>Paradigma de comunicação</h3>

<p>
  O paradigma implementado na solução do problema é o stateful; ou seja: quando o cliente conecta com o servidor, ele não precisa enviar a cada requisição todas as informações necessárias para ver algum trecho ou efetuar alguma compra. Dessa forma, o usuário só precisa enviar uma informação por vez (cpf, origem de viagem, destino de viagem, número de passagens, etc) de acordo com a necessidade da requisição atual, já que o programa o mantém conectado e com suas informações “carregadas” e atualizadas enquanto estiver online com o servidor. Segue abaixo, em específico, aplicações que provam o paradigma adotado. 
</p>

<p><strong>Manutenção da Conexão e Login: </strong>O cliente se conecta ao servidor e mantém uma conexão aberta enquanto realiza várias operações, como consultar trechos e efetuar compras. O estado do cliente, como o CPF e a sessão de login, é mantido no servidor enquanto a conexão permanece ativa.
</p>
<p><strong>Lista de Clientes Conectados: </strong>O servidor mantém uma lista dos clientes conectados, verificando se o cliente já está logado antes de permitir uma nova conexão.</p>
<p><strong>Manutenção do Estado das Compras e Trechos: </strong>O estado da compra e os trechos escolhidos são mantidos ao longo da sessão, permitindo que o cliente navegue entre diferentes opções e finalize a compra posteriormente, sem perder o contexto; ou seja, quando o cliente efetua a compra, essa informação é diretamente atrelada ao seu objeto, independente de qual ação ele esteja realizando no momento.
</p>
<p><strong>Sessão de Conexão: </strong>O cliente continua conectado ao servidor enquanto navega pelos menus, consulta trechos e faz compras. O estado do cliente é mantido no servidor durante toda a sessão, e o cliente pode realizar múltiplas operações sem precisar se autenticar novamente ou enviar todos os dados anteriores.
</p>

<p>A escolha desse paradigma foi devido ao suas vantagens, como: </p>

<ul>
  <li>Manter um controle melhor de um usuário durante toda a execução da aplicação</li>
  <li>Mais intuitivo, já que os dados de cada entidade são mantidos independente de uma nova requisição</li>
  <li>Reduz a necessidade de enviar informações repetitivas, já que na implementação atual muitas trocas de informações são feitas na interação cliente-servidor</li>
  <li>Se por acaso o cliente desconectar, mas tenha conseguido ao menos efetuar a compra, ela ficará salva e visível para o cliente em uma próxima conexão (SE DIOGO IMPLEMENTAR NE)  
</li>
</ul>

<h3>Protocolo de comunicação</h3>

<p>O protocolo de comunicação de rede adotado na solução do projeto é o TCP/IP, que combina os protocolos TCP (Transmission Control Protocol) e IP (Internet Protocol). Com esse protocolo, é possível enviar mensagens para o servidor por meio de uma conexão via socket, garantindo a entrega confiável e ordenada dos dados. Segue um esquema na Figura 2 mostrando como o protocolo funciona e sua relação com os sockets.</p>

<div align="center"> 
  <img src = "https://github.com/user-attachments/assets/17af6375-7d9e-423f-84e3-035ceb8b5467" width="450px" />
</div>
<p align="center"><strong>Figura 2. Esquema de comunicação via socket</strong></p>

<p>Segue abaixo a ordem de troca de mensagens entre cliente e servidor durante a execução da aplicação em algumas requisições.</p>

<p><strong>Login/autenticação: </strong></p>
<p>Cliente -> Servidor: cliente envia seu CPF e o tipo de operação, que neste caso é consulta de login</p>
<p>Servidor -> Cliente: retorna objeto cliente e status de permissão de acesso (True ou False) </p>
<p><strong>Solicitação para ver trechos:</strong></p>
<p>Cliente -> Servidor: requisição: trechos</p>
<p>Servidor -> Cliente: trechos disponíveis</p>
<p><strong>Busca de possibilidades: </strong></p>
<p>Cliente -> Servidor: requisição: viagem, origem e destino</p>
<p>Servidor -> Cliente: trechos disponíveis de acordo com a origem e destino</p>
<p><strong>Compra de passagens:</strong></p>
<p>Cliente -> Servidor: requisição: compra, trecho selecionado </p>
<p>Servidor -> Cliente: status de compra </p>

<h3>Formatação e tratamento de dados</h3>

<p>A formatação de dados utilizada para transmitir informações no código é a serialização com pickle. A biblioteca pickle permite transformar objetos Python em uma sequência de bytes, que pode ser facilmente enviada entre o cliente e o servidor por meio de sockets. Assim, os dados são serializados no lado do cliente e deserializados no lado do servidor (e vice-versa), mantendo a integridade das informações.</p>
<p>Embora seja fácil de implementar e funcione muito bem com programas escritos em Python, se houver a necessidade de lidar com um servidor desenvolvido em outra linguagem, estabelecer a comunicação cliente-servidor pode se tornar mais complexo, uma vez que a biblioteca pickle é específica para Python.</p>
<p>A escolha desse método de comunicação foi uma decisão de projeto, visando a comunicação via objetos, o que exige uma biblioteca específica para Python para a serialização e deserialização dos dados</p>

<h3>Tratamento de conexões simultâneas</h3>

<p>O sistema implementa threads para lidar com as conexões simultâneas. Segue abaixo o detalhamento delas: </p>

<h4>Threads</h4>

<p>As threads em Python são utilizadas para realizar a execução simultânea de múltiplas tarefas dentro de um mesmo processo. Isso permite que diferentes partes de um programa rodem "ao mesmo tempo", sendo útil para lidar com tarefas que podem ser executadas de forma independente, como, por exemplo, a conexão de diversos clientes em um mesmo período de tempo.
Na solução do problema, especificamente na função que estabelece a conexão com um usuário, é criada uma nova thread para cada cliente, por meio da biblioteca threading. Isso garante que não ocorra um problema que foi frequente durante os testes: a necessidade de um cliente se desconectar para que outro possa fazer login. Mais detalhes sobre a implementação na documentação do projeto. 
</p>

<h3>Tratamento de concorrência</h3>

<p>O sistema implementa mutexes para lidar com as concorrência. Segue abaixo o detalhamento sobre: </p>

<h4>Mutex (lock) </h4>

<p>A biblioteca threading também oferece ferramentas para lidar com a concorrência de acesso de recursos, garantindo assim que nenhuma inconsistência de dados ocorra. Os mutexes foram utilizados nos seguintes contextos: </p>

<p><strong>Salvar cliente e carregar cliente:</strong> tanto no momento de salvar um novo cliente quanto ao verificar se ele já está presente no banco de dados (JSON), o lock bloqueia o acesso, impedindo que múltiplas threads acessem o arquivo simultaneamente.
</p>
<p><strong>Adicionar cliente:</strong> no servidor, há uma lista de clientes que auxilia na verificação de clientes conectados. Como não é permitido que dois clientes com o mesmo CPF acessem o sistema simultaneamente, foi implementado um lock para evitar essa situação.
</p>
<p><strong>Editar trecho:</strong> durante a compra de passagens, um lock também é utilizado para garantir que o arquivo seja atualizado corretamente na etapa de modificação das vagas disponíveis, evitando inconsistências no número de vagas e garantindo uma atualização coerente.</p>
<p><strong>Verificar clientes conectados:</strong> foi adicionado um lock também no momento de verificar se o cliente que está solicitando conexão já está conectado. Dessa forma, apesar de ser um acontecimento raro, o cliente não tentará fazer uma conexão multiplica com o mesmo CPF ao mesmo tempo, evitando possíveis bugs. 
</p>

<h3>Desempenho</h3>

<p>Para melhorar o desempenho, foi implementado threads com o mesmo objetivo já citado anteriormente: permitir conexões simultâneas. A melhora foi evidente porque no cenário anterior quando as threads ainda não haviam sido implementadas, um cliente precisaria esperar o outro desconectar para assim conseguir estabelecer a conexão com o servidor e efetuar alguma tarefa. Essa solução melhorou consideravelmente o throughput total.</p>
<p>Para efetuar os testes, foi utilizado um arquivo bat, onde nele é possível executar comandos de execução no terminal e simular vários clientes tentando se conectar ao mesmo tempo. Segue um exemplo dos comandos abaixo: </p>


```bat
start cmd /k "cd /d D:\vscode\mi redes\PBL-rede-de-computadores && python servidor.py && pause" REM inicia o servidor 
start cmd /k "cd /d D:\vscode\mi redes\PBL-rede-de-computadores && python cliente.py 112132312 && pause" REM conecta o cliente 1 
start cmd /k "cd /d D:\vscode\mi redes\PBL-rede-de-computadores && python cliente.py 243536366 && pause" REM conecta o cliente 2 
start cmd /k "cd /d D:\vscode\mi redes\PBL-rede-de-computadores && python cliente.py 376586588 && pause" REM conecta o cliente 3 
start cmd /k "cd /d D:\vscode\mi redes\PBL-rede-de-computadores && python cliente.py 476345232 && pause" REM conecta o cliente 4 
start cmd /k "cd /d D:\vscode\mi redes\PBL-rede-de-computadores && python cliente.py 589736455 && pause" REM conecta o cliente 5 
```
<p>No script acima, é iniciado o servidor e depois cinco clientes distintos são conectados em sequência.</p>


</div>

