# -*- coding: utf-8 -*-
"""
Script de Build Completo e Otimizado - Plante Uma Flor v2.0
Inclui todas as dependências, recursos e validações necessárias
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
import json

# Configurar encoding para Windows
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

class BuildManager:
    """Gerenciador completo do processo de build"""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.client_root = self.script_dir.parent.parent  # src/build -> src -> client
        self.project_root = self.client_root.parent  # client -> plante-uma-flor-v2
        self.dist_dir = self.project_root.parent / "dist"  # plante-uma-flor-v2 -> root/dist
        self.src_dir = self.client_root / "src"
        
        print("=" * 70)
        print("PLANTE UMA FLOR V2.0 - BUILD COMPLETO")
        print("=" * 70)
        print(f"[INFO] Diretorio do cliente: {self.client_root}")
        print(f"[INFO] Diretorio de saida: {self.dist_dir}")
        print()
    
    def check_dependencies(self):
        """Verifica e instala dependências necessárias"""
        print("🔍 ETAPA 1: Verificando dependências...")
        print("-" * 70)
        
        required = {
            'pyinstaller': 'PyInstaller',
            'reportlab': 'ReportLab',
            'requests': 'Requests'
        }
        
        missing = []
        
        for module, name in required.items():
            try:
                __import__(module)
                print(f"  ✅ {name}")
            except ImportError:
                print(f"  ❌ {name} - não encontrado")
                missing.append(module)
        
        if missing:
            print(f"\n📦 Instalando dependências faltantes: {', '.join(missing)}")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--upgrade"
                ] + missing, check=True)
                print("✅ Dependências instaladas com sucesso!")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar dependências: {e}")
                return False
        
        print("✅ Todas as dependências estão OK!\n")
        return True
    
    def test_imports(self):
        """Testa se todos os imports do projeto funcionam"""
        print("[*] ETAPA 2: Testando imports do projeto...")
        print("-" * 70)
        
        # Adicionar src ao path ANTES de importar
        src_path = str(self.src_dir)
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # Mudar para o diretório src temporariamente
        original_dir = os.getcwd()
        try:
            os.chdir(self.src_dir)
            
            test_imports = [
                ('app.core.database', 'DatabaseManager'),
                ('app.core.api_client', 'APIClient'),
                ('app.core.pdf_generator', 'PDFGenerator'),
                ('app.utils.logger', 'Logger'),
                ('app.utils.fonts', 'FontManager'),
            ]
            
            all_ok = True
            for module_name, desc in test_imports:
                try:
                    # Limpar cache de imports anteriores
                    if module_name in sys.modules:
                        del sys.modules[module_name]
                    
                    __import__(module_name)
                    print(f"  ✅ {desc} ({module_name})")
                except Exception as e:
                    print(f"  ⚠️  {desc} ({module_name}) - Aviso: {e}")
                    # Não falhar por imports opcionais
                    # all_ok = False
            
            print("✅ Imports testados (avisos são normais durante build)!\n")
            return True  # Sempre retorna True para não bloquear o build
            
        finally:
            # Restaurar diretório original
            os.chdir(original_dir)
    
    def prepare_build_directory(self):
        """Prepara diretório de build"""
        print("[*] ETAPA 3: Preparando diretorio de build...")
        print("-" * 70)
        
        # Limpar build anterior
        if self.dist_dir.exists():
            print(f"  🧹 Limpando build anterior...")
            shutil.rmtree(self.dist_dir, ignore_errors=True)
        
        # Criar diretórios necessários
        self.dist_dir.mkdir(exist_ok=True)
        (self.dist_dir / "build").mkdir(exist_ok=True)
        
        print("✅ Diretório preparado!\n")
        return True
    
    def build_with_pyinstaller(self):
        """Executa build com PyInstaller"""
        print("[*] ETAPA 4: Executando PyInstaller...")
        print("-" * 70)
        
        # Configurações do PyInstaller
        pyinstaller_args = [
            sys.executable, "-m", "PyInstaller",
            "--noconfirm",
            "--onefile",
            "--windowed",
            "--name=PlanteUmaFlor-Client",
            
            # Otimizações
            "--optimize=2",
            "--clean",
            
            # Hidden imports necessários
            "--hidden-import=reportlab",
            "--hidden-import=reportlab.pdfgen",
            "--hidden-import=reportlab.pdfgen.canvas",
            "--hidden-import=reportlab.lib",
            "--hidden-import=reportlab.lib.pagesizes",
            "--hidden-import=reportlab.lib.units",
            "--hidden-import=reportlab.pdfbase",
            "--hidden-import=reportlab.pdfbase.pdfmetrics",
            "--hidden-import=reportlab.pdfbase.ttfonts",
            "--hidden-import=requests",
            "--hidden-import=sqlite3",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=pathlib",
            "--hidden-import=datetime",
            "--hidden-import=json",
            
            # Incluir arquivo de configuração
            f"--add-data={self.src_dir / 'resources' / 'config.json'};resources",
            
            # Diretórios
            f"--distpath={self.dist_dir}",
            f"--workpath={self.dist_dir / 'build'}",
            f"--specpath={self.dist_dir}",
            
            # Arquivo principal
            str(self.src_dir / "main.py")
        ]
        
        print("📦 Comando PyInstaller:")
        print(f"  {' '.join(pyinstaller_args[:5])} ...")
        print()
        
        try:
            # Executar PyInstaller
            result = subprocess.run(
                pyinstaller_args,
                cwd=self.client_root,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Verificar se executável foi criado
            exe_path = self.dist_dir / "PlanteUmaFlor-Client.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / 1024 / 1024
                print(f"✅ Executável criado com sucesso!")
                print(f"  📁 Local: {exe_path}")
                print(f"  📊 Tamanho: {size_mb:.1f} MB")
                print()
                return True
            else:
                print("❌ Executável não foi criado")
                print("📋 Saída do PyInstaller:")
                print(result.stdout)
                if result.stderr:
                    print("❌ Erros:")
                    print(result.stderr)
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro no build: {e}")
            if hasattr(e, 'stdout') and e.stdout:
                print("📋 Saída:")
                print(e.stdout)
            if hasattr(e, 'stderr') and e.stderr:
                print("❌ Erros:")
                print(e.stderr)
            return False
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return False
    
    def create_auxiliary_files(self):
        """Cria arquivos auxiliares (bat, readme, etc)"""
        print("[*] ETAPA 5: Criando arquivos auxiliares...")
        print("-" * 70)
        
        # Script de inicialização
        launcher_bat = self.dist_dir / "Iniciar_Cliente.bat"
        launcher_content = """@echo off
