# 8 Exploring data with the GUI

[Previous](07-outputs-and-quality.md) · [Contents](table-of-contents.md) · [Next](09-raster-processing.md)

## 8.1 Interface orientation and loading

The desktop workflow has four steps: **Inputs**, **Parameters**, **Outputs** and **Jobs**. A map or table preview, time-series plot and **Phenology Parameters** table present the results. Later steps become available after data are loaded. Begin with the generated [chapter 11 dataset](11-worked-examples.md) to learn the controls without a large-data dependency.

1. Start the reference GUI build and select **Inputs**.
2. Use **Data File > Browse...** to select a CSV table, image-list TXT or temporal GeoTIFF stack. Check the displayed **Data Type** and **No. Point**.
3. For raster input, select the matching **Quality File** and optional **Landcover File** where applicable. Quality information must describe the same observations; it is not simply an arbitrary mask with similar dimensions.
4. Inspect the available layer/map preview and check that dates and value ranges are sensible.
5. Use **Select Subarea** when the dataset requires a smaller loading region, then select **Load Data**. Check the completion message before proceeding to **Parameters**.

The **Generate Filelist...** tool searches selected VI and optional QA folders using filename patterns. Semicolons separate multiple glob rules; exclusions remove matching names. Confirm that the generated lists contain the desired dates and matched products. Do not infer scientific suitability from a filename match.

Raster-stack selection can load the complete stack into memory. Image-list loading can use a selected subarea, but small datasets may be loaded in full and report that the subarea was ignored. Check the loading message and the actual loaded region. Prepare a physically smaller stack for exploration if a full stack exceeds available memory; a selected display region is not a guaranteed memory limit.

## 8.2 Table series and raster pixels

For a table, the date column defines time and subsequent numeric columns define individual series. Navigate the available series using the table/series navigation controls and confirm the plot title. A table column is treated as a series, not a spatial raster column.

For raster data, select a pixel on the map or use the row/column/navigation controls. The displayed row and column are user-facing coordinates; record them with the raster grid and subarea. Confirm the plot's pixel title when changing position. A relative position inside a loaded subarea is not a complete geographic location without that context.

Layer selection, colour map, opacity and display limits assist inspection. These display operations do not define VI scale/offset supplied to scientific processing. Check calibrated data values and the effective range separately.

## 8.3 Region summaries

An ROI is an area for descriptive inspection. The current ROI series summarizes the raw pixel values at each date with a spatial mean and standard deviation, ignoring NaNs. The plotted mean ±2 SD describes spatial spread, not a confidence interval for a fitted seasonal date. It does not constitute a Core fit of a regional average or an area-aggregated productivity product.

Use ROI inspection to find heterogeneous regions or anomalies, then inspect relevant individual pixels and their QA. Mixed land cover can give a smooth regional average while individual pixels have very different seasons.

## 8.4 Comparing fits and seasonal metrics

1. In **Parameters**, check **Data Range** in actual processing units.
2. Under **Weights**, choose **Intervals (3 columns)** or **Value map (2 columns)** and enter an explicit scientifically appropriate mapping. Use **Add Row**/**Remove Row** to adjust rules. The tutorial's binary 0/1 mapping has a known meaning and avoids fractional remapping ambiguity.
3. Select **Double Logistic (DL)** or **Smoothing Spline (SP)**. Interactive inspection can compare both curves; a raster batch run requires one selected method.
4. For SP, adjust **Smoothing parameter** and inspect both seasonal shape and remaining noise. For either method, set **Iterations/Strength** deliberately.
5. Check **Seasonal Method/Par**, **Start Method** and **Start/End Cutoff** against the supported combinations in [section 5.7](05-scientific-methods.md#57-startend-definitions-and-supported-combinations).
6. Display **Raw data**, **Weight**, **Season start/end** and **Season Details** as needed. Inspect the corresponding rows in **Phenology Parameters** rather than selecting parameters from one attractive curve.

**More** under preprocessing reveals **Enable outlier detection**, **Availability Window** and **Base Level**. These have the shared meanings in chapters 5–6. Increasing availability half-width changes coverage counts; it does not create new independent observations.

The **Coarse season** overlay is for inspecting approximate seasonal structure. Recheck the selected fitting method before a batch run after comparing curves or using overlays. The four displayed start-method labels do not establish that every season/threshold combination is supported. Use the documented matrix in [section 5.7](05-scientific-methods.md#57-startend-definitions-and-supported-combinations).

## 8.5 Saving and exporting

Use **File > Save Settings...** to save a parameter preset. Use **File > Load Settings...** to load its supported fields. Preserve the authoritative CLI JSON separately when it contains multiple classes or advanced controls. Loading input data and preserving an entire session are distinct from saving parameter settings.

Use **Save Time Series** to select a base CSV name. The application writes fitted, raw and quality CSVs with the suffixes described in [section 7.6](07-outputs-and-quality.md#76-interactive-export-and-precision). Check dates, selected DL/SP columns and quality semantics before analysis outside TIMESAT. Use **Save** beside **Phenology Parameters** to export the displayed seasonal table to CSV. Its displayed precision applies to that export.

Use the plot toolbar's save-figure facility for an image. Include the variable/units, component versions, date convention, fitting method and key settings in a separate caption or analysis record. Keep input filenames/paths, restricted data and personal information out of figures intended for sharing.

## 8.6 Before continuing to batch processing

Choose representative pixels spanning the study's seasonal and quality conditions. Confirm matching observations, quality weights, band/calibration, class parameters, dates and output conventions for a reproducible comparison. Corresponding scientific results should agree across preview, GUI batch and terminal processing. Investigate any disagreement using [section 12.4](12-troubleshooting.md#124-previewbatch-comparisons), keeping original files and configurations.

These procedures describe the reference GUI workflow. The [validation record](validation.md) distinguishes numerical checks of matching GUI-source services from a complete test of official executables and UI actions. Check the installed interface and effective settings before production processing.
