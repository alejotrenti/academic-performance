import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

df = pd.read_csv('data/students.csv')
df.columns = df.columns.str.lower().str.replace(' ', '_')
df['average_score'] = df[['math_score', 'reading_score', 'writing_score']].mean(axis=1)

st.set_page_config(page_title="Desempeño de estudiantes", layout="wide")

st.title("📚 Análisis del desempeño de estudiantes")

with st.sidebar:
    st.header("🗺️ Navegación")
    seccion = st.radio("Ir a calificaciones en:", 
                        ["Todo", "Matemáticas", "Habilidad escrita", 
                        "Habilidad lectura"])
    st.sidebar.title('Seleccione o remueva:')
    # Filtros
    gender = st.sidebar.multiselect("Seleccione género", options=df['gender'].unique(), default=df['gender'].unique())
    ethnicity = st.sidebar.multiselect("Seleccione grupo", options=df['race/ethnicity'].unique(), default=df['race/ethnicity'].unique())
    degree = st.sidebar.multiselect("Seleccione grado", options=df['parental_level_of_education'].unique(), default=df['parental_level_of_education'].unique())
    
    url = 'repo'
    st.link_button("Ir a repositorio: ", url)
    

df_filtered = df[(df['gender'].isin(gender)) & (df['race/ethnicity'].isin(ethnicity)) & (df['parental_level_of_education'].isin(degree))]

etiquetas = {
    'average_score': 'Notas promedio',
    'math_score': 'Matemáticas',
    'reading_score': 'Lectura',
    'writing_score': 'Escritura'
}

colores = {
    'average_score': '#EF553B',
    'math_score': '#636EFA',
    'reading_score': "#D6A64C",
    'writing_score': "#59D848"
}
if seccion == 'Todo':

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("Promedio Matemáticas", f"{df_filtered['math_score'].mean():.2f}")
    col2.metric("Promedio Lectura", f"{df_filtered['reading_score'].mean():.2f}")
    col3.metric("Promedio Escritura", f"{df_filtered['writing_score'].mean():.2f}")

    # Suponiendo que 'df_filtered' ya contiene la columna 'average_score'
    st.subheader("Distribución de Notas Promedio")

    tab1, tab2 = st.tabs(["Histograma", "Densidad (KDE)"])

    with tab1:
        fig1 = px.histogram(
            df_filtered,
            x='average_score',
            nbins=20,
            title='Distribución de Notas Promedio',
        )   
        fig1.update_layout(xaxis_title='Nota promedio', yaxis_title='Frecuencia')
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:

        
        # Selección de variables
        opciones = st.multiselect(
            "Seleccioná las variables a comparar",
            options=['average_score', 'math_score', 'reading_score', 'writing_score'],
            default=['average_score']
        )

        # Validación segura
        if not opciones:
            st.warning('Por favor, seleccioná al menos una variable para mostrar la gráfica.')
        else:
            hist_data = [df_filtered[var] for var in opciones]
            group_labels = [etiquetas[var] for var in opciones]
            colors = [colores[var] for var in opciones]

            fig2 = ff.create_distplot(
                hist_data,
                group_labels,
                show_hist=False,
                colors=colors
            )

            fig2.update_layout(
                title='Densidad de Variables de Notas',
                xaxis_title='Notas',
                yaxis_title='Densidad'
            )
            st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 2: Comparación por género
    fig2 = px.box(
        df_filtered, 
        x='gender', 
        y='average_score', 
        title='Rendimiento por Género',
        )
    st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        fig3 = px.scatter(
            df_filtered,
            x='math_score', 
            y='reading_score', 
            color='gender',
            title='Relación entre Matemáticas y Lectura'
        )
        st.plotly_chart(fig3, use_container_width=True)
        
    with col2:
        # Agrupamos por género y calculamos promedio de cada materia
        df_radar = df_filtered.groupby('gender')[['math_score', 'reading_score', 'writing_score']].mean().reset_index()

        # Preparamos el DataFrame en formato largo (long format)
        df_long = df_radar.melt(id_vars='gender', var_name='Asignatura', value_name='Promedio')

        # Gráfico radar
        fig3 = px.line_polar(
            df_long,
            r='Promedio',
            theta='Asignatura',
            color='gender',
            line_close=True,
            title='Puntajes Promedio por Género (Radar Chart)',
        )
        fig3.update_traces(fill='toself')
        st.plotly_chart(fig3, use_container_width=True)


