clear all
close all
clc

%gt_pa = './data/highway/groundtruth/';
%gt_ft = 'png';

TP_all=0;
FP_all=0;
FN_all=0;

for frame=[1 20 40 60 80 100 120 140 160 180 200 220 240 260 280 300 320 340 360 380 400 420 440 458]
    g=strcat('bear02_0',num2str(frame));
    gtim = double(imread(strcat(g,'_gt.png')));
    f=strcat('modified_pca_binary_mask_bear02_0',num2str(frame));
    fgim = double(imread(strcat(f,'.jpg.png')));
    [TP FP FN TN] = evaluation_entry(fgim,gtim);
    TP_all=TP_all+TP;
    FP_all=FP_all+FP;
    FN_all=FN_all+FN;
end


Re = TP_all/(TP_all + FN_all)
Pr = TP_all / (TP_all + FP_all)
Fm = (2*Pr*Re)/(Pr + Re)
