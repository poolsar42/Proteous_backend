from models.request import XGBoostRequest
from models.response import XGBoostResponse

from Bio.SeqUtils.ProtParam import ProteinAnalysis

import pickle
import pandas as pd
import re


# PhysioChemical Properties of Amino acids

# Aromaticity


def calculate_aromaticity(row):
    sequence = str(row[1])
    analysis = ProteinAnalysis(sequence)
    return float("%0.2f" % analysis.aromaticity())


# Molecular Weight
def calculate_molecular_weight(row):
    sequence = str(row[0])
    analysis = ProteinAnalysis(sequence)
    return float("%0.2f" % analysis.molecular_weight())


# Instability Index
def calculate_instability_index(row):
    sequence = str(row[0])
    analysis = ProteinAnalysis(sequence)
    return float("%0.2f" % analysis.instability_index())


# Hydrophobicity
def calculate_hydrophobicity(row):
    sequence = str(row[0])
    analysis = ProteinAnalysis(sequence)
    return float("%0.2f" % analysis.gravy(scale='KyteDoolitle'))


# Isoelectric Point
def calculate_isoelectric_point(row):
    sequence = str(row[0])
    analysis = ProteinAnalysis(sequence)
    return float("%0.2f" % analysis.isoelectric_point())


# Charge
def calculate_charge(row):
    sequence = str(row[0])
    analysis = ProteinAnalysis(sequence)
    return float("%0.2f" % analysis.charge_at_pH(row[2]))


def return_amino_acid_df(df):
    # Feature Engineering on Train Data
    amino_acids = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    for amino_acid in amino_acids:
        df[amino_acid] = df['protein_sequence'].str.count(amino_acid, re.I) / df['sequence_length']
        # df[amino_acid]=df['protein_sequence'].str.count(amino_acid,re.I)
    return df


class XGBoostService:

    @staticmethod
    def predict(request: XGBoostRequest) -> XGBoostResponse:
        """Predict the Tm of a sequence using the XGBoost model."""

        prot_sequence = request.sequence

        # Feature Engineering on Test Data
        df = pd.DataFrame({'protein_sequence': [prot_sequence]})
        df['sequence_length'] = df['protein_sequence'].str.len()
        df['pH'] = 7.4
        df = return_amino_acid_df(df)
        print(df)
        df['Aromaticity'] = df.apply(calculate_aromaticity, axis=1)
        df['Molecular Weight'] = df.apply(calculate_molecular_weight, axis=1)
        df['Instability Index'] = df.apply(calculate_instability_index, axis=1)
        df['Hydrophobicity'] = df.apply(calculate_hydrophobicity, axis=1)
        df['Isoelectric Point'] = df.apply(calculate_isoelectric_point, axis=1)
        df['Charge'] = df.apply(calculate_charge, axis=1)

        # Calculate pH

        df = df.drop(['protein_sequence'], axis=1)
        df = df.drop(['sequence_length'], axis=1)

        # Load the model
        model = pickle.load(open("xgboost_model_dalyan", "rb"))

        # Make predictions
        predictions = model.predict(df)
        predicted_tm = predictions[0]

        return XGBoostResponse(tm=predicted_tm)

