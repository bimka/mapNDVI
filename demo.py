from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, make_path_filter
import glob
import rasterio as rio

user = 'mintdragonevo'
password = 'k5h46g3kt4'
geojson_path = 'map.geojson'

def get_map_images(geojson_path):
    ''' Функция скачивает последние  изображения карты в красном, 
        инфракрасном и видимом спектре. Получаемые изображения в формате .jp2
    '''    
    chanels = ['B04', 'B08', 'TCI']  
    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    footprint = geojson_to_wkt(read_geojson(geojson_path))
    products = api.query(footprint, # координаты полигона
                        date=('NOW-14DAYS', 'NOW'), # период съёмки карты
                        #filename = 'S2A_MSIL2A*', 
                        platformname='Sentinel-2', 
                        cloudcoverpercentage=(0, 30), # допустимая облачность 
                        limit = 1)
    for chanel in chanels:
        path_filter = make_path_filter(f"*{chanel}_10m.jp2")
        api.download_all(products, nodefilter=path_filter)






"""def get_color_map():
    ''' Функция объединяет красный, зеленый и синие каналы для 
        получения цветного изображения карты
    '''
    paths = sorted(glob.glob('*MSIL2A_*/GRANULE/**/IMG_DATA/R10m/*.jp2'))
    print(paths)
    red = rio.open(paths[0])
    green = rio.open(paths[1])
    blue = rio.open(paths[2])
    with rio.open('RGB.tiff','w',driver='Gtiff', width=red.width, height=red.height, 
              count=3,crs=red.crs,transform=red.transform, dtype=red.dtypes[0]) as rgb:
        rgb.write(red.read(1),1) 
        rgb.write(green.read(1),2) 
        rgb.write(blue.read(1),3) 
        rgb.close()"""

if __name__ == '__main__':
    get_map_images(geojson_path)
    #get_color_map()
    