import tkinter as tk
from tkinter import ttk
import turtle

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

# Inicializar a variável tree_root fora do loop
tree_root = None

def insert_contact(root, name):
    if root is None:
        return TreeNode(name)

    if name < root.name:
        root.left = insert_contact(root.left, name)
    elif name > root.name:
        root.right = insert_contact(root.right, name)

    return root

def delete_contact(root, name):
    if root is None:
        return root

    if name < root.name:
        root.left = delete_contact(root.left, name)
    elif name > root.name:
        root.right = delete_contact(root.right, name)
    else:
        if root.left is None:
            return root.right
        elif root.right is None:
            return root.left

        root.name = min_value_node(root.right).name
        root.right = delete_contact(root.right, root.name)

    return root

def min_value_node(node):
    current = node
    while current.left is not None:
        current = current.left
    return current

def display_tree(tree, tree_view):
    tree_view.delete(*tree_view.get_children())  # Limpar a visualização atual

    def display_node(node, parent=''):
        if node is not None:
            node_id = tree_view.insert(parent, 'end', text=node.name)
            display_node(node.left, node_id)
            display_node(node.right, node_id)

    display_node(tree)

def draw_tree(node, x, y, x_spacing, turtle_pen):
    if node is not None:
        turtle_pen.penup()
        turtle_pen.goto(x, y)
        turtle_pen.pendown()
        turtle_pen.circle(20)  # Desenha um círculo para representar o nó

        turtle_pen.penup()
        turtle_pen.goto(x, y - 20)
        turtle_pen.pendown()
        turtle_pen.write(node.name, align="center")  # Escreve o nome do nó

        if node.left is not None:
            draw_tree(node.left, x - x_spacing, y - 50, x_spacing / 2, turtle_pen)
            # Desenha a linha para o nó filho à esquerda
            turtle_pen.penup()
            turtle_pen.goto(x, y - 20)
            turtle_pen.pendown()
            turtle_pen.goto(x - x_spacing, y - 50)

        if node.right is not None:
            draw_tree(node.right, x + x_spacing, y - 50, x_spacing / 2, turtle_pen)
            # Desenha a linha para o nó filho à direita
            turtle_pen.penup()
            turtle_pen.goto(x, y - 20)
            turtle_pen.pendown()
            turtle_pen.goto(x + x_spacing, y - 50)

def on_add_contact():
    contact_name = entry_contact.get()
    global tree_root
    tree_root = insert_contact(tree_root, contact_name)
    display_tree(tree_root, tree_view)
    entry_contact.delete(0, 'end')

def on_delete_contact():
    selected_item = tree_view.selection()
    if selected_item:
        contact_name = tree_view.item(selected_item, 'text')
        global tree_root
        tree_root = delete_contact(tree_root, contact_name)
        display_tree(tree_root, tree_view)

def on_show_tree():
    global tree_root
    turtle_screen.clear()
    turtle_pen.clear()
    draw_tree(tree_root, 0, 0, 200, turtle_pen)

# Criar a janela principal
root = tk.Tk()
root.title("Árvore de Contatos")

# Criar uma entrada para adicionar contatos
label_contact = ttk.Label(root, text="Nome do Contato:")
label_contact.grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_contact = ttk.Entry(root, width=20)
entry_contact.grid(row=0, column=1, padx=5, pady=5)
button_add = ttk.Button(root, text="Adicionar Contato", command=on_add_contact)
button_add.grid(row=0, column=2, padx=5, pady=5)

# Criar uma árvore para visualizar os contatos
tree_view = ttk.Treeview(root)
tree_view.heading("#0", text="Contatos")
tree_view.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

# Criar um botão para excluir contatos
button_delete = ttk.Button(root, text="Excluir Contato", command=on_delete_contact)
button_delete.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

# Função para exibir a árvore inicial
button_show_tree = ttk.Button(root, text="Visualizar Árvore", command=on_show_tree)
button_show_tree.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

# Configuração do Turtle
turtle_screen = turtle.Screen()
turtle_screen.title("Árvore de Contatos")
turtle_pen = turtle.Turtle()

# Executar a interface gráfica
root.mainloop()