elif seccion == 'Matemáticas':
    st.subheader("🧮 Rendimiento en matemáticas:")
     
     
    tab1, tab2 = st.tabs(["Histograma", "Densidad (KDE)"])

    with tab1:
        fig1 = px.histogram(
            df_filtered, 
            x='math_score', 
            nbins=20, 
            title='Distribución de Notas Promedio',
            color_discrete_sequence=['#636EFA']
            )
        st.plotly_chart(fig1, use_container_width=True)
    with tab2:
        fig2 = ff.create_distplot(
            hist_data=[df_filtered['math_score']],
            group_labels=['Matemáticas'],
            show_hist=False,
            colors=['#636EFA'] 
        )
        fig2.update_layout(
            title='Distribución de Densidad (KDE) - Matemáticas',
            xaxis_title='Nota',
            yaxis_title='Densidad'
        )
        st.plotly_chart(fig2, use_container_width=True)

    fig2 = px.box(
            df_filtered,
            x='gender',
            y='math_score',
            title='Rendimiento por Género',
            color_discrete_sequence=['#636EFA']
        )
    st.plotly_chart(fig2, use_container_width=True)


elif seccion == 'Habilidad escrita':
    st.subheader("🖊️ Rendimiento en escritura:")
     
    tab1, tab2 = st.tabs(["Histograma", "Densidad (KDE)"])

    with tab1:
        fig1 = px.histogram(
            df_filtered, 
            x='writing_score', 
            nbins=20, 
            title='Distribución de Notas Promedio',
            color_discrete_sequence=['#59D848']
            )
        st.plotly_chart(fig1, use_container_width=True)
    with tab2:
        fig2 = ff.create_distplot(
            hist_data=[df_filtered['writing_score']],
            group_labels=['Escritura'],
            show_hist=False,
            colors=['#59D848'] 
        )
        fig2.update_layout(
            title='Distribución de Densidad (KDE) - Escritura',
            xaxis_title='Nota',
            yaxis_title='Densidad'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    fig2 = px.box(
        df_filtered,
        x='gender',
        y='writing_score',
        title='Rendimiento por Género',
        color_discrete_sequence=['#59D848']
        )
    st.plotly_chart(fig2, use_container_width=True)
    
elif seccion == 'Habilidad lectura':
    st.subheader("📖 Rendimiento en lectura:")
     
    tab1, tab2 = st.tabs(["Histograma", "Densidad (KDE)"])

    with tab1:
        fig1 = px.histogram(
            df_filtered, 
            x='reading_score', 
            nbins=20, 
            title='Distribución de Notas Promedio',
            color_discrete_sequence=['#D6A64C']
            )
        st.plotly_chart(fig1, use_container_width=True)
    with tab2:
        fig2 = ff.create_distplot(
            hist_data=[df_filtered['reading_score']],
            group_labels=['Lectura'],
            show_hist=False,
            colors=['#D6A64C'] 
        )
        fig2.update_layout(
            title='Distribución de Densidad (KDE) - Lectura',
            xaxis_title='Nota',
            yaxis_title='Densidad'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
    fig2 = px.box(
        df_filtered,
        x='gender',
        y='reading_score',
        title='Rendimiento por Género',
        color_discrete_sequence=['#D6A64C']
        )
    st.plotly_chart(fig2, use_container_width=True)
