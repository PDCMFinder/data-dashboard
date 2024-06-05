import pandas as pd
from pandas import read_csv

labels = {'DR_6.2': 'Data release 6.2', 'DR_6.1': 'Data release 6.1', 'DR_6.0': 'Data release 6.0',
    #'latest': 'Latest Release',
          'DR_5.3': 'Data release 5.3', 'DR_5.2': 'Data release 5.2', 'DR_5.1': 'Data release 5.1',
          'DR_4.0': 'Data release 4.0',
          'DR_3.0': 'Data release 3.0',
          'DR_2.1': 'Data release 2.1', 'DR_2.0': 'Data release 2.0',
          'DR_1.0': 'Data release 1.0'}

reactive_categories = {'Providers': 'provider', 'Model Type': 'model_type',
                 'Publications': 'publications', 'Age': 'age_in_years_at_collection',
                 'Diagnosis': 'diagnosis', 'Tumour Type': 'tumour_type',
                 'Primary Site': 'primary_site', 'Gender': 'sex', 'Ethnicity': 'ethnicity'}

primary_site_mapping = {
    "Central Nervous System": [
        "4Th Ventricle", "Brain", "Brain Stem", "Cerebellum", "Cerebrum",
        "Frontal Cortex", "Frontal Lobe", "Infratemporal Fossa", "Occipital Mass",
        "Parietal Lobe", "Pineal", "Posterior Fossa", "Temporal Cortex",
        "Ventricular Mass", "Central Nervous System", "Neurologic",
        "Pontine Meninges", "Right Parietal Lobe", "Right Sylvian Fissure", "Thalamus"
    ],
    "Head and Neck": [
        "Base Of Tongue", "Buccal Mucosa", "Eye", "Face", "Floor Of Mouth",
        "Glottis", "Hard Palate", "Head", "Jaw", "Larynx", "Mouth", "Nasal Cavity",
        "Neck", "Oropharynx", "Oral Cavity", "Orbit", "Pharynx", "Salivary Gland",
        "Scalp", "Soft Tissue", "Supraglottis", "Tonsil", "Tongue", "Head And Neck",
        "Head Face Or Neck", "Neck Mass", "Left Occipital Mass", "Right Neck Mass",
        "Laryngeal", "Post-Cricoid", "Shoulder", "Supra-Orbital Area",
        "Paranasal", "Parapharyngeal", "Os Frontalis"
    ],
    "Thorax": [
        "Breast", "Breast Cancer (Her2-Enriched)", "Breast Cancer (Triple Negative)",
        "Chest", "Chest Mass", "Chest Wall", "Esophagus", "Lung",
        "Lung Recurrence (What Does This Mean)", "Lung Recurrence (Same)", "Mediastinum",
        "Pleura", "Respiratory/Thoracic", "Thoracic", "Thorax", "Bronchus And Lung",
        "Melanoma", "Small Cell Lung Cancer", "Pleural Cavity", "Posterior Mediastinum"
    ],
    "Abdomen and Pelvis": [
        "Abdomen", "Abdominal Mass", "Abdominal Wall", "Abdominalpelvic",
        "Adrenal", "Adrenal Gland", "Adrenal Mass", "Adrenal Resection",
        "Ampulla Of Vater", "Appendix", "Biliary Tract", "Bladder", "Bladder Cancer",
        "Bowel", "Caecum", "Cecum", "Colon", "Colon Cancer (Asian)",
        "Colon Cancer (Caucasian, Europe)", "Colorectal", "Duodenum", "Gallbladder",
        "Gastric", "Gastric Antrum", "Gastric Body Mucosa", "Gastric Cancer (Caucasian)",
        "Gastric Cardia", "Gastric Fundus", "Gastro Oesophageal Junction",
        "Gastroesophageal Junction", "Genitourinary", "Genitourinary Tract",
        "Hepatic Flexure", "Hepatic Flexure Of Colon", "Ileocecal Valve", "Kidney",
        "Large Intestine", "Left Colon", "Left Kidney", "Liver", "Liver And Intrahepatic Duct",
        "Liver Cancer (Caucasian, Cholangiocarcinoma)", "Liver/Biliary Ducts",
        "Oesophagus", "Pancreas", "Pancreas Head", "Pancreatic Cancer (Caucasian)",
        "Peritoneal Mass", "Rectosigmoid Colon", "Rectosigmoid Junction", "Rectum",
        "Sigmoid Colon", "Sigmoid Flexure", "Small Intestine", "Splenic Flexure Of Colon",
        "Stomach", "Transverse Colon", "Endocrine And Neuroendocrine",
        "Extrahepatic Bile Duct", "Intrahepatic Bile Duct", "Distal Pancreas",
        "Digestive/Gastrointestinal", "Gynecologic", "Omentum", "Pelvis",
        "Perineum", "Aortocaval", "Retroperitoneal Mass", "Retroperitoneum",
        "Retroperitoneum ", "Paraspinal Mass", "Paraspinal Mass Resection",
        "Paracaval Lymph Node", "Periorbital", "Peritracheal"
    ],
    "Lymphatic and Hematologic": [
        "Lymph Node", "Lymph Nodes", "Lymphoma", "Lymphoma (Dlbcl)",
        "Haematopoietic And Lymphoid", "Hematologic/Blood", "Leukemia",
        "Leukemia (Aml)", "Peripheral Blood", "Leukapheresis", "Lower Alveolus And Gingiva",
        "Renal Cancer (Caucasian)"
    ],
    "Musculoskeletal": [
        "Bone", "Bone Marrow", "Femur", "Humerus", "Muscle", "Musculoskeletal",
        "Skeletal Muscle", "Soft Tissue", "Back", "Back Mass", "Back Soft Tissue",
        "Distal Femur", "Femur ", "Leg", "Right Proximal Tibia", "Right Proximal Ulna",
        "Calf", "Arm", "Axilla", "Shoulder", "Inferior Leg", "Superior Leg", "Right Buttock",
        "Thigh", "Left Thigh", "Left Distal Femur", "Left Femur",
        "Left Proximal Humerus/Bone Marrow", "Left Proximal Tibia", "Tibia", "Rib",
        "8Th Rib", "Right Distal Femur", "Right Colon", "Right Kidney",
        "Femalelank Mass", "Right Proximal Tibia", "Spine", "Spleen"
    ],
    "Other": [
        "Not Collected", "Not Provided", "Unknown Cancer", "Unknown Primary", "Other", "Other (Specify)"
    ],
    "Reproductive": [
        "Ovary", "Prostate", "Prostate Cancer", "Prostate Gland", "Testes",
        "Testicle", "Testis", "Testis Cancer", "Uterus", "Vulva",
        "Peripheral Nervous System", "Placenta", "Gynecologic", "Upper Tract Urothelial Carcinoma (Utuc)"
    ]
}


diagnosis_to_cancer = read_csv('assets/diagnosis_mappings.tsv', sep='\t')
diagnosis_to_cancer = dict(zip(diagnosis_to_cancer['sample_diagnosis'], diagnosis_to_cancer['mappedTermLabel']))
#cancer_system = pd.read_json("https://www.cancermodels.org/api/model_metadata?select=histology,cancer_system").drop_duplicates()
#cancer_system['histology'] = cancer_system['histology'].str.title()
#cancer_system = None