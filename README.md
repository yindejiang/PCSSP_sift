# PCSSP_sift
PCSSP_sift is the short for Pulsar Candidate Sifting and Synthesis Pipeline. This scripts are designed for the ”accelsearch“ results files from PulsaR Exploration and Search TOolkit (PRESTO,  a large suite of pulsar search and analysis software).

These scripts are written based on python and shell！

---

You just need to copy PCSSP_sift.py and PCSP _ sift.sh to your directory of "*ACCEL*0" files from accelsearch search of PRESTO and run PCSSP_sift.sh!

That is, on your terminal:

sh PCSSP_sift.sh

---

Before you run these scripts directly to generate the diagnosis plots of pulsar candidates, you'd better check whether the relevant packages and libraries are installed in your system！
1. pandas, os, shutil, re, numpy, glob, matplotlib are necessary for python3.x.
If you choose to install ananconda on your system, these basic packages are available.

2. You must install ImageMagick in order to synthesize the diagnostic map of pulsar candidates.
ImageMagick is a free, open-source software suite, used for editing and manipulating digital images. It can be used to create, edit, compose, or convert bitmap images, and supports a wide range of file formats, including JPEG, PNG, GIF, TIFF, and PDF.

The following are the instructionswhen I installed Imagemagick in my Centos 7 , which you can use as a reference.

2.1 Install some dependencies

sudo yum group install "Development Tools" --setopt=group_package_types=mandatory,default,optional

2.2 Install Imagemagick

yum install ImageMagick
yum install ImageMagick-devel

2.3 Testing in the terminal, enter convert.

convert -v

# Notes
The writing of this script inspired the DM-Sigma plot of Pan et al and the ACCEL_sift.py from PRESTO.

This script was originally designed to select faint millisecond pulsars with high dispersion mearsure (e.g., DM > 100 cm$\-3$pc).

In this script, you are allowed to set the conditions of pulsar candidate filtering in the first few lines of python script.

The following are related references：

1. PRESTO

https://github.com/scottransom/presto

2. DM-Sigma plot from Pan et al

https://ui.adsabs.harvard.edu/abs/2021RAA....21..143P/abstract




