from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import asyncio

async def crawl_example(urls):
    """
    简单的网页爬虫函数，爬取页面中所有包含data-symbol属性的<tr>元素，
    并将TD0的内容与TD8的内容对应组成一个字典
    
    参数:
    urls: 要爬取的网址列表
    
    返回:
    dict: TD0与TD8的对应字典
    """
    
    # 创建异步网页爬虫实例
    async with AsyncWebCrawler(verbose=True) as crawler:
        for url in urls:
            print(f"正在爬取: {url}")
            
            # 爬取网页
            result = await crawler.arun(url=url)
            
            print(f"爬取结果状态: {result.success}")
            if result.success:
                print(f"爬取成功 ({url})")
                crawl_result = result._results[0]
                soup = BeautifulSoup(crawl_result.html, 'html.parser')
                
                # 查找所有包含data-symbol属性的<tr>元素
                tr_elements = soup.find_all('tr', attrs={'data-symbol': True})
                
                
                # 创建字典存储TD0与TD8的对应关系
                td0_td8_dict = {}
                
                # 遍历所有找到的元素并提取信息
                for i, tr_element in enumerate(tr_elements):
                    # 获取data-symbol属性值
                    data_symbol = tr_element.get('data-symbol', 'N/A')
                    
                    # 提取该行的所有<td>元素
                    td_elements = tr_element.find_all('td')
                    
                    # 获取TD0和TD8的内容
                    td0_content = td_elements[0].get_text(strip=True) if len(td_elements) > 0 else "N/A"
                    td8_content = td_elements[8].get_text(strip=True) if len(td_elements) > 8 else "N/A"
                    
                    # 将TD0的内容与TD8的内容对应组成字典
                    td0_td8_dict[td0_content] = td8_content

                
                # 返回TD0与TD8的对应字典
                return td0_td8_dict
                
            else:
                print(f"爬取失败 ({url}):", getattr(result, 'error_message', 'Unknown error'))
    
    # 如果没有成功爬取任何URL，返回空字典
    return {}

# 运行示例
if __name__ == "__main__":
    # 在这里替换为您要爬取的网址
    urls_to_crawl = [
        "https://zh.tradingeconomics.com/commodities"
    ]
    
    # 运行爬虫
    result_dict = asyncio.run(crawl_example(urls_to_crawl))
    print("\n最终返回的字典:")
    print(result_dict)