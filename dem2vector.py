import sys
from osgeo import gdal, ogr

def generate_contours(input_raster, output_shapefile_base, contour_interval):
    # 将 ".shp" 扩展名添加到基础路径以创建完整的输出文件路径
    output_shapefile = output_shapefile_base + ".shp"
    # 打开栅格文件
    ds = gdal.Open(input_raster)
    if ds is None:
        print("Failed to open file: " + input_raster)
        return

    # 获取第一个波段
    band = ds.GetRasterBand(1)

    # 创建输出Shapefile
    drv = ogr.GetDriverByName("ESRI Shapefile")
    if drv is None:
        print("Driver not found!")
        return
    dst_ds = drv.CreateDataSource(output_shapefile)
    if dst_ds is None:
        print("Failed to create file: " + output_shapefile)
        return

    # 创建等高线图层
    layer = dst_ds.CreateLayer("contour")

    # 创建一个名为“ELEV”的字段，用于存储等高线的高度值
    field_defn = ogr.FieldDefn("ELEV", ogr.OFTReal)
    layer.CreateField(field_defn)

    # 生成等高线
    gdal.ContourGenerate(
        band,
        contour_interval,
        0,
        [],
        0,
        0,
        layer,
        0,
        1
    )

    # 清理
    ds = None
    dst_ds = None

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("使用方法: python generate_contours.py <tif输入文件> <输出shp文件路径（不包括扩展名）> <等高线间隔>")
        sys.exit(1)

    tif_input = sys.argv[1]
    output_shp_path_without_extension = sys.argv[2]
    contour_interval = float(sys.argv[3])  # 接受等高线间隔作为浮点数

    generate_contours(tif_input, output_shp_path_without_extension, contour_interval)