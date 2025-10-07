"""
Views - Interface de Usuário - Projeto Airbnb Rio
=================================================

Este módulo contém as views da aplicação web Streamlit:
- Interface principal da aplicação
- Componentes de entrada de dados
- Visualizações e gráficos
- Componentes reutilizáveis

Autor: Projeto Airbnb Rio
Data: 2024
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path

# Imports locais
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import Config


class BaseView:
    """Classe base para todas as views"""
    
    def __init__(self):
        """Inicializa a view base"""
        self.setup_page_config()
    
    def setup_page_config(self):
        """Configura a página Streamlit"""
        st.set_page_config(**Config.STREAMLIT_CONFIG)
    
    def show_header(self, title: str, subtitle: str = None):
        """
        Exibe cabeçalho da página
        
        Args:
            title (str): Título principal
            subtitle (str, optional): Subtítulo
        """
        st.title(title)
        if subtitle:
            st.markdown(f"*{subtitle}*")
        st.markdown("---")
    
    def show_success_message(self, message: str):
        """Exibe mensagem de sucesso"""
        st.success(f"✅ {message}")
    
    def show_error_message(self, message: str):
        """Exibe mensagem de erro"""
        st.error(f"❌ {message}")
    
    def show_warning_message(self, message: str):
        """Exibe mensagem de aviso"""
        st.warning(f"⚠️ {message}")
    
    def show_info_message(self, message: str):
        """Exibe mensagem informativa"""
        st.info(f"ℹ️ {message}")


class PropertyInputView(BaseView):
    """View para entrada de dados do imóvel"""
    
    def __init__(self):
        super().__init__()
        self.property_data = {}
    
    def render_input_form(self) -> Dict[str, Any]:
        """
        Renderiza formulário de entrada de dados do imóvel
        
        Returns:
            Dict[str, Any]: Dados do imóvel inseridos
        """
        st.subheader("🏠 Dados do Imóvel")
        
        with st.form("property_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Características Básicas**")
                
                # Tipo de propriedade
                property_type = st.selectbox(
                    "Tipo de Propriedade",
                    ["Apartment", "House", "Condominium", "Loft", "Bed and breakfast", 
                     "Guest suite", "Guesthouse", "Hostel", "Outros", "Serviced apartment"],
                    help="Selecione o tipo de propriedade"
                )
                
                # Tipo de quarto
                room_type = st.selectbox(
                    "Tipo de Acomodação",
                    ["Entire home/apt", "Private room", "Shared room", "Hotel room"],
                    help="Como o espaço é compartilhado"
                )
                
                # Acomodações
                accommodates = st.number_input(
                    "Número de Pessoas",
                    min_value=1,
                    max_value=20,
                    value=2,
                    help="Quantas pessoas podem se hospedar"
                )
                
                # Quartos
                bedrooms = st.number_input(
                    "Número de Quartos",
                    min_value=0,
                    max_value=10,
                    value=1,
                    help="Número de quartos disponíveis"
                )
                
                # Camas
                beds = st.number_input(
                    "Número de Camas",
                    min_value=1,
                    max_value=20,
                    value=1,
                    help="Número total de camas"
                )
                
                # Banheiros
                bathrooms = st.number_input(
                    "Número de Banheiros",
                    min_value=0.5,
                    max_value=10.0,
                    value=1.0,
                    step=0.5,
                    help="Número de banheiros (0.5 = lavabo)"
                )
            
            with col2:
                st.markdown("**Localização e Políticas**")
                
                # Localização
                latitude = st.number_input(
                    "Latitude",
                    min_value=-23.1,
                    max_value=-22.8,
                    value=-22.9,
                    format="%.6f",
                    help="Coordenada de latitude (Rio de Janeiro)"
                )
                
                longitude = st.number_input(
                    "Longitude",
                    min_value=-43.8,
                    max_value=-43.1,
                    value=-43.2,
                    format="%.6f",
                    help="Coordenada de longitude (Rio de Janeiro)"
                )
                
                # Diárias mínimas
                minimum_nights = st.number_input(
                    "Mínimo de Noites",
                    min_value=1,
                    max_value=365,
                    value=1,
                    help="Número mínimo de noites para reserva"
                )
                
                # Taxa para pessoas extras
                extra_people = st.number_input(
                    "Taxa Pessoa Extra (R$)",
                    min_value=0.0,
                    max_value=500.0,
                    value=0.0,
                    help="Taxa cobrada por pessoa extra"
                )
                
                # Reserva instantânea
                instant_bookable = st.checkbox(
                    "Reserva Instantânea",
                    value=False,
                    help="Permite reserva sem aprovação prévia"
                )
                
                # Política de cancelamento
                cancellation_policy = st.selectbox(
                    "Política de Cancelamento",
                    ["flexible", "moderate", "strict", "strict_14_with_grace_period"],
                    help="Política de cancelamento da reserva"
                )
            
            # Características do anfitrião
            st.markdown("**Características do Anfitrião**")
            col3, col4 = st.columns(2)
            
            with col3:
                host_is_superhost = st.checkbox(
                    "Superhost",
                    value=False,
                    help="Anfitrião possui status de Superhost"
                )
                
                host_listings_count = st.number_input(
                    "Número de Propriedades do Host",
                    min_value=1,
                    max_value=100,
                    value=1,
                    help="Quantas propriedades o anfitrião possui"
                )
            
            with col4:
                n_amenities = st.number_input(
                    "Número de Comodidades",
                    min_value=0,
                    max_value=50,
                    value=10,
                    help="Total de amenidades oferecidas"
                )
                
                # Data da estadia
                st.markdown("**Data da Estadia**")
                ano = st.number_input(
                    "Ano",
                    min_value=2018,
                    max_value=2030,
                    value=2024,
                    help="Ano da estadia planejada"
                )
                
                mes = st.number_input(
                    "Mês",
                    min_value=1,
                    max_value=12,
                    value=6,
                    help="Mês da estadia planejada"
                )
            
            # Botão de submit
            submitted = st.form_submit_button(
                "🔮 Prever Preço",
                help="Clique para obter a previsão de preço"
            )
            
            if submitted:
                # Coletar todos os dados no formato que o modelo espera
                self.property_data = {
                    # Features básicas
                    'Unnamed: 0': 0,  # Índice (será ignorado)
                    'host_is_superhost': 1 if host_is_superhost else 0,
                    'host_listings_count': host_listings_count,
                    'latitude': latitude,
                    'longitude': longitude,
                    'accommodates': accommodates,
                    'bathrooms': bathrooms,
                    'bedrooms': bedrooms,
                    'beds': beds,
                    'extra_people': extra_people,
                    'minimum_nights': minimum_nights,
                    'instant_bookable': 1 if instant_bookable else 0,
                    'ano': ano,
                    'mes': mes,
                    'n_amenities': n_amenities,
                }
                
                # Adicionar variáveis dummy para tipo de propriedade
                property_types = ["Apartment", "Bed and breakfast", "Condominium", "Guest suite", 
                                "Guesthouse", "Hostel", "House", "Loft", "Outros", "Serviced apartment"]
                for ptype in property_types:
                    self.property_data[f'property_type_{ptype}'] = 1 if property_type == ptype else 0
                
                # Adicionar variáveis dummy para tipo de quarto
                room_types = ["Entire home/apt", "Hotel room", "Private room", "Shared room"]
                for rtype in room_types:
                    self.property_data[f'room_type_{rtype}'] = 1 if room_type == rtype else 0
                
                # Adicionar variáveis dummy para política de cancelamento
                cancellation_policies = ["flexible", "moderate", "strict", "strict_14_with_grace_period"]
                for cpolicy in cancellation_policies:
                    self.property_data[f'cancellation_policy_{cpolicy}'] = 1 if cancellation_policy == cpolicy else 0
                
                return self.property_data
        
        return None


class PredictionResultView(BaseView):
    """View para exibir resultados da predição"""
    
    def render_prediction_result(self, prediction_result: Dict[str, Any]):
        """
        Renderiza o resultado da predição
        
        Args:
            prediction_result (Dict): Resultado da predição
        """
        if prediction_result.get('success', False):
            predicted_price = prediction_result['predicted_price']
            model_used = prediction_result['model_used']
            
            # Exibir resultado principal
            st.subheader("💰 Previsão de Preço")
            
            # Métrica destacada
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.metric(
                    label="Preço Sugerido por Noite",
                    value=f"R$ {predicted_price:.2f}",
                    help="Preço previsto pelo modelo de machine learning"
                )
            
            with col3:
                st.metric(
                    label="Modelo Utilizado",
                    value=model_used,
                    help="Algoritmo usado para a predição"
                )
            
            # Informações adicionais
            with st.expander("📊 Informações Adicionais", expanded=True):
                col4, col5 = st.columns(2)
                
                with col4:
                    st.markdown("**💡 Dicas de Precificação:**")
                    
                    # Faixas de preço
                    if predicted_price < 100:
                        st.info("💚 Preço econômico - Atrativo para orçamentos menores")
                    elif predicted_price < 300:
                        st.info("💛 Preço intermediário - Bom custo-benefício")
                    else:
                        st.info("💜 Preço premium - Foco em qualidade e conforto")
                    
                    # Margem de ajuste
                    margin_low = predicted_price * 0.9
                    margin_high = predicted_price * 1.1
                    st.markdown(f"**Faixa sugerida:** R$ {margin_low:.2f} - R$ {margin_high:.2f}")
                
                with col5:
                    st.markdown("**🎯 Fatores Importantes:**")
                    st.markdown("• Localização (proximidade de pontos turísticos)")
                    st.markdown("• Sazonalidade (alta/baixa temporada)")
                    st.markdown("• Comodidades disponíveis")
                    st.markdown("• Qualidade das fotos e descrição")
                    st.markdown("• Histórico de avaliações")
            
            # Visualização comparativa
            self._render_price_comparison(predicted_price)
            
        else:
            # Exibir erro
            error_message = prediction_result.get('error', 'Erro desconhecido')
            self.show_error_message(f"Erro na predição: {error_message}")
    
    def _render_price_comparison(self, predicted_price: float):
        """
        Renderiza gráfico comparativo de preços
        
        Args:
            predicted_price (float): Preço previsto
        """
        st.subheader("📊 Comparação com Faixas de Mercado")
        
        # Faixas de referência do mercado Rio de Janeiro
        market_ranges = {
            'Econômico': 80,
            'Intermediário': 200,
            'Seu Imóvel': predicted_price,
            'Premium': 400,
            'Luxo': 600
        }
        
        # Criar gráfico de barras
        fig = go.Figure()
        
        colors = ['lightblue', 'lightgreen', 'red', 'orange', 'purple']
        
        for i, (category, price) in enumerate(market_ranges.items()):
            color = 'red' if category == 'Seu Imóvel' else colors[i]
            
            fig.add_trace(go.Bar(
                x=[category],
                y=[price],
                marker_color=color,
                text=f'R$ {price:.0f}',
                textposition='outside',
                name=category
            ))
        
        fig.update_layout(
            title="Comparação com Faixas de Mercado",
            xaxis_title="Categoria",
            yaxis_title="Preço por Noite (R$)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)


class DataExplorationView(BaseView):
    """View para exploração de dados"""
    
    def render_data_overview(self, data: pd.DataFrame):
        """
        Renderiza visão geral dos dados
        
        Args:
            data (pd.DataFrame): Dataset para explorar
        """
        st.subheader("📊 Visão Geral dos Dados")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Registros", f"{len(data):,}")
        
        with col2:
            st.metric("Número de Features", len(data.columns))
        
        with col3:
            if 'price' in data.columns:
                avg_price = data['price'].mean()
                st.metric("Preço Médio", f"R$ {avg_price:.2f}")
        
        with col4:
            missing_values = data.isnull().sum().sum()
            st.metric("Valores Ausentes", f"{missing_values:,}")
        
        # Mostrar estatísticas descritivas
        if st.checkbox("Mostrar Estatísticas Descritivas"):
            st.subheader("📈 Estatísticas Descritivas")
            st.dataframe(data.describe())
        
        # Mostrar primeiras linhas
        if st.checkbox("Mostrar Primeiros Registros"):
            st.subheader("👀 Primeiros Registros")
            n_rows = st.slider("Número de linhas", 5, 50, 10)
            st.dataframe(data.head(n_rows))
    
    def render_price_analysis(self, data: pd.DataFrame):
        """
        Renderiza análise de preços
        
        Args:
            data (pd.DataFrame): Dataset com coluna de preços
        """
        if 'price' not in data.columns:
            self.show_warning_message("Coluna 'price' não encontrada nos dados")
            return
        
        st.subheader("💰 Análise de Preços")
        
        # Histograma de preços
        fig_hist = px.histogram(
            data, 
            x='price', 
            nbins=50,
            title="Distribuição de Preços",
            labels={'price': 'Preço (R$)', 'count': 'Frequência'}
        )
        fig_hist.update_layout(height=400)
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Boxplot por tipo de quarto (se disponível)
        if 'room_type' in data.columns:
            fig_box = px.box(
                data,
                x='room_type',
                y='price',
                title="Preços por Tipo de Acomodação"
            )
            fig_box.update_layout(height=400)
            st.plotly_chart(fig_box, use_container_width=True)
    
    def render_location_analysis(self, data: pd.DataFrame):
        """
        Renderiza análise de localização
        
        Args:
            data (pd.DataFrame): Dataset com coordenadas
        """
        if not all(col in data.columns for col in ['latitude', 'longitude']):
            self.show_warning_message("Colunas de latitude/longitude não encontradas")
            return
        
        st.subheader("🗺️ Análise de Localização")
        
        # Mapa de calor dos preços
        if 'price' in data.columns:
            # Amostrar dados para performance
            sample_size = min(5000, len(data))
            data_sample = data.sample(n=sample_size, random_state=42)
            
            fig_map = px.scatter_mapbox(
                data_sample,
                lat='latitude',
                lon='longitude',
                color='price',
                size='price',
                color_continuous_scale='Viridis',
                title="Distribuição de Preços por Localização",
                mapbox_style='open-street-map',
                height=600,
                zoom=10
            )
            
            st.plotly_chart(fig_map, use_container_width=True)


class ModelPerformanceView(BaseView):
    """View para visualizar performance dos modelos"""
    
    def render_model_comparison(self, model_results: pd.DataFrame):
        """
        Renderiza comparação entre modelos
        
        Args:
            model_results (pd.DataFrame): Resultados dos modelos
        """
        st.subheader("🏆 Comparação de Modelos")
        
        # Tabela de resultados
        st.dataframe(model_results, use_container_width=True)
        
        # Gráfico de barras para R²
        if 'R²' in model_results.columns:
            fig = px.bar(
                model_results,
                x='Modelo',
                y='R²',
                title="Comparação de Performance (R²)",
                text='R²'
            )
            fig.update_traces(texttemplate='%{text}', textposition='outside')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_feature_importance(self, importance_df: pd.DataFrame):
        """
        Renderiza importância das features
        
        Args:
            importance_df (pd.DataFrame): DataFrame com importâncias
        """
        if importance_df.empty:
            self.show_info_message("Importância das features não disponível para este modelo")
            return
        
        st.subheader("📊 Importância das Features")
        
        # Gráfico de barras horizontais
        fig = px.bar(
            importance_df.head(15),  # Top 15 features
            x='importance',
            y='feature',
            orientation='h',
            title="Top 15 Features Mais Importantes",
            labels={'importance': 'Importância', 'feature': 'Feature'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela detalhada
        with st.expander("📋 Tabela Detalhada de Importâncias"):
            st.dataframe(importance_df, use_container_width=True)


if __name__ == "__main__":
    # Teste das views
    st.title("🧪 Teste das Views - Projeto Airbnb Rio")
    
    # Teste da view de entrada
    input_view = PropertyInputView()
    property_data = input_view.render_input_form()
    
    if property_data:
        st.success("✅ Dados coletados com sucesso!")
        st.json(property_data)