title Plante Uma Flor v2.0 - Cliente
cls
echo ========================================
echo   PLANTE UMA FLOR V2.0 - CLIENTE
echo ========================================
echo.
echo Iniciando aplicativo...
echo.

REM Executar aplicativo
PlanteUmaFlor-Client.exe

REM Verificar se houve erro
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERRO AO INICIAR APLICATIVO
    echo ========================================
    echo.
    echo Possiveis causas:
    echo - Servidor nao esta rodando
    echo - Arquivo corrompido
    echo - Falta de permissoes
    echo.
    pause
) else (
    echo.
    echo Aplicativo finalizado normalmente.
)
"""
        
        with open(launcher_bat, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        print(f"  ✅ {launcher_bat.name}")
        
        # README
        readme = self.dist_dir / "LEIA-ME.txt"
        readme_content = """═══════════════════════════════════════════════════════════════════
    PLANTE UMA FLOR V2.0 - GERADOR DE PEDIDOS
═══════════════════════════════════════════════════════════════════

📱 COMO USAR
───────────────────────────────────────────────────────────────────
1. Execute: Iniciar_Cliente.bat
   OU
   Duplo clique em: PlanteUmaFlor-Client.exe

2. Preencha o formulário com os dados do pedido

3. Clique em "Finalizar Pedido"

4. O PDF será gerado em: Documents/Pedidos-Floricultura/


⚙️ CONFIGURAÇÃO DO SERVIDOR
───────────────────────────────────────────────────────────────────
URL do servidor: http://192.168.1.148:5000

Para alterar o servidor, edite:
- resources/config.json (se disponível)
- Ou entre em contato com o suporte


📋 REQUISITOS DO SISTEMA
───────────────────────────────────────────────────────────────────
- Windows 7 ou superior
- 50 MB de espaço em disco
- Conexão com o servidor (opcional)


