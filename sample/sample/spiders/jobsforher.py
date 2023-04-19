import scrapy
from scrapy import Selector
headers = {
    "authority":"www.jobsforher.com",
    "accept":"application/json, text/javascript, */*; q=0.01",
    "accept-language":"en-GB,en-US;q=0.9,en;q=0.8",
    "content-type":"application/json",
    "cookie":"PHPSESSID=7a3cade0f6d461612ce89dd1aad5a1a6dc0c089d; _gcl_au=1.1.549844178.1681713081; _gid=GA1.2.536823724.1681713081; _fbp=fb.1.1681713081470.985175027; _hjSessionUser_449476=eyJpZCI6IjZmNTUyNTcyLWU2MmMtNTdlYS05MDY0LTY0NGRjZjgwYTdiNyIsImNyZWF0ZWQiOjE2ODE3MTMwODE1MjYsImV4aXN0aW5nIjp0cnVlfQ==; ln_or=eyIyODAzOCw0NjE4NCI6ImQifQ%3D%3D; _gcl_aw=GCL.1681883049.CjwKCAjw__ihBhADEiwAXEazJm1QL9P6vprNcE1OL0HJ_aor_qV0rT6O8as_lEjQJ1SsxyagN-nS7BoCOwwQAvD_BwE; _hjIncludedInSessionSample_449476=0; _hjSession_449476=eyJpZCI6IjhhNjlmYjI0LTVjNzgtNGUzMy04MWY3LTgwYTZhYTY4NjhiNyIsImNyZWF0ZWQiOjE2ODE4ODMwNDk0MjUsImluU2FtcGxlIjpmYWxzZX0=; _hjAbsoluteSessionInProgress=0; _gac_UA-60016083-1=1.1681883081.CjwKCAjw__ihBhADEiwAXEazJm1QL9P6vprNcE1OL0HJ_aor_qV0rT6O8as_lEjQJ1SsxyagN-nS7BoCOwwQAvD_BwE; __atuvc=17%7C16; __atuvs=643f804c8f98d063001; _gat_UA-60016083-1=1; _ga=GA1.1.1033238405.1681713081; _ga_C88NSLSR15=GS1.1.1681883049.13.1.1681884285.53.0.0; _ga_D46MB6H4H3=GS1.1.1681883049.11.1.1681884285.0.0.0",
    "referer":"https://www.jobsforher.com/jobs",
    # sec-ch-ua:"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"
    "sec-ch-ua-mobile":"?0",
    "sec-ch-ua-platform":"Linux",
    "sec-fetch-dest":"empty",
    "sec-fetch-mode":"cors",
    "sec-fetch-site":"same-origin",
    "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "x-requested-with":"XMLHttpRequest"
}
class JobsforherSpider(scrapy.Spider):
    name = "jobsforher"
    allowed_domains = ["jobsforher.com"]
    
    def start_requests(self):

        urls = ["https://www.jobsforher.com/jobs"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        jobsforher = response.xpath("//div[@class='card-body']//a[@class='text-left mb-1']").xpath('@href').getall()
        for job in jobsforher:
            job_url = "https://www.jobsforher.com/"+job
            yield scrapy.Request(url=job_url, callback=self.parse_job, headers=headers)
            break

    def parse_job(self, response):
        try:
            Jobtitle = response.xpath("//div[@class='d-flex']//h1/text()").get().strip()
        except:
            Jobtitle = response.xpath("//div[@class='d-flex']//h1/text()").get()
        try:
            Jobcompany = response.xpath("//div//h2[@class='pl-2 jd-title2-18']/text()").get().strip()
        except:
            Jobcompany = response.xpath("//div//h2[@class='pl-2 jd-title2-18']/text()").get()
        try:
            JobArea = response.xpath("//div[@class='mb-1 jd-title3-18 d-none d-md-block']/text()").get().replace("\n","").replace("\t","").strip()
        except:
            JobArea = response.xpath("//div[@class='mb-1 jd-title3-18 d-none d-md-block']/text()").get().replace("\n","").replace("\t","")

        try:
            Jobdescription = response.xpath("//div[@class='descriptionless jd-title-color']/text()").getall().strip()
        except:
            Jobdescription = response.xpath("//div[@class='descriptionless jd-title-color']/text()").getall()

        job_dict = {
            'Jobtitle': Jobtitle,
            'Jobcompany': Jobcompany,
            'JobArea': JobArea,
            'Jobdescription': Jobdescription
        }
        # print(job_dict , "::::::::::::::::::::::::")
        # job_details = response.xpath("//div[@class='mb-3']").getall()
        # for i in job_details:
        #     tit = Selector(text=i)
        #     k = tit.xpath("//p[@class='text-12 color-9A9A9A']/text()").get().strip()
        #     v = tit.xpath("//p[@class='text-12 color-6F6E6E']/text()").get().strip()
        #     job_dict[k]=v
        print(job_dict)
        yield job_dict
