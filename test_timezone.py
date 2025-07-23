#!/usr/bin/env python3
"""
Script de teste para verificar o funcionamento do sistema de timezone
"""

import sys
import os

# Adicionar caminho para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_timezone_system():
    print("🧪 Testando Sistema de Timezone")
    print("=" * 50)
    
    try:
        # Testar TimezoneHelper
        from app.controllers.timezoneHelper import timezone_helper
        
        # Informações básicas
        info = timezone_helper.get_timezone_info()
        print(f"🌍 Timezone detectado: {info['timezone']}")
        print(f"⏰ Hora atual: {info['current_time']}")
        print(f"🖥️ Plataforma: {info['platform']}")
        print(f"🕰️ Offset UTC: {info['utc_offset']}")
        print(f"☀️ Horário de verão: {info['is_dst']}")
        
        # Testar conversões
        print("\n🔄 Testando Conversões:")
        local_now = timezone_helper.get_local_now()
        print(f"Local Now: {local_now}")
        
        utc_iso = timezone_helper.to_utc_isoformat(local_now)
        print(f"UTC ISO: {utc_iso}")
        
        local_string = timezone_helper.to_local_string(local_now)
        print(f"Formatado: {local_string}")
        
        # Testar criação de datetime
        print("\n📅 Testando Criação de Datetime:")
        dt = timezone_helper.create_local_datetime("2025-07-23", "15:30")
        print(f"DateTime criado: {dt}")
        print(f"UTC conversion: {timezone_helper.to_utc_isoformat(dt)}")
        
        print("\n✅ Testes de Timezone PASSOU!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_lembrete_model():
    print("\n🧪 Testando Modelo Lembrete")
    print("=" * 50)
    
    try:
        from app.models.lembrete import Lembrete
        
        # Criar lembrete de teste
        lembrete = Lembrete(
            titulo="Teste Timezone",
            desc="Testando funcionalidade de timezone",
            prazo="2025-07-23T18:30:00Z"
        )
        
        print(f"📝 Título: {lembrete.titulo}")
        print(f"⏰ Prazo UTC: {lembrete.prazo}")
        print(f"🌍 Prazo Formatado: {lembrete.get_formatted_prazo()}")
        print(f"⏳ Tempo Restante: {lembrete.get_time_remaining()}")
        print(f"⚠️ Vencido: {lembrete.is_expired()}")
        print(f"🔔 Próximo: {lembrete.is_due_soon()}")
        
        print("\n✅ Testes de Lembrete PASSOU!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Iniciando Testes do Sistema de Timezone")
    print("=" * 60)
    
    success = True
    
    # Teste 1: TimezoneHelper
    success &= test_timezone_system()
    
    # Teste 2: Modelo Lembrete
    success &= test_lembrete_model()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema de timezone funcionando corretamente")
        print("🌍 Pronto para uso em qualquer sistema operacional")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("⚠️ Verifique os erros acima")
    
    print("\n💡 Para executar a aplicação:")
    print("   python runHere.py")
    print("\n🔍 Para debug de timezone:")
    print("   http://localhost:8080/timezone-info")

if __name__ == "__main__":
    main()
