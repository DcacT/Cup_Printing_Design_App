# Cup_Printing_Design_App

An automated design tool that generates print-ready layouts for curved-surface paper cups — developed to streamline and solve printing challenges at SafeCo Packaging.

## 🧾 Overview

Printing on cylindrical paper cups isn't as straightforward as printing on flat surfaces. SafeCo Packaging needed a solution to automate the creation of print layouts that:

- Respect the **curved geometry** of the cup's surface
- Compensate for **visual warping** due to the cup's tapering (wider at the top than bottom)

`Cup_Printing_Design_App` solves these issues by converting 2D artwork into a warped "fan-shaped" layout that aligns correctly during the physical printing and wrapping process.

## ❗ Problems Solved

### 1. ❌ X/Y Movement on a Curved Surface

On a flat editor, dragging images in X and Y directions makes sense — but on a cup, that movement should follow a **curved arc**. This app models the cup as a frustum (truncated cone) and adjusts object placement accordingly.

### 2. ❌ Image Warping During Wrapping (WIP)

Because cups are **wider at the top**, naive printing leads to images:
- Being **stretched** near the top rim
- **Compressed** near the bottom base

The app pre-processes images to **counteract this distortion**, ensuring that once wrapped, they appear visually consistent and proportionally accurate.

## ✅ Features

- Project-Based file management system
- Automatic distortion correction based on cup geometry
- Automatic x-axis warp correction based on cup geometry
- Fan-shaped layout configuration
- Live visual preview of cup layout
- Export to SVG or PNG for printing
- Configuration presets for various cup sizes

## 🖼️ Screenshots

<!-- Replace with real image paths -->
![Sample UI](stuffs\screenshots\template_8oz_standard.png)
![Exported Layout](stuffs\screenshots\app_preview2.png)




