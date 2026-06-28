CREATE TABLE USUARIOPESSOA (
  nome_completo VARCHAR(150) NOT NULL,
  data_nascimento DATE NOT NULL,
  cpf VARCHAR(14) PRIMARY KEY NOT NULL,
  email VARCHAR(100) NOT NULL,
  senha VARCHAR(64) NOT NULL,
  sexo VARCHAR(20) NOT NULL,
  tipo_sanguineo VARCHAR(5) NOT NULL,
  logradouro VARCHAR(150) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  bairro VARCHAR(100) NOT NULL,
  cep VARCHAR(10) NOT NULL,
  telefone VARCHAR(20)
);

CREATE TABLE INSTITUICAO (
  id_instituicao INT PRIMARY KEY NOT NULL,
  cnpj VARCHAR(18) NOT NULL,
  nome VARCHAR(150) NOT NULL,
  registro_cnes VARCHAR(50) NOT NULL,
  telefone_institucional VARCHAR(20) NOT NULL,
  email_institucional VARCHAR(100) NOT NULL,
  senha VARCHAR(64) NOT NULL,
  cep VARCHAR(10) NOT NULL,
  logradouro VARCHAR(150) NOT NULL,
  cidade VARCHAR(100) NOT NULL,
  bairro VARCHAR(100) NOT NULL
);

CREATE TABLE CAMPANHAS (
  id_campanha INT PRIMARY KEY NOT NULL,
  nome VARCHAR(150) NOT NULL,
  regiao VARCHAR(100) NOT NULL,
  data_inicio DATE NOT NULL,
  data_fim DATE NOT NULL,
  status VARCHAR(50) NOT NULL,
  redes_sociais VARCHAR(150),
  id_instituicao INT NOT NULL
);

CREATE TABLE USUARIODOADOR (
  id_doador INT NOT NULL,
  pontuacao INT NOT NULL,
  id_campanha INT NOT NULL,
  cpf VARCHAR(14) NOT NULL,
  PRIMARY KEY (id_doador, cpf)
);

CREATE TABLE USUARIOPACIENTE (
  id_paciente INT NOT NULL,
  data_entrada_fila DATE NOT NULL,
  id_instituicao INT NOT NULL,
  cpf VARCHAR(14) NOT NULL,
  PRIMARY KEY (id_paciente, cpf)
);

CREATE TABLE AGENDAMENTODEDOACAO (
  id_agendamento INT PRIMARY KEY NOT NULL,
  data_doacao DATE NOT NULL,
  status_agendamento VARCHAR(50) NOT NULL,
  tipo_doacao VARCHAR(50) NOT NULL,
  horario_agendamento VARCHAR(10) NOT NULL,
  id_doador INT NOT NULL,
  cpf_doador VARCHAR(14) NOT NULL,
  id_campanha INT NOT NULL
);

CREATE TABLE TRIAGEM (
  id_triagem INT PRIMARY KEY NOT NULL,
  peso_doador DECIMAL(5,2) NOT NULL,
  pressao_doador VARCHAR(20) NOT NULL,
  frequencia_doador INT NOT NULL,
  temperatura_doador DECIMAL(4,1) NOT NULL,
  nivel_hemoglobina DECIMAL(4,2) NOT NULL,
  resultado_triagem VARCHAR(50) NOT NULL,
  id_responsavel_triagem INT NOT NULL,
  tempo_inaptidao INT NOT NULL,
  id_agendamento INT NOT NULL
);

CREATE TABLE DOACAO (
  id_doacao INT PRIMARY KEY NOT NULL,
  data_validade DATE NOT NULL,
  tipo_sanguineo VARCHAR(5) NOT NULL,
  litros DECIMAL(4,2) NOT NULL,
  codigo_bolsa VARCHAR(50) NOT NULL,
  horario_inicio_doacao VARCHAR(10) NOT NULL,
  horario_final_doacao VARCHAR(10) NOT NULL,
  recao_doacao VARCHAR(255) NOT NULL,
  id_instituicao INT NOT NULL,
  id_triagem INT NOT NULL
);

CREATE TABLE SOLICITACAODEDOACAO (
  id_solicitacao INT NOT NULL,
  prazo_recebimento DATE NOT NULL,
  prazo_maximo DATE NOT NULL,
  id_hospital_internado INT NOT NULL,
  descricao VARCHAR(255) NOT NULL,
  numero_prontuario VARCHAR(50) NOT NULL,
  id_paciente INT NOT NULL,
  cpf_paciente VARCHAR(14) NOT NULL,
  id_campanha INT NOT NULL,
  PRIMARY KEY (id_solicitacao, id_paciente, id_campanha)
);

CREATE TABLE TROCADEPONTOS (
  nome_item VARCHAR(100) NOT NULL,
  custo_pontos_item INT NOT NULL,
  quantidade_item INT NOT NULL,
  id_item INT NOT NULL,
  descricao VARCHAR(255) NOT NULL,
  status_item VARCHAR(50) NOT NULL,
  categoria VARCHAR(50) NOT NULL,
  id_instituicao INT NOT NULL,
  PRIMARY KEY (id_item, id_instituicao)
);

CREATE TABLE SOLICITA_TROCA (
  id_doador int NOT NULL,
  cpf_doador VARCHAR(14) NOT NULL,
  id_item int NOT NULL,
  id_instituicao int NOT NULL,
  PRIMARY KEY (id_doador, cpf_doador, id_item, id_instituicao)
);

CREATE TABLE CAMPANHAS_METAS (
  metas VARCHAR(255) NOT NULL,
  id_campanha INT NOT NULL,
  PRIMARY KEY (metas, id_campanha)
);

