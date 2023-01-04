from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from .brd import BRD


class HomeInvestimento(LoginRequiredMixin, TemplateView):
    template_name = 'invest_inicio.html'

    def get_login_url(self) -> str:
        return super().get_login_url()


class Ajuda(LoginRequiredMixin, TemplateView):
    template_name = 'ajuda_inicio.html'
    
    
class Valor_compra(LoginRequiredMixin, TemplateView):
    template_name = 'valor_compra.html'
    calculo_brd = {'Compra':{}, 'Venda':{}}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        brd_ativo = BRD(self.request)
        if brd_ativo.ativo_selecionado.ticket:
            self.monta_tabela_custos(brd_ativo)
        context['calculo_brd'] = self.calculo_brd
        return context
    
    def monta_tabela_custos(self, brd):
        brd.calcular_preco_referencia()
        self.gera_linha_tabela('Compra',brd)
        self.gera_linha_tabela('Venda', brd)
    
    def gera_linha_tabela(self, operacao, brd):
        self.calculo_brd[operacao]['Ticket'] = brd.ativo_selecionado.ticket
        self.calculo_brd[operacao]['USA'] = brd.ativo_selecionado.ticket_original
        self.calculo_brd[operacao]['Desdobramento'] = int(brd.ativo_selecionado.desdobramento)
        self.calculo_brd[operacao]['Custo BRD'] = brd.custos_brd
        self.calculo_brd[operacao]['Preço U$'] = brd.ticket_original_valor_us
        if operacao == 'Venda':
            self.calculo_brd[operacao]['Dolar'] = brd.dolar_compra
            self.calculo_brd[operacao]['Preço Referência'] = '{:.2f}'.format(brd.preco_referencia_venda)
        else:
            self.calculo_brd[operacao]['Dolar'] = brd.dolar_venda
            self.calculo_brd[operacao]['Preço Referência'] = '{:.2f}'.format(brd.preco_referencia_compra)
            
        