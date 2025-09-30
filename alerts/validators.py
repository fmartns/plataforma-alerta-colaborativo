"""
Validators modulares para o app alerts
"""

import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_file_size(file):
    """
    Valida o tamanho do arquivo (máximo 50MB)
    
    Args:
        file: Arquivo a ser validado
        
    Raises:
        ValidationError: Se o arquivo for maior que 50MB
    """
    max_size = 50 * 1024 * 1024
    if file.size > max_size:
        raise ValidationError(f"Arquivo muito grande. Tamanho máximo: 50MB. Tamanho atual: {file.size / (1024*1024):.1f}MB")


def validate_media_type(file):
    """
    Valida se o arquivo é uma imagem ou vídeo válido
    
    Args:
        file: Arquivo a ser validado
        
    Raises:
        ValidationError: Se o tipo de arquivo não for suportado
    """
    if not file:
        return
    
    valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    valid_video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']
    valid_extensions = valid_image_extensions + valid_video_extensions
    
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext not in valid_extensions:
        raise ValidationError(
            f"Tipo de arquivo não suportado: {ext}. "
            f"Tipos válidos: {', '.join(valid_extensions)}"
        )


def validate_coordinates(latitude, longitude):
    """
    Valida coordenadas geográficas
    
    Args:
        latitude: Latitude a ser validada
        longitude: Longitude a ser validada
        
    Raises:
        ValidationError: Se as coordenadas forem inválidas
    """
    if latitude is not None:
        if not (-90 <= float(latitude) <= 90):
            raise ValidationError("Latitude deve estar entre -90 e 90 graus")
    
    if longitude is not None:
        if not (-180 <= float(longitude) <= 180):
            raise ValidationError("Longitude deve estar entre -180 e 180 graus")


def validate_post_content(content):
    """
    Valida o conteúdo do post
    
    Args:
        content: Conteúdo a ser validado
        
    Raises:
        ValidationError: Se o conteúdo for inválido
    """
    if not content or not content.strip():
        raise ValidationError("Conteúdo do post não pode estar vazio")
    
    if len(content.strip()) < 10:
        raise ValidationError("Conteúdo do post deve ter pelo menos 10 caracteres")
    
    if len(content) > 10000:
        raise ValidationError("Conteúdo do post não pode exceder 10.000 caracteres")


def validate_comment_content(content):
    """
    Valida o conteúdo do comentário
    
    Args:
        content: Conteúdo a ser validado
        
    Raises:
        ValidationError: Se o conteúdo for inválido
    """
    if not content or not content.strip():
        raise ValidationError("Comentário não pode estar vazio")
    
    if len(content.strip()) < 3:
        raise ValidationError("Comentário deve ter pelo menos 3 caracteres")
    
    if len(content) > 1000:
        raise ValidationError("Comentário não pode exceder 1.000 caracteres")


def validate_alert_description(description):
    """
    Valida a descrição do alerta
    
    Args:
        description: Descrição a ser validada
        
    Raises:
        ValidationError: Se a descrição for inválida
    """
    if not description or not description.strip():
        raise ValidationError("Descrição do alerta não pode estar vazia")
    
    if len(description.strip()) < 10:
        raise ValidationError("Descrição do alerta deve ter pelo menos 10 caracteres")
    
    if len(description) > 2000:
        raise ValidationError("Descrição do alerta não pode exceder 2.000 caracteres")


def validate_priority(priority):
    """
    Valida a prioridade do alerta
    
    Args:
        priority: Prioridade a ser validada
        
    Raises:
        ValidationError: Se a prioridade for inválida
    """
    valid_priorities = [1, 2, 3, 4]
    if priority not in valid_priorities:
        raise ValidationError(f"Prioridade deve ser uma das opções: {valid_priorities}")


location_validator = RegexValidator(
    regex=r"^[a-zA-ZÀ-ÿ0-9\s\-\,\.]+$",
    message="Localização deve conter apenas letras, números, espaços e pontuação básica",
    code="invalid_location"
)


def validate_florianopolis_location(location):
    """
    Valida se a localização está em Florianópolis (validação básica)
    
    Args:
        location: Localização a ser validada
        
    Raises:
        ValidationError: Se a localização não parecer ser de Florianópolis
    """
    if not location:
        return
    
    florianopolis_keywords = [
        'florianópolis', 'florianopolis', 'fpolis', 'ilha da magia',
        'centro', 'trindade', 'lagoa', 'canasvieiras', 'ingleses',
        'jurerê', 'barra da lagoa', 'campeche', 'pantanal', 'córrego grande',
        'santa mônica', 'carvoeira', 'serrinha', 'joão paulo', 'monte verde',
        'saco grande', 'itacorubi', 'agronômica', 'capoeiras', 'coqueiros',
        'estreito', 'balneário', 'coloninha', 'abraão', 'bom abrigo',
        'canto', 'santinho', 'cachoeira do bom jesus', 'ponta das canas',
        'lagoinha', 'daniela', 'praia brava', 'galheta', 'mole', 'joaquina',
        'armação', 'matadeiro', 'lagoinha do leste', 'pântano do sul',
        'costa de dentro', 'ribeirão da ilha', 'tapera', 'caieira da barra do sul',
        'alto ribeirão', 'sede fragas', 'costeira do pirajubaé', 'saco dos limões',
        'josé mendes', 'prainha', 'bom retiro', 'jardim atlântico',
        'vargem do bom jesus', 'vargem grande', 'vargem pequena',
        'santo antônio de lisboa', 'ratones', 'cacupé', 'sambaqui',
        'barra do sambaqui', 'monte cristo', 'sc', 'santa catarina'
    ]
    
    location_lower = location.lower()
    
    for keyword in florianopolis_keywords:
        if keyword in location_lower:
            return
    
    raise ValidationError(
        "Localização deve estar em Florianópolis. "
        "Inclua o nome do bairro ou região na descrição."
    )


def format_file_size(size_bytes):
    """
    Formata o tamanho do arquivo para exibição
    
    Args:
        size_bytes: Tamanho em bytes
        
    Returns:
        str: Tamanho formatado
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def get_media_info(file):
    """
    Retorna informações sobre o arquivo de mídia
    
    Args:
        file: Arquivo de mídia
        
    Returns:
        dict: Informações do arquivo
    """
    if not file:
        return None
    
    ext = os.path.splitext(file.name)[1].lower()
    
    info = {
        'name': file.name,
        'size': file.size,
        'size_formatted': format_file_size(file.size),
        'extension': ext,
        'type': 'unknown'
    }
    
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        info['type'] = 'image'
    elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']:
        info['type'] = 'video'
    
    return info

