import tkinter as tk
from tkinter import messagebox
import random

class JogoAdivinhacao:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo de Adivinhação")
        self.master.geometry("450x400")
        self.master.resizable(False, False)

        # Inicialização de variáveis
        self.dificuldade = 1
        self.numero_aleatorio = 0
        self.tentativas = 0
        self.pontuacao_total = 0

        # Multiplicadores de dificuldade
        self.multiplicadores = {1: 1, 2: 2, 3: 3, 4: 4}

        # Configuração da interface
        self.create_widgets()
        self.iniciar_nova_rodada()

    def create_widgets(self):
        # Frame para exibição da dificuldade atual e botão para mudar dificuldade
        self.frame_config = tk.Frame(self.master)
        self.frame_config.pack(padx=10, pady=10, fill="x")

        self.label_dificuldade = tk.Label(
            self.frame_config,
            text=f"Dificuldade Atual: {self.get_nome_dificuldade()}",
            font=("Arial", 12)
        )
        self.label_dificuldade.pack(side="left", padx=10)

        self.botao_mudar_dificuldade = tk.Button(
            self.frame_config,
            text="Mudar Dificuldade",
            command=self.abrir_janela_dificuldade,
            font=("Arial", 10),
            bg="#2196F3",
            fg="white"
        )
        self.botao_mudar_dificuldade.pack(side="right", padx=10)

        # Frame para entrada de palpite
        self.frame_palpite = tk.Frame(self.master)
        self.frame_palpite.pack(pady=10)

        tk.Label(self.frame_palpite, text="Digite seu palpite:", font=("Arial", 12)).pack()

        self.entry_palpite = tk.Entry(self.frame_palpite, font=("Arial", 12), width=20)
        self.entry_palpite.pack(pady=5)
        self.entry_palpite.bind("<Return>", lambda event: self.processar_palpite())  # Permite pressionar Enter para chutar

        # Botão "Chutar"
        self.botao_chutar = tk.Button(
            self.master,
            text="Chutar",
            command=self.processar_palpite,
            font=("Arial", 12),
            width=15,
            bg="#4CAF50",
            fg="white"
        )
        self.botao_chutar.pack(pady=5)

        # Frame para mensagens
        self.frame_mensagem = tk.Frame(self.master)
        self.frame_mensagem.pack(pady=10)

        self.label_mensagem = tk.Label(
            self.frame_mensagem,
            text="Bem-vindo ao Jogo de Adivinhação!",
            font=("Arial", 12)
        )
        self.label_mensagem.pack()

        # Frame para pontuação
        self.frame_pontuacao = tk.Frame(self.master)
        self.frame_pontuacao.pack(pady=10)

        self.label_pontuacao = tk.Label(
            self.frame_pontuacao,
            text=f"Pontuação Total: {self.pontuacao_total} pontos",
            font=("Arial", 12)
        )
        self.label_pontuacao.pack()

    def get_nome_dificuldade(self):
        return {
            1: "FÁCIL",
            2: "MÉDIO",
            3: "DIFÍCIL",
            4: "INSANO"
        }.get(self.dificuldade, "FÁCIL")

    def iniciar_nova_rodada(self):
        # Atualiza a dificuldade com base na seleção atual
        self.dificuldade = self.dificuldade  # Mantém a dificuldade atual
        self.numero_aleatorio = self.gerar_numero_aleatorio(self.dificuldade)
        self.tentativas = 0
        self.label_mensagem.config(text="Nova rodada iniciada! Faça seu palpite.")
        self.entry_palpite.delete(0, tk.END)
        self.entry_palpite.focus_set()

        # Atualiza a exibição da dificuldade
        self.label_dificuldade.config(text=f"Dificuldade Atual: {self.get_nome_dificuldade()}")

        # Para fins de depuração (remova em produção)
        print(f"DEBUG: Número aleatório (dificuldade {self.dificuldade}): {self.numero_aleatorio}")

    def gerar_numero_aleatorio(self, dificuldade):
        ranges = {1: 10, 2: 30, 3: 50, 4: 100}
        return random.randint(1, ranges.get(dificuldade, 10))

    def processar_palpite(self):
        palpite = self.entry_palpite.get().strip()
        if not palpite:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira um número antes de chutar.")
            return

        try:
            palpite = int(palpite)
        except ValueError:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira um número válido.")
            return

        max_num = {1: 10, 2: 30, 3: 50, 4: 100}[self.dificuldade]

        if palpite < 1 or palpite > max_num:
            messagebox.showwarning("Palpite Inválido", f"Por favor, insira um número entre 1 e {max_num}.")
            return

        self.tentativas += 1

        if palpite == self.numero_aleatorio:
            pontos = self.calcular_pontos()
            self.pontuacao_total += pontos
            mensagem = self.criar_mensagem_acerto(pontos)
            self.label_mensagem.config(text=mensagem)
            self.label_pontuacao.config(text=f"Pontuação Total: {self.pontuacao_total} pontos")
            self.finalizar_rodada()
        elif palpite < self.numero_aleatorio:
            self.label_mensagem.config(text="O número é maior!")
        else:
            self.label_mensagem.config(text="O número é menor!")

        self.entry_palpite.delete(0, tk.END)

    def calcular_pontos(self):
        if self.tentativas == 1:
            pontos = 10
        elif self.tentativas == 2:
            pontos = 5
        elif self.tentativas == 3:
            pontos = 3
        else:
            pontos = 1

        multiplicador = self.multiplicadores.get(self.dificuldade, 1)
        pontos_multiplicados = pontos * multiplicador
        return pontos_multiplicados

    def criar_mensagem_acerto(self, pontos):
        if self.tentativas == 1:
            return f"DE PRIMEIRA! Você ganhou {pontos} pontos."
        elif self.tentativas == 2:
            return f"Parabéns, acertou na 2ª tentativa! Você ganhou {pontos} pontos."
        elif self.tentativas == 3:
            return f"Acertou na 3ª tentativa! Você ganhou {pontos} pontos."
        else:
            return f"Acertou em {self.tentativas} tentativas! Você ganhou {pontos} pontos."

    def finalizar_rodada(self):
        resposta = messagebox.askyesno(
            "Rodada Finalizada",
            f"Você ganhou {self.pontuacao_total} pontos no total.\nDeseja jogar novamente?"
        )
        if resposta:
            self.iniciar_nova_rodada()
        else:
            self.master.quit()

    def abrir_janela_dificuldade(self):
        # Cria uma nova janela para seleção de dificuldade
        janela_dificuldade = tk.Toplevel(self.master)
        janela_dificuldade.title("Mudar Dificuldade")
        janela_dificuldade.geometry("300x250")
        janela_dificuldade.resizable(False, False)

        tk.Label(janela_dificuldade, text="Selecione a nova dificuldade:", font=("Arial", 12)).pack(pady=10)

        var_nova_dificuldade = tk.IntVar(value=self.dificuldade)
        dificuldades = [
            ("FÁCIL (1 a 10)", 1),
            ("MÉDIO (1 a 30)", 2),
            ("DIFÍCIL (1 a 50)", 3),
            ("INSANO (1 a 100)", 4)
        ]

        for texto, valor in dificuldades:
            tk.Radiobutton(
                janela_dificuldade,
                text=texto,
                variable=var_nova_dificuldade,
                value=valor,
                font=("Arial", 10)
            ).pack(anchor='w', padx=20, pady=2)

        # Botão para confirmar a mudança de dificuldade
        def confirmar_mudanca():
            self.dificuldade = var_nova_dificuldade.get()
            self.label_dificuldade.config(text=f"Dificuldade Atual: {self.get_nome_dificuldade()}")
            messagebox.showinfo("Dificuldade Atualizada", f"Dificuldade alterada para {self.get_nome_dificuldade()}.")
            janela_dificuldade.destroy()

        botao_confirmar = tk.Button(
            janela_dificuldade,
            text="Confirmar",
            command=confirmar_mudanca,
            font=("Arial", 10),
            bg="#FF9800",
            fg="white"
        )
        botao_confirmar.pack(pady=20)

    # Você pode remover ou comentar esta linha de depuração após os testes
    # def debug_numero_aleatorio(self):
    #     print(f"DEBUG: Número aleatório: {self.numero_aleatorio}")

def main():
    root = tk.Tk()
    jogo = JogoAdivinhacao(root)
    root.mainloop()

if __name__ == "__main__":
    main()