from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    data_cadastro = models.DateField()

class Quarto(models.Model):
    numero = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    tipo = models.CharField(max_length=10)
    ocupado = models.BooleanField(default=False)

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    quarto = models.ForeignKey(Quarto, on_delete=models.PROTECT)
    data_entrada = models.DateTimeField()
    data_saida = models.DateTimeField()
    pago = models.BooleanField(default=False)

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2)

TIPO_PAGAMENTO = [
    ('CC', 'Cartão de Crédito'),
    ('CD', 'Cartão de Débito'),
    ('DIN', 'Dinheiro à vista'),
    ('PIX', 'PIX'),
]
class Pagamento(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_PAGAMENTO)


TIPO_FUNCIONARIO = [
    ('ADM', 'Administrador'),
    ('REC', 'Recepcionista'),
]

class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    cpf = models.CharField(max_length=11, unique=True)
    tipo = models.CharField(max_length=3, choices=TIPO_FUNCIONARIO)