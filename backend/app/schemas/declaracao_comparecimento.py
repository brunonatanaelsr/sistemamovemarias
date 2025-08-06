"""
Schemas para serialização/deserialização de Declaração de Comparecimento.

Este módulo contém os schemas Marshmallow para validação e
serialização dos dados de declaração de comparecimento.
"""

from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import datetime, time

from app.schemas.base import BaseSchema


class DeclaracaoComparecimentoSchema(BaseSchema):
    """Schema para Declaração de Comparecimento."""
    
    # Identificação
    id = fields.UUID(dump_only=True, description="ID único da declaração")
    
    # Relacionamentos
    beneficiaria_id = fields.UUID(
        required=True,
        description="ID da beneficiária",
        error_messages={
            'required': 'ID da beneficiária é obrigatório',
            'invalid': 'ID da beneficiária deve ser um UUID válido'
        }
    )
    
    # Dados do comparecimento
    data_comparecimento = fields.DateTime(
        required=True,
        format='%Y-%m-%d',
        description="Data do comparecimento",
        error_messages={
            'required': 'Data do comparecimento é obrigatória',
            'invalid': 'Data deve estar no formato YYYY-MM-DD'
        }
    )
    
    hora_entrada = fields.Time(
        allow_none=True,
        format='%H:%M',
        description="Horário de entrada",
        error_messages={
            'invalid': 'Hora deve estar no formato HH:MM'
        }
    )
    
    hora_saida = fields.Time(
        allow_none=True,
        format='%H:%M',
        description="Horário de saída",
        error_messages={
            'invalid': 'Hora deve estar no formato HH:MM'
        }
    )
    
    profissional_responsavel = fields.String(
        required=True,
        validate=validate.Length(min=2, max=200),
        description="Nome da profissional responsável",
        error_messages={
            'required': 'Nome da profissional responsável é obrigatório',
            'invalid': 'Nome deve ter entre 2 e 200 caracteres'
        }
    )
    
    # Informações adicionais
    observacoes = fields.String(
        allow_none=True,
        validate=validate.Length(max=1000),
        description="Observações sobre o atendimento"
    )
    
    tipo_atendimento = fields.String(
        allow_none=True,
        validate=validate.Length(max=100),
        description="Tipo de atendimento realizado"
    )
    
    # Auditoria
    criado_em = fields.DateTime(dump_only=True, format='iso')
    atualizado_em = fields.DateTime(dump_only=True, format='iso')
    
    @validates_schema
    def validate_horarios(self, data, **kwargs):
        """Valida se horário de saída é posterior ao de entrada."""
        hora_entrada = data.get('hora_entrada')
        hora_saida = data.get('hora_saida')
        
        if hora_entrada and hora_saida:
            if hora_saida <= hora_entrada:
                raise ValidationError(
                    'Horário de saída deve ser posterior ao de entrada',
                    field_name='hora_saida'
                )
    
    @validates_schema
    def validate_data_comparecimento(self, data, **kwargs):
        """Valida se a data de comparecimento não é futura."""
        data_comparecimento = data.get('data_comparecimento')
        
        if data_comparecimento and data_comparecimento.date() > datetime.now().date():
            raise ValidationError(
                'Data de comparecimento não pode ser futura',
                field_name='data_comparecimento'
            )


class DeclaracaoComparecimentoCreateSchema(DeclaracaoComparecimentoSchema):
    """Schema para criação de declaração de comparecimento."""
    
    class Meta:
        exclude = ('id', 'criado_em', 'atualizado_em')


class DeclaracaoComparecimentoUpdateSchema(DeclaracaoComparecimentoSchema):
    """Schema para atualização de declaração de comparecimento."""
    
    # Todos os campos são opcionais na atualização
    beneficiaria_id = fields.UUID(allow_none=True)
    data_comparecimento = fields.DateTime(allow_none=True, format='%Y-%m-%d')
    profissional_responsavel = fields.String(
        allow_none=True,
        validate=validate.Length(min=2, max=200)
    )
    
    class Meta:
        exclude = ('id', 'criado_em', 'atualizado_em')


class DeclaracaoComparecimentoListSchema(Schema):
    """Schema para listagem de declarações de comparecimento."""
    
    id = fields.UUID(description="ID único da declaração")
    beneficiaria_id = fields.UUID(description="ID da beneficiária")
    beneficiaria_nome = fields.String(description="Nome da beneficiária")
    data_comparecimento = fields.DateTime(format='%Y-%m-%d')
    hora_entrada = fields.Time(format='%H:%M', allow_none=True)
    hora_saida = fields.Time(format='%H:%M', allow_none=True)
    profissional_responsavel = fields.String()
    tipo_atendimento = fields.String(allow_none=True)
    criado_em = fields.DateTime(format='iso')


class DeclaracaoComparecimentoReportSchema(Schema):
    """Schema para relatórios de declarações de comparecimento."""
    
    # Dados da beneficiária
    beneficiaria_nome = fields.String()
    beneficiaria_cpf = fields.String()
    
    # Dados da declaração
    data_comparecimento = fields.DateTime(format='%d/%m/%Y')
    hora_entrada = fields.Time(format='%H:%M', allow_none=True)
    hora_saida = fields.Time(format='%H:%M', allow_none=True)
    profissional_responsavel = fields.String()
    tipo_atendimento = fields.String(allow_none=True)
    observacoes = fields.String(allow_none=True)
    
    # Auditoria
    criado_em = fields.DateTime(format='%d/%m/%Y %H:%M')


# Instâncias dos schemas para uso nas rotas
declaracao_comparecimento_schema = DeclaracaoComparecimentoSchema()
declaracao_comparecimento_create_schema = DeclaracaoComparecimentoCreateSchema()
declaracao_comparecimento_update_schema = DeclaracaoComparecimentoUpdateSchema()
declaracao_comparecimento_list_schema = DeclaracaoComparecimentoListSchema(many=True)
declaracao_comparecimento_report_schema = DeclaracaoComparecimentoReportSchema(many=True)
