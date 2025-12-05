#! /usr/bin/env python3

#		        This program is part of
#          Paul's Preponderating Prepresser v1.0
#            (CC-BY-SA) 2025 era vulgaris, by
#        The Rev. Paul T. Fusco-Gessick, J.D., SDA
#                <<paul@neroots.net>>

#                I.F.E.T.  --  I.V.V.S.

import sys, os, math, subprocess, PyPDF2, csv

# values for signature start and end pages, to 30 (and sometimes 40!) signatures apiece
# sig X beginning page is sig##[x-1] -- sig X end page is sig##[x]

sig48 =(1,48,49,96,97,144,145,192,193,240,241,288,289,336,337,384,385,432,433,480,481,528,529,576,577,624,625,672,673,720,721,768,769,816,817,864,865,912,913,960,961,1008,1009,1056,1057,1104,1105,1152,1153,1200,1201,1248,1249,1296,1297,1344,1345,1392,1393,1440,1441,1488,1489,1536,1537,1584,1585,1632,1633,1680,1681,1728,1729,1776,1777,1824,1825,1872,1873,1920)
sig44 = (1,44,45,88,89,132,133,176,177,220,221,264,265,308,309,352,353,396,397,440,441,484,485,528,529,572,573,616,617,660,661,704,705,748,749,792,793,836,837,880,881,924,925,968,969,1012,1013,1056,1057,1100,1101,1144,1145,1188,1189,1232,1233,1276,1277,1320,1321,1364,1365,1408,1409,1452,1453,1496,1497,1540,1541,1584,1585,1628,1629,1672,1673,1716,1717,1760)
sig40 = (1,40,41,80,81,120,121,160,161,200,201,240,241,280,281,320,321,360,361,400,401,440,441,480,481,520,521,560,561,600,601,640,641,680,681,720,721,760,761,800,801,840,841,880,881,920,921,960,961,1000,1001,1040,1041,1080,1081,1120,1121,1160,1161,1200,1201,1240,1241,1280,1281,1320,1321,1360,1361,1400,1401,1440,1441,1480,1481,1520,1521,1560,1561,1600)
sig36 =(1,36,37,72,73,108,109,144,145,180,181,216,217,252,253,288,289,324,325,360,361,396,397,432,433,468,469,504,505,540,541,576,577,612,613,648,649,684,685,720,721,756,757,792,793,828,829,864,865,900,901,936,937,972,973,1008,1009,1044,1045,1080,1081,1116,1117,1152,1153,1188,1189,1224,1225,1260,1261,1296,1297,1332,1333,1368,1369,1404,1405,1440,1441,1476,1477,1512,1513,1548,1549,1584,1585,1620,1621,1656,1657,1692,1693,1728,1729,1764,1765,1800)
sig32 = (1,32,33,64,65,96,97,128,129,160,161,192,193,224,225,256,257,288,289,320,321,352,353,384,385,416,417,448,449,480,481,512,513,544,545,576,577,608,609,640,641,672,673,704,705,736,737,768,769,800,801,832,833,864,865,896,897,928,929,960,961,992,993,1024,1025,1056,1057,1088,1089,1120,1121,1152,1153,1184,1185,1216,1217,1248,1249,1280,1281,1312,1313,1344,1345,1376,1377,1408,1409,1440,1441,1472,1473,1504,1505,1536,1537,1568,1569,1600)
sig28 = (1,28,29,56,57,84,85,112,113,140,141,168,169,196,197,224,225,252,253,280,281,308,309,336,337,364,365,392,393,420,421,448,449,476,477,504,505,532,533,560,561,588,589,616,617,644,645,672,673,700,701,728,729,756,757,784,785,812,813,840,841,868,869,896,897,924,925,952,953,980,981,1008,1009,1036,1037,1064,1065,1092,1093,1120)
sig24 = (1,24,25,48,49,72,73,96,97,120,121,144,145,168,169,192,193,216,217,240,241,264,265,288,289,312,313,336,337,360,361,384,385,408,409,432,433,456,457,480,481,504,505,528,529,552,553,576,577,600,601,624,625,648,649,672,673,696,697,720,721,744,745,768,769,792,793,816,817,840,841,864,865,888,889,912,913,936,937,960)
sig20 = (1,20,21,40,41,60,61,80,81,100,101,120,121,140,141,160,161,180,181,200,201,220,221,240,241,260,261,280,281,300,301,320,321,340,341,360,361,380,381,400,401,420,421,440,441,460,461,480,481,500,501,520,521,540,541,560,561,580,581,600)
sig16 = (1,16,17,32,33,48,49,64,65,80,81,96,97,112,113,128,129,144,145,160,161,176,177,192,193,208,209,224,225,240,241,256,257,272,273,288,289,304,305,320,321,336,337,352,353,368,369,384,385,400,401,416,417,432,433,448,449,465,480)
sig12 = (1,12,13,24,25,36,37,48,49,60,61,72,73,84,85,96,97,108,109,120,121,132,133,144,145,156,157,168,169,180,181,192,193,204,205,216,217,228,229,240,241,252,253,264,265,276,277,288,289,300,301,312,313,324,325,336,337,348,349,360)
sig8 = (1,8,9,16,17,24,25,32,33,40,41,48,49,56,57,64,65,72,73,80,81,88,89,96,97,104,105,112,113,120,121,128,129,136,137,144,145,152,153,160,161,168,169,176,177,184,185,192,193,200,201,208,209,216,217,224,225,232,233,240)
sig4 = (1,4,5,8,9,12,13,16,17,20,21,24,25,28,29,32,33,36,37,40,41,44,45,48,49,52,53,56,57,60,61,64,65,68,69,72,73,76,77,80,81,84,85,88,89,92,93,96,97,100,101,104,105,108,109,112,113,116,117,120)

