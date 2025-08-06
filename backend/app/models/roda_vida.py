"""
Modelo para Roda da Vida.

A Roda da Vida é uma ferramenta de coaching e desenvolvimento pessoal
que avalia diferentes áreas da vida da beneficiária em uma escala de 0 a 10.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.extensions import db


class RodaVida(db.Model):
    """
    Modelo para avaliação da Roda da Vida.
    
    A Roda da Vida é uma ferramenta visual que permite avaliar
    diferentes áreas da vida em uma escala de 0 a 10, identificando
    áreas de satisfação e áreas que precisam de desenvolvimento.
    """
    
    __tablename__ = 'roda_vida'
    
    # Chave primária
    id = Column(Integer, primary_key=True)
    
    # Relacionamento com beneficiária
    beneficiaria_id = Column(Integer, ForeignKey('beneficiarias.id'), nullable=False)
    beneficiaria = relationship('Beneficiaria', back_populates='rodas_vida')
    
    # Dados da avaliação
    data_avaliacao = Column(DateTime, nullable=False, default=datetime.utcnow)
    profissional_responsavel = Column(String(255), nullable=False)
    observacoes_gerais = Column(Text)
    
    # Áreas da Roda da Vida (escala 0-10)
    # Relacionamentos e Família
    relacionamentos_familia = Column(Float, nullable=True)
    observacoes_relacionamentos = Column(Text)
    
    # Relacionamentos e Amigos
    relacionamentos_amigos = Column(Float, nullable=True)
    observacoes_amigos = Column(Text)
    
    # Amor e Relacionamento Afetivo
    amor_relacionamento = Column(Float, nullable=True)
    observacoes_amor = Column(Text)
    
    # Carreira e Trabalho
    carreira_trabalho = Column(Float, nullable=True)
    observacoes_carreira = Column(Text)
    
    # Finanças
    financas = Column(Float, nullable=True)
    observacoes_financas = Column(Text)
    
    # Saúde e Bem-estar
    saude_bem_estar = Column(Float, nullable=True)
    observacoes_saude = Column(Text)
    
    # Desenvolvimento Pessoal
    desenvolvimento_pessoal = Column(Float, nullable=True)
    observacoes_desenvolvimento = Column(Text)
    
    # Lazer e Diversão
    lazer_diversao = Column(Float, nullable=True)
    observacoes_lazer = Column(Text)
    
    # Espiritualidade
    espiritualidade = Column(Float, nullable=True)
    observacoes_espiritualidade = Column(Text)
    
    # Ambiente Físico
    ambiente_fisico = Column(Float, nullable=True)
    observacoes_ambiente = Column(Text)
    
    # Contribuição Social
    contribuicao_social = Column(Float, nullable=True)
    observacoes_contribuicao = Column(Text)
    
    # Educação e Aprendizado
    educacao_aprendizado = Column(Float, nullable=True)
    observacoes_educacao = Column(Text)
    
    # Análise e objetivos
    areas_prioritarias = Column(Text)
    objetivos_curto_prazo = Column(Text)
    objetivos_medio_prazo = Column(Text)
    objetivos_longo_prazo = Column(Text)
    acoes_imediatas = Column(Text)
    
    # Próxima avaliação
    data_proxima_avaliacao = Column(DateTime)
    
    # Campos de auditoria
    criado_em = Column(DateTime, nullable=False, default=datetime.utcnow)
    atualizado_em = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    criado_por = Column(String(255))
    atualizado_por = Column(String(255))
    ativo = Column(Boolean, nullable=False, default=True)
    
    def __init__(self, **kwargs):
        """Inicializar nova avaliação da Roda da Vida."""
        super().__init__(**kwargs)
    
    def __repr__(self):
        """Representação string do objeto."""
        return f'<RodaVida {self.id} - Beneficiária {self.beneficiaria_id}>'
    
    def to_dict(self):
        """
        Converter objeto para dicionário.
        
        Returns:
            dict: Dados da Roda da Vida
        """
        return {
            'id': self.id,
            'beneficiaria_id': self.beneficiaria_id,
            'data_avaliacao': self.data_avaliacao.isoformat() if self.data_avaliacao else None,
            'profissional_responsavel': self.profissional_responsavel,
            'observacoes_gerais': self.observacoes_gerais,
            'areas': {
                'relacionamentos_familia': {
                    'valor': self.relacionamentos_familia,
                    'observacoes': self.observacoes_relacionamentos
                },
                'relacionamentos_amigos': {
                    'valor': self.relacionamentos_amigos,
                    'observacoes': self.observacoes_amigos
                },
                'amor_relacionamento': {
                    'valor': self.amor_relacionamento,
                    'observacoes': self.observacoes_amor
                },
                'carreira_trabalho': {
                    'valor': self.carreira_trabalho,
                    'observacoes': self.observacoes_carreira
                },
                'financas': {
                    'valor': self.financas,
                    'observacoes': self.observacoes_financas
                },
                'saude_bem_estar': {
                    'valor': self.saude_bem_estar,
                    'observacoes': self.observacoes_saude
                },
                'desenvolvimento_pessoal': {
                    'valor': self.desenvolvimento_pessoal,
                    'observacoes': self.observacoes_desenvolvimento
                },
                'lazer_diversao': {
                    'valor': self.lazer_diversao,
                    'observacoes': self.observacoes_lazer
                },
                'espiritualidade': {
                    'valor': self.espiritualidade,
                    'observacoes': self.observacoes_espiritualidade
                },
                'ambiente_fisico': {
                    'valor': self.ambiente_fisico,
                    'observacoes': self.observacoes_ambiente
                },
                'contribuicao_social': {
                    'valor': self.contribuicao_social,
                    'observacoes': self.observacoes_contribuicao
                },
                'educacao_aprendizado': {
                    'valor': self.educacao_aprendizado,
                    'observacoes': self.observacoes_educacao
                }
            },
            'analise': {
                'areas_prioritarias': self.areas_prioritarias,
                'objetivos_curto_prazo': self.objetivos_curto_prazo,
                'objetivos_medio_prazo': self.objetivos_medio_prazo,
                'objetivos_longo_prazo': self.objetivos_longo_prazo,
                'acoes_imediatas': self.acoes_imediatas
            },
            'data_proxima_avaliacao': self.data_proxima_avaliacao.isoformat() if self.data_proxima_avaliacao else None,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None,
            'ativo': self.ativo
        }
    
    def calcular_media_geral(self):
        """
        Calcular média geral da Roda da Vida.
        
        Returns:
            float: Média das áreas avaliadas
        """
        areas = [
            self.relacionamentos_familia,
            self.relacionamentos_amigos,
            self.amor_relacionamento,
            self.carreira_trabalho,
            self.financas,
            self.saude_bem_estar,
            self.desenvolvimento_pessoal,
            self.lazer_diversao,
            self.espiritualidade,
            self.ambiente_fisico,
            self.contribuicao_social,
            self.educacao_aprendizado
        ]
        
        # Filtrar áreas avaliadas
        areas_avaliadas = [area for area in areas if area is not None]
        
        if not areas_avaliadas:
            return 0.0
        
        return round(sum(areas_avaliadas) / len(areas_avaliadas), 2)
    
    def get_areas_baixas(self, limite=3.0):
        """
        Obter áreas com pontuação baixa.
        
        Args:
            limite (float): Pontuação limite para considerar baixa
            
        Returns:
            list: Lista de áreas com pontuação baixa
        """
        areas_map = {
            'Relacionamentos e Família': self.relacionamentos_familia,
            'Relacionamentos e Amigos': self.relacionamentos_amigos,
            'Amor e Relacionamento': self.amor_relacionamento,
            'Carreira e Trabalho': self.carreira_trabalho,
            'Finanças': self.financas,
            'Saúde e Bem-estar': self.saude_bem_estar,
            'Desenvolvimento Pessoal': self.desenvolvimento_pessoal,
            'Lazer e Diversão': self.lazer_diversao,
            'Espiritualidade': self.espiritualidade,
            'Ambiente Físico': self.ambiente_fisico,
            'Contribuição Social': self.contribuicao_social,
            'Educação e Aprendizado': self.educacao_aprendizado
        }
        
        areas_baixas = []
        for nome, valor in areas_map.items():
            if valor is not None and valor <= limite:
                areas_baixas.append({
                    'area': nome,
                    'valor': valor
                })
        
        # Ordenar por valor (menor primeiro)
        return sorted(areas_baixas, key=lambda x: x['valor'])
    
    def get_areas_altas(self, limite=7.0):
        """
        Obter áreas com pontuação alta.
        
        Args:
            limite (float): Pontuação limite para considerar alta
            
        Returns:
            list: Lista de áreas com pontuação alta
        """
        areas_map = {
            'Relacionamentos e Família': self.relacionamentos_familia,
            'Relacionamentos e Amigos': self.relacionamentos_amigos,
            'Amor e Relacionamento': self.amor_relacionamento,
            'Carreira e Trabalho': self.carreira_trabalho,
            'Finanças': self.financas,
            'Saúde e Bem-estar': self.saude_bem_estar,
            'Desenvolvimento Pessoal': self.desenvolvimento_pessoal,
            'Lazer e Diversão': self.lazer_diversao,
            'Espiritualidade': self.espiritualidade,
            'Ambiente Físico': self.ambiente_fisico,
            'Contribuição Social': self.contribuicao_social,
            'Educação e Aprendizado': self.educacao_aprendizado
        }
        
        areas_altas = []
        for nome, valor in areas_map.items():
            if valor is not None and valor >= limite:
                areas_altas.append({
                    'area': nome,
                    'valor': valor
                })
        
        # Ordenar por valor (maior primeiro)
        return sorted(areas_altas, key=lambda x: x['valor'], reverse=True)
    
    def get_dados_grafico(self):
        """
        Obter dados formatados para gráfico da Roda da Vida.
        
        Returns:
            dict: Dados para gráfico polar/radar
        """
        areas_labels = [
            'Relacionamentos/Família',
            'Amigos',
            'Amor',
            'Carreira',
            'Finanças',
            'Saúde',
            'Desenvolvimento',
            'Lazer',
            'Espiritualidade',
            'Ambiente',
            'Contribuição',
            'Educação'
        ]
        
        valores = [
            self.relacionamentos_familia or 0,
            self.relacionamentos_amigos or 0,
            self.amor_relacionamento or 0,
            self.carreira_trabalho or 0,
            self.financas or 0,
            self.saude_bem_estar or 0,
            self.desenvolvimento_pessoal or 0,
            self.lazer_diversao or 0,
            self.espiritualidade or 0,
            self.ambiente_fisico or 0,
            self.contribuicao_social or 0,
            self.educacao_aprendizado or 0
        ]
        
        return {
            'labels': areas_labels,
            'valores': valores,
            'media': self.calcular_media_geral()
        }
    
    @classmethod
    def get_by_beneficiaria(cls, beneficiaria_id, limit=None):
        """
        Obter avaliações da Roda da Vida de uma beneficiária.
        
        Args:
            beneficiaria_id (int): ID da beneficiária
            limit (int): Limite de registros
            
        Returns:
            list: Lista de avaliações da Roda da Vida
        """
        query = cls.query.filter_by(beneficiaria_id=beneficiaria_id, ativo=True)\
                        .order_by(cls.data_avaliacao.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @classmethod
    def get_ultima_avaliacao(cls, beneficiaria_id):
        """
        Obter última avaliação da Roda da Vida de uma beneficiária.
        
        Args:
            beneficiaria_id (int): ID da beneficiária
            
        Returns:
            RodaVida: Última avaliação ou None
        """
        return cls.query.filter_by(beneficiaria_id=beneficiaria_id, ativo=True)\
                       .order_by(cls.data_avaliacao.desc())\
                       .first()
    
    def validar_dados(self):
        """
        Validar dados da Roda da Vida.
        
        Returns:
            list: Lista de erros encontrados
        """
        erros = []
        
        if not self.profissional_responsavel:
            erros.append('Profissional responsável é obrigatório')
        
        if not self.data_avaliacao:
            erros.append('Data da avaliação é obrigatória')
        
        if self.data_avaliacao and self.data_avaliacao > datetime.utcnow():
            erros.append('Data da avaliação não pode ser futura')
        
        # Validar valores das áreas (0-10)
        areas = [
            ('Relacionamentos/Família', self.relacionamentos_familia),
            ('Amigos', self.relacionamentos_amigos),
            ('Amor', self.amor_relacionamento),
            ('Carreira', self.carreira_trabalho),
            ('Finanças', self.financas),
            ('Saúde', self.saude_bem_estar),
            ('Desenvolvimento', self.desenvolvimento_pessoal),
            ('Lazer', self.lazer_diversao),
            ('Espiritualidade', self.espiritualidade),
            ('Ambiente', self.ambiente_fisico),
            ('Contribuição', self.contribuicao_social),
            ('Educação', self.educacao_aprendizado)
        ]
        
        for nome, valor in areas:
            if valor is not None and (valor < 0 or valor > 10):
                erros.append(f'Valor para {nome} deve estar entre 0 e 10')
        
        if (self.data_proxima_avaliacao and 
            self.data_avaliacao and 
            self.data_proxima_avaliacao <= self.data_avaliacao):
            erros.append('Data da próxima avaliação deve ser posterior à atual')
        
        return erros
