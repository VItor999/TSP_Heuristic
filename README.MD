# Genetic Algorithm for Traveling Salesman Problem (TSP)

## Project Overview

This repository contains the implementation of a **Genetic Algorithm (GA)** to solve the **Symmetric Traveling Salesman Problem (TSP)**. The project is part of **ELE316 – Otimização Heurística**, and it covers heuristic optimization methods applied to combinatorial problems. The goal is to explore and compare the implementation developed by the the students of Genetic Algorithms (GA) and Simulated Annealing (SA) when applied to solve the TSP against an out of the box solver, namely Google-OR (https://developers.google.com/optimization). The Google-OR solution will be used as a benchmark for the quality of the solution developed by the students 

## Group Information

- **Group Number**: 6
- **Members**: Diego Stocchero & Vitor Carvalho

## Problem Description

The TSP requires finding the shortest possible route that visits each city exactly once and returns to the origin city. The problem we are addressing involves **more than 20 cities**, making it a complex combinatorial problem suitable for heuristic methods like Genetic Algorithms.

### Files
- **`benchmark.py`**: Python implementation to solve the TSP using Google-OR.
- **`main.py`**: Python script that is responsible to call both the benchmark solution and the developed solution and calculate specific metrics in order to deliver information about the desired performance metrics.
- **`README.md`**: This documentation file.
- **`trab1-2024_2.pdf`**: The complete description of the task. This document is in portuguese.