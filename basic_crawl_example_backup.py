
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import re
from database_manager import DatabaseManager

# commodity与中文名称的对应字典
commodity_cn_name_dict = {
    'crude-oil': '原油USD/Bbl',
    'brent-crude-oil': '布伦特原油USD/Bbl',
    'natural-gas': '天然气USD/MMBtu',
    'gasoline': '汽油USD/Gal',
    'heating-oil': '取暖油USD/Gal',
    'coal': '煤炭USD/T',
    'eu-natural-gas': ' TTF 天然气EUR/MWh',
    'uk-natural-gas': ' 英国天然气GBp/thm',
    'ethanol': '乙醇USD/Gal',
    'naphtha': '石脑油USD/T',
    'uranium': '铀USD/Lbs',
    'propane': '丙烷USD/Gal',
    'methanol': '甲醇CNY/T',
    'coking-coal': 'Coking CoalCNY/T',
    'germany-natural-gas-the': 'Germany Natural Gas THEEUR/MWh',
    'urals-oil': '乌拉尔油USD/Bbl',
    'gold': '黄金USD/t.oz',
    'silver': '银USD/t.oz',
    'copper': '铜USD/Lbs',
    'steel': '钢CNY/T',
    'lithium': '锂CNY/T',
    'iron-ore-cny': '铁矿石 人民币CNY/T',
    'platinum': '铂USD/t.oz',
    'hrc-steel': 'HRC钢USD/T',
    'iron-ore': '铁矿USD/T',
    'silicon': 'SiliconCNY/T',
    'scrap-steel': 'Scrap SteelUSD/T',
    'titanium': '钛CNY/KG',
    'soybeans': '大豆USd/Bu',
    'wheat': '小麦USd/Bu',
    'lumber': '木料USD/1000 board feet',
    'palm-oil': '棕榈油MYR/T',
    'cheese': '奶酪USD/Lbs',
    'milk': '牛奶USD/CWT',
    'rubber': '橡胶USD Cents / Kg',
    'orange-juice': '橙汁USd/Lbs',
    'coffee': '咖啡USd/Lbs',
    'cotton': '棉花USd/Lbs',
    'rice': '大米USD/cwt',
    'canola': '油菜籽CAD/T',
    'oat': '燕麦USd/Bu',
    'wool': '羊毛AUD/100Kg',
    'sugar': '白糖USd/Lbs',
    'cocoa': '可可USD/T',
    'tea': '茶INR/Kgs',
    'sunflower-oil': '葵花籽油INR/10 kg',
    'rapeseed-oil': '油菜籽EUR/T',
    'barley': '大麦INR/T',
    'butter': '黄油EUR/T',
    'potatoes': '土豆EUR/100KG',
    'corn': '玉米USd/BU',
    'bitumen': '沥青CNY/T',
    'cobalt': '钴USD/T',
    'lead': '铅USD/T',
    'aluminum': '铝USD/T',
    'tin': '锡USD/T',
    'zinc': '锌USD/T',
    'nickel': '镍USD/T',
    'molybden': '钼CNY/Kg',
    'palladium': '钯USD/t.oz',
    'rhodium': '铑USD/t oz.',
    'phosphorus': 'PhosphorusCNY/T',
    'polyethylene': '聚乙烯CNY/T',
    'polyvinyl': '聚氯乙烯',
    'polypropylene': '聚丙烯CNY/T',
    'synthetic-rubber': 'Synthetic RubberCNY/T',
    'soda-ash': '苏打粉CNY/T',
    'neodymium': '钕CNY/T',
    'sulfur': 'SulfurCNY/T',
    'tellurium': '碲CNY/Kg',
    'urea': '尿尿素USD/T素',
    'di-ammonium': '二铵USD/T',
    'magnesium': '镁CNY/T',
    'gallium': '镓CNY/Kg',
    'germanium': '锗CNY/Kg',
    'manganese': '锰CNY/mtu',
    'indium': '铟CNY/Kg',
    'kraft-pulp': '牛皮纸浆CNY/T',
    'feeder-cattle': '育肥用牛USd/Lbs',
    'live-cattle': '活牛USd',
    'lean-hogs': '瘦肉猪USd/Lbs',
    'beef': '牛肉BRL/15KG',
    'poultry': '家禽BRL/Kgs',
    'eggs-us': ' 鸡蛋美国USD/Dozen',
    'eggs-ch': '鸡蛋 CHCNY/T',
    'salmon': '三文鱼NOK/KG'
}

