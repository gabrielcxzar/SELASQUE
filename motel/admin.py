from django.contrib import admin
from .models import Cliente, Quarto, Reserva, Produto, Pagamento, Funcionario, Consumo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email', 'data_cadastro')
    search_fields = ('nome', 'cpf')


@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display=('numero', 'tipo','valor')
    search_fields=('numero', 'tipo')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display=('quarto','cliente','data_entrada','data_saida','pago')
    search_fields=('cliente__nome','quarto__numero')
    list_filter=('pago',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display=('nome', 'valor')
    search_fields=('nome', 'valor')

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display=('reserva', 'tipo')
    search_fields=('reserva__id', 'tipo')

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email', 'tipo')
    search_fields = ('nome', 'cpf', 'tipo')

@admin.register(Consumo)
class ConsumoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'quarto_numero', 'quantidade',  'reserva')
    search_fields = ('produto__nome', 'reserva__quarto__numero', 'reserva__quarto__tipo')
    def quarto_numero(self, obj):
        return obj.reserva.quarto.numero
    quarto_numero.short_description = 'Quarto'

from .models import Cliente, Quarto, Reserva, Pagamento, Funcionario

# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'email', 'telefone', 'data_nascimento', 'esta_ativo', 'data_cadastro')
    search_fields = ('nome', 'cpf', 'email')
    list_filter = ('esta_ativo', 'data_cadastro')
    ordering = ('nome',)

@admin.register(Quarto)
class QuartoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo', 'preco_hora', 'preco_periodo', 'preco_pernoite', 'capacidade', 'status', 'esta_ativo')
    search_fields = ('numero', 'tipo')
    list_filter = ('status', 'tipo', 'esta_ativo')
    ordering = ('tipo', 'numero')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'quarto', 'tipo_reserva', 'entrada', 'saida', 'status', 'status_pagamento', 'valor_total')
    search_fields = ('cliente__nome', 'quarto__numero', 'tipo_reserva')
    list_filter = ('status', 'tipo_reserva', 'status_pagamento')
    ordering = ('-entrada',)

@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'tipo',)
    search_fields = ('reserva__cliente__nome', 'tipo')
    list_filter = ('tipo',)
    ordering = ('-reserva__entrada',)



@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'tipo')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('tipo',)
    ordering = ('nome',)
