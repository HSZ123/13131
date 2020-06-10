#coding:gbk
"""
�ۺ���Ŀ:������ʷ���ݻ������༰����ӻ�
���ߣ�������
���ڣ�2020��6��9��
"""
import csv
import math
import pygal
import pygal_maps_world #������Ҫʹ�õĿ�

def read_csv_as_nested_dict(filename, keyfield, separator, quote): #��ȡԭʼcsv�ļ������ݣ���ʽΪǶ���ֵ�`	
	result={}
	with open(filename,'rt',newline="")as csvfile:
		csvreader=csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
		for row in csvreader:
			rowid=row[keyfield]
			result[rowid]=row
	return result
def reconcile_countries_by_name(plot_countries, gdp_countries):
	Hit={}
	MIN=set()
	Tup1=(Hit,MIN1)
	for sex1 in plot_countries.keys():
		for values in gdp_countries.values():
			if plot_countries[sex1]==values['Country Name']:
				for year in range(1960,2016):
					if values[str(year)]!="":
						Hit[sex1]=values
	for sex2 in plot_countries.keys():
		if sex2 not in Hit:
			MIN1.add(sex2)				
	return Tup1
def build_map_dict_by_name(gdpinfo, plot_countries, year):
	set1=set()
	set2=set()
	set3=set()
	HIt={}
	Tup1=reconcile_countries_by_name(plot_countries,read_csv_as_nested_dict("isp_gdp.csv","Country Code",",",'"'))
	f=open(gdpinfo['gdpfile'],'rt')
	readers=csv.DictReader(f,delimiter=gdpinfo["separator"],quotechar=gdpinfo["quote"])
	for item in readers:
		for keys in plot_countries:
			countryname=plot_countries[keys]
			if countryname==item[gdpinfo['country_name']] and item[year]!='':
				Tup1[keys]=math.log10(eval(item[year]))
			elif countryname==item[gdpinfo['country_name']] and item[year]!="":
				set2.add(keys)
	set1=Tup1[1]
	set3=set2-set1
	Tup2=(Hit,set1,set3)
	return tuple2			
def render_world_map(gdpinfo, plot_countries, year, map_file):
	worldmap_chart=pygal.maps.world.World()
	worldmap_chart.title="{}��ȫ��GDP�ֲ�ͼ".format(year)			
	worldmap_chart.add(year,build_map_dict_by_name(gdpinfo, plot_countries, year)[0])
	worldmap_chart.add('Not find in the world bank',build_map_dict_by_name(gdpinfo, plot_countries, year)[1])
	worldmap_chart.add('no data this year',build_map_dict_by_name(gdpinfo, plot_countries, year)[2])
	worldmap_chart.render_to_file(map_file)
	
def test_render_world_map(year):  #���Ժ���
    """
    �Ը����ܺ������в���
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    } #���������ֵ�
  
   
    pygal_countries = pygal.maps.world.COUNTRIES   # ��û�ͼ��pygal���Ҵ����ֵ�

    # ����ʱ����1970��Ϊ�����Ժ����������ԣ������н�����ṩ��svg���жԱȣ�������ݿɽ��ļ���������
    render_world_map(gdpinfo, pygal_countries, year, "isp_gdp_world_name_{}.svg".format(year))
    print('�ļ�������')
    
print("��ӭʹ������GDP���ݿ��ӻ���ѯ")
print("----------------------")
year=input("���������ѯ�ľ������:")
test_render_world_map(year)

	

		
		
		
		
		
			
				

 		
		
