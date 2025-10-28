# -*- coding: utf-8 -*-
"""
Cliente API otimizado para comunicação com servidor
"""
import requests
import json
from typing import Dict, Optional
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

class APIClient:
    """Cliente API com retry e timeout otimizados"""
    
    def __init__(self, base_url: str = "http://192.168.1.148:5000", timeout: int = 5):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Headers padrão
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'PlanteUmaFlor-Client/2.0'
        })
    
    def send_pedido(self, pedido_data: Dict) -> Optional[Dict]:
        """Envia pedido para o servidor"""
        try:
            # Preparar dados para envio
            api_data = {
                "cliente": pedido_data.get("cliente", ""),
                "produto": pedido_data.get("produto", ""),
                "quantidade": pedido_data.get("quantidade", 1),
                "horario": pedido_data.get("hora_entrega", ""),
                "dia_entrega": pedido_data.get("data_entrega", ""),
                "destinatario": pedido_data.get("destinatario", ""),
                "mensagem": pedido_data.get("mensagem", "")
            }
            
            # Enviar requisição
            response = self.session.post(
                f"{self.base_url}/api/pedidos",
                json=api_data,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Pedido enviado com sucesso: {result.get('pedido_id')}")
            return result
            
        except requests.exceptions.ConnectionError:
            logger.warning("Servidor não está acessível - pedido salvo apenas localmente")
            return None
        except requests.exceptions.Timeout:
            logger.warning("Timeout na comunicação com servidor")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erro HTTP {e.response.status_code}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Erro ao enviar pedido: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Testa conexão com servidor"""
        try:
            response = self.session.get(
                f"{self.base_url}/",
                timeout=self.timeout
            )
            return response.status_code == 200
        except Exception as e:
            logger.debug(f"Teste de conexão falhou: {e}")
            return False
    
    def close(self):
        """Fecha sessão HTTP"""
        self.session.close()