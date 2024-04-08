# Preprocess Script ViT4Mal

This script is used for preprocessing APK files using ViT4Mal protocol. It takes an input folder containing APK files, processes them, and saves the converted images to an output folder.

## Usage

```bash
python preprocess.py <input_folder> <output_folder> [-r]
```

`-r` flag specify recursive search on depth 1.

Example usage:

```bash
python preprocess.py data/apks/D0/goodware data/images/D0/goodware
```