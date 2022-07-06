from sureal.subjective_model import MosModel, MaximumLikelihoodEstimationModel, MaximumLikelihoodEstimationModelContentObliviousAlternativeProjection2
from sureal.routine import run_subjective_models
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import pdb
import os


parser = argparse.ArgumentParser(description='SUREAL computation')
parser.add_argument('--excel_file', default='coding_raw_data.xlsx', help='Path to excel file')
parser.add_argument('--codec', default=None, help='Codec substring')
parser.add_argument('--write_to_file', action='store_true', default=True, help='write results to excel sheet')
parser.add_argument('--show_plots', action='store_true', default=False, help='display sureal plots')
args = parser.parse_args()


def plot_sample_results(dataset_filepath, subjective_model_classes, show_plots=True):
    dataset, subjective_models, results = run_subjective_models(
            dataset_filepath=dataset_filepath,
            subjective_model_classes = subjective_model_classes,
            normalize_final=False, # True or False
            do_plot=[
                'raw_scores',
                'quality_scores',
                'subject_scores',
                'quality_scores_vs_raw_scores'
            ],
        )
    if show_plots:
        plt.show()
    return results


dataset_filepath = os.path.splitext(args.excel_file)[0]
py_filepath = dataset_filepath

# we assume py file has codec at end of name e.g. '..._vp9.py'
# and only contains specific codec instances
if args.codec:
    py_filepath += f'_{args.codec}'
py_filepath += '.py'

results = plot_sample_results(py_filepath,
                    [
                        MaximumLikelihoodEstimationModelContentObliviousAlternativeProjection2,
                        MosModel,
                    ], show_plots=args.show_plots)

if args.write_to_file:
    excel_file = dataset_filepath + '.xlsx'

    xls = pd.ExcelFile(excel_file)
    df = pd.read_excel(xls, 'Sheet1')

    # filter based on codec
    quality_scores = results[0]['quality_scores']
    raw_scores = results[1]['quality_scores']

    quality_scores_ci95 = results[0]['quality_scores_ci95'][0]
    raw_scores_ci95 = results[1]['quality_scores_ci95'][0]

    if args.codec:
        df = df.loc[(df['Codec'] == args.codec)]
    else:
        quality_scores += (len(df) - len(quality_scores)) * [np.nan]
        raw_scores += (len(df) - len(raw_scores)) * [np.nan]
        quality_scores_ci95 += (len(df) - len(quality_scores)) * [np.nan]
        raw_scores_ci95 += (len(df) - len(quality_scores)) * [np.nan]

    df['Recovered_Quality_Score'] = quality_scores
    df['CI95_Recovered_Quality_Score'] = quality_scores_ci95

    df['Raw_Score'] = raw_scores
    df['CI95_Raw_Score'] = raw_scores_ci95

    with pd.ExcelWriter(excel_file, mode='a', if_sheet_exists="replace") as writer:
        out_sheet = args.codec if args.codec else 'joint'
        df.reset_index(inplace=True, drop=True)
        df.to_excel(writer, sheet_name=out_sheet)
