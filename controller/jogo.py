from model.database import Database

class JogoController:
    def __init__(self):
        self.db = Database()

    def inserir_jogo(self, nome, descricao, preco, data_lancamento):
        sql = """
        INSERT INTO gamix.jogo (nome, descricao, preco, data_lancamento)
        VALUES (?, ?, ?, ?)
        """
        self.db.executar(sql, (nome, descricao, preco, data_lancamento))

    def listar_jogos(self):
        sql = "SELECT id_jogo, nome, preco FROM gamix.jogo"
        return self.db.consultar(sql)

    def atualizar_preco(self, id_jogo, novo_preco):
        sql = "UPDATE gamix.jogo SET preco = ? WHERE id_jogo = ?"
        self.db.executar(sql, (novo_preco, id_jogo))

    def excluir_jogo(self, id_jogo):
        sql = "DELETE FROM gamix.jogo WHERE id_jogo = ?"
        self.db.executar(sql, (id_jogo,))
