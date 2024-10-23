# Biblioteca CRUD Oracle 📚

## Requisitos 📋
Antes de começar, verifique se você atendeu aos seguintes requisitos:
- Você instalou a versão mais recente do [`Git`](https://git-scm.com/downloads).
- Você instalou o [`Python versão 3.10.8`](https://www.python.org/downloads/release/python-3108/) ou inferior em razão da descontinuação do suporte a biblioteca [cx_Oracle](https://oracle.github.io/python-cx_Oracle/).
- Você instalou e configurou o [`OracleDB`](https://www.oracle.com/br/database/technologies/xe-downloads.html).

## Executando o Sistema 🚀
Clone o repositório `biblioteca_crud_oracle` para o seu computador usando o seguinte comando:
```git
git clone https://github.com/gustavopradobr/biblioteca_crud_oracle.git
```
Após realizar o download do projeto, execute o seguinte comando no terminal: 
```shell
pip install -r requirements.txt
```

Após a instalação das dependências, execute o seguinte comando no terminal:
```shell
python run.py 
```

Ao rodar o comando será feito o acesso da pasta src, a criação e inserção dos dados nas tabelas e será iniciado o programa.

Para que possa testar as conexões com o banco de dados Oracle e o módulo Conexion desenvolvido para esse projeto, basta executar o script Python a seguir:
```shell
python test.py
```
## Diretórios do projeto 📁
- No diretório "`diagrams`" pode ser encontrado o `diagrama relacional do sistema`. O sistema é composto por quatro entidades fundamentais: "LIVROS," "USUÁRIOS," "EMPRÉSTIMOS," e "DEVOLUÇÕES."

- Dentro do diretório "`sql`" estão os scripts destinados à `criação das tabelas` e à `inclusão de dados iniciais` para a utilização imediata do sistema. Certifique-se de que o usuário do banco de dados esteja devidamente autorizado com todos os privilégios necessários antes de executar os scripts de criação.

- O script "`create_tables_biblioteca.sql`" é responsável pela geração e exclusão das tabelas e sequences, caso já estejam criadas.

- O script "`inserting_samples_biblioteca.sql`" realiza a inclusão de registros fictícios para fins de teste no sistema. Foram incluídas informações como livros, usuários, empréstimos e devoluções, que são fundamentais para o funcionamento do sistema de gerenciamento de biblioteca escolar.

- No diretório "`src`" são encontrados os scripts que compõem o sistema.

- No diretório "`conexion`" estão os scripts responsáveis pelo módulo de conexão com o banco de dados Oracle. Esse módulo oferece funcionalidades úteis para a execução de instruções DML e DDL, permitindo a obtenção de resultados em formatos como JSON, matrizes e Pandas DataFrame.

- No diretório "`controller`" estão as classes controladoras, que têm a responsabilidade de executar operações de inserção, modificação e exclusão de registros nas tabelas.

- No diretório "`model`" estão localizadas as classes que representam as entidades conforme descritas no diagrama relacional.

- Dentro do diretório "`reports`" é possível encontrar a classe encarregada de gerar todos os relatórios do sistema.

- No diretório "`sql`" estão disponíveis os scripts utilizados para a criação dos relatórios a partir da classe Relatorio.

- No diretório "`utils`" se encontram os scripts voltados para configuração e automatização da tela de informações iniciais.

- O script "`create_tables_biblioteca.py`" é responsável por criar as tabelas e inserir registros fictícios. A execução deste script deve ser antes de rodar o "principal.py" para garantir a criação das tabelas necessárias para execução do programa. Caso preferir, também é possível executar os scripts diretamente no SQL Developer ou em outra IDE de acesso ao banco de dados.

- O "`principal.py`" atua como a interface entre o usuário e os módulos de acesso ao banco de dados, e deve ser executado após a criação das tabelas para garantir o funcionamento adequado do sistema.

## Vídeo demonstrativo 🎬
[`Acesse aqui`](https://www.youtube.com/watch?v=xRB0KWsuqss) o vídeo demonstrativo da aplicação

## 🤝 Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/luizfelipemacedo">
        <img src="https://github.com/luizfelipemacedo.png" width="100px;" alt="Foto de Luiz Felipe"/><br>
        <sub>
          <b>Luiz Felipe Macedo</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/gustavopradobr">
        <img src="https://github.com/gustavopradobr.png" width="100px;" alt="Foto de Gustavo"/><br>
        <sub>
          <b>Gustavo Prado</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/pedrohmarinho">
        <img src="https://github.com/pedrohmarinho.png" width="100px;" alt="Foto de Pedro"/><br>
        <sub>
          <b>Pedro Marinho</b>
        </sub>
      </a>
    </td>
  </tr>
</table>
