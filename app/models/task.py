class Task:
    def __init__(self, nome, prioridade):
        self.nome = nome
        try:
            self.prioridade = int(prioridade)
        except (ValueError, TypeError):
            self.prioridade = 3  # Padrão baixa se houver erro