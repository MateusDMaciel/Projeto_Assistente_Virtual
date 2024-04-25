import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class WatchedManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Séries/Filmes Assistidos")
        self.root.configure(background="#2c3e50")
        root.resizable(False, False)
        # Configurar o estilo do ttk
        style = ttk.Style(self.root)
        style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic' são algumas das opções

        # Conectando-se ao banco de dados
        self.conn = sqlite3.connect('watched_list.db')

        # Criando a estrutura da interface gráfica
        self.create_widgets()

        # Carregando as séries/filmes já adicionados
        self.load_watched()

    def create_widgets(self):
        # Lista de Séries/Filmes
        self.listbox = tk.Listbox(self.root, width=50, height=20, font=("Segoe UI", 10))
        self.listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Botão para adicionar Séries/Filmes
        add_button = tk.Button(self.root, text="+ Adicionar Série/Filme", command=self.open_add_window, bg="#d3d3d3", relief="flat")
        add_button.grid(row=1, column=0, padx=5, pady=5, sticky="we")

        # Botão para deletar Séries/Filmes
        delete_button = ttk.Button(self.root, text="Deletar", command=self.delete_watched)
        delete_button.grid(row=2, column=0, padx=5, pady=5, sticky="we")

        # Botão para editar o número do episódio
        edit_button = ttk.Button(self.root, text="Editar", command=self.edit_watched)
        edit_button.grid(row=3, column=0, padx=5, pady=5, sticky="we")
        

    def load_watched(self):
        # Limpar a lista
        self.listbox.delete(0, tk.END)

        # Carregar séries/filmes do banco de dados
        cursor = self.conn.execute("SELECT title, last_episode FROM watched")
        for row in cursor:
            title, last_episode = row
            self.listbox.insert(tk.END, f"{title} - Último Episódio: {last_episode}")

    def open_add_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Adicionar Série/Filme")
        add_window.configure(background="#2c3e50")

        tk.Label(add_window, text="Título:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        title_entry = tk.Entry(add_window, width=30)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(add_window, text="Último Episódio:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        last_episode_entry = tk.Entry(add_window, width=10)
        last_episode_entry.grid(row=1, column=1, padx=10, pady=5)

        save_button = tk.Button(add_window, text="Salvar", command=lambda: self.add_watched(title_entry.get(), last_episode_entry.get(), add_window))
        save_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="we")

    def add_watched(self, title, last_episode, add_window):
        # Verifique se a série já existe no banco de dados
        cursor = self.conn.execute("SELECT * FROM watched WHERE title=?", (title,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Série/filme já adicionado.")
            return
        try:
            # Adicionar dados ao banco de dados
            self.conn.execute("INSERT INTO watched (title, last_episode) VALUES (?, ?)", (title, last_episode))
            self.conn.commit()

            # Atualizar a lista após adicionar
            self.load_watched()
            add_window.destroy()
            messagebox.showinfo("Sucesso", "Série/filme adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar série/filme: {str(e)}")
    def delete_watched(self):
        # Obtenha o item selecionado na lista
        selected_item = self.listbox.curselection()
        if selected_item:
            index = selected_item[0]
            title = self.listbox.get(index).split(" - ")[0]

            # Remova a série/filme do banco de dados
            self.conn.execute("DELETE FROM watched WHERE title=?", (title,))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Série/filme deletado com sucesso!")

            # Atualize a lista após excluir
            self.load_watched()
    def edit_watched(self):
        # Obtenha o item selecionado na lista
        selected_item = self.listbox.curselection()
        if selected_item:
            index = selected_item[0]
            title, last_episode = self.listbox.get(index).split(" - ")

            # Abra uma janela de edição para o número do episódio
            edit_window = tk.Toplevel(self.root)
            edit_window.title(f"Editar Episódio de {title}")

            tk.Label(edit_window, text="Novo Episódio:").pack()
            new_episode_entry = tk.Entry(edit_window)
            new_episode_entry.pack()

            save_button = tk.Button(edit_window, text="Salvar", command=lambda: self.update_episode(title, new_episode_entry.get(), edit_window))
            save_button.pack()
            

    def update_episode(self, title, new_episode, edit_window):
        try:
            # Atualize o número do episódio no banco de dados
            self.conn.execute("UPDATE watched SET last_episode=? WHERE title=?", (new_episode, title))
            self.conn.commit()

            # Atualize a lista após editar
            self.load_watched()

            # Feche a janela de edição
            messagebox.showinfo("Sucesso", "episódio editado com sucesso!")
            edit_window.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar episódio: {str(e)}")

# Criando a instância do aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = WatchedManagerApp(root)
    root.mainloop()
