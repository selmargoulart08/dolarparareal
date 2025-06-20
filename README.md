🌍 Conversor de Moedas
Um aplicativo web simples e intuitivo para converter valores entre diversas moedas globais, utilizando a API ExchangeRate-API.com. Desenvolvido com Flask (Python) e HTML/CSS.

✨ Recursos
Conversão de Moedas: Converta valores entre uma ampla variedade de moedas.
Seleção por Dropdown: Escolha moedas facilmente através de listas suspensas.
Símbolos Monetários: Exibição dos símbolos de cada moeda para uma melhor visualização.
Atualização em Tempo Real: Dados de câmbio atualizados fornecidos pela ExchangeRate-API.com.
Fuso Horário Local: Resultados de data e hora de atualização exibidos no horário de Brasília.
Interface Amigável: Design limpo e responsivo.
🚀 Como Rodar Localmente
Siga estes passos para configurar e executar o aplicativo em seu ambiente de desenvolvimento:

Pré-requisitos
Certifique-se de ter o Python (versão 3.8 ou superior recomendada) e o pip instalados.

1. Clonar o Repositório
Bash

git clone https://github.com/selmargoulart08/dolarparareal.git
cd SEU_REPOSITORIO/conversor_moedas # Ou o nome da sua pasta raiz do projeto
(Lembre-se de substituir SEU_USUARIO e SEU_REPOSITORIO pelo seu nome de usuário e nome do repositório no GitHub).

2. Criar e Ativar um Ambiente Virtual (Recomendado)
É uma boa prática usar ambientes virtuais para isolar as dependências do projeto.

Bash

python -m venv venv
Ativar o ambiente virtual:

Windows (Prompt de Comando):
Bash

.\venv\Scripts\activate
Windows (PowerShell):
PowerShell

.\venv\Scripts\Activate.ps1
macOS / Linux:
Bash

source venv/bin/activate
3. Instalar Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

Bash

pip install -r requirements.txt
4. Configurar a Chave da API
Este projeto utiliza a ExchangeRate-API.com para obter as taxas de câmbio. Você precisará de uma chave de API gratuita.

Vá para ExchangeRate-API.com e registre-se para obter sua chave.

Para execução local, você pode definir a chave como uma variável de ambiente no seu terminal antes de rodar o aplicativo:

Windows (Prompt de Comando):
Bash

set API_KEY=SUA_CHAVE_AQUI
macOS / Linux:
Bash

export API_KEY=SUA_CHAVE_AQUI
(Substitua SUA_CHAVE_AQUI pela sua chave real da API).

Alternativa (menos segura para produção, mas prática para testes locais):
Você pode inserir a chave diretamente no arquivo app.py na linha API_KEY = os.getenv('API_KEY', 'SUA_CHAVE_AQUI'), substituindo 'SUA_CHAVE_AQUI' pela sua chave real. Lembre-se de remover isso antes de commitar para um repositório público se não quiser expor sua chave.

5. Executar o Aplicativo
Com a chave da API configurada e as dependências instaladas, execute o aplicativo:

Bash

python app.py
O aplicativo estará acessível em seu navegador no endereço: http://127.0.0.1:5000/

☁️ Deploy no PythonAnywhere
Este aplicativo foi projetado para ser facilmente hospedado em plataformas como o PythonAnywhere.

Para fazer o deploy, siga os passos de configuração de um Web App Flask no PythonAnywhere, certificando-se de:

Fazer o upload de todos os arquivos do projeto (app.py, requirements.txt, pasta templates/).
Instalar as dependências via console Bash no ambiente virtual.
Definir a API_KEY na seção "Environment variables" da configuração do seu Web App no PythonAnywhere.
Recarregar o aplicativo web.
🤝 Contribuição
Contribuições são bem-vindas! Se você tiver ideias para melhorias, novas funcionalidades ou encontrar algum bug, sinta-se à vontade para abrir uma issue ou enviar um pull request.

📄 Licença
Este projeto está licenciado sob a Licença MIT.