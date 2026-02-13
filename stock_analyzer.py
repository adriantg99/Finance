import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


class StockAnalyzer:
    """Analizador de acciones con estrategias basadas en indicadores técnicos"""
    
    def __init__(self, period="10y"):
        self.period = period
        
    def download_data(self, symbol: str) -> pd.DataFrame:
        """Descarga datos históricos de una acción"""
        try:
            df = yf.download(symbol, period=self.period, progress=False)
            if df.empty:
                return None
            # Asegurarse de que las columnas son simples, no MultiIndex
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        except:
            return None
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula indicadores técnicos"""
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Medias móviles
        df['MA20'] = df['Close'].rolling(20).mean()
        df['MA50'] = df['Close'].rolling(50).mean()
        df['MA200'] = df['Close'].rolling(200).mean()
        
        # MACD
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # Bollinger Bands
        df['BB_middle'] = df['Close'].rolling(20).mean()
        df['BB_std'] = df['Close'].rolling(20).std()
        df['BB_upper'] = df['BB_middle'] + (df['BB_std'] * 2)
        df['BB_lower'] = df['BB_middle'] - (df['BB_std'] * 2)
        
        # Volatilidad
        df['Volatility'] = df['Close'].pct_change().rolling(20).std()
        
        return df
    
    def calculate_future_returns(self, df: pd.DataFrame, horizon: int) -> pd.DataFrame:
        """Calcula retornos futuros"""
        df[f'Return_{horizon}d'] = df['Close'].shift(-horizon) / df['Close'] - 1
        return df
    
    def strategy_oversold_rsi(self, df: pd.DataFrame) -> pd.Series:
        """Estrategia: RSI sobrevendido con tendencia alcista"""
        return (
            (df['RSI'] < 35) &
            (df['MA20'] > df['MA50']) &
            (df['Close'] > df['MA20'])
        )
    
    def strategy_golden_cross(self, df: pd.DataFrame) -> pd.Series:
        """Estrategia: Cruce dorado (MA50 cruza por encima de MA200)"""
        return (
            (df['MA50'] > df['MA200']) &
            (df['MA50'].shift(1) <= df['MA200'].shift(1)) &
            (df['RSI'] > 40) & (df['RSI'] < 70)
        )
    
    def strategy_macd_cross(self, df: pd.DataFrame) -> pd.Series:
        """Estrategia: MACD cruza por encima de la señal"""
        return (
            (df['MACD'] > df['Signal']) &
            (df['MACD'].shift(1) <= df['Signal'].shift(1)) &
            (df['RSI'] < 70)
        )
    
    def strategy_bollinger_bounce(self, df: pd.DataFrame) -> pd.Series:
        """Estrategia: Rebote en banda inferior de Bollinger"""
        return (
            (df['Close'] < df['BB_lower']) &
            (df['RSI'] < 40) &
            (df['MA50'] > df['MA200'])
        )
    
    def strategy_strong_momentum(self, df: pd.DataFrame) -> pd.Series:
        """Estrategia: Momento fuerte alcista"""
        return (
            (df['Close'] > df['MA20']) &
            (df['MA20'] > df['MA50']) &
            (df['MA50'] > df['MA200']) &
            (df['RSI'] > 50) & (df['RSI'] < 75) &
            (df['MACD'] > df['Signal'])
        )
    
    def analyze_strategy(self, df: pd.DataFrame, condition: pd.Series, 
                        horizon: int = 15) -> Dict:
        """Analiza el desempeño histórico de una estrategia"""
        df = self.calculate_future_returns(df, horizon)
        
        # Filtrar muestras donde se cumple la condición
        samples = df[condition].copy()
        
        if len(samples) < 10:
            return None
        
        # Calcular métricas
        returns = samples[f'Return_{horizon}d'].dropna()
        
        if len(returns) == 0:
            return None
        
        prob_up = (returns > 0).mean()
        avg_return = returns.mean()
        median_return = returns.median()
        std_return = returns.std()
        max_gain = returns.max()
        max_loss = returns.min()
        
        # Calcular riesgo (desviación estándar de pérdidas)
        losses = returns[returns < 0]
        risk = abs(losses.mean()) if len(losses) > 0 else 0
        
        return {
            'probability': prob_up * 100,
            'avg_return': avg_return * 100,
            'median_return': median_return * 100,
            'std_return': std_return * 100,
            'risk': risk * 100,
            'max_gain': max_gain * 100,
            'max_loss': max_loss * 100,
            'samples': len(returns)
        }
    
    def get_current_signals(self, symbol: str, horizon: int = 15) -> List[Dict]:
        """Obtiene señales de compra actuales para una acción"""
        df = self.download_data(symbol)
        
        if df is None or df.empty:
            return []
        
        df = self.calculate_indicators(df)
        
        strategies = {
            'RSI Sobrevendido': self.strategy_oversold_rsi,
            'Cruce Dorado': self.strategy_golden_cross,
            'MACD Alcista': self.strategy_macd_cross,
            'Rebote Bollinger': self.strategy_bollinger_bounce,
            'Momentum Fuerte': self.strategy_strong_momentum
        }
        
        signals = []
        current_condition = df.iloc[-1]
        
        for strategy_name, strategy_func in strategies.items():
            condition = strategy_func(df)
            
            # Verificar si la condición actual cumple la estrategia
            if condition.iloc[-1]:
                metrics = self.analyze_strategy(df, condition, horizon)
                
                if metrics and metrics['probability'] > 50:
                    signals.append({
                        'symbol': symbol,
                        'strategy': strategy_name,
                        'probability': metrics['probability'],
                        'risk': metrics['risk'],
                        'avg_return': metrics['avg_return'],
                        'max_loss': metrics['max_loss'],
                        'samples': metrics['samples'],
                        'current_price': current_condition['Close'],
                        'rsi': current_condition['RSI']
                    })
        
        return signals


class StockRecommender:
    """Generador de recomendaciones de compra"""
    
    def __init__(self):
        self.analyzer = StockAnalyzer()
    
    def analyze_multiple_stocks(self, symbols: List[str], 
                                horizon: int = 15) -> List[Dict]:
        """Analiza múltiples acciones y genera recomendaciones"""
        all_signals = []
        
        print(f"🔍 Analizando {len(symbols)} acciones...\n")
        
        for symbol in symbols:
            print(f"Procesando {symbol}...", end=" ")
            signals = self.analyzer.get_current_signals(symbol, horizon)
            
            if signals:
                all_signals.extend(signals)
                print(f"✓ {len(signals)} señal(es) encontrada(s)")
            else:
                print("✗ Sin señales")
        
        # Ordenar por probabilidad y riesgo
        all_signals.sort(key=lambda x: (x['probability'], -x['risk']), reverse=True)
        
        return all_signals
    
    def print_recommendations(self, signals: List[Dict], horizon: int = 15):
        """Imprime recomendaciones en formato legible"""
        if not signals:
            print("\n❌ No se encontraron oportunidades de compra en este momento.\n")
            return
        
        print("\n" + "="*80)
        print("📈 RECOMENDACIONES DE COMPRA")
        print("="*80 + "\n")
        
        for i, signal in enumerate(signals, 1):
            color = self._get_color_by_probability(signal['probability'])
            
            print(f"{i}. {signal['symbol']} - Estrategia: {signal['strategy']}")
            print(f"   {color}{'='*70}{self._reset()}")
            
            message = (
                f"   Según esta estrategia, {signal['symbol']} tiene "
                f"{signal['probability']:.0f}% probabilidad histórica de subir "
                f"en los próximos {horizon} días, con un riesgo del {signal['risk']:.1f}%."
            )
            print(message)
            
            print(f"\n   📊 Detalles:")
            print(f"      • Precio actual: ${signal['current_price']:.2f}")
            print(f"      • RSI: {signal['rsi']:.1f}")
            print(f"      • Retorno promedio esperado: {signal['avg_return']:.2f}%")
            print(f"      • Pérdida máxima histórica: {signal['max_loss']:.2f}%")
            print(f"      • Muestras históricas: {signal['samples']}")
            
            # Recomendación
            if signal['probability'] >= 70 and signal['risk'] < 10:
                recommendation = "🟢 COMPRA FUERTE"
            elif signal['probability'] >= 65 and signal['risk'] < 15:
                recommendation = "🟡 COMPRA MODERADA"
            else:
                recommendation = "🟠 COMPRA CAUTELOSA"
            
            print(f"\n   {recommendation}\n")
        
        print("="*80 + "\n")
    
    def _get_color_by_probability(self, prob: float) -> str:
        """Retorna código de color según probabilidad"""
        if prob >= 70:
            return "\033[92m"  # Verde
        elif prob >= 60:
            return "\033[93m"  # Amarillo
        else:
            return "\033[94m"  # Azul
    
    def _reset(self) -> str:
        """Resetea color"""
        return "\033[0m"
    
    def export_to_csv(self, signals: List[Dict], filename: str = "recomendaciones.csv"):
        """Exporta recomendaciones a CSV"""
        if not signals:
            print("No hay señales para exportar.")
            return
        
        df = pd.DataFrame(signals)
        df.to_csv(filename, index=False)
        print(f"\n💾 Recomendaciones guardadas en: {filename}")


def main():
    """Función principal"""
    # Lista de acciones populares para analizar
    symbols = [
        # Tecnología
        'TSLA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'AMD',
        # Finanzas
        'JPM', 'BAC', 'GS', 'V', 'MA',
        # Consumo
        'WMT', 'HD', 'NKE', 'MCD', 'SBUX',
        # Salud
        'JNJ', 'PFE', 'UNH', 'ABBV',
        # Energía
        'XOM', 'CVX',
    ]
    
    # Crear recomendador
    recommender = StockRecommender()
    
    # Analizar acciones
    horizon = 15  # días
    signals = recommender.analyze_multiple_stocks(symbols, horizon)
    
    # Mostrar recomendaciones
    recommender.print_recommendations(signals, horizon)
    
    # Exportar a CSV
    if signals:
        recommender.export_to_csv(signals)


if __name__ == "__main__":
    main()
