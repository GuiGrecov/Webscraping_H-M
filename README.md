# Webscraping H&M 

![image](https://user-images.githubusercontent.com/94385953/148562978-f79cb28b-da2c-4ce3-9d4b-8077aad3e671.png)

 <b> AVISO: </b> O CEO citado no problema de negócios não existe. Esse webscraping foi feito para fins de estudos e demonstração de habilidades/competências não me responsabilizo para o uso indefido desse código de Webscraping. 
 <br>
  * <b> O QUE É WEBSCRAPING: </b> Webscraping é uma técnica capaz de organizar em uma tabela os dados de um site, isso é feito varrendo o HTLM. Muito utilizada em E-COMMERCE para monitorar o preço de concorrentes. 
 
 

 # Problema de Negócio 
 O CEO de uma marca de jeans Brasileiro, gostaria de abrir uma loja nos EUA no meio do ano de 2022. 
 <br> Para isso ele combinou junto com o seu sócio que gostaria de monitorar a H&M a principal concorrente durante 2 meses, para entender qual o  <b>  tipo de material</b>, <b> preço</b>, <b> estilo de jeans</b>, <b> cores disponíveis</b>e o  <b> tamanho da jeans </b> que a H&M utiliza na suas roupas. 
 <br> Essas informações são imporatantes para os investidores Brasileiros, por conta de que eles querem competir com um gigante dos EUA. Eles procuram inserir um único estilo de Jeans para o público masculino, com 3 cores disponíveis, e com os mesmos materias que a H&M utiliza. 
 

 # Questão de Negócio 
 Fazer o Webscraping para esses investidores Brasileiros, por 2 meses, até conseguirmos dados suficientes para uma análise. 
 
 # Planejamento da Solução 
 
 ## Qual é a solução? 
 Necessário retirar os dados do site da H&M utilizando técnicas de Web Scraping e rodar isso de uma maneira automatizada em um servidor, para termos consultas todos os dias totalizando a amostra de 2 meses 
 
 ## Como será a solução? 
 Como não temos um servidor disponível, por ser um projeto de portfólio, vou gerar um csv com as informações do Webscraping para totalizar os 2 meses. Temos como agendar tarefas no Windows para esse processo ocorrer de forma automática toda vez que iniciamos o notebook. 
 
 ## Onde ficará o CSV? 
Programei para o Webscrping gerar um arquivo por dia, para totalizar os 2 meses de amostra. 
 ![image](https://user-images.githubusercontent.com/94385953/148567479-0b096e52-ca07-48b5-9d00-4660e58de4ff.png)
  <br>
  A cada dia que o Webscraping for executado ele atualiza um arquivo novo com o final de data diferente. 
  
  ## Modelo de Entrega dos Dados 
  
product_id	color_name	Art. No.	Fit	More sustainable materials	color_id	product_price	product_name	style_id	product_category	scrapy_datetime	size_model	size_number	cotton	polyester	spandex	elasterell
690449001	light_denim_blue/trashed	690449001	skinny_fit		1	16.99	skinny_jeans	690449	men_jeans_ripped	25/12/2021 12:27			0.99		0.01	
690449002	denim_blue	690449002	skinny_fit		2	14.99	skinny_jeans	690449	men_jeans_ripped	25/12/2021 12:27			0.98		0.02	
690449006	black/washed	690449006	skinny_fit		6	7.99	skinny_jeans	690449	men_jeans_ripped	25/12/2021 12:27			0.98		0.02	
690449007	light_denim_blue	690449007	skinny_fit		7	14.99	skinny_jeans	690449	men_jeans_ripped	25/12/2021 12:27			0.98		0.02	
690449009	black_washed_out	690449009	skinny_fit		9	19.99	skinny_jeans	690449	men_jeans_ripped	25/12/2021 12:27			0.99		0.01	
690449011	white	690449011	skinny_fit		11	19.99	skinny_jeans	690449	men_jeans_ripped	25/12/2021 12:27			0.99		0.01	
![image](https://user-images.githubusercontent.com/94385953/148568095-a9d0fa5b-80fc-493a-84b2-a0f548554dda.png)


