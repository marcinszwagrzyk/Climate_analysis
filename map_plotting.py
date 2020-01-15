import arcpy
import os, sys
from arcpy import env

# env.workspace = r"c:\Users\marci\git\iMGW\output\shp_output"
# lista_shp = arcpy.ListFeatureClasses()
# arcpy.env.overwriteOutput = True
# for i in lista_shp:
#     rok = str(i)[:4]
#     filename_tif = os.path.join(r"c:\Users\marci\git\iMGW\output\tiff_output\raw", str(rok) + ".tif")
#     filename_tif_final = os.path.join(r"c:\Users\marci\git\iMGW\output\tiff_output\cliped", str(rok) + ".tif")
#     raster_raw = arcpy.TopoToRaster_3d(in_topo_features="{} anomalia PointElevation".format(str(i)),
#                                        out_surface_raster =filename_tif,
#                                        cell_size="2000",
#                                        extent="112393,451910046 87742,4464509226 972291,005038486 875799,216277817",
#                                        Margin="20", minimum_z_value="", maximum_z_value="", enforce="ENFORCE",
#                                        data_type="CONTOUR", maximum_iterations="20", roughness_penalty="",
#                                        discrete_error_factor="1", vertical_standard_error="0", tolerance_1="2,5",
#                                        tolerance_2="100", out_stream_features="", out_sink_features="",
#                                        out_diagnostic_file="", out_parameter_file="", profile_penalty="",
#                                        out_residual_feature="", out_stream_cliff_error_feature="",
#                                        out_contour_error_feature="")
#
#     maska = r'c:\Users\marci\git\iMGW\shp\pl_border.shp'
#     arcpy.gp.ExtractByMask_sa(raster_raw, maska, filename_tif_final)
#
# folder_rastry = r'c:\Users\marci\git\iMGW\output\tiff_output\cliped'
# env.workspace = folder_rastry
# rastry = arcpy.ListRasters()
#
# # reklasyfikacja
# for raster in rastry:
#     rok = str(raster)[:4]
#     filename_reklas = os.path.join(r"c:\Users\marci\git\iMGW\output\tiff_output\reklas", str(rok) + ".tif")
#
#     arcpy.Reclassify_3d(in_raster=raster, reclass_field="VALUE",
#
#                         remap="-5,0 -2,0 -3;"
#                               "-2,0 -1,0 -2;"
#                               "-1,0 -0,25 -1;"
#                               "-0,25 0,25 0;"
#                               "0,25 1,0 1;"
#                               "1,0 2,0 2;"
#                               "2,0 3,0 3;"
#                               "3,0 10,0 4",
#
#                         out_raster=filename_reklas,
#                         missing_values="DATA")
#
# env.workspace = r"c:\Users\marci\git\iMGW\output\tiff_output\reklas"
# rastry = arcpy.ListRasters()
#
# # wektoryzacja
# for i in rastry:
#     rok = str(i)[:4]
#     out_shp = os.path.join(r"c:\Users\marci\git\iMGW\output\tiff_output\shp", str(rok) + ".shp")
#     arcpy.RasterToPolygon_conversion(in_raster=i,
#                                      out_polygon_features = out_shp,
#                                      simplify="SIMPLIFY", raster_field="Value")


mxd = arcpy.mapping.MapDocument(r'c:\Users\marci\git\iMGW\shp\obrazek.mxd')
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]


env.workspace = r"c:\Users\marci\git\iMGW\output\tiff_output\shp"
shps = arcpy.ListFeatureClasses()

print(shps)

for shp in shps:
    print(shp)

    in_symbology_layer = r'c:\Users\marci\git\iMGW\shp\wektor_layer.lyr'
    lyr_source = arcpy.mapping.Layer(in_symbology_layer)
    arcpy.mapping.AddLayer(df, lyr_source, "AUTO_ARRANGE")
    addLayer = arcpy.mapping.Layer(shp)
    arcpy.ApplySymbologyFromLayer_management(addLayer, in_symbology_layer)
    arcpy.mapping.AddLayer(df, addLayer, "AUTO_ARRANGE")
    # zasieg
    ext = addLayer.getExtent()
    df.extent = ext
    df.scale = 19500000

    arcpy.mapping.ExportToPNG(mxd, r"c:\Users\marci\git\iMGW\png\{}.png".format(shp[:4]), df,
                              df_export_width=400,
                              df_export_height=400,
                              world_file=False)

import math
import os
import matplotlib.pyplot as plt

png_folder = 'c:\Users\marci\git\iMGW\png'
result_filename = r'c:\Users\marci\git\iMGW\mozaika_arcpy.jpg'
result_figsize_resolution = 40  # 1 = 100px

images_list = os.listdir(png_folder)
images_count = len(images_list)
print('Images: ', images_list)
print('Images count: ', images_count)

# Calculate the grid size:
grid_size = math.ceil(math.sqrt(images_count))

# Create plt plot:
fig, axes = plt.subplots(int(grid_size), int(grid_size), figsize=(result_figsize_resolution, result_figsize_resolution))
current_file_number = 0
for image_filename in images_list:
    x_position = int(current_file_number // grid_size)
    y_position = int(current_file_number % grid_size)

    plt_image = plt.imread(images_dir + '/' + images_list[current_file_number])

    axes[x_position, y_position].imshow(plt_image)
    rok = image_filename[:4]
    axes[x_position, y_position].set_title("{} ".format(rok), fontsize=24)
    axes[x_position, y_position].axis('off')
    # print((current_file_number + 1), '/', images_count, ': ', image_filename)

    current_file_number += 1

plt.subplots_adjust(left=0.0, right=1.0, bottom=0.0, top=1.0)
plt.savefig(result_grid_filename)