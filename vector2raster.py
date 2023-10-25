from osgeo import gdal, ogr, osr


# 矢量转栅格 shp和reference的坐标系要一致
def shp_to_tiff(shp_file, reference_tif, output_tiff):
    """
     将shp文件转换成tiff文件，用来去黑边
    :param shp_file: 边界矢量数据
    :param reference_tif: 参考的tif
    :param output_tiff:  转换后的tiff格式
    """
    # 读取shp文件
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.Open(shp_file, 1)
    # 获取图层文件对象
    shp_layer = data_source.GetLayer()

    # 初始化栅格模板
    img = gdal.Open(reference_tif)
    projection = img.GetProjection()
    transform = img.GetGeoTransform()
    cols = img.RasterXSize
    rows = img.RasterYSize
    img = None  # todo 释放内存，只有强制为None才可以释放干净
    del img

    # 根据模板tif属性信息创建对应标准的目标栅格
    target_ds = gdal.GetDriverByName('GTiff').Create(output_tiff, cols, rows, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform(transform)
    target_ds.SetProjection(projection)

    band = target_ds.GetRasterBand(1)
    # 设置背景数值
    NoData_value = 0
    band.SetNoDataValue(NoData_value)
    band.FlushCache()

    # 调用栅格化函数。gdal.RasterizeLayer函数有四个参数，分别有栅格对象，波段，矢量对象，value的属性值将为栅格值
    gdal.RasterizeLayer(target_ds, [1], shp_layer, options=["ATTRIBUTE=name"])
    # 直接写入？？
    y_buffer = band.ReadAsArray()
    target_ds.WriteRaster(0, 0, cols, rows, y_buffer.tobytes())
    target_ds = None  # todo 释放内存，只有强制为None才可以释放干净
    del target_ds, shp_layer



# 栅格转矢量
def tif_to_shp(input_File, out_File):
    ds = gdal.Open(input_File)
    srcband = ds.GetRasterBand(1)
    maskband = srcband.GetMaskBand()
    drv = ogr.GetDriverByName('ESRI Shapefile')
    dst_ds = drv.CreateDataSource(out_File)
    srs = None
    dst_layername = 'out'
    dst_layer = dst_ds.CreateLayer(dst_layername, srs=srs)
    dst_fieldname = 'DN'
    fd = ogr.FieldDefn(dst_fieldname, ogr.OFTInteger)
    dst_layer.CreateField(fd)
    dst_field = 0
    options = []
    # 参数  输入栅格图像波段\掩码图像波段、矢量化后的矢量图层、需要将DN值写入矢量字段的索引、算法选项、进度条回调函数、进度条参数
    gdal.Polygonize(srcband, maskband, dst_layer, dst_field, options)



# shp_file        要转换的shp文件地址
# reference_tif   参考的tif文件地址
# output_tiff     根据shp输出的tif文件地址
shp_file = 'shp_input/shp_input.shp'
reference_tif = 'ref.tif'
output_tiff = 'shp_to_tiff_output.tif'

# tif_input       要转换的tif文件地址
# output_shp      根据tif输出的shp文件地址
tif_input = 'tif_input.tif'
output_shp = 'tif_to_shp_output.shp'


if __name__ == '__main__':
    shp_to_tiff(shp_file, reference_tif, output_tiff)
    # tif_to_shp(tif_input, output_shp)

