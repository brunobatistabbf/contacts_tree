import tkinter as tk
from tkinter import ttk, messagebox
import turtle
class TreeNode:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

tree_root = None

contacts_added_order = []

def insert_contact(root, name):
    global contacts_added_order
    if root is None:
        contacts_added_order.append(name)
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

def in_order_traversal(node, result):
    if node is not None:
        in_order_traversal(node.left, result)
        result.append(node.name)
        in_order_traversal(node.right, result)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    lesser = [x for x in arr[1:] if x < pivot]
    greater = [x for x in arr[1:] if x >= pivot]
    return quicksort(lesser) + [pivot] + quicksort(greater)

def display_tree(tree, tree_view):
    tree_view.delete(*tree_view.get_children())

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
        turtle_pen.circle(20)

        turtle_pen.penup()
        turtle_pen.goto(x, y - 20)
        turtle_pen.pendown()
        turtle_pen.write(node.name, align="center")

        if node.left is not None:
            draw_tree(node.left, x - x_spacing, y - 50, x_spacing / 2, turtle_pen)
            turtle_pen.penup()
            turtle_pen.goto(x, y - 20)
            turtle_pen.pendown()
            turtle_pen.goto(x - x_spacing, y - 50)

        if node.right is not None:
            draw_tree(node.right, x + x_spacing, y - 50, x_spacing / 2, turtle_pen)
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

def on_show_alphabetical_order():
    global tree_root
    result = []
    in_order_traversal(tree_root, result)
    sorted_result = quicksort(result)
    messagebox.showinfo("Visualizar Ordem Alfabética", "\n".join(sorted_result))

def on_show_added_order():
    global contacts_added_order
    messagebox.showinfo("Visualizar Ordem de Adição", "\n".join(contacts_added_order))

root = tk.Tk()
root.title("Árvore de Contatos")

label_contact = ttk.Label(root, text="Nome do Contato:")
label_contact.grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_contact = ttk.Entry(root, width=20)
entry_contact.grid(row=0, column=1, padx=5, pady=5)
button_add = ttk.Button(root, text="Adicionar Contato", command=on_add_contact)
button_add.grid(row=0, column=2, padx=5, pady=5)

tree_view = ttk.Treeview(root)
tree_view.heading("#0", text="Contatos")
tree_view.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

button_delete = ttk.Button(root, text="Excluir Contato", command=on_delete_contact)
button_delete.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

button_show_tree = ttk.Button(root, text="Visualizar Árvore", command=on_show_tree)
button_show_tree.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

button_show_alphabetical_order = ttk.Button(root, text="Visualizar Ordem Alfabética", command=on_show_alphabetical_order)
button_show_alphabetical_order.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

button_show_added_order = ttk.Button(root, text="Visualizar Ordem de Adição", command=on_show_added_order)
button_show_added_order.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

turtle_screen = turtle.Screen()
turtle_screen.title("Árvore de Contatos")
turtle_pen = turtle.Turtle()

root.mainloop()
