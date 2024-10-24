![Deploy Action](https://github.com/coastal-AI/coastalDroneMetadataMap/actions/workflows/deploy.yml/badge.svg)

## Coastal Drone Metadata Map

This platform is a collaborative effort to make coastal drone orthomosaics accessible, providing insight into areas where flights have already been conducted and helping to avoid duplicating efforts. It showcases the metadata of photogrammetric flights carried out by contributing institutions, allowing users to consult flight dates, extents, and other key information. A small preview image of each orthomosaic will be displayed, though the full orthomosaic itself is not available here. To access the complete orthomosaics and make data sharing easier, please contact the listed representative.

All metadata and orthomosaic previews will be available under the CC BY-NC 4.0 license (https://creativecommons.org/licenses/by-nc/4.0/deed.en). Contributing institutions will determine whether to share the full orthomosaics and will establish the licensing terms for their use.

### How to contribute to this repository

For contributing to this repository you need to follow these steps.

1) Create a fork of the repository and clone it.
2) Install miniconda (follow the instructions [here](https://docs.anaconda.com/miniconda/miniconda-install/)) in your local computer.
3) In a terminal,  navigate to the cloned project and create a new conda environment with the dependencies needed for this project:
```conda env create --file=environment.yml```.
4) Make the modifications in the `data` directory to add your points in the excel provided.
5) Generate the new website locally to check that the points have been added to the repository (`python drone_metadata_map.py`).
6) Once you are happy with the result, push your changes to your repository and create a pull request so we can add your contributions to the main site.