CREATE TABLE CAMPANHAS_INCRICOES (
  incricoes INT NOT NULL,
  id_campanha INT NOT NULL,
  PRIMARY KEY (incricoes, id_campanha)
);

CREATE TABLE AGENDAMENTODEDOACAO_OBSERVACOES_ACESSIBILIDADE (
  observacoes_acessibilidade VARCHAR(255) NOT NULL,
  id_agendamento INT NOT NULL,
  PRIMARY KEY (observacoes_acessibilidade, id_agendamento)
);

CREATE TABLE SOLICITACAODEDOACAO_QUANTIDADE_BOLSA (
  quantidade_bolsa INT NOT NULL,
  id_solicitacao INT NOT NULL,
  id_paciente INT NOT NULL,
  id_campanha INT NOT NULL,
  PRIMARY KEY (quantidade_bolsa, id_solicitacao, id_paciente, id_campanha)
);

CREATE TABLE TROCADEPONTOS_ITENS (
  itens VARCHAR(100) NOT NULL,
  id_item INT NOT NULL,
  id_instituicao INT NOT NULL,
  PRIMARY KEY (itens, id_item, id_instituicao)
);

CREATE TABLE TROCADEPONTOS_DIAS_DISPONIVEIS (
  dias_disponiveis VARCHAR(50) NOT NULL,
  id_item INT NOT NULL,
  id_instituicao INT NOT NULL,
  PRIMARY KEY (dias_disponiveis, id_item, id_instituicao)
);

CREATE UNIQUE INDEX USUARIOPESSOA_index_0 ON USUARIOPESSOA (email);
CREATE UNIQUE INDEX INSTITUICAO_index_1 ON INSTITUICAO (cnpj);
CREATE UNIQUE INDEX INSTITUICAO_index_2 ON INSTITUICAO (registro_cnes);
CREATE UNIQUE INDEX INSTITUICAO_index_3 ON INSTITUICAO (telefone_institucional);
CREATE UNIQUE INDEX INSTITUICAO_index_4 ON INSTITUICAO (email_institucional);
ALTER TABLE CAMPANHAS ADD FOREIGN KEY (id_instituicao) REFERENCES INSTITUICAO (id_instituicao);

ALTER TABLE USUARIODOADOR ADD FOREIGN KEY (id_campanha) REFERENCES CAMPANHAS (id_campanha);
ALTER TABLE USUARIODOADOR ADD FOREIGN KEY (cpf) REFERENCES USUARIOPESSOA (cpf);

ALTER TABLE USUARIOPACIENTE ADD FOREIGN KEY (cpf) REFERENCES USUARIOPESSOA (cpf);

ALTER TABLE AGENDAMENTODEDOACAO ADD FOREIGN KEY (id_doador, cpf_doador) REFERENCES USUARIODOADOR (id_doador, cpf);
ALTER TABLE AGENDAMENTODEDOACAO ADD FOREIGN KEY (id_campanha) REFERENCES CAMPANHAS (id_campanha);

ALTER TABLE TRIAGEM ADD FOREIGN KEY (id_agendamento) REFERENCES AGENDAMENTODEDOACAO (id_agendamento);

ALTER TABLE DOACAO ADD FOREIGN KEY (id_instituicao) REFERENCES INSTITUICAO (id_instituicao);
ALTER TABLE DOACAO ADD FOREIGN KEY (id_triagem) REFERENCES TRIAGEM (id_triagem);

ALTER TABLE SOLICITACAODEDOACAO ADD FOREIGN KEY (id_paciente, cpf_paciente) REFERENCES USUARIOPACIENTE (id_paciente, cpf);
ALTER TABLE SOLICITACAODEDOACAO ADD FOREIGN KEY (id_campanha) REFERENCES CAMPANHAS (id_campanha);

ALTER TABLE TROCADEPONTOS ADD FOREIGN KEY (id_instituicao) REFERENCES INSTITUICAO (id_instituicao);

ALTER TABLE SOLICITA_TROCA ADD FOREIGN KEY (id_doador, cpf_doador) REFERENCES USUARIODOADOR (id_doador, cpf);

ALTER TABLE SOLICITA_TROCA ADD FOREIGN KEY (id_item, id_instituicao) REFERENCES TROCADEPONTOS (id_item, id_instituicao);

ALTER TABLE CAMPANHAS_METAS ADD FOREIGN KEY (id_campanha) REFERENCES CAMPANHAS (id_campanha);

ALTER TABLE CAMPANHAS_INCRICOES ADD FOREIGN KEY (id_campanha) REFERENCES CAMPANHAS (id_campanha);

ALTER TABLE AGENDAMENTODEDOACAO_OBSERVACOES_ACESSIBILIDADE ADD FOREIGN KEY (id_agendamento) REFERENCES AGENDAMENTODEDOACAO (id_agendamento);

ALTER TABLE SOLICITACAODEDOACAO_QUANTIDADE_BOLSA ADD FOREIGN KEY (id_solicitacao, id_paciente, id_campanha) REFERENCES SOLICITACAODEDOACAO (id_solicitacao, id_paciente, id_campanha);

ALTER TABLE TROCADEPONTOS_ITENS ADD FOREIGN KEY (id_item, id_instituicao) REFERENCES TROCADEPONTOS (id_item, id_instituicao);

ALTER TABLE TROCADEPONTOS_DIAS_DISPONIVEIS ADD FOREIGN KEY (id_item, id_instituicao) REFERENCES TROCADEPONTOS (id_item, id_instituicao);