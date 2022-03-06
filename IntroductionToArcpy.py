import arcpy

arcpy.env.workspace = r"C:\Users\wcarter\Documents\ArcPy"
wksp = arcpy.env.workspace
arcpy.env.overwriteOutput = True
desc = arcpy.Describe(r"C:\Users\wcarter\Documents\ArcPy")

fc = "C:/Users/wcarter/Documents/ArcPy/Practice.gdb"

arcpy.CreateFileGDB_management(wksp, "castles")

castlegdb = f"{wksp}\castles.gdb"

castlesdict = {"Edinburgh": [55.9485977,-3.2021022, 1103],
               "Stirling": [56.12291,-3.9477502, 1490],
               "Culzean": [55.354698,-4.7915147, 1792],
               "Balmoral": [57.0396675,-3.2314249, 1856],
               "Inverness": [57.4763275,-4.2277073, 1836],
               "Dunnotar": [56.9457796,-2.1993788, 1392]}

WGS84 = arcpy.SpatialReference("WGS 1984")

arcpy.env.workspace = castlegdb

# For each coordinate pair, populate the Point object and create a new
# PointGeometry object

arcpy.CreateFeatureclass_management(
    arcpy.env.workspace, "Castles", "POINT", spatial_reference=WGS84)

arcpy.AddFields_management("Castles",
                           [["Name", "Text", "Name", 20],
                           ["Year", "Short", "Year", 4],
                           ["Lat", "Float", "Lat", 9],
                           ["Lon", "Float", "Lon", 9]])

with arcpy.da.InsertCursor(
        'Castles', ["Shape@", "Name", "Year", "Lat", "Lon"]) as icur:
    for key,value in castlesdict.items():
        pGeom = arcpy.PointGeometry(arcpy.Point(value[1], value[0]), WGS84)
        row = (pGeom, key, value[2], value[0], value[1])
        icur.insertRow(row)

scotCounties = arcpy.FeatureClassToFeatureClass_conversion(
    "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/GBR_Boundaries_2019/FeatureServer/4",
    "",
    "ScottishCounties",
    "ID LIKE 's1%'")

arcpy.SpatialJoin_analysis(
    f"{castlegdb}/Castles",
    scotCounties,
    f"{castlegdb}/castlescounties",
    "#", "#", "#", "CLOSEST")

arcpy.SpatialJoin_analysis(
    f"{castlegdb}/Castles",
    f"{castlegdb}/Towns",
    f"{castlegdb}/castlestowns",
    "#", "#", "#", "CLOSEST")