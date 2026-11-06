# mpl_topics

## Overview

This GitHub project is part of ongoing research, and its results are currently under consideration for publication. The purpose of sharing this code publicly is to facilitate reproducibility and provide transparency in the methods used.

The project analyses the scientific literature on microplastics. Abstracts retrieved from SCOPUS are grouped into research topics with [BERTopic](https://maartengr.github.io/BERTopic/), and each paper is assigned to an ocean basin using named-entity recognition (NER) on the locations mentioned in its abstract. The two classifications are then combined with publication dates and citation counts.

A significant portion of the code relies on third-party libraries and modules, contributing to the robustness and efficiency of the implementation. Notably, we leverage popular libraries such as scikit-learn, BERTopic and spaCy, all of which are publicly available and widely used in the research community.

Please feel free to explore the project, reproduce our findings, and contribute to the development. Feedback and contributions are highly appreciated!

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
3. [Data](#data)
4. [Ocean basin classification (NER)](#ocean-basin-classification-ner)
5. [Topic modelling](#topic-modelling)
6. [Results](#results)

## Installation

Requires **Python 3.12 or newer**. The code runs on Windows, Linux and macOS. On macOS, PyTorch needs an Apple Silicon Mac running macOS 14 or later.

Create a virtual environment and install the pinned dependencies, which include the spaCy model `en_core_web_trf`:

```bash
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```powershell
# Windows (PowerShell)
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The exact versions used are listed in `requirements.txt`. Newer pandas (3.x) and matplotlib (3.9+) releases remove functions the notebooks use, so keep the pinned versions.

`hyperparameter_tuning.ipynb` can optionally run UMAP and HDBSCAN on an NVIDIA GPU via [RAPIDS cuML](https://docs.rapids.ai/install) (Linux only). If cuML is not installed, it falls back to the CPU automatically.

## Usage

The project is organized into folders, one per stage of the analysis. Run the notebooks in this order:

| Step | Notebook | What it does | Main output |
|---|---|---|---|
| 1 | `get_data/scopus api.ipynb` | Cleans the SCOPUS export (removes duplicate DOIs, missing abstracts and corrigenda) | `get_data/alldata.csv` |
| 2 | `bertopic/generate_embeddings.ipynb` | Pre-computes abstract embeddings with the `allenai-specter` sentence-transformer | `bertopic/preprocessed_data/embeddings.csv.npy` |
| 3 | `bertopic/hyperparameter_tuning.ipynb` | Random search over UMAP/HDBSCAN parameters | `bertopic/preprocessed_data/tuning_results.csv` |
| 4 | `NER/NER.ipynb` | Extracts locations, geocodes them and assigns each paper an ocean basin | `NER/merged_fuzzy_classes_labels.csv` |
| 5 | `NER/maps/map.ipynb` | Maps the number of papers per ocean basin | `graphs/map.svg`, `graphs/map.png` |
| 6 | `bertopic/bertopic.ipynb` | Topic modelling and the combined topic / basin / citation analysis | `graphs/`, `bertopic/preprocessed_data/` |

Every intermediate file is included in the repository, so any step can be run on its own without repeating the earlier ones.

All file paths are relative to the folder of the notebook that uses them, and they work on Windows, Linux and macOS. Jupyter starts each notebook in its own folder, so launching `jupyter lab` from the repository root works. If you copy code into a script, run it from the notebook's folder.

Open reproducibility gaps are listed in [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Data

The complete dataset, `get_data/alldata.csv` (12,398 papers with publication years 1977–2025), is stored in this repository, so the analysis can be reproduced without SCOPUS access. The data were retrieved from SCOPUS in 2024.

Retrieving the data from SCOPUS cannot be fully reproduced, because it requires a confidential API key. If you have SCOPUS access and want to update the dataset:

1. Run your SCOPUS search (optionally modifying the query to suit your needs) and export the results as CSV to `get_data/scopus_data.csv`. API credentials, if used, are read by `get_data/helper.py` from `get_data/configurations.ini`, which is excluded from version control.
2. Run `get_data/scopus api.ipynb` to clean the export and write `get_data/alldata.csv`.
3. Re-run every later step. The other files refer to papers by their row position in `alldata.csv`, so changing the dataset invalidates the existing embeddings, basin classes and topic model.

## Ocean basin classification (NER)

`NER/NER.ipynb` assigns each paper to an ocean basin in four stages:

1. **Entity extraction:** spaCy's `en_core_web_trf` model extracts geographic entities (`GPE` and `LOC`) from every abstract.
2. **Geocoding:** each location is looked up with the [GeoNames](https://www.geonames.org/) search API. Locations that fail an exact search are retried with fuzzy search. Locations that GeoNames cannot find or places wrongly are given coordinates by hand (`error_dict` in the notebook). The requests are throttled to respect the API's rate limits.
3. **Basin assignment:** each location is matched to the nearest cell of a 1° ocean-basin grid (`NER/range_area.csv`, whose basin codes are named in `NER/range_basin_list.csv`). The match uses great-circle (haversine) distance. Only locations without a basin yet are matched, so existing assignments stay stable: when a location is exactly equidistant from two grid cells, scikit-learn versions break the tie differently.
4. **Paper classification:** each paper receives the basin that occurs most often among its located places, and coastal and open-ocean variants of the same basin are merged. Names that could not be geocoded do not take part in the vote. Papers without any located place are classified as `Unknown`.

The GeoNames API needs a free account. The notebook reads the username from `NER/configurations.ini`, which is excluded from version control. Create it from the template before re-running the geocoding cells:

```bash
cp NER/configurations.ini.example NER/configurations.ini   # then set your username
```

## Topic modelling

1. **Generate embeddings:** `generate_embeddings.ipynb` pre-computes the embeddings to speed up topic modelling. The stored embeddings are then passed to BERTopic when the model is built.
2. **Hyperparameter tuning:** `hyperparameter_tuning.ipynb` runs a randomized search over the UMAP and HDBSCAN parameters, generating 100 models (seed 42). The models are ranked by the density-based clustering validation (DBCV) index, computed on the clustered (non-outlier) documents. Ties are broken by silhouette score, then by the smaller fraction of outliers. The chosen parameters are set by hand in `bertopic.ipynb`.
3. **Analysis:** `bertopic.ipynb` holds the core analysis of the research: topic labels, topics over time, topics per ocean basin, and citation-based metrics such as the Gini coefficient of citations within each topic.

The topic model used in the paper is saved in `bertopic/model`. The settings cell at the top of `bertopic.ipynb` controls how it is used:

- `FIT_MODEL = False` (default) loads the saved model.
- `FIT_MODEL = True` fits a new model with the chosen parameters and saves it over `bertopic/model`.

UMAP results differ across machines and library versions even with a fixed random seed. A new fit therefore gives different topics, and the hand-written `topic_labels` must then be rewritten; the notebook checks that the labels match the model's topics.

Each topic's full name (`topic_labels`) summarizes its top words and its three most representative documents. The representative documents are not stored in the saved model, so the notebook recomputes them with BERTopic's own seeded procedure. They are saved to `bertopic/preprocessed_data/rep_docs.csv` with their DOI and title.

`bertopic/preprocessed_data/topic_frequency.csv` lists each topic's number of papers, full name and mean age-corrected citation count.

**Citation age correction:** to compare papers of different ages, citation counts are divided by the paper's age:

```
corrected citations = citations / max(REFERENCE_YEAR - publication year, 1)
```

`REFERENCE_YEAR` is the year the data were retrieved (2024), so papers from the last two publication years keep their raw citation count. The plots over time also stop at `REFERENCE_YEAR`. Update it in the settings cell of `bertopic.ipynb` if you retrieve a new dataset.

## Results

The main results are in the `graphs` folder: interactive Plotly figures (`.html`) and vector figures (`.svg`). All results can also be viewed in the `.ipynb` files. Figures only display in an appropriate renderer, such as Jupyter or VS Code; GitHub's notebook preview does not show them.
