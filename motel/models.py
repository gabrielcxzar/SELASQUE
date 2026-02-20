from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    data_cadastro = models.DateField()
    def __str__(self):
        return f"{self.nome} ({self.cpf})"
    
TIPO_QUARTO =[
    ('BAS', 'BÁSICO'),
    ('VIP', 'PREMIUM')
]




class Produto(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

TIPO_PAGAMENTO = [
    ('CC', 'Cartão de Crédito'),
    ('CD', 'Cartão de Débito'),
    ('DIN', 'Dinheiro à vista'),
    ('PIX', 'PIX'),
]


TIPO_FUNCIONARIO = [
    ('ADM', 'Administrador'),
    ('REC', 'Recepcionista'),
]

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf = models.CharField(max_length=11, unique=True)
    tipo = models.CharField(max_length=3, choices=TIPO_FUNCIONARIO)

class Consumo(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    reserva = models.ForeignKey('Reserva', on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"Consumo: #{self.produto} - {self.reserva}"
    
class Quarto(models.Model):
    numero = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    tipo = models.CharField(max_length=10, choices=TIPO_QUARTO)
    ocupado = models.BooleanField(default=False)
    def __str__(self):
        return f"Quarto {self.numero} - {self.get_tipo_display()}"


    
class Pagamento(models.Model):
    reserva = models.ForeignKey('Reserva', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_PAGAMENTO)
    def __str__(self):
        return f"Pagamento: #{self.reserva} - {self.tipo}"

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    quarto = models.ForeignKey(Quarto, on_delete=models.PROTECT)
    data_entrada = models.DateTimeField()
    data_saida = models.DateTimeField()
    pago = models.BooleanField(default=False)
    def __str__(self):
        return f"Reserva #{self.id}- {self.cliente} - {self.quarto}"