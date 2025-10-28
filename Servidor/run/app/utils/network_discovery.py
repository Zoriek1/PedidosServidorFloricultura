# -*- coding: utf-8 -*-
"""
Sistema de Descoberta de Rede via UDP Broadcast
Permite que clientes encontrem o servidor automaticamente na rede local
"""
import socket
import json
import threading
import time
import logging

# Logger lazy - só inicializa quando necessário
_logger = None

def get_logger():
    """Retorna logger (lazy initialization)"""
    global _logger
    if _logger is None:
        from app.utils.logger import setup_logger
        _logger = setup_logger(__name__)
    return _logger

class NetworkDiscovery:
    """
    Servidor de descoberta de rede via UDP broadcast
    Anuncia presença do servidor na rede local periodicamente
    """
    
    def __init__(self, port=5000, broadcast_port=37020, interval=5):
        """
        Args:
            port: Porta do servidor Flask
            broadcast_port: Porta para broadcasts UDP
            interval: Intervalo entre broadcasts (segundos)
        """
        self.port = port
        self.broadcast_port = broadcast_port
        self.interval = interval
        self.running = False
        self.thread = None
        self.sock = None
        
    def get_local_ip(self):
        """
        Detecta o IP local da máquina na rede
        
        Returns:
            str: Endereço IP local (ex: 192.168.1.100)
        """
        try:
            # Truque: conectar a um endereço externo para descobrir IP local
            # Não precisa realmente estabelecer conexão
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            get_logger().warning(f"Erro ao detectar IP local: {e}. Usando 127.0.0.1")
            return "127.0.0.1"
    
    def start(self):
        """Inicia o serviço de broadcast"""
        if self.running:
            get_logger().warning("NetworkDiscovery já está rodando")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        self.thread.start()
        get_logger().info(f"NetworkDiscovery iniciado na porta {self.broadcast_port}")
    
    def stop(self):
        """Para o serviço de broadcast"""
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
        if self.thread:
            self.thread.join(timeout=2)
        get_logger().info("NetworkDiscovery parado")
    
    def _broadcast_loop(self):
        """Loop principal de broadcast"""
        try:
            # Criar socket UDP
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            get_logger().info("Socket UDP criado para broadcast")
            
            while self.running:
                try:
                    # Obter IP atual
                    local_ip = self.get_local_ip()
                    
                    # Criar mensagem de broadcast
                    message = {
                        "service": "plante-uma-flor-server",
                        "ip": local_ip,
                        "port": self.port,
                        "timestamp": time.time()
                    }
                    
                    # Serializar para JSON
                    data = json.dumps(message).encode('utf-8')
                    
                    # Enviar broadcast
                    self.sock.sendto(data, ('<broadcast>', self.broadcast_port))
                    
                    get_logger().debug(f"Broadcast enviado: {local_ip}:{self.port}")
                    
                    # Aguardar próximo intervalo
                    time.sleep(self.interval)
                    
                except Exception as e:
                    get_logger().error(f"Erro ao enviar broadcast: {e}")
                    time.sleep(self.interval)
                    
        except Exception as e:
            get_logger().error(f"Erro fatal no broadcast loop: {e}")
        finally:
            if self.sock:
                try:
                    self.sock.close()
                except Exception:
                    pass


class NetworkDiscoveryClient:
    """
    Cliente de descoberta de rede
    Escuta broadcasts e descobre servidores disponíveis
    Para uso no PDFgen.py (cliente desktop)
    """
    
    def __init__(self, broadcast_port=37020, timeout=10):
        """
        Args:
            broadcast_port: Porta para escutar broadcasts
            timeout: Tempo máximo para procurar servidor (segundos)
        """
        self.broadcast_port = broadcast_port
        self.timeout = timeout
        self.sock = None
        
    def discover_server(self):
        """
        Descobre servidor na rede local
        
        Returns:
            dict: Informações do servidor encontrado ou None
                  {"ip": "192.168.1.100", "port": 5000}
        """
        get_logger().info(f"Procurando servidor na porta {self.broadcast_port}...")
        
        try:
            # Criar socket UDP
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', self.broadcast_port))
            self.sock.settimeout(self.timeout)
            
            start_time = time.time()
            
            while time.time() - start_time < self.timeout:
                try:
                    # Receber broadcast
                    data, addr = self.sock.recvfrom(1024)
                    message = json.loads(data.decode('utf-8'))
                    
                    # Verificar se é o serviço correto
                    if message.get('service') == 'plante-uma-flor-server':
                        server_info = {
                            'ip': message.get('ip'),
                            'port': message.get('port'),
                            'timestamp': message.get('timestamp')
                        }
                        
                        get_logger().info(f"Servidor encontrado: {server_info['ip']}:{server_info['port']}")
                        return server_info
                        
                except socket.timeout:
                    get_logger().warning("Timeout ao procurar servidor")
                    break
                except json.JSONDecodeError:
                    get_logger().warning("Broadcast recebido com formato inválido")
                    continue
                except Exception as e:
                    get_logger().error(f"Erro ao receber broadcast: {e}")
                    continue
                    
            get_logger().warning("Nenhum servidor encontrado")
            return None
            
        except Exception as e:
            get_logger().error(f"Erro ao descobrir servidor: {e}")
            return None
        finally:
            if self.sock:
                try:
                    self.sock.close()
                except Exception:
                    pass
    
    def discover_with_fallback(self, fallback_ips=None):
        """
        Tenta descobrir servidor via broadcast, com fallback para IPs comuns
        
        Args:
            fallback_ips: Lista de IPs para tentar se broadcast falhar
            
        Returns:
            str: URL do servidor (ex: "http://192.168.1.100:5000")
        """
        if fallback_ips is None:
            fallback_ips = [
                "192.168.1.100", "192.168.1.101", "192.168.1.105",
                "192.168.0.100", "192.168.0.101", 
                "10.0.0.100", "10.0.0.101",
                "127.0.0.1"
            ]
        
        # Tentar broadcast primeiro
        server_info = self.discover_server()
        if server_info:
            return f"http://{server_info['ip']}:{server_info['port']}"
        
        # Fallback: tentar IPs comuns
        get_logger().info("Tentando IPs comuns como fallback...")
        import requests
        
        for ip in fallback_ips:
            try:
                url = f"http://{ip}:5000/api/stats"
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    get_logger().info(f"Servidor encontrado via fallback: {ip}:5000")
                    return f"http://{ip}:5000"
            except Exception:
                continue
        
        get_logger().error("Não foi possível encontrar o servidor")
        return None

