"""
Validadores de dados.

Este módulo contém funções para validação de dados como CPF, email, etc.
"""

import re
from datetime import date


def validate_cpf(cpf):
    """
    Validar CPF brasileiro.
    
    Args:
        cpf (str): CPF a ser validado (apenas números)
        
    Returns:
        bool: True se o CPF for válido, False caso contrário
    """
    # Remover caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    # Verificar se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verificar se todos os dígitos são iguais (CPF inválido)
    if cpf == cpf[0] * 11:
        return False
    
    # Calcular primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    primeiro_digito = 0 if resto < 2 else 11 - resto
    
    # Verificar primeiro dígito
    if int(cpf[9]) != primeiro_digito:
        return False
    
    # Calcular segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    segundo_digito = 0 if resto < 2 else 11 - resto
    
    # Verificar segundo dígito
    if int(cpf[10]) != segundo_digito:
        return False
    
    return True


def validate_email(email):
    """
    Validar email.
    
    Args:
        email (str): Email a ser validado
        
    Returns:
        bool: True se o email for válido, False caso contrário
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    Validar telefone brasileiro.
    
    Args:
        phone (str): Telefone a ser validado
        
    Returns:
        bool: True se o telefone for válido, False caso contrário
    """
    # Remover caracteres não numéricos
    phone = ''.join(filter(str.isdigit, phone))
    
    # Verificar se tem entre 10 e 11 dígitos
    return len(phone) in [10, 11]


def validate_date_range(start_date, end_date=None):
    """
    Validar se uma data está em um range válido.
    
    Args:
        start_date (date): Data inicial
        end_date (date, optional): Data final (padrão: hoje)
        
    Returns:
        bool: True se a data estiver no range válido
    """
    if end_date is None:
        end_date = date.today()
    
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        return False
    
    return start_date <= end_date


def validate_age_range(birth_date, min_age=0, max_age=120):
    """
    Validar se a idade está em um range válido.
    
    Args:
        birth_date (date): Data de nascimento
        min_age (int): Idade mínima
        max_age (int): Idade máxima
        
    Returns:
        bool: True se a idade estiver no range válido
    """
    if not isinstance(birth_date, date):
        return False
    
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    
    return min_age <= age <= max_age


def format_cpf(cpf):
    """
    Formatar CPF para exibição.
    
    Args:
        cpf (str): CPF sem formatação
        
    Returns:
        str: CPF formatado (000.000.000-00)
    """
    # Remover caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        return cpf
    
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'


def format_phone(phone):
    """
    Formatar telefone para exibição.
    
    Args:
        phone (str): Telefone sem formatação
        
    Returns:
        str: Telefone formatado
    """
    # Remover caracteres não numéricos
    phone = ''.join(filter(str.isdigit, phone))
    
    if len(phone) == 10:
        # Telefone fixo: (11) 1234-5678
        return f'({phone[:2]}) {phone[2:6]}-{phone[6:]}'
    elif len(phone) == 11:
        # Celular: (11) 91234-5678
        return f'({phone[:2]}) {phone[2:7]}-{phone[7:]}'
    
    return phone


def sanitize_string(text, max_length=None):
    """
    Sanitizar string removendo caracteres especiais e limitando tamanho.
    
    Args:
        text (str): Texto a ser sanitizado
        max_length (int, optional): Tamanho máximo do texto
        
    Returns:
        str: Texto sanitizado
    """
    if not text:
        return ''
    
    # Remover espaços extras
    text = ' '.join(text.split())
    
    # Limitar tamanho se especificado
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()


def validate_score_range(score, min_score=1, max_score=10):
    """
    Validar se uma pontuação está no range válido.
    
    Args:
        score (int): Pontuação
        min_score (int): Pontuação mínima
        max_score (int): Pontuação máxima
        
    Returns:
        bool: True se a pontuação estiver no range válido
    """
    if not isinstance(score, int):
        return False
    
    return min_score <= score <= max_score
