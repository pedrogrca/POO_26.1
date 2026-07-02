from ui import UI
from models import Produto, Categoria

if __name__ == "__main__":
    ui = UI()
    ui.view.categoria_dao.inserir(Categoria(1, "Eletrônicos"))
    ui.view.produto_dao.inserir(Produto(1, "Smartphone", 1500.0, 10, 1))
    ui.view.produto_dao.inserir(Produto(2, "Fone Bluetooth", 200.0, 20, 1))
    
    while True:
        ui.menu_visitante()