"""
Script para limpiar los archivos del proyecto de la ubicación anterior
C:\laragon\www\scripts

⚠️  ADVERTENCIA: Este script eliminará los archivos del proyecto de la
ubicación anterior. Asegúrate de que todo funciona en la nueva ubicación
antes de ejecutar este script.
"""

import os
import sys

# Archivos a eliminar
ARCHIVOS_PROYECTO = [
    'inicio_rapido.py',
    'buscar_acciones.py',
    'dashboard.py',
    'stock_analyzer.py',
    'config.py',
    'analizar_personalizado.py',
    'ejemplos_avanzados.py',
    'README_STOCKS.md',
    'GUIA_COMPLETA.md',
    'LEEME.txt',
    'RESUMEN_PROYECTO.py',
    'mis_recomendaciones.csv',
    'dashboard_signals.csv',
    'recomendaciones.csv'
]

RUTA_ANTERIOR = r"C:\laragon\www\scripts"


def main():
    print("\n" + "="*80)
    print("🧹 LIMPIEZA DE UBICACIÓN ANTERIOR")
    print("="*80)
    print(f"\nSe eliminarán los archivos del proyecto de:")
    print(f"📁 {RUTA_ANTERIOR}\n")
    
    # Verificar archivos existentes
    archivos_existentes = []
    for archivo in ARCHIVOS_PROYECTO:
        ruta_completa = os.path.join(RUTA_ANTERIOR, archivo)
        if os.path.exists(ruta_completa):
            archivos_existentes.append(archivo)
    
    if not archivos_existentes:
        print("✅ No se encontraron archivos del proyecto en la ubicación anterior.")
        print("   Posiblemente ya fueron eliminados.\n")
        return
    
    print(f"Se encontraron {len(archivos_existentes)} archivo(s) del proyecto:\n")
    for archivo in archivos_existentes:
        print(f"   • {archivo}")
    
    print("\n" + "="*80)
    print("⚠️  ADVERTENCIA")
    print("="*80)
    print("\nEstos archivos serán ELIMINADOS permanentemente.")
    print("Asegúrate de que el proyecto funciona correctamente en:")
    print(f"📁 C:\\laragon\\www\\Finance")
    print("\nSi no estás seguro, presiona 'n' y haz un respaldo manual primero.\n")
    
    # Confirmar
    respuesta = input("¿Deseas continuar con la eliminación? (s/N): ").strip().lower()
    
    if respuesta != 's':
        print("\n❌ Operación cancelada. No se eliminó ningún archivo.\n")
        return
    
    # Segunda confirmación
    print("\n⚠️  ÚLTIMA CONFIRMACIÓN")
    respuesta2 = input("¿Estás COMPLETAMENTE seguro? (escribe 'ELIMINAR'): ").strip()
    
    if respuesta2 != 'ELIMINAR':
        print("\n❌ Operación cancelada. No se eliminó ningún archivo.\n")
        return
    
    # Proceder con la eliminación
    print("\n🗑️  Eliminando archivos...\n")
    
    eliminados = 0
    errores = 0
    
    for archivo in archivos_existentes:
        ruta_completa = os.path.join(RUTA_ANTERIOR, archivo)
        try:
            os.remove(ruta_completa)
            print(f"✅ Eliminado: {archivo}")
            eliminados += 1
        except Exception as e:
            print(f"❌ Error al eliminar {archivo}: {e}")
            errores += 1
    
    print("\n" + "="*80)
    print("📊 RESUMEN")
    print("="*80)
    print(f"\n✅ Archivos eliminados: {eliminados}")
    print(f"❌ Errores: {errores}")
    
    if eliminados > 0:
        print("\n🎉 Limpieza completada exitosamente.")
        print(f"\nEl proyecto ahora solo existe en:")
        print(f"📁 C:\\laragon\\www\\Finance\n")
    else:
        print("\n⚠️  No se eliminó ningún archivo.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario.\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}\n")
        sys.exit(1)
