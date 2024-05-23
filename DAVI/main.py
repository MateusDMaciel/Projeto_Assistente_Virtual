import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter
import sqlite3
from hashlib import sha256

# Definindo a classe principal do aplicativo de login
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")  # Título da janela
        self.root.geometry("300x250")  # Tamanho da janela
        self.root.configure(background="#f2f2f2")  # Cor de fundo da janela
        self.conn = sqlite3.connect('watched_list.db')  # Conectando ao banco de dados
        self.create_table()  # Criando as tabelas necessárias no banco de dados
        self.create_widgets()  # Criando os elementos da interface gráfica

    def create_table(self):
        try:
            # Criando a tabela de usuários, se não existir
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')
            # Criando a tabela de séries/filmes assistidos, se não existir
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS watched (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    title TEXT NOT NULL,
                    last_episode TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            self.conn.commit()  # Confirmando as mudanças no banco de dados
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar tabelas: {str(e)}")  # Exibindo mensagem de erro

    def create_widgets(self):
        # Criando e posicionando os elementos da interface gráfica
        self.username_label = customtkinter.CTkLabel(self.root, text="Usuário")
        self.username_label.pack(pady=5)
        self.username_entry = customtkinter.CTkEntry(self.root)
        self.username_entry.pack(pady=5)

        self.password_label = customtkinter.CTkLabel(self.root, text="Senha")
        self.password_label.pack(pady=5)
        self.password_entry = customtkinter.CTkEntry(self.root, show='*')
        self.password_entry.pack(pady=5)

        self.login_button = customtkinter.CTkButton(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = customtkinter.CTkButton(self.root, text="Registrar", command=self.open_register_window)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = sha256(self.password_entry.get().encode()).hexdigest()  # Criptografando a senha

        try:
            # Buscando o usuário no banco de dados
            cursor = self.conn.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            if user:
                self.root.destroy()  # Fechando a janela de login
                root = tk.Tk()
                app = WatchedManagerApp(root, user[0])  # Abrindo a janela de gerenciamento de séries/filmes
                root.mainloop()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {str(e)}")

    def open_register_window(self):
        self.register_window = tk.Toplevel(self.root)
        self.register_window.title("Registrar")
        self.register_window.geometry("300x250")
        self.register_window.configure(background="#f2f2f2")

        self.new_username_label = customtkinter.CTkLabel(self.register_window, text="Novo Usuário")
        self.new_username_label.pack(pady=10)
        self.new_username_entry = customtkinter.CTkEntry(self.register_window)
        self.new_username_entry.pack(pady=5)

        self.new_password_label = customtkinter.CTkLabel(self.register_window, text="Nova Senha")
        self.new_password_label.pack(pady=10)
        self.new_password_entry = customtkinter.CTkEntry(self.register_window, show='*')
        self.new_password_entry.pack(pady=5)

        self.register_new_user_button = customtkinter.CTkButton(self.register_window, text="Registrar", command=self.register_user)
        self.register_new_user_button.pack(pady=10)

    def register_user(self):
        username = self.new_username_entry.get()
        password = sha256(self.new_password_entry.get().encode()).hexdigest()  # Criptografando a senha

        try:
            self.conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()  # Confirmando o registro do novo usuário
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            self.register_window.destroy()  # Fechando a janela de registro
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nome de usuário já existe.")  # Exibindo mensagem de erro se o usuário já existir
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao registrar usuário: {str(e)}")


# Classe para gerenciar séries/filmes assistidos
class WatchedManagerApp:
    def __init__(self, root, user_id):
        try:
            self.root = root
            self.root.title("Séries/Filmes Assistidos")
            self.root.configure(background="#f2f2f2")
            root.resizable(False, False)
            self.center_window()  # Centralizando a janela

            style = ttk.Style(self.root)
            style.theme_use('clam')  # Configurando o estilo da interface gráfica

            self.conn = sqlite3.connect('watched_list.db')  # Conectando ao banco de dados
            self.create_table()  # Criando a tabela de séries/filmes, se não existir

            self.create_widgets()  # Criando os elementos da interface gráfica

            self.load_watched()  # Carregando as séries/filmes já adicionados
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na inicialização do aplicativo: {str(e)}")

    def center_window(self):
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()

            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 5

            self.root.geometry(f"+{x}+{y}")  # Definindo a posição da janela
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao centralizar a janela: {str(e)}")

    def create_table(self):
        try:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS watched (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    last_episode TEXT NOT NULL
                )
            ''')
            self.conn.commit()  # Confirmando a criação da tabela
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar tabela: {str(e)}")

    def create_widgets(self):
        try:
            # Criando e posicionando os elementos da interface gráfica
            title_label = customtkinter.CTkLabel(self.root, text="Séries Assistidas / Último episódio assistido", font=("Segoe UI", 16))
            title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
            self.listbox = tk.Listbox(self.root, width=50, height=20, font=("Segoe UI", 10))
            self.listbox.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

            add_button = customtkinter.CTkButton(self.root, text="+ Adicionar Série/Filme", command=self.open_add_window)
            add_button.grid(row=2, column=0, padx=5, pady=5, sticky="we")

            delete_button = customtkinter.CTkButton(self.root, text="Deletar", command=self.delete_watched)
            delete_button.grid(row=3, column=0, padx=5, pady=5, sticky="we")

            edit_button = customtkinter.CTkButton(self.root, text="Editar", command=self.edit_watched)
            edit_button.grid(row=4, column=0, padx=5, pady=5, sticky="we")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar widgets: {str(e)}")

    def load_watched(self):
        try:
            self.listbox.delete(0, tk.END)  # Limpando a lista

            cursor = self.conn.execute("SELECT id, title, last_episode FROM watched")
            for row in cursor:
                id, title, last_episode = row
                self.listbox.insert(tk.END, f"{id} - {title} - Episódio: {last_episode}")  # Adicionando itens na lista
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar séries/filmes: {str(e)}")

    def open_add_window(self):
        try:
            add_window = tk.Toplevel(self.root)
            add_window.title("Adicionar Série/Filme")
            add_window.resizable(False, False)

            def center_add_window():
                screen_width = add_window.winfo_screenwidth()
                screen_height = add_window.winfo_screenheight()
                window_width = add_window.winfo_width()
                window_height = add_window.winfo_height()

                x = (screen_width - window_width) // 2
                y = (screen_height - window_height) // 2

                add_window.geometry(f"+{x}+{y}")  # Centralizando a janela

            center_add_window()
            tk.Label(add_window, text="Título:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            title_entry = customtkinter.CTkEntry(add_window, placeholder_text="Insira o titulo")
            title_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(add_window, text="Episódio assistido:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            last_episode_entry = customtkinter.CTkEntry(add_window, placeholder_text="Insira o episódio")
            last_episode_entry.grid(row=1, column=1, padx=10, pady=5)

            save_button = customtkinter.CTkButton(add_window, text="Salvar", command=lambda: self.add_watched(title_entry.get(), last_episode_entry.get(), add_window))
            save_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="we")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir janela de adicionar série/filme: {str(e)}")

    def add_watched(self, title, last_episode, add_window):
        try:
            cursor = self.conn.execute("SELECT * FROM watched WHERE title=?", (title,))
            if cursor.fetchone():
                messagebox.showerror("Erro", "Série/filme já adicionado.")
                return

            self.conn.execute("INSERT INTO watched (title, last_episode) VALUES (?, ?)", (title, last_episode))
            self.conn.commit()  # Confirmando a adição da nova série/filme

            self.load_watched()  # Atualizando a lista
            add_window.destroy()  # Fechando a janela de adição
            messagebox.showinfo("Sucesso", "Série/filme adicionado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar série/filme: {str(e)}")

    def delete_watched(self):
        try:
            selected_item = self.listbox.curselection()
            if selected_item:
                index = selected_item[0]
                item = self.listbox.get(index)
                id = item.split(" - ")[0]

                self.conn.execute("DELETE FROM watched WHERE id=?", (id,))
                self.conn.commit()  # Confirmando a exclusão da série/filme
                messagebox.showinfo("Sucesso", "Série/filme deletado com sucesso!")

                self.load_watched()  # Atualizando a lista
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar série/filme: {str(e)}")

    def edit_watched(self):
        try:
            selected_item = self.listbox.curselection()
            if selected_item:
                index = selected_item[0]
                item = self.listbox.get(index)
                id, title, last_episode = item.split(" - ")

                edit_window = tk.Toplevel(self.root)
                edit_window.resizable(False, False)

                def center_edit_window():
                    screen_width = edit_window.winfo_screenwidth()
                    screen_height = edit_window.winfo_screenheight()
                    window_width = edit_window.winfo_width()
                    window_height = edit_window.winfo_height()

                    x = (screen_width - window_width) // 2
                    y = (screen_height - window_height) // 2

                    edit_window.geometry(f"+{x}+{y}")  # Centralizando a janela

                center_edit_window()

                edit_window.title(f"Editar Episódio de {title}")

                customtkinter.CTkLabel(edit_window, text="Novo Episódio:").pack()
                new_episode_entry = customtkinter.CTkEntry(edit_window)
                new_episode_entry.pack()

                save_button = customtkinter.CTkButton(edit_window, text="Salvar", command=lambda: self.update_episode(id, new_episode_entry.get(), edit_window))
                save_button.pack(padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar série/filme: {str(e)}")

    def update_episode(self, id, new_episode, edit_window):
        try:
            self.conn.execute("UPDATE watched SET last_episode=? WHERE id=?", (new_episode, id))
            self.conn.commit()  # Confirmando a atualização do episódio

            self.load_watched()  # Atualizando a lista
            messagebox.showinfo("Sucesso", "Episódio editado com sucesso!")
            edit_window.destroy()  # Fechando a janela de edição
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar episódio: {str(e)}")

# Criando a instância do aplicativo
if __name__ == "__main__":
    try:
        customtkinter.set_appearance_mode("Light")  # Configurando o modo de aparência
        customtkinter.set_default_color_theme("dark-blue")  # Configurando o tema de cores
        root = customtkinter.CTk()
        app = LoginApp(root)  # Iniciando o aplicativo de login
        root.mainloop()  # Executando o loop principal da interface gráfica
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar o aplicativo: {str(e)}")