##定义三个列表
energyList = ['crude-oil', 'brent-crude-oil', 'natural-gas','gasoline','heating-oil','coal','eu-natural-gas','uk-natural-gas',
              'ethanol','naphtha','uranium','propane','methanol','coking-coal','germany-natural-gas-the','urals-oil']
metalList = ['gold', 'silver', 'copper','steel','lithium','iron-ore-cny','platinum','hrc-steel',
             'iron-ore','silicon','scrap-steel','titanium']
agricultureList = ['soybeans', 'wheat', 'lumber','palm-oil','cheese','milk','rubber','orange-juice','coffee',
                   'cotton','rice','canola','oat','wool','sugar','cocoa','tea','sunflower-oil','rapeseed-oil','barley','butter','potatoes','corn']
industryList = ['bitumen','cobalt','lead','aluminum','tin','zinc','nickel','molybden','palladium','rhodium',
                'phosphorus','polyethylene','polyvinyl','polypropylene','synthetic-rubber','soda-ash','neodymium','sulfur',
                'tellurium','urea','di-ammonium','magnesium','gallium','germanium','manganese','indium','kraft-pulp','kraft-pulp']
livestockList = ['feeder-cattle','live-cattle','lean-hogs','beef','poultry','eggs-us','eggs-ch','salmon']

async def crawl_example(commodities, data_dict=None):
    # 创建数据库管理器实例
    db = DatabaseManager()
    
    # 创建异步网页爬虫实例
    async with AsyncWebCrawler(verbose=True) as crawler:
        for commodity in commodities:
            # 构建 URL
            url = f"https://zh.tradingeconomics.com/commodity/{commodity}"
            print(f"正在爬取: {commodity}")
            
            # 爬取示例网页
            result = await crawler.arun(url=url)
            
            # 数据处理
            summary = ""
            stats = ""
            forecast = ""
            news = ""
            
            print(f"爬取结果状态: {result.success}")
            if result.success:
                print(f"爬取成功 ({commodity})")
                crawl_result = result._results[0]
                soup = BeautifulSoup(crawl_result.html, 'html.parser')
                markdown = crawl_result.markdown or ""
                
                # 摘要内容
                historical_div = soup.find('div', {'id': 'historical-desc'})
                if historical_div:
                    summary = historical_div.get_text(strip=True)
                
                # 统计内容
                stats_div = soup.find('div', id='stats')
                if stats_div:
                    stats = stats_div.get_text(strip=True)
                
           
                forecast_match = re.search(r'### (.*?)(?=\n\|\s*物价\s*\||$)', markdown, re.DOTALL)
                if forecast_match:
                    forecast = forecast_match.group(1).strip()
                
                # 新闻: 从指定的 div 标签中提取
                news_divs = soup.find_all('div', class_='list-group-item indc_news_stream', style='border-left: none; border-right: none; border-top: none')
                if news_divs:
                    news = '\n'.join([div.get_text(strip=True) for div in news_divs])
                else:
                    print(f"未找到指定的新闻 div 元素 for {url}")
                
                # 存储数据到数据库
                print(f"数据库连接状态: {db.connection is not None}")
                if db.connection:

                    ##根据commodity所在的列表确定data_type
                    if commodity in energyList:
                        data_type = "energy"
                    elif commodity in metalList:
                        data_type = "metal"
                    elif commodity in agricultureList:
                        data_type = "agriculture"
                    elif commodity in industryList:
                        data_type ="industry"
                    elif commodity in livestockList:
                        data_type = "livestock"
                    else:
                        data_type = "other"
                    
                    # 获取商品的中文名称
                    cn_name = commodity_cn_name_dict.get(commodity, commodity)
                    
                    # 如果提供了data_dict且其中包含该商品，则使用data_dict中的值作为时间字段
                    # 否则使用当前时间作为time字段的值
                    if data_dict and cn_name in data_dict:
                        time_value = data_dict[cn_name]
                    else:
                        import datetime
                        time_value = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    db.insert_data(
                        name=commodity,
                        cn_name=cn_name,
                        time=time_value,
                        summary=summary,
                        statistics=stats,
                        prediction=forecast,
                        news=news,
                        data_type=data_type
                    )
                else:
                    print(f"数据库未连接，无法插入数据 ({commodity})")
                
            else:
                print(f"爬取失败 ({url}):", getattr(result, 'error_message', 'Unknown error'))
    
    # 关闭数据库连接
    db.close()

# 运行示例
if __name__ == "__main__":
    import asyncio
    
    # 合并所有商品到一个列表
    commodities = energyList + metalList + agricultureList + industryList + livestockList
   
    
    # 运行爬虫
    asyncio.run(crawl_example(commodities))