2/5/2025:
- Retrained model with new mel spectrogram parameters of lower FFT and add hop length
- Added multi processing capabilities to extract_phoneme.py, now only takes 15 minutes to run
- Updated all "MFCC" occurrences to "Mel"
- Newly trained model improved on loss by 0.03

2/3/2025:
- Updated extract_phoneme.py with changes & bug fixes from Daphne
- Added multithreading capabilities to extract_phoneme.py to speed up runtime by 2 hours (3 hrs unthreaded -> 1 hr threaded)
- Added multithreading to scripts that check for white images
- Added more comments
- Retrained model to latest changes
- Added .gitignore
