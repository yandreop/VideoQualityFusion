# Domain-Specific Fusion Of Objective Video Quality Metrics

Please cite the following paper if you use the code or data in your work:

Aaron Chadha, Ioannis Katsavounidis, Ayan Kumar Bhunia, Cosmin Stejerean, Mohammad Umar Khan, and Yiannis Andreopoulos. Domain-Specific Fusion Of Objective Video Quality Metrics. ACM Multimedia 2022.

## Summary

### Raw MOS data on AV2CTC dataset
This repository contains excel files of metadata and raw mean opinion scores (MOS) for individual raters on AV2CTC data, for the coding and denoising applications described in our paper.  The data is extracted over multiple codecs (vp9, x264 and x265), multiple crfs and resolutions.  We also provide the recovered quality scores after SUREAL processing [1], confidence intervals and quality metrics (VMAF, VMAF-NEG, SSIM and PSNR) in the excel files, which can be fused into a single metric using the method decribed in Section 3.3 of the paper.  The source videos for this data can be found at: https://www.dropbox.com/sh/2wxj5107njhunn4/AABfaxX7h1Kv5RX333r5FVIQa?dl=0

### SUREAL processing 
Prior to fusion into a single quality metric, we clean the MOS ratings with SUREAL processing [1] to obtain the recovered quality scores.  The excel data must first be converted to dictionary format in a py file (example provided for coding application). We then provide a simple script for extracting the recovered quality scores from the MOS ratings.
The script writes the recovered quality scores back to the original excel file:

`
python sureal_mle.py --excel_file <path_to_excel_file> --codec <codec_substr> --write_to_file <write_to_excel (bool)> --show_plots <display sureal plots (bool)>
`


[1] Netflix SUREAL package: https://github.com/Netflix/sureal
