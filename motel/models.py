from django.db import models
from django.utils import timezone
from datetime import timedelta


# class Cliente(models.Model):
#     nome = models.CharField(max_length=100)
#     cpf = models.CharField(max_length=11, unique=True)
#     email = models.EmailField()
#     data_cadastro = models.DateField()

class Cliente (models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=11, unique=True, verbose_name='CPF')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(max_length=15, verbose_name='Telefone')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')

    esta_ativo = models.BooleanField(default=True, verbose_name='Está Ativo?')
    data_cadastro = models.DateField(auto_now_add=True, verbose_name='Data de Cadastro')

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome
    



   

# class Quarto(models.Model):
#     numero = models.IntegerField()
#     valor = models.DecimalField(max_digits=8, decimal_places=2)
#     tipo = models.CharField(max_length=10)
#     ocupado = models.BooleanField(default=False)


class Quarto(models.Model):

    STATUS_QUARTO = [
        ('livre', 'Livre'),
        ('ocupado', 'Ocupado'),
        ('manutencao', 'Manutenção'),
        ('limpeza', 'Limpeza'),
        ('reservado', 'Reservado'),
    ]

    TIPO_QUARTO = [
        ('simples', 'Simples'),
        ('luxo', 'Luxo'),
        ('suite_master', 'Suíte Master'),
        ('presidencial', 'Presidencial'),
    ]

    numero = models.CharField(max_length=10, unique=True, verbose_name='Número do Quarto')
    tipo = models.CharField(max_length=20, verbose_name='Tipo do Quarto', choices=TIPO_QUARTO)

    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição do Quarto')
    preco_hora = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço por Hora')
    preco_periodo = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço por Período')
    preco_pernoite = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço por Pernoite')

    capacidade = models.IntegerField(default=2, verbose_name='Capacidade de Pessoas')
    status = models.CharField(max_length=20, default='livre', verbose_name='Status do Quarto', choices=STATUS_QUARTO)

    possui_garagem = models.BooleanField(default=False, verbose_name='Possui Garagem?')
    possui_hidro = models.BooleanField(default=False, verbose_name='Possui Hidromassagem?')
    possui_ar_condicionado = models.BooleanField(default=False, verbose_name='Possui Ar Condicionado?')
    possui_frigobar = models.BooleanField(default=False, verbose_name='Possui Frigobar?')
    possui_tv = models.BooleanField(default=False, verbose_name='Possui TV?')
    possui_wifi = models.BooleanField(default=False, verbose_name='Possui Wi-Fi?')

    esta_ativo = models.BooleanField(default=True, verbose_name='Está Ativo?')

    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')


    class Meta:
        verbose_name = 'Quarto'
        verbose_name_plural = 'Quartos'
        ordering = ['tipo','numero']

    def __str__(self):
        return f'Quarto {self.numero} - {self.tipo}'
    


# class Reserva(models.Model):
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     quarto = models.ForeignKey(Quarto, on_delete=models.PROTECT)
#     data_entrada = models.DateTimeField()
#     data_saida = models.DateTimeField()
#     pago = models.BooleanField(default=False)


class Reserva(models.Model):
    
    TIPO_RESERVA = [
        ('hora', 'Hora'),
        ('periodo', 'Período'),
        ('pernoite', 'Pernoite'),
    ]

    STATUS_RESERVA = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    STATUS_PAGAMENTO = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Cliente')
    quarto = models.ForeignKey(Quarto, on_delete=models.PROTECT, verbose_name='Quarto')
    tipo_reserva = models.CharField(max_length=20, verbose_name='Tipo de Reserva', choices=TIPO_RESERVA)
    entrada = models.DateTimeField (auto_now_add=True ,verbose_name='Data e Hora de Entrada')
    saida = models.DateTimeField (verbose_name='Data e Hora de Saída')

    status = models.CharField(max_length=20, default='pendente', verbose_name='Status da Reserva', choices=STATUS_RESERVA)
    status_pagamento = models.CharField(max_length=20, choices=STATUS_PAGAMENTO, default='pendente', verbose_name='Status do Pagamento')
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Valor Total')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-entrada']

    def __str__(self):
        return f'Reserva {self.cliente.nome} - {self.quarto.numero}'

    # Calcula automaticamente os campos de saída e valor total levando em conta o tipo de reserva
    def save(self, *args, **kwargs):

        if not self.saida:
            if self.tipo_reserva == 'hora':
                self.saida = self.entrada + timedelta(hours=1)
                self.valor_total = self.quarto.preco_hora
            elif self.tipo_reserva == 'periodo':
                self.saida = self.entrada + timedelta(hours=4)
                self.valor_total = self.quarto.preco_periodo
            elif self.tipo_reserva == 'pernoite':
                self.saida = self.entrada + timedelta(days=1)
                self.valor_total = self.quarto.preco_pernoite

        super().save(*args, **kwargs)

    def quarto_disponivel(self):
        if self.quarto.status != 'livre' or not self.quarto.esta_ativo:
            return False
        
        conflitos = Reserva.objects.filter(
            quarto=self.quarto,
            status__in=['pendente', 'confirmada'],
            entrada__lt=self.saida,
            saida__gt=self.entrada
        ).exclude(id=self.id)

        return not conflitos.exists()





# class Produto(models.Model):
#     nome = models.CharField(max_length=100)
#     valor = models.DecimalField(max_digits=8, decimal_places=2)

TIPO_PAGAMENTO = [
    ('credito', 'Cartão de Crédito'),
    ('debito', 'Cartão de Débito'),
    ('dinheiro', 'Dinheiro à vista'),
    ('pix', 'PIX'),
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

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']

    def __str__(self):
        return self.nome   


