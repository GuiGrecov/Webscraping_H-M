# Webscraping H&M 

![image](https://user-images.githubusercontent.com/94385953/148562978-f79cb28b-da2c-4ce3-9d4b-8077aad3e671.png)

 <b> AVISO: </b> O CEO citado no problema de negócios não existe. Esse webscraping foi feito para fins de estudos e demonstração de habilidades/competências não me responsabilizo para o uso indefido desse código de Webscraping. 
 <br>
  * <b> O QUE É WEBSCRAPING: </b> Webscraping é uma técnica capaz de organizar em uma tabela os dados de um site, isso é feito varrendo o HTLM. Muito utilizada em E-COMMERCE para monitorar o preço de concorrentes. 
 
 

 # 1. Problema de Negócio 
 O CEO de uma marca de jeans Brasileiro, gostaria de abrir uma loja nos EUA no meio do ano de 2022. 
 <br> Para isso ele combinou junto com o seu sócio que gostaria de monitorar a H&M a principal concorrente durante 2 meses, para entender qual o  <b>  tipo de material</b>, <b> preço</b>, <b> estilo de jeans</b>, <b> cores disponíveis</b>e o  <b> tamanho da jeans </b> que a H&M utiliza na suas roupas. 
 <br> Essas informações são imporatantes para os investidores Brasileiros, por conta de que eles querem competir com um gigante dos EUA. Eles procuram inserir um único estilo de Jeans para o público masculino, com 3 cores disponíveis, e com os mesmos materias que a H&M utiliza. 
 

 # 2. Questão de Negócio 
 Fazer o Webscraping para esses investidores Brasileiros, por 2 meses, até conseguirmos dados suficientes para uma análise. 
 
 # 3. Planejamento da Solução 
 
 ## 3.1 Qual é a solução? 
 Necessário retirar os dados do site da H&M utilizando técnicas de Web Scraping e rodar isso de uma maneira automatizada em um servidor, para termos consultas todos os dias totalizando a amostra de 2 meses 
 
 ## 3.2 Como será a solução? 
 Como não temos um servidor disponível, por ser um projeto de portfólio, vou gerar um csv com as informações do Webscraping para totalizar os 2 meses. Temos como agendar tarefas no Windows para esse processo ocorrer de forma automática toda vez que iniciamos o notebook. 
 
 ## 3.4 Onde ficará o CSV? 
Programei para o Webscraping gerar um arquivo por dia, para totalizar os 2 meses de amostra. 
 ![image](https://user-images.githubusercontent.com/94385953/148567479-0b096e52-ca07-48b5-9d00-4660e58de4ff.png)
  <br>
  A cada dia que o Webscraping for executado ele atualiza um arquivo novo com o final de data diferente. 
  
  ## 3.5 Modelo de Entrega dos Dados 
![image](https://user-images.githubusercontent.com/94385953/148568519-8c208c5d-0840-462e-8a30-8b0ccb46aa5e.png)
Vamos entregar uma tabela dessa cada dia, com os valores retirados do site diariamente, ou seja, o preço, produto, cores, podem variar de acordo com o estoque e mudanças nas coleções.


# 4. Arquitetura do Webscraping
O webscraping que fizemos foi dividido por 4 jobs (4 tarefas) que rodam em sequência para conseguir gerar o csv com as informações diárias de produtos. 
![image](https://user-images.githubusercontent.com/94385953/148576978-17f4a841-00cd-4a6e-b776-d5a599e4a84f.png)
<br> 
* **JOB 1** : O primeiro trabalho é responsável por entrar na página de JEANS MASCULINOS e selecionar a vitrine das calças JEANS.
* **JOB 2** : O segundo trabalho é responsável por entrar em cada produta da loja e pegar as informações de cores de produto, tipos de modelos, código do produto no e-commerce, código único do produto.
**OBSERVAÇÃO**- a maior dificuldade do JOB 2 foi selecionar o pegar as informações pela cor do produto - quando o usuário muda a cor da calça sua composição e modelo muda junto. O JOB 2 é responsável por varrer essa informação. 
* **JOB 3**: Etapa conhecida como DATA CLEANING precisamos rodar algumas REGEX para limpar os dados e transformar de um jeito que o modelo consiga entender. 
* **JOB 4**: Essa última tarefa é responsável por salvar os CSV gerados diariamente em uma pasta pré-configurada no Windows. 
**OBSERVAÇÃO**- caso esse processo fosse feito em uma empresa essa etapa seria substítuida por um servidor. 