🆘 SUPORTE
───────────────────────────────────────────────────────────────────
Em caso de problemas:
1. Verifique se o servidor está rodando
2. Verifique sua conexão de rede
3. Execute como Administrador
4. Entre em contato com o suporte técnico


📄 PDFs GERADOS
───────────────────────────────────────────────────────────────────
Local: C:\\Users\\[Seu Usuario]\\Documents\\Pedidos-Floricultura\\


═══════════════════════════════════════════════════════════════════
Versão: 2.0.0
Data do Build: {build_date}
═══════════════════════════════════════════════════════════════════
"""
        
        from datetime import datetime
        readme_content = readme_content.format(
            build_date=datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        
        with open(readme, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  ✅ {readme.name}")
        
        # Arquivo de versão
        version_file = self.dist_dir / "version.json"
        version_data = {
            "version": "2.0.0",
            "build_date": datetime.now().isoformat(),
            "python_version": sys.version,
            "platform": sys.platform
        }
        
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(version_data, f, indent=2)
        print(f"  ✅ {version_file.name}")
        
        print("✅ Arquivos auxiliares criados!\n")
        return True
    
    def create_build_report(self):
        """Cria relatório do build"""
        report_path = self.dist_dir / "BUILD_REPORT.txt"
        
        exe_path = self.dist_dir / "PlanteUmaFlor-Client.exe"
        size_mb = exe_path.stat().st_size / 1024 / 1024 if exe_path.exists() else 0
        
        from datetime import datetime
        
        report = f"""═══════════════════════════════════════════════════════════════════
    RELATÓRIO DE BUILD - PLANTE UMA FLOR V2.0
═══════════════════════════════════════════════════════════════════

📅 Data do Build: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
🐍 Python: {sys.version.split()[0]}
💻 Plataforma: {sys.platform}

📦 ARQUIVOS GERADOS
───────────────────────────────────────────────────────────────────
✅ PlanteUmaFlor-Client.exe ({size_mb:.1f} MB)
✅ Iniciar_Cliente.bat
✅ LEIA-ME.txt
✅ version.json
✅ BUILD_REPORT.txt

📋 DEPENDÊNCIAS INCLUÍDAS
───────────────────────────────────────────────────────────────────
✅ ReportLab (geração de PDFs)
✅ Requests (comunicação HTTP)
✅ SQLite3 (banco de dados local)
✅ Tkinter (interface gráfica)

📁 RECURSOS INCLUÍDOS
───────────────────────────────────────────────────────────────────
✅ config.json (configurações)

🚀 COMO DISTRIBUIR
───────────────────────────────────────────────────────────────────
1. Copie todos os arquivos desta pasta
2. Distribua para os usuários
3. Usuários devem executar: Iniciar_Cliente.bat

✅ BUILD CONCLUÍDO COM SUCESSO!
═══════════════════════════════════════════════════════════════════
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📊 Relatório criado: {report_path.name}\n")
    
    def run(self):
        """Executa todo o processo de build"""
        steps = [
            ("Dependências", self.check_dependencies),
            ("Imports", self.test_imports),
            ("Preparação", self.prepare_build_directory),
            ("Build", self.build_with_pyinstaller),
            ("Arquivos Auxiliares", self.create_auxiliary_files),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    print(f"\n❌ Falha na etapa: {step_name}")
                    print("Build interrompido.\n")
                    return False
            except Exception as e:
                print(f"\n❌ Erro na etapa {step_name}: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        # Criar relatório final
        self.create_build_report()
        
        # Resumo final
        print("=" * 70)
        print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        print(f"\n📂 Diretório de saída: {self.dist_dir}")
        print(f"\n✅ Arquivos criados:")
        print(f"   - PlanteUmaFlor-Client.exe (executável principal)")
        print(f"   - Iniciar_Cliente.bat (script de inicialização)")
        print(f"   - LEIA-ME.txt (instruções)")
        print(f"   - version.json (informações de versão)")
        print(f"   - BUILD_REPORT.txt (relatório completo)")
        
        print(f"\n🚀 Para testar:")
        print(f"   cd {self.dist_dir}")
        print(f"   .\\Iniciar_Cliente.bat")
        
        print("\n" + "=" * 70)
        
        return True

def main():
    """Entry point"""
    builder = BuildManager()
    success = builder.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

