# Use an official Conda runtime as a parent image
FROM continuumio/miniconda3:latest

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create and activate the Conda environment
RUN conda env create -f environment.yml && \
    conda init bash && \
    echo "conda activate sudoku_solver" >> ~/.bashrc
