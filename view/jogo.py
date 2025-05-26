from controller.jogo_controller import JogoController

def menu_jogos():
    controller = JogoController()

    while True:
        print("\n=== GESTÃO DE JOGOS ===")
        print("1. Inserir Jogo")
        print("2. Listar Jogos")
        print("3. Atualizar Preço")
        print("4. Excluir Jogo")
        print("5. Sair")

        opcao = input("Escolha: ")
        if opcao == "1":
            nome = input("Nome: ")
            desc = input("Descrição: ")
            preco = float(input("Preço: "))
            data = input("Data de Lançamento (YYYY-MM-DD): ")
            controller.inserir_jogo(nome, desc, preco, data)

        elif opcao == "2":
            jogos = controller.listar_jogos()
            for j in jogos:
                print(f"[{j[0]}] {j[1]} - R${j[2]}")

        elif opcao == "3":
            id_jogo = int(input("ID do jogo: "))
            preco = float(input("Novo preço: "))
            controller.atualizar_preco(id_jogo, preco)

        elif opcao == "4":
            id_jogo = int(input("ID do jogo: "))
            controller.excluir_jogo(id_jogo)

        elif opcao == "5":
            break