VALID_SIG_SIZES = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]
SIG_TABLES = {
    4: sig4, 8: sig8, 12: sig12, 16: sig16, 20: sig20, 24: sig24,
    28: sig28, 32: sig32, 36: sig36, 40: sig40, 44: sig44, 48: sig48
}

# Get and validate source file
while True:
    print('source: ', end='')
    theSource = input().strip()
    if not theSource:
        sys.exit('ERROR: No source file specified.')

    # Add .pdf extension if not present
    if not theSource.endswith('.pdf'):
        theSource = theSource + '.pdf'

    # Check if file exists
    if not os.path.isfile(theSource):
        print(f'ERROR: File "{theSource}" not found. Please try again.')
        continue

    # Try to read the PDF and get page count
    try:
        with open(theSource, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            actualPageCount = len(reader.pages)
        print(f'Found PDF with {actualPageCount} pages.')
        break
    except Exception as e:
        print(f'ERROR: Could not read PDF file: {e}')
        continue

# Get and validate signature bulk
while True:
    print(f'Sig bulk to print (valid options: {", ".join(map(str, VALID_SIG_SIZES))}): ', end='')
    sigBulk = input().strip()
    try:
        sigBulk = int(sigBulk)
        if sigBulk not in VALID_SIG_SIZES:
            print(f'ERROR: Signature size must be one of: {", ".join(map(str, VALID_SIG_SIZES))}')
            continue
        break
    except ValueError:
        print('ERROR: Please enter a valid number.')
        continue

# Check if page count is divisible by signature size
if actualPageCount % sigBulk != 0:
    print(f'WARNING: Page count ({actualPageCount}) is not evenly divisible by signature size ({sigBulk}).')
    pagesNeeded = sigBulk - (actualPageCount % sigBulk)
    print(f'You need to add {pagesNeeded} blank page(s) to make this work correctly.')
    print('Use pdftk to concatenate the appropriate padding file (1pp.pdf, 2pp.pdf, or 3pp.pdf).')
    print('Example: pdftk A={} B={}pp.pdf cat A B output padded-{}'.format(theSource, pagesNeeded, theSource))
    sys.exit(1)

# Calculate number of signatures automatically
numSigs = actualPageCount // sigBulk
print(f'This will create {numSigs} signature(s) of {sigBulk} pages each.')
print('Proceed? [y/n]: ', end='')
confirm = input().strip().lower()
if confirm not in ['y', 'yes']:
    sys.exit('Aborted.')

ite = int(numSigs) + 1

# Get the signature table for the chosen size
sig_table = SIG_TABLES[sigBulk]

# Split the PDF into signatures
print(f'Splitting {theSource} into {numSigs} signature(s)...')
for i in range(1, int(ite)):
    s = (2 * i) - 1
    j = s - 1
    pagenums = f'{sig_table[j]}-{sig_table[s]}'
    outputnum = f'sig{str(i).zfill(2)}.pdf'
    print(f'  Creating {outputnum}...')
    subprocess.run(["pdftk", str(theSource), "cat", str(pagenums), "output", str(outputnum)],
                   check=True, capture_output=True)

print(f'\nSuccess! Created {numSigs} signature file(s).')
print('Next steps:')
print('  1. Review the sig##.pdf files')
print('  2. Run "fppp" or manually run singledingle on each signature to impose for printing')        
