import streamlit as st
import pandas as pd
import joblib
import json

st.set_page_config(
    page_title="Jaya Jaya Institute | Student Dropout Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; font-weight: bold;}
    .stButton>button:hover {background-color: #45a049;}
    .header-text {color: #2c3e50;}
    .metric-card {background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center;}
    </style>
""", unsafe_allow_html=True)

@st.cache_resource(ttl=300)  # Cache 5 menit lalu reload otomatis
def load_model_and_features():
    try:
        model = joblib.load('model/rf_model.joblib')
        with open('model/features.json', 'r') as f:
            features = json.load(f)
        return model, features
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

model, feature_names = load_model_and_features()

# Debug: tampilkan info model di sidebar
if model is not None:
    st.sidebar.markdown(f"**Model classes:** `{list(model.classes_)}`")
    st.sidebar.markdown(f"**Jumlah kelas:** `{len(model.classes_)}`")

st.title("🎓 Jaya Jaya Institute - Student Dashboard & Predictor")
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Business Dashboard", "🔮 Dropout Predictor"])

with tab1:
    st.header("Metrik Kinerja Siswa (Dashboard Analitik)")
    st.markdown("Bagian ini menampilkan eksplorasi data untuk faktor utama yang memengaruhi tingkat *dropout* di Jaya Jaya Institute. **(Untuk tampilan dashboard lebih interaktif menggunakan Google Looker Studio, silakan cek link di README.)**")
    
    try:
        df = pd.read_csv('clean_data.csv')
        
        col1, col2, col3 = st.columns(3)
        total_students = len(df)
        dropout_students = len(df[df['Status'] == 'Dropout'])
        dropout_rate = (dropout_students / total_students) * 100
        
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Total Siswa</h3><h2>{total_students}</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>Siswa Dropout</h3><h2>{dropout_students}</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><h3>Tingkat Dropout</h3><h2>{dropout_rate:.1f}%</h2></div>', unsafe_allow_html=True)
            
        st.write("")
        st.write("")
        
        col4, col5 = st.columns(2)
        with col4:
            st.subheader("Distribusi Status Siswa")
            st.bar_chart(df['Status'].value_counts())
            
        with col5:
            st.subheader("Tunggakan SPP (Tuition fees up to date) vs Status")
            # Create a localized crosstab chart
            ct_fees = pd.crosstab(df['Tuition_fees_up_to_date'], df['Status'])
            st.bar_chart(ct_fees)
            
        st.subheader("Pengaruh Beasiswa (Scholarship holder)")
        ct_scholars = pd.crosstab(df['Scholarship_holder'], df['Status'])
        st.bar_chart(ct_scholars)
        
    except FileNotFoundError:
        st.warning("Data bersih belum tersedia. Harap jalankan Jupyter Notebook terlebih dahulu untuk mengekspor data.")


with tab2:
    st.header("Prediksi Risiko Dropout")
    st.markdown("Masukkan data profil dan akademis siswa untuk memprediksi apakah siswa tersebut berisiko *dropout* atau akan *graduate*.")
    
    if model is not None and feature_names is not None:
        with st.form("prediction_form"):
            st.subheader("Informasi Akademik & Finansial")
            col1, col2 = st.columns(2)
            
            with col1:
                tuition_fees = st.selectbox("Tuition fees up to date (1=Yes, 0=No)", options=[1, 0])
                scholarship = st.selectbox("Scholarship holder (1=Yes, 0=No)", options=[0, 1])
                debtor = st.selectbox("Debtor (1=Yes, 0=No)", options=[0, 1])
                gender = st.selectbox("Gender (1=Male, 0=Female)", options=[1, 0]) 
                age = st.slider("Age at enrollment", 17, 60, 20)

            with col2:
                cur_units_1_approved = st.number_input("Curricular units 1st sem (approved)", min_value=0, max_value=30, value=6)
                cur_units_1_grade = st.number_input("Curricular units 1st sem (grade)", min_value=0.0, max_value=20.0, value=12.0)
                cur_units_2_approved = st.number_input("Curricular units 2nd sem (approved)", min_value=0, max_value=30, value=6)
                cur_units_2_grade = st.number_input("Curricular units 2nd sem (grade)", min_value=0.0, max_value=20.0, value=12.0)
                admission_grade = st.number_input("Admission grade", min_value=0.0, max_value=200.0, value=100.0)

            st.markdown("---")
            
            submit_button = st.form_submit_button(label="🔮 Analisis Risiko Siswa")
            
            if submit_button:
                # Build feature dictionary defaults all 0
                input_data = {col: 0 for col in feature_names}
                
                # Update critical features
                input_data['Tuition_fees_up_to_date'] = tuition_fees
                input_data['Scholarship_holder'] = scholarship
                input_data['Debtor'] = debtor
                input_data['Age_at_enrollment'] = age
                input_data['Gender'] = gender
                input_data['Curricular_units_1st_sem_approved'] = cur_units_1_approved
                input_data['Curricular_units_1st_sem_grade'] = cur_units_1_grade
                input_data['Curricular_units_2nd_sem_approved'] = cur_units_2_approved
                input_data['Curricular_units_2nd_sem_grade'] = cur_units_2_grade
                input_data['Admission_grade'] = admission_grade
                
                # Make dataframe
                input_df = pd.DataFrame([input_data])
                
                # Prediction
                prediction = model.predict(input_df)[0]
                proba = model.predict_proba(input_df)[0]
                
                status_mapping = {0: 'Dropout', 1: 'Graduate'}
                pred_status = status_mapping[prediction]
                
                st.markdown("### Hasil Prediksi")
                
                if pred_status == 'Dropout':
                    st.error(f"⚠️ **PERINGATAN TINGGI**: Siswa ini diprediksi berisiko **DROPOUT**. (Probabilitas: {proba[0]:.2%})")
                    st.info("💡 **Rekomendasi Tindakan:** Segera jadwalkan sesi konseling dan tawarkan program bantuan akademis/finansial.")
                else:
                    st.success(f"✅ **AMAN**: Siswa ini diprediksi akan **GRADUATE**. (Probabilitas: {proba[1]:.2%})")
                    
    else:
        st.error("Model machine learning belum dilatih. Harap jalankan Jupyter Notebook terlebih dahulu.")